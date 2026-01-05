#!/usr/bin/env python3
import asyncio
import sys
import os
import argparse
import logging

# Add app to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.governance.global_renamer import global_rename_service

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("GLOBAL_RENAME_CLI")

async def main():
    parser = argparse.ArgumentParser(description="Gravitas GlobalRename Service - Robust Doc Refactoring")
    parser.add_argument("--dir", default="docs", help="Directory to process (relative to root)")
    parser.add_argument("--search", default="Gravitas", help="Term to find")
    parser.add_argument("--replace", default="Gravitas", help="Term to replace with")
    parser.add_argument("--commit", action="store_true", help="Actually write changes (if not set, runs in dry-run mode)")
    parser.add_argument("--ext", default=".md,.txt", help="Comma-separated file extensions to process")
    
    args = parser.parse_args()
    
    # Resolve absolute path
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    target_dir = os.path.join(root_dir, args.dir)
    
    if not os.path.exists(target_dir):
        logger.error(f"❌ Directory not found: {target_dir}")
        sys.exit(1)

    extensions = args.ext.split(",")
    
    logger.info("🛠️ Initializing GlobalRename Service...")
    
    results = await global_rename_service.run(
        directory=target_dir,
        search_term=args.search,
        replace_term=args.replace,
        extensions=extensions,
        dry_run=not args.commit
    )
    
    if args.commit:
        print("\n✅ Operation Complete. Backups created as .bak files.")
    else:
        print("\n🔎 DRY RUN COMPLETE. No files were modified. Use --commit to apply changes.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Operation cancelled by user.")
    except Exception as e:
        logger.error(f"💥 Fatal Error: {e}")
        sys.exit(1)
