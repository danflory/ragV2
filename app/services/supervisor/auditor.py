import argparse
import asyncio
import json
import logging
import re
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional

from app.services.supervisor.guardian import Certificate, SupervisorGuardian

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

@dataclass
class QualityScore:
    total: int
    breakdown: Dict[str, int]

@dataclass
class AuditReport:
    agents_audited: int
    flagged_agents: List[str]
    details: Dict[str, QualityScore]

class ReasoningPipeAuditor:
    """
    Post-hoc quality validation of ReasoningPipe output.
    """

    def __init__(self, certificates_dir: str = "app/.certificates", journals_dir: str = "docs/journals"):
        self.certificates_dir = Path(certificates_dir)
        self.journals_dir = Path(journals_dir)
        self.guardian = SupervisorGuardian(certificates_dir=str(self.certificates_dir))

    async def monthly_audit(self) -> AuditReport:
        """
        Runs an audit on all certified agents based on the last 30 days of data.
        """
        logger.info("Starting monthly audit of ReasoningPipe quality.")
        
        certified_agents = self.guardian.certified_agents.keys()
        flagged_agents = []
        report_details = {}
        
        cutoff_date = datetime.now() - timedelta(days=30)
        
        for agent_name in certified_agents:
            # Collect pipe files for this agent from the last 30 days
            pipe_files = []
            pattern = f"ReasoningPipe_{agent_name}_*.md"
            for pipe_file in self.journals_dir.glob(pattern):
                # Check file mtime for 30 day window
                mtime = datetime.fromtimestamp(pipe_file.stat().st_mtime)
                if mtime > cutoff_date:
                    pipe_files.append(pipe_file)
            
            if not pipe_files:
                logger.warning(f"No pipe files found for agent {agent_name} in the last 30 days.")
                continue

            score = self._audit_quality(pipe_files)
            report_details[agent_name] = score
            
            if score.total < 75:
                reason = f"Quality score {score.total}/100 is below threshold (75). Breakdown: {score.breakdown}"
                await self._flag_for_recertification(agent_name, reason)
                flagged_agents.append(agent_name)
                logger.warning(f"Agent {agent_name} flagged for recertification: {reason}")
            else:
                logger.info(f"Agent {agent_name} passed audit with score {score.total}")

        return AuditReport(
            agents_audited=len(report_details),
            flagged_agents=flagged_agents,
            details=report_details
        )

    def _audit_quality(self, pipe_files: List[Path]) -> QualityScore:
        """
        Scores quality based on format, completeness, efficiency, and cost.
        """
        total_format = 0
        total_completeness = 0
        total_efficiency = 0
        total_cost = 0
        
        n = len(pipe_files)
        
        for pipe_file in pipe_files:
            with open(pipe_file, "r") as f:
                content = f.read()
            
            # 1. Format Compliance (40 pts)
            format_pts = 0
            if content.startswith("# ReasoningPipe:"): format_pts += 10
            if "**Started**:" in content and "**Model**:" in content: format_pts += 10
            if "## Thought Stream" in content and "## Session Metadata" in content: format_pts += 10
            if "**Finalized**:" in content: format_pts += 10
            total_format += format_pts
            
            # 2. Completeness (30 pts)
            comp_pts = 0
            if "THOUGHT:" in content: comp_pts += 15
            if "RESULT:" in content: comp_pts += 15
            # Action is optional but favored
            if "ACTION:" in content: comp_pts = min(30, comp_pts + 5) 
            total_completeness += comp_pts
            
            # 3. Efficiency (20 pts)
            # Find "Efficiency: 370.57 tok/s"
            eff_match = re.search(r"\*\*Efficiency\*\*:\s*([\d.]+)\s*tok/s", content)
            if eff_match:
                eff = float(eff_match.group(1))
                # Acceptable range 1-1000 for various models
                if 1.0 <= eff <= 1000.0:
                    total_efficiency += 20
                else:
                    total_efficiency += 10
            
            # 4. Cost Accuracy (10 pts)
            # Find "Cost: $0.0001 (L1)"
            cost_match = re.search(r"\*\*Cost\*\*:\s*\$([\d.]+)\s*\((L\d)\)", content)
            if cost_match:
                total_cost += 10
        
        avg_breakdown = {
            "format": int(total_format / n),
            "completeness": int(total_completeness / n),
            "efficiency": int(total_efficiency / n),
            "cost": int(total_cost / n)
        }
        
        total_score = sum(avg_breakdown.values())
        return QualityScore(total=total_score, breakdown=avg_breakdown)

    async def _flag_for_recertification(self, agent: str, reason: str):
        """
        Updates the certificate to pending_review and records the failure reason.
        """
        cert_file = self.certificates_dir / f"{agent}.json"
        if not cert_file.exists():
            return

        with open(cert_file, "r") as f:
            data = json.load(f)
        
        data["status"] = "pending_review"
        data["audit_flag"] = {
            "flagged_at": datetime.now().isoformat(),
            "reason": reason
        }
        
        with open(cert_file, "w") as f:
            json.dump(data, f, indent=4)

def main():
    parser = argparse.ArgumentParser(description="Gravitas ReasoningPipe Auditor")
    parser.add_argument("--audit", action="store_true", help="Run monthly quality audit")
    parser.add_argument("--agent", type=str, help="Audit a specific agent only")

    args = parser.parse_args()
    auditor = ReasoningPipeAuditor()

    if args.audit:
        report = asyncio.run(auditor.monthly_audit())
        print("\n--- Audit Report ---")
        print(f"Agents Audited: {report.agents_audited}")
        print(f"Flagged Agents: {', '.join(report.flagged_agents) if report.flagged_agents else 'None'}")
        print("\nDetails:")
        for agent, score in report.details.items():
            print(f" - {agent}: {score.total}/100 {score.breakdown}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
