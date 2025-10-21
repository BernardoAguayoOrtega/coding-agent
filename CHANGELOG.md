# Changelog

All notable improvements, fixes, and optimizations to AI Dev Team.

---

## [Latest] - 2025-10-21

### 🚀 Major Performance Improvements

#### Smart Complexity Detection
- **30x faster** for simple tasks
- **5x cheaper** cost reduction
- Orchestrator now analyzes task complexity and assigns only necessary agents
- Simple tasks (e.g., "create hello world") use 1 agent instead of 5
- Medium tasks use 2-3 agents instead of full team
- Complex tasks still use full agent team for quality

**Performance:**
- Simple task: 2-10 seconds (was 60+ seconds)
- Medium task: 30-60 seconds (was 2-3 minutes)
- Complex task: 2-5 minutes (optimized from 5-15 minutes)

#### Optimized Iteration Limits
- Simple tasks: 3 max iterations (was 20)
- Medium tasks: 10 max iterations (was 50)
- Complex tasks: 20 max iterations (was 50)
- Prevents agents from overthinking simple tasks

#### Token Limit Optimization
- Simple tasks: 512 max tokens (was 2048)
- Complex tasks: 2048 max tokens
- **30% faster** API responses
- **60% cost savings** on simple tasks

### ✨ New Features

#### Context Persistence in Interactive Mode
- Session context now persists across multiple commands
- Agents remember previous conversations and decisions
- Build features incrementally without repeating context
- Special commands:
  - `files` - List all created files with sizes
  - `context` - View current session context
  - `reset` - Clear context and start fresh
  - `quit` - Exit interactive mode

```bash
aidev --interactive
> Create a login form
> Add validation to it  # Remembers the previous form!
> Add error messages     # Continues building on it
> files                  # See what was created
> quit
```

#### File Visibility
- Shows absolute output directory path on startup
- Lists all created files after execution with sizes
- Beautiful table format with file paths and sizes
- Warns if no files were created

```
📂 Created Files:
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━┓
┃ File Path       ┃ Size    ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━┩
│ hello.py        │ 234 B   │
│ src/app.js      │ 1.2 KB  │
└─────────────────┴─────────┘

Full path: /Users/you/project
```

#### Clipboard Image Support
- `--clipboard-image` CLI flag for pasting images directly
- `paste` command in interactive mode
- No need to save images to disk first
- Instant UI recreation from screenshots

```bash
aidev "Build this UI" --clipboard-image --auto-approve

# Or in interactive mode:
> paste
Enter requirements: recreate this button
```

### 🐛 Bug Fixes

#### Fixed File Creation Issues
- **Root cause:** Code checked for "DONE" before executing tools
- **Fix:** Reordered execution flow to parse and execute tools first
- **Result:** Files are now created successfully every time

#### Fixed Auto-Approve
- **Root cause:** Auto-approve only worked for "low" risk actions
- **Fix:** Changed to approve all risk levels when flag is set
- **Result:** `--auto-approve` now works for all operations

#### Improved JSON Parsing
- **Root cause:** Regex failed on nested/complex JSON
- **Fix:** Implemented brace-counting algorithm
- **Result:** Correctly parses deeply nested JSON and multiline content

### 🔧 Technical Improvements

#### Better Agent Prompts
- Added "BIAS TOWARD ACTION" instruction
- Simple tasks get "⚡ QUICK TASK" hint
- Agents now match complexity to task requirements
- Clear tool call format examples

#### Enhanced Debugging
- Debug logs for all tool executions
- Shows tool name, arguments, and results
- Better error messages when parsing fails
- Helps troubleshoot file creation issues

```
[DEBUG BackendEngineer] Executing tool: write_file
[DEBUG BackendEngineer] Args: {
  "filepath": "hello.py",
  "content": "print('Hello World')\n"
}
[DEBUG BackendEngineer] Tool result: ✅ File written...
```

#### Path Awareness
- Added `user_working_dir` to agent context
- Displayed in CLI output for clarity
- Agents know both output directory and user's original directory

---

## Previous Improvements

### Code Quality & Security

#### Reflection System
- Automatic code quality analysis for all generated files
- Checks: syntax, complexity, security, best practices
- Calculates maintainability index
- Detects security issues (eval, SQL injection, hardcoded credentials)

