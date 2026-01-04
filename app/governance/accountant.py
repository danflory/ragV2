import logging
from ..config import config
from ..database import db

logger = logging.getLogger("AGY_ACCOUNTANT")

class CostAccountant:
    """
    Financial Governance Agent.
    Calculates ROI and savings by comparing local inference vs cloud equivalents.
    """
    
    async def calculate_roi(self):
        """
        Queries usage_stats and calculates financial impact.
        Returns a dict with savings data.
        """
        if not db.is_ready():
            await db.connect()

        try:
            async with db.pool.acquire() as conn:
                # 1. Query usage stats
                rows = await conn.fetch("SELECT layer, prompt_tokens, completion_tokens, duration_ms FROM usage_stats")
                
                total_input_tokens = 0
                total_output_tokens = 0
                l2_input_tokens = 0
                l2_output_tokens = 0
                total_duration_ms = 0
                
                for row in rows:
                    total_input_tokens += row['prompt_tokens'] or 0
                    total_output_tokens += row['completion_tokens'] or 0
                    total_duration_ms += row['duration_ms'] or 0
                    if row['layer'] == 'L2':
                        l2_input_tokens += row['prompt_tokens'] or 0
                        l2_output_tokens += row['completion_tokens'] or 0

                # 2. Logic:
                # Cost_If_Cloud = Total Tokens (All layers) * Ref_Rate
                cost_if_cloud = (
                    (total_input_tokens / 1000.0) * config.REF_COST_INPUT_1K +
                    (total_output_tokens / 1000.0) * config.REF_COST_OUTPUT_1K
                )

                # Actual_Cost = L2 Fees + Est. Electricity
                l2_fees = (
                    (l2_input_tokens / 1000.0) * config.REF_COST_INPUT_1K +
                    (l2_output_tokens / 1000.0) * config.REF_COST_OUTPUT_1K
                )
                
                # Est. Electricity: (Duration in Hours) * (Est. Kw Usage) * (Cost per KWh)
                # Assuming 0.25 kW (250W) average load for Titan RTX during inference.
                est_kw_usage = 0.25
                duration_hours = total_duration_ms / 1000.0 / 3600.0
                electricity_cost = duration_hours * est_kw_usage * config.GRAVITAS_COST_KWH
                
                actual_cost = l2_fees + electricity_cost
                
                net_savings_usd = cost_if_cloud - actual_cost
                savings_percentage = (net_savings_usd / cost_if_cloud * 100) if cost_if_cloud > 0 else 0
                
                return {
                    "total_input_tokens": total_input_tokens,
                    "total_output_tokens": total_output_tokens,
                    "cost_if_cloud": round(cost_if_cloud, 4),
                    "actual_cost": round(actual_cost, 4),
                    "net_savings_usd": round(net_savings_usd, 2),
                    "savings_percentage": round(savings_percentage, 1),
                    "audit_status": "active"
                }
        except Exception as e:
            logger.error(f"❌ ACCOUNTANT ROI FAILURE: {e}")
            return {
                "total_input_tokens": 0,
                "total_output_tokens": 0,
                "cost_if_cloud": 0.0,
                "actual_cost": 0.0,
                "net_savings_usd": 0.0,
                "savings_percentage": 0.0,
                "audit_status": "error"
            }

accountant = CostAccountant()
