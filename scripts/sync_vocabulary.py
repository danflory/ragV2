import re
import os

def sync():
    source_path = "/home/dflory/dev_env/rag_local/docs/HOWTO_DEV_REMINDERS.md"
    target_path = "/home/dflory/dev_env/rag_local/.agent/vocabulary.md"
    
    if not os.path.exists(source_path):
        return

    if os.path.exists(target_path):
        source_mtime = os.path.getmtime(source_path)
        target_mtime = os.path.getmtime(target_path)
        if target_mtime >= source_mtime:
            return

    with open(source_path, 'r') as f:
        content = f.read()

    vocab = ["### LLM readable vocabulary extracted from HOWTO_DEV_RMINDERS ###\n"]
    vocab.append("# PROTOCOL_V1: GRAVITAS_JOURNALING")
    vocab.append("- DIRECTORY: /docs/journals/")
    
    # Extract bullet points that look like rules (e.g. "**Deep Reconciliation**:")
    capabilities = re.findall(r"- \*\*(.*?)\*\*: (.*)", content)
    for key, val in capabilities:
        vocab.append(f"- RULE_{key.upper().replace(' ', '_')}: {val}")

    # Extract numbered methodology steps
    methodology = re.findall(r"\d+\.\s+\*\*(.*?)\*\*: (.*)", content)
    for key, val in methodology:
        vocab.append(f"- PROTOCOL_{key.upper().replace(' ', '_')}: {val}")

    # Extract magic words specifically from the list
    vocab.append("- MAGIC_WORDS:")
    magic_words = re.findall(r"  - \*\*(.*?)\*\*: (.*)", content)
    for word, desc in magic_words:
        vocab.append(f"  - {word}: {desc}")

    vocab.append("- RECON_PRIORITY: [1] Load .agent/vocabulary.md [2] Exec.md (tail 50) [3] Ready")

    with open(target_path, 'w') as f:
        f.write("\n".join(vocab))

if __name__ == "__main__":
    sync()
