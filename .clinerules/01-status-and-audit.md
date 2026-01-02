# Status Check Protocol
- Trigger: When the user says "Status Check".
- Goal: Extract internal logs and save an enhanced Markdown report to `docs2/tmp/`.
- Process:

### 1. Dynamic Path Detection
Detect VS Code environment and set appropriate paths:
```bash
# Check if running in VS Code server (remote/WSL)
if [ -d ~/.vscode-server/data/User/globalStorage/saoudrizwan.claude-dev ]; then
    TASKS_DIR=~/.vscode-server/data/User/globalStorage/saoudrizwan.claude-dev/tasks
else
    TASKS_DIR=~/.config/Code/User/globalStorage/saoudrizwan.claude-dev/tasks
fi

# Checkpoint file for incremental processing
CHECKPOINT_FILE=docs2/tmp/.status_checkpoint.json
```

### 2. Workspace-Specific Task Identification
Find the task folder that matches the current workspace:
```bash
# Get workspace identity
WORKSPACE_PATH="$(pwd)"
GIT_REMOTE=$(git remote get-url origin 2>/dev/null || echo "")

# Find task folder containing workspace files or git remote
CURRENT_TASK=$(find "$TASKS_DIR" -name "task_metadata.json" \
  -exec grep -l "$WORKSPACE_PATH" {} \; 2>/dev/null | head -1 | xargs dirname 2>/dev/null)

# Fallback to git remote matching
if [ -z "$CURRENT_TASK" ] && [ -n "$GIT_REMOTE" ]; then
  CURRENT_TASK=$(find "$TASKS_DIR" -name "task_metadata.json" \
    -exec grep -l "$GIT_REMOTE" {} \; 2>/dev/null | head -1 | xargs dirname 2>/dev/null)
fi

# Final fallback to most recent (with warning)
if [ -z "$CURRENT_TASK" ]; then
  echo "Warning: Could not match workspace, using most recent task" >&2
  CURRENT_TASK=$(ls -td "$TASKS_DIR"/* 2>/dev/null | head -1)
fi

TARGET_FILE="$CURRENT_TASK/api_conversation_history.json"
```

### 3. Incremental Processing with Checkpoints
Only process new data since last run:
```bash
# Load checkpoint or initialize
if [ -f "$CHECKPOINT_FILE" ]; then
  LAST_TS=$(jq -r '.last_processed_timestamp // 0' "$CHECKPOINT_FILE")
else
  LAST_TS=0
  mkdir -p docs2/tmp
  echo '{"last_processed_timestamp": 0}' > "$CHECKPOINT_FILE"
fi

# Default time window (24 hours) but respect checkpoint
TIME_WINDOW_HOURS=${TIME_WINDOW_HOURS:-24}
CUTOFF_TS=$(( $(date +%s) - (TIME_WINDOW_HOURS * 3600) ))
ANALYSIS_START_TS=$(( LAST_TS > CUTOFF_TS ? LAST_TS : CUTOFF_TS ))
```

### 4. Streamlined JSON Processing with jq
Use jq for efficient parsing instead of text processing:
```bash
# Extract session metadata
SESSION_DATA=$(jq -r "{
  task: (.conversation[0].content // \"Unknown task\"),
  model: .model,
  provider: .resolvedProvider,
  total_input: (.usage.input_tokens // 0),
  total_output: (.usage.output_tokens // 0)
}" "$TARGET_FILE")

# Filter recent conversation entries
RECENT_CONVERSATION=$(jq --argjson start_ts "$ANALYSIS_START_TS" \
  '[.conversation[] | select(.ts > $start_ts)]' "$TARGET_FILE")

# Count tool usage efficiently
TOOL_STATS=$(echo "$RECENT_CONVERSATION" | jq '
  [.[].tool_calls // [] | .[].tool_name] | 
  group_by(.) | map({(.[0]): length}) | add // {}'
)

# Extract file operations
FILE_CHANGES=$(echo "$RECENT_CONVERSATION" | jq -r '
  [.[] | select(.tool_calls) | .tool_calls[] | 
   select(.tool_name | IN("write_to_file", "replace_in_file")) | 
   .arguments.path] | unique[]' 2>/dev/null || echo "")

# Extract commands executed
COMMANDS_RUN=$(echo "$RECENT_CONVERSATION" | jq -r '
  [.[] | select(.tool_calls) | .tool_calls[] | 
   select(.tool_name == "execute_command") | 
   .arguments.command] | unique[]' 2>/dev/null || echo "")
```

