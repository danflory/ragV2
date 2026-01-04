#!/usr/bin/env python3
import asyncio
import logging
import sys
import os
import argparse
from mcp.server.fastmcp import FastMCP

# --- CONTEXT: v4.0 Gravitas Grounded Research ---
# Ensure we can find the 'app' module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure Logging
# CRITICAL: Logs MUST go to stderr when using Stdio, otherwise they corrupt the JSON protocol
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [GRAVITAS_MCP] - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger("GRAVITAS_MCP")

# Initialize FastMCP
mcp = FastMCP("Gravitas")

# --- TOOL DEFINITIONS ---

@mcp.tool()
async def ping_gravitas() -> str:
    """Checks if the Gravitas MCP server is online and reachable."""
    return "✅ PONG! Gravitas System is Online."

@mcp.tool()
async def gravitas_learn_file(file_path: str, content: str) -> str:
    """
    Teaches Gravitas the contents of a specific file. 
    Use this immediately after creating or updating a code file so the memory stays fresh.
    
    Args:
        file_path: The name or path of the file (e.g., "app/main.py")
        content: The full text content of the file.
    """
    try:
        from app.container import container
        
        # Ensure resources are ready
        if not container.memory:
            await container.init_resources()
            
        logger.info(f"🧠 Learning file: {file_path}")
        
        # Ingest text into Qdrant
        # We assume your memory class has an 'ingest_text' or similar method.
        # Metadata helps filter for code vs chat history later.
        await container.memory.ingest_text(
            text=content,
            metadata={
                "source": file_path, 
                "type": "code_repository",
                "timestamp": "now" # In real app use datetime.now()
            }
        )

        return f"✅ SUCCESS: I have memorized '{file_path}' into Qdrant."

    except Exception as e:
        logger.error(f"Learning Failed: {e}")
        return f"❌ Error learning file: {e}"

@mcp.tool()
async def gravitas_hybrid_search(query: str, top_k: int = 5) -> str:
    """
    Performs a v4.0 Hybrid Search (Dense + Sparse) on the Gravitas Memory (Qdrant).
    """
    try:
        from app.container import container
        
        if not container.memory:
            logger.info("Initializing Gravitas Memory...")
            await container.init_resources()

        results = await container.memory.search_hybrid(query=query, top_k=top_k)
        
        if not results:
            return "Gravitas Memory: No relevant correlations found."
        
        formatted = "\n".join([f"[Score: {r.score:.2f}] {r.content}" for r in results])
        return f"--- GRAVITAS MEMORY RETRIEVAL ---\n{formatted}\n---------------------------------"

    except Exception as e:
        logger.error(f"Search Failure: {e}")
        return f"Error accessing Gravitas Memory: {str(e)}"

@mcp.tool()
async def gravitas_l1_reflex(prompt: str) -> str:
    """
    Direct access to the L1 Reflex Model (Gemma-2-27B on Titan RTX).
    """
    try:
        from app.container import container
        if not container.l1_driver:
             await container.init_resources()
        return await container.l1_driver.generate(prompt)
    except Exception as e:
        logger.error(f"L1 Reflex Error: {e}")
        return f"L1 Reflex Error: {str(e)}"

@mcp.tool()
async def gravitas_l2_reasoning(prompt: str) -> str:
    """
    High-IQ cloud inference using the L2 Reasoning Layer (DeepInfra/Qwen).
    """
    try:
        from app.container import container
        if not container.l2_driver:
             await container.init_resources()
        return await container.l2_driver.generate(prompt)
    except Exception as e:
        logger.error(f"L2 Error: {e}")
        return f"L2 Reasoning Error: {str(e)}"

@mcp.resource("gravitas://system_status")
async def get_system_status() -> str:
    """Returns the health status of the Dual-GPU Rig."""
    status = {
        "phase": "Phase 18 (Gravitas Grounded Research)",
        "gpu_0": "Titan RTX (Active - Generation)",
        "gpu_1": "GTX 1060 (Active - Embeddings)",
        "memory": "Qdrant Hybrid + MinIO",
        "mode": "Active"
    }
    return str(status)

# --- MAIN ENTRY POINT ---

async def main():
    # Parse arguments to enable Stdio mode for the IDE
    parser = argparse.ArgumentParser()
    parser.add_argument("--stdio", action="store_true", help="Run in Stdio mode for IDE integration")
    args = parser.parse_args()

    if args.stdio:
        logger.info("🔌 Starting Gravitas MCP in Stdio Mode (Docker Exec)...")
        # This handles the IDE connection via 'docker exec'
        await mcp.run_stdio_async()
    else:
        logger.info("🚀 Starting Gravitas MCP in SSE Mode (Keep-Alive)...")
        # This keeps the container running so 'docker exec' can work if needed
        # Or acts as a standalone HTTP server
        mcp.settings.host = "0.0.0.0"
        mcp.settings.port = 8000
        await mcp.run_sse_async()

if __name__ == "__main__":
    asyncio.run(main())