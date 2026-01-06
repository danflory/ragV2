from app.utils.repo_walker import gather_repository_content
import os

def main():
    print("Running repo_walker against current directory...")
    content = gather_repository_content(".")
    
    files = sorted(content.keys())
    print(f"Found {len(files)} files.")
    
    print("\nFirst 20 files:")
    for f in files[:20]:
        print(f" - {f}")
        
    # Check for problematic files
    problematic = ["v12_log.txt", ".git", "__pycache__", "venv", ".venv"]
    for p in problematic:
        found = [f for f in files if p in f]
        if found:
            print(f"\nWARNING: Found files containing '{p}':")
            for f in found[:5]:
                print(f" !! {f}")

if __name__ == "__main__":
    main()
