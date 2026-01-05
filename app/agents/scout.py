import logging
from ..interfaces import LLMDriver, VectorMemory

logger = logging.getLogger("Gravitas_SCOUT")

class ScoutAgent:
    """
    The Scout: Deep Research Agent.
    Orchestrates memory retrieval and L3 synthesis for high-fidelity reporting.
    """
    def __init__(self, l3_driver: LLMDriver, memory: VectorMemory):
        self.l3 = l3_driver
        self.memory = memory

    async def research(self, query: str) -> str:
        """
        Coordinates a deep research task.
        1. Contextualize the query.
        2. Retrieve knowledge from Gravitas Grounded Research.
        3. Synthesize via L3.
        """
        logger.info(f"🔭 DEPLOYING SCOUT for research: '{query}'")

        # 1. Retrieve Knowledge
        # Scout uses a larger context window (top_k=10) for deep reasoning.
        context_chunks = await self.memory.search(query, top_k=10)
        
        if not context_chunks:
            context_text = "No specific local context found in Gravitas memory. Use general knowledge."
            logger.info("⚠️ No local context found for Scout research.")
        else:
            context_text = "\n\n".join([f"--- SOURCE {i+1} ---\n{c}" for i, c in enumerate(context_chunks)])
            logger.info(f"📚 Context retrieval complete: {len(context_chunks)} chunks found.")

        # 2. Construct Deep Research Prompt
        prompt = f"""
# GRAVITAS DEEP RESEARCH PROTOCOL
MISSION: Provide a comprehensive, high-fidelity report on the target topic.
TARGET TOPIC: {query}

# LOCAL CONTEXT (FROM GRAVITAS MEMORY)
The following information was retrieved from local datasets:
{context_text}

# INSTRUCTIONS
1. SYNTHESIZE: Combine the unique local context provided above with your global world knowledge.
2. ANALYZE: Identify core trends, technical nuances, and strategic implications.
3. STRUCTURE: Organize the report into:
   - Executive Summary
   - Key Findings
   - Technical Deep Dive
   - Strategic Synthesis
4. CONTRAST: Point out any nuances where local context differs from common trends.
5. QUALITY: Ensure a professional, objective, and authoritative tone.

FINAL REPORT:
"""

        # 3. Generate via L3 (Gemini 1.5 Pro)
        report = await self.l3.generate(prompt)
        
        logger.info("✅ SCOUT REPORT SYNTHESIZED.")
        return report