### 5. Automated Timestamp-based Report Naming
Use ISO timestamps for unique, sortable filenames:
```bash
REPORT_FILE="docs2/tmp/status_$(date +%Y%m%d_%H%M%S).md"
```

### 6. Selective Time Window Analysis
Focus analysis on recent activity:
```bash
# Only process conversation entries newer than ANALYSIS_START_TS
# This is integrated into step 4 above
# Configurable via TIME_WINDOW_HOURS environment variable
```

### 7. Generate Enhanced Report
Create the status report with all collected data:
```bash
# Extract values from JSON data
TASK_DESC=$(echo "$SESSION_DATA" | jq -r '.task')
MODEL_NAME=$(echo "$SESSION_DATA" | jq -r '.model')
PROVIDER=$(echo "$SESSION_DATA" | jq -r '.provider')
INPUT_TOKENS=$(echo "$SESSION_DATA" | jq -r '.total_input')
OUTPUT_TOKENS=$(echo "$SESSION_DATA" | jq -r '.total_output')
TOTAL_TOKENS=$((INPUT_TOKENS + OUTPUT_TOKENS))

# Calculate estimated cost (implementation details in section 5)
ESTIMATED_COST=$(calculate_cost "$MODEL_NAME" "$INPUT_TOKENS" "$OUTPUT_TOKENS")

# Generate report
cat > "$REPORT_FILE" << EOF
# Cline Status Report
**Generated**: $(date '+%Y-%m-%d %H:%M:%S %Z')
**Analyzed Period**: Last ${TIME_WINDOW_HOURS} hours
**Workspace**: $WORKSPACE_PATH

## Session Summary
**Task**: $TASK_DESC
**Status**: $(determine_status "$RECENT_CONVERSATION")

### Recent Activity:
$(summarize_activity "$RECENT_CONVERSATION")

### Key Outcomes:
$(extract_outcomes "$RECENT_CONVERSATION")

## Agent Details
- **Model**: $MODEL_NAME
- **Provider**: $PROVIDER
- **Tokens Used**:
  - Input: $INPUT_TOKENS
  - Output: $OUTPUT_TOKENS
  - Total: $TOTAL_TOKENS
- **Estimated Cost**: \$$ESTIMATED_COST

## File Changes
$(list_file_changes "$FILE_CHANGES")

## Commands Executed
$(list_commands "$COMMANDS_RUN")

## Tool Usage Stats
$(format_tool_stats "$TOOL_STATS")

## Notes
$(generate_notes "$RECENT_CONVERSATION")
EOF

# Update checkpoint
jq --arg ts "$(date +%s)000" '.last_processed_timestamp = ($ts | tonumber)' \
  "$CHECKPOINT_FILE" > "${CHECKPOINT_FILE}.tmp" && mv "${CHECKPOINT_FILE}.tmp" "$CHECKPOINT_FILE"
```

### 8. Task Data Cleanup
Delete task folders older than 30 days:
```bash
# Remove old task directories to save disk space
find "$TASKS_DIR" -type d -mtime +30 -exec rm -rf {} \; 2>/dev/null || true
echo "Cleaned up task folders older than 30 days"
```

#### Report Template:
```markdown
# Cline Status Report #{n}
**Generated**: {timestamp}

## Session Summary
**Task**: {original_user_request}
**Status**: {✅ Completed / ⚠️ In Progress / ❌ Blocked}

### What Cline Did:
- {action 1}
- {action 2}

### Key Outcomes:
- {outcome 1}
- {outcome 2}

## Agent Details
- **Model**: {model_name}
- **Provider**: {provider}
- **Tokens Used**: 
  - Input: {input_tokens}
  - Output: {output_tokens}
  - Total: {total_tokens}
- **Estimated Cost**: ${calculated_cost}

## File Changes
### Modified: {count}
- {list}

### Created: {count}
- {list}

## Commands Executed
```bash
{list_of_commands}
```

## Tool Usage Stats
- `read_file`: {count}
- `write_to_file`: {count}
- `execute_command`: {count}
- `browser_action`: {count}
- Other: {count}

## Notes
{context/blockers/next_steps}
```

### 5. Cost Estimation Logic
Use these rates (per 1M tokens) for the "Estimated Cost" field:
- **Claude 3.5 Sonnet**: $3.00 Input / $15.00 Output
- **Claude 3 Opus**: $15.00 Input / $75.00 Output
- **Claude 3 Haiku**: $0.25 Input / $1.25 Output
- **GPT-4o**: $5.00 Input / $15.00 Output
- Others: Estimate based on current market rates.