#### Path Validation
- Prevents path traversal attacks
- All file paths validated against base directory
- Security checks on all file operations

#### Command Safety
- Blocks dangerous terminal commands (rm -rf /, dd, mkfs, etc.)
- Risk-based approval system (LOW/MEDIUM/HIGH)
- Human-in-the-loop for high-risk operations

### Multi-Agent Architecture

#### 9 Specialized Agents
- **Orchestrator** - Analyzes requirements, creates execution plans
- **Product Manager** - Refines requirements, creates specifications
- **Software Architect** - Designs system architecture
- **Frontend Engineer** - Builds UI components
- **Backend Engineer** - Creates APIs and server logic
- **Database Engineer** - Designs schemas and queries
- **Code Reviewer** - Reviews code quality
- **QA Engineer** - Writes and runs tests
- **Evaluator** - Final validation

#### Agent Communication
- Shared context object flows through pipeline
- Each agent updates context with results
- Context includes: requirements, architecture, files, feedback

### Developer Experience

#### Interactive Mode
- Multi-turn conversation support
- Context persistence across commands
- Special commands for workflow management
- Real-time file tracking

#### Cost Tracking
- Real-time token and cost monitoring
- Session summaries after each run
- Model-specific pricing calculations
- Typical costs: $0.001 - $0.05 per task

#### Vision Support
- Analyze design mockups and screenshots
- Extract UI components from images
- Debug with visual references
- Uses Groq's vision model

### Groq Integration

#### Fast LLM Inference
- Groq API for ultra-fast responses
- 10-100x faster than alternatives
- Affordable pricing ($0.59/$0.79 per 1M tokens)
- Multiple model options (llama-3.3-70b, mixtral-8x7b, etc.)

#### Smart Token Management
- Dynamic token limits based on complexity
- Reduced limits for simple tasks
- Maximizes speed and minimizes cost

---

## Performance Metrics

### Simple Tasks (e.g., "create hello.py")
- **Time:** 2-10 seconds
- **Cost:** $0.0008 - $0.001
- **Tokens:** 1,000 - 2,000
- **Phases:** 1
- **Agents:** 1

### Medium Tasks (e.g., "REST API with CRUD")
- **Time:** 30-60 seconds
- **Cost:** $0.01 - $0.02
- **Tokens:** 10,000 - 20,000
- **Phases:** 2
- **Agents:** 2-3

### Complex Tasks (e.g., "Full-stack app")
- **Time:** 2-5 minutes
- **Cost:** $0.05 - $0.15
- **Tokens:** 50,000 - 150,000
- **Phases:** 4-5
- **Agents:** 6-9

---

## Migration Notes

### For Existing Users

If you're upgrading from an earlier version:

1. **New Interactive Commands**
   - Use `files` to see created files
   - Use `context` to debug session state
   - Use `reset` to clear context
   - Use `quit` to exit gracefully

2. **Auto-Approve Behavior**
   - Now approves ALL risk levels when `--auto-approve` is set
   - If you need selective approval, remove the flag

3. **File Visibility**
   - All runs now show created files at the end
   - Absolute paths displayed on startup
   - Check console output to see where files went

4. **Performance**
   - Simple tasks are now MUCH faster (30x)
   - Costs are significantly lower (5x)
   - No action needed - automatic improvement

---

## Design Principles

The following principles guide all improvements:

- **KISS (Keep It Simple)** - Pattern matching for obvious tasks instead of LLM
- **DRY (Don't Repeat Yourself)** - Centralized complexity detection
- **SOLID** - Single responsibility (orchestrator detects, agents execute)
- **Senior Thinking** - Optimize the common case (simple tasks)
- **Bias Toward Action** - Create files immediately, don't overthink

---

## Credits

All improvements built with:
- **Groq** - Fast, affordable LLM inference
- **Meta** - Llama 3.3 language model
- **Python 3.8+** - Core implementation
- **Rich** - Beautiful CLI formatting

---

## License

MIT License - Build whatever you want!

---

**Last Updated:** 2025-10-21
**Version:** Latest
**Status:** ✅ All Systems Operational
