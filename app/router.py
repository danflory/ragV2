import logging
import re
from fastapi import APIRouter
from pydantic import BaseModel

from .container import container
from .reflex import execute_shell, write_file, execute_git_sync
from .config import config

logger = logging.getLogger("Gravitas_ROUTER")

class ChatRequest(BaseModel):
    message: str

class ModeRequest(BaseModel):
    mode: str

class ResearchRequest(BaseModel):
    query: str

router = APIRouter()

def parse_reflex_action(response_text: str):
    """
    Robustly scans response for XML-style reflex tags.
    Supports both <reflex action="..."/> (self-closing) and 
    <reflex action="...">content</reflex> formats.
    """
    # 1. Check for Shell Command
    shell_match = re.search(r'<reflex action="shell">(.*?)</reflex>', response_text, re.DOTALL)
    if shell_match:
        return "shell", shell_match.group(1).strip()
    
    # 2. Check for File Write
    write_match = re.search(r'<reflex action="write" path="(.*?)">(.*?)</reflex>', response_text, re.DOTALL)
    if write_match:
        path = write_match.group(1).strip()
        content = write_match.group(2).strip()
        return "write", (path, content)

    # 3. Check for Git Sync (Supports both formats)
    git_match_full = re.search(r'<reflex action="git_sync">(.*?)</reflex>', response_text, re.DOTALL)
    if git_match_full:
        return "git_sync", git_match_full.group(1).strip()
    
    if '<reflex action="git_sync"' in response_text:
        return "git_sync", "Automated sync from system."

    return None, None

def strip_reflex_tags(text: str) -> str:
    """
    Removes all <reflex> tags from the response text to leave only the conversational chat.
    """
    # Remove full tags with content
    text = re.sub(r'<reflex action=".*?">.*?</reflex>', '', text, flags=re.DOTALL)
    # Remove self-closing tags
    text = re.sub(r'<reflex action=".*?"\s*/>', '', text)
    return text.strip()

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    logger.info(f"📨 USER: {request.message}")

    # 1. FORCED ESCALATION CHECK
    forced_escalate = request.message.strip().startswith("\\L2")
    l1_response = ""

    # --- SAVE USER MESSAGE TO HISTORY ---
    from .database import db
    if not forced_escalate:
        await db.save_history("user", request.message)
    
    # 0. RETRIEVAL (RAG)
    context_hint = ""
    if container.memory:
        try:
            docs = container.memory.search(request.message, n_results=3)
            if docs:
                context_hint = "--- KNOWLEDGE BASE ---\n" + "\n".join(docs) + "\n\n"
                logger.info(f"🧠 RAG: Retrieved {len(docs)} chunks.")
        except Exception as e:
            logger.error(f"⚠️ RAG SEARCH FAILED: {e}")

    # 1. LAYER 1: LOCAL GENERATION (The Reflex)
    # Skip L1 if we are forcing escalation
    if forced_escalate:
        l1_response = "ESCALATE"
    else:
        l1_response = await container.l1_driver.generate(f"{context_hint}{request.message}")
    
    # 2. PARSE ACTION (Unified)
    action_type, payload = parse_reflex_action(l1_response)
    clean_l1_text = strip_reflex_tags(l1_response)
    
    # 3. INTERCEPT & EXECUTE
    if action_type:
        logger.info(f"⚡ ACTION DETECTED: {action_type}")
        result_msg = ""
        if action_type == "git_sync":
            sync_result = await execute_git_sync(payload) 
            result_msg = f"🤖 **Git Sync Triggered:**\n\n{sync_result}"
        elif action_type == "shell":
            result_msg = await execute_shell(payload)
        elif action_type == "write":
            path, content = payload
            result_msg = await write_file(path, content)

        final_msg = f"{clean_l1_text}\n\n{result_msg}".strip()
        return {"response": final_msg, "layer": "L1"}

    # 4. ESCALATION CHECK
    # If L1 says ESCALATE, returns an error, or is too short, we go to L2
    if "ESCALATE" in l1_response or "L1 Error" in l1_response or len(l1_response) < 2:
        logger.info("🚀 ESCALATING TO L2 (with History)...")
        
        # --- CONTEXT BUILDING (History) ---
        from .database import db
        history_rows = await db.get_recent_history(limit=5)
        history_block = ""
        if history_rows:
            history_block = "--- RECENT CONVERSATION HISTORY ---\n"
            for h in history_rows:
                history_block += f"{h['role'].upper()}: {h['content']}\n"
            history_block += "---\n\n"

        system_hint = (
            "You are an Agentic AI with Full Situational Awareness. "
            "Use the conversation history and knowledge base provided to give the best answer. "
            "To run shell: <reflex action=\"shell\">command</reflex> "
            "To write file: <reflex action=\"write\" path=\"filename\">content</reflex> "
            "To save work: <reflex action=\"git_sync\">Commit Message</reflex>\n\n"
        )
        
        # If forced, strip the trigger word from the prompt we send to L2
        actual_msg = request.message
        if forced_escalate:
            actual_msg = actual_msg.replace("\\L2", "", 1).strip()

        full_prompt = f"{system_hint}{history_block}{context_hint}User: {actual_msg}"
        l2_response = await container.l2_driver.generate(full_prompt)
        
        # Parse potential L2 actions
        l2_action, l2_payload = parse_reflex_action(l2_response)
        clean_l2_text = strip_reflex_tags(l2_response)

        if l2_action:
             result_msg = ""
             if l2_action == "git_sync":
                 sync_result = await execute_git_sync(l2_payload)
                 result_msg = sync_result
             elif l2_action == "shell":
                 result_msg = await execute_shell(l2_payload)
             elif l2_action == "write":
                 path, content = l2_payload
                 result_msg = await write_file(path, content)
            
             final_msg = f"{clean_l2_text}\n\n{result_msg}".strip()
             await db.save_history("ai", final_msg)
             return {"response": final_msg, "layer": "L2"}
        
        await db.save_history("ai", l2_response)
        return {"response": l2_response, "layer": "L2"}

    await db.save_history("ai", l1_response)
    return {"response": l1_response, "layer": "L1"}

