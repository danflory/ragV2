import logging
import re
from fastapi import APIRouter
from pydantic import BaseModel

from .container import container
from .reflex import execute_shell, write_file, execute_git_sync
from .config import config

logger = logging.getLogger("AGY_ROUTER")

class ChatRequest(BaseModel):
    message: str

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

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    logger.info(f"📨 USER: {request.message}")

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
    # L1 handles simple commands and basic chat.
    l1_response = await container.l1_driver.generate(f"{context_hint}{request.message}")
    
    # 2. PARSE ACTION (Unified)
    action_type, payload = parse_reflex_action(l1_response)
    
    # 3. INTERCEPT & EXECUTE
    if action_type:
        logger.info(f"⚡ ACTION DETECTED: {action_type}")
        if action_type == "git_sync":
            result = await execute_git_sync(payload) 
            return {"response": f"🤖 **Git Sync Triggered:**\n\n{result}"}
        
        # If shell/write came from L1 (unlikely but possible), handle them
        if action_type == "shell":
            result = await execute_shell(payload)
            return {"response": result}
        elif action_type == "write":
            path, content = payload
            result = await write_file(path, content)
            return {"response": result}

    # 4. ESCALATION CHECK
    # If L1 says ESCALATE, returns an error, or is too short, we go to L2
    if "ESCALATE" in l1_response or "L1 Error" in l1_response or len(l1_response) < 2:
        logger.info("🚀 ESCALATING TO L2...")
        system_hint = (
            "You are an Agentic AI. You can execute commands. "
            "To run shell: <reflex action=\"shell\">command</reflex> "
            "To write file: <reflex action=\"write\" path=\"filename\">content</reflex> "
            "To save work: <reflex action=\"git_sync\">Commit Message</reflex>\n\n"
        )
        full_prompt = f"{system_hint}{context_hint}User: {request.message}"
        l2_response = await container.l2_driver.generate(full_prompt)
        
        # Parse potential L2 actions
        l2_action, l2_payload = parse_reflex_action(l2_response)
        if l2_action:
             if l2_action == "git_sync":
                 sync_result = await execute_git_sync(l2_payload)
                 return {"response": sync_result}
             elif l2_action == "shell":
                 result = await execute_shell(l2_payload)
                 return {"response": result}
             elif l2_action == "write":
                 path, content = l2_payload
                 result = await write_file(path, content)
                 return {"response": result}
        
        return {"response": l2_response}

    return {"response": l1_response}

@router.post("/ingest")
async def trigger_ingestion():
    """
    Manually triggers the Document Ingestor.
    """
    if not container.ingestor:
        return {"status": "error", "message": "Ingestor not initialized (Vector Store missing?)"}
    
    try:
        # We run this in a background task if it's large, but for now blocking is okay for a dev tool
        container.ingestor.ingest_all()
        return {"status": "success", "message": "Knowledge ingestion complete."}
    except Exception as e:
        logger.error(f"❌ INGESTION ENDPOINT ERROR: {e}")
        return {"status": "error", "message": str(e)}