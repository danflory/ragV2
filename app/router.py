import logging
import re
from fastapi import APIRouter
from pydantic import BaseModel

from .container import container
from .reflex import execute_shell, write_file, execute_git_sync

logger = logging.getLogger("AGY_ROUTER")

class ChatRequest(BaseModel):
    message: str

router = APIRouter()

def parse_reflex_action(response_text: str):
    """
    Scans L2 response for XML-style reflex tags.
    Target Syntax: 
      1. <reflex action="shell">ls -la</reflex>
      2. <reflex action="write" path="app/test.py">CONTENT</reflex>
      3. <reflex action="git_sync">Commit Message</reflex>
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

    # 3. Check for Git Sync
    git_match = re.search(r'<reflex action="git_sync">(.*?)</reflex>', response_text, re.DOTALL)
    if git_match:
        return "git_sync", git_match.group(1).strip()

    return None, None

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    logger.info(f"📨 USER: {request.message}")

    # 1. GENERATE THOUGHT (L2 via Container)
    # We inject a System Prompt hint so it knows it *can* use reflexes.
    system_hint = (
        "You are an Agentic AI. You can execute commands. "
        "To run shell: <reflex action=\"shell\">command</reflex> "
        "To write file: <reflex action=\"write\" path=\"filename\">content</reflex> "
        "To save work: <reflex action=\"git_sync\">Commit Message</reflex>"
    )
    
    full_prompt = f"{system_hint}\nUser: {request.message}"
    
    response_text = await container.l2_driver.generate(full_prompt)

    # 2. PARSE ACTION
    action_type, payload = parse_reflex_action(response_text)

    # 3. INTERCEPT & EXECUTE
    if action_type:
        logger.info(f"⚡ ACTION DETECTED: {action_type}")
        
        if action_type == "shell":
            result = await execute_shell(payload)
            return {"response": f"🤖 **I executed a command:**\n`{payload}`\n\n**Result:**\n{result}"}
            
        elif action_type == "write":
            path, content = payload
            result = await write_file(path, content)
            return {"response": f"🤖 **I wrote a file:**\n`{path}`\n\n**Result:**\n{result}"}
            
        elif action_type == "git_sync":
            result = await execute_git_sync(payload)
            return {"response": f"🤖 **Git Sync Triggered:**\n\n{result}"}

    # 4. DEFAULT CHAT
    return {"response": response_text}