@router.post("/ingest")
async def trigger_ingestion():
    """
    Manually triggers the Document Ingestor.
    """
    if not container.ingestor:
        return {"status": "error", "message": "Ingestor not initialized (Vector Store missing?)"}
    
    try:
        # We run this in a background task if it's large, but for now blocking is okay for a dev tool
        await container.ingestor.ingest_all()
        return {"status": "success", "message": "Knowledge ingestion complete."}
    except Exception as e:
        logger.error(f"❌ INGESTION ENDPOINT ERROR: {e}")
        return {"status": "error", "message": str(e)}

@router.delete("/history")
async def clear_chat_history():
    """
    Clears the short-term chat history from the database.
    """
    try:
        from .database import db
        count = await db.clear_history()
        return {"status": "success", "message": f"Chat history cleared ({count} messages purged)."}
    except Exception as e:
        logger.error(f"❌ CLEAR HISTORY ENDPOINT ERROR: {e}")
        return {"status": "error", "message": str(e)}

@router.get("/stats/summary")
async def get_stats_summary():
    """
    Returns a high-level summary of usage statistics for the dashboard.
    """
    try:
        from .database import db
        if not db.pool:
            return {"status": "error", "message": "Database not connected"}
            
        async with db.pool.acquire() as conn:
            totals = await conn.fetchrow('''
                SELECT 
                    COUNT(*) as total_requests,
                    SUM(prompt_tokens) as total_prompt,
                    SUM(completion_tokens) as total_completion,
                    AVG(duration_ms) as avg_latency,
                    SUM(CASE WHEN layer = 'L2' THEN prompt_tokens + completion_tokens ELSE 0 END) as l2_tokens
                FROM usage_stats
            ''')
            
            breakdown = await conn.fetch('''
                SELECT model, layer, COUNT(*) as count
                FROM usage_stats
                GROUP BY model, layer
            ''')
            
            return {
                "status": "success",
                "summary": {
                    "total_requests": totals["total_requests"] or 0,
                    "total_tokens": (totals["total_prompt"] or 0) + (totals["total_completion"] or 0),
                    "l2_tokens": totals["l2_tokens"] or 0,
                    "avg_latency_ms": float(totals["avg_latency"] or 0),
                },
                "breakdown": [dict(row) for row in breakdown]
            }
    except Exception as e:
        logger.error(f"❌ STATS SUMMARY ERROR: {e}")
        return {"status": "error", "message": str(e)}

