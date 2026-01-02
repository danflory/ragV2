import os
import shutil
import subprocess
import sys

def update_context():
    # Paths using WSL mount points
    base_dir = "/mnt/d/D/AntiGravityNexusContext"
    text_dir = os.path.join(base_dir, "Text")
    
    print(f"🚀 Updating context in: {base_dir}")
    
    # 1. Check if base directory exists
    if not os.path.exists(base_dir):
        print(f"❌ Error: Base directory {base_dir} not found.")
        sys.exit(1)
        
    # 2. Delete Text subfolder if it exists
    if os.path.exists(text_dir):
        print(f"🧹 Removing existing Text folder...")
        # Since these are linked files, shutil.rmtree might hit the same I/O errors
        # if the kernel gets confused. We'll use PowerShell for the heavy lifting
        # to ensure Windows link metadata doesn't break the process.
        try:
            subprocess.run([
                "powershell.exe", "-Command", 
                f"if (Test-Path 'D:\\D\\AntiGravityNexusContext\\Text') {{ Remove-Item 'D:\\D\\AntiGravityNexusContext\\Text' -Recurse -Force }}"
            ], check=True)
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Warning during cleanup: {e}")

    # 3. Create fresh Text folder
    print(f"📂 Creating fresh Text folder...")
    os.makedirs(text_dir, exist_ok=True)

    # 4. Copy files using PowerShell to safely dereference Windows links
    # This is the most reliable way since WSL 'ls/cp' returns I/O errors on these specific link types
    print(f"📋 Copying content (dereferencing links)...")
    ps_command = (
        "$base='D:\\D\\AntiGravityNexusContext'; "
        "$target='D:\\D\\AntiGravityNexusContext\\Text'; "
        "Get-ChildItem $base -File | ForEach-Object { Copy-Item $_.FullName -Destination $target -Force }"
    )
    
    try:
        result = subprocess.run(["powershell.exe", "-Command", ps_command], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Successfully updated Context/Text directory.")
            # List files to confirm
            files = os.listdir(text_dir)
            print(f"📦 Total files in Text: {len(files)}")
            for f in files:
                if f == "Initial Context Prompt.md":
                    print(f"  ⭐ {f} (USE THIS FIRST)")
                else:
                    print(f"  - {f}")
            # 5. Open Explorer to the new Text folder
            print("🪟 Opening Windows Explorer...")
            subprocess.run(["explorer.exe", "D:\\D\\AntiGravityNexusContext\\Text"], check=False)
        else:
            print(f"❌ PowerShell Error: {result.stderr}")
    except Exception as e:
        print(f"💥 Failed to execute update: {e}")

if __name__ == "__main__":
    update_context()
