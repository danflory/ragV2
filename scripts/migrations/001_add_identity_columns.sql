-- Migration 001: Add Ghost/Shell Identity Columns
-- Phase 6.5: The Conceptual Shift
-- Date: 2026-01-06

-- PURPOSE:
-- Separate agent IDENTITY (Ghost) from execution MODEL (Shell) in the history table.
-- This enables clean model upgrades without losing identity tracking.

-- STEP 1: Add nullable columns (allows existing data to remain valid)
ALTER TABLE history
ADD COLUMN IF NOT EXISTS ghost_id VARCHAR(50),
ADD COLUMN IF NOT EXISTS shell_id VARCHAR(100);

-- STEP 2: Backfill existing records with legacy identifiers
-- All pre-migration data gets marked as "legacy_ghost" and "legacy_shell"
UPDATE history
SET ghost_id = 'legacy_ghost',
    shell_id = 'legacy_shell'
WHERE ghost_id IS NULL OR shell_id IS NULL;

-- STEP 3: Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_history_ghost_id ON history(ghost_id);
CREATE INDEX IF NOT EXISTS idx_history_shell_id ON history(shell_id);
CREATE INDEX IF NOT EXISTS idx_history_ghost_shell ON history(ghost_id, shell_id);

-- STEP 4: Add constraints (make columns required going forward)
-- Note: Run this AFTER verifying that all application write paths are updated
-- ALTER TABLE history
-- ALTER COLUMN ghost_id SET NOT NULL,
-- ALTER COLUMN shell_id SET NOT NULL;

-- VERIFICATION QUERIES:
-- Check column exists:
--   SELECT column_name, data_type, is_nullable 
--   FROM information_schema.columns 
--   WHERE table_name = 'history' AND column_name IN ('ghost_id', 'shell_id');

-- Check backfill status:
--   SELECT ghost_id, shell_id, COUNT(*) as count 
--   FROM history 
--   GROUP BY ghost_id, shell_id;

-- SUCCESS CRITERIA:
-- 1. Columns exist and are indexed
-- 2. All existing records have ghost_id and shell_id populated
-- 3. New inserts include both fields