@router.get("/health/detailed")
async def get_detailed_health():
    """
    Checks connectivity for all microservices and GPU stats.
    """
    from .database import db
    import subprocess
    
    health = {
        "api": "online",
        "postgres": "online" if db.is_ready() else "offline",
        "chroma": "offline",
        "ollama": "offline",
        "gpu": {"used": 0, "total": 0, "percentage": 0}
    }
    
    # Check Ollama
    if await container.l1_driver.check_health():
        health["ollama"] = "online"
        
    # Check Chroma
    try:
        if container.memory and container.memory.collection:
             health["chroma"] = "online"
    except:
        pass

    # Check GPU (NVIDIA)
    try:
        # Get first GPU's memory usage
        res = subprocess.check_output(["nvidia-smi", "--query-gpu=memory.used,memory.total", "--format=csv,noheader,nounits"], encoding="utf-8")
        lines = res.strip().split("\n")
        if lines:
            used, total = map(int, lines[0].split(","))
            health["gpu"] = {
                "used": used,
                "total": total,
                "percentage": round((used / total) * 100, 1) if total > 0 else 0
            }
    except Exception as e:
        logger.warning(f"Failed to fetch GPU stats: {e}")
        
    return {"status": "success", "health": health, "current_mode": container.current_mode}

class PullRequest(BaseModel):
    model: str

@router.post("/model/pull")
async def pull_model_endpoint(request: PullRequest):
    """
    Triggers an asynchronous model pull in the Ollama container.
    """
    try:
        # We temporarily change the driver's target model to the requested one
        old_model = container.l1_driver.model_name
        container.l1_driver.model_name = request.model
        
        # Trigger pull (non-blocking in our implementation)
        success = await container.l1_driver.ensure_model()
        
        # Revert driver model (the endpoint is for management, not permanent switch)
        container.l1_driver.model_name = old_model
        
        if success:
            return {"status": "success", "message": f"Pulling {request.model}..."}
        else:
            return {"status": "error", "message": f"Failed to initiate pull for {request.model}"}
    except Exception as e:
        logger.error(f"❌ MODEL PULL ENDPOINT ERROR: {e}")
        return {"status": "error", "message": str(e)}

@router.post("/system/mode")
async def switch_system_mode(request: ModeRequest):
    """
    Switches the system between RAG and DEV modes (Mutually Exclusive).
    """
    success = await container.switch_mode(request.mode)
    if success:
        return {
            "status": "success", 
            "message": f"System switched to {request.mode} mode.",
            "current_mode": container.current_mode,
            "model": container.l1_driver.model_name
        }
    else:
        return {"status": "error", "message": f"Failed to switch to {request.mode} mode."}

@router.get("/governance/financials")
async def get_financial_report():
    """
    Returns the ROI and savings report from the Cost Accountant.
    """
    try:
        from .governance.accountant import accountant
        report = await accountant.calculate_roi()
        return report
    except Exception as e:
        logger.error(f"❌ FINANCIALS ENDPOINT ERROR: {e}")
        return {"status": "error", "message": str(e)}

@router.post("/agents/librarian/run")
async def run_librarian():
    """
    Manually triggers the Librarian Agent to process the inbox.
    """
    try:
        result = await container.librarian.process_inbox()
        return result
    except Exception as e:
        logger.error(f"❌ LIBRARIAN ENDPOINT ERROR: {e}")
        return {"status": "error", "message": str(e)}

@router.post("/agents/scout/research")
async def scout_research(request: ResearchRequest):
    """
    Triggers the Scout Agent for Deep Research.
    """
    try:
        if not container.scout:
             return {"status": "error", "message": "Scout Agent not initialized."}
        
        report = await container.scout.research(request.query)
        return {"status": "success", "report": report}
    except Exception as e:
        logger.error(f"❌ SCOUT ENDPOINT ERROR: {e}")
        return {"status": "error", "message": str(e)}