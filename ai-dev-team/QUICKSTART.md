# Quick Start Guide 🚀

Get your AI development team running in 3 minutes!

## Step 1: Install Dependencies

```bash
cd ai-dev-team

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install
pip install -r requirements.txt
```

## Step 2: Configure API Key

Your Groq API key is already set in `.env` file! ✅

To verify:
```bash
cat .env | grep GROQ_API_KEY
```

## Step 3: Test the System

### Simple Test

```bash
python -m ai_dev_team "Create a simple Python hello world script"
```

### Full-Stack Example

```bash
python -m ai_dev_team "Build a todo list app with:
- React frontend
- Python Flask backend
- SQLite database
- CRUD operations for todos
- Simple authentication"
```

### With Image Reference

```bash
python -m ai_dev_team "Recreate this UI design" --image path/to/mockup.png
```

### Interactive Mode

```bash
python -m ai_dev_team --interactive
```

## What Happens?

1. **Orchestrator** analyzes your requirements
2. **Product Manager** creates detailed specifications
3. **Architect** designs the system
4. **Engineers** (Frontend, Backend, Database) build the code
5. **Code Reviewer** checks quality using reflection
6. **QA Engineer** creates tests
7. **Evaluator** validates everything

All code is generated in the `workspace/` directory!

## Human-in-the-Loop

You'll be asked to approve:
- Critical file operations
- Code with quality issues
- Terminal commands
- Major decisions

To skip approvals (autonomous mode):
```bash
python -m ai_dev_team "..." --auto-approve
```

## Cost Tracking

Every run shows:
```
💰 Session Cost: $0.0123
📊 Tokens Used: 8,450 input / 5,320 output
```

Typical costs:
- Simple script: $0.001 - $0.01
- Full-stack app: $0.01 - $0.05
- Complex system: $0.05 - $0.20

## Tips

### Be Specific

✅ **Good:**
```bash
"Build a REST API for a bookstore with:
- FastAPI framework
- PostgreSQL database
- Endpoints for books, authors, orders
- JWT authentication
- OpenAPI documentation"
```

❌ **Too Vague:**
```bash
"Make an API"
```

### Use Images

Reference designs, mockups, or screenshots:
```bash
python -m ai_dev_team "Build this exact UI" --image figma-export.png
```

### Review Code Quality

The system automatically checks:
- ✅ Syntax correctness
- ✅ Code complexity
- ✅ Best practices
- ✅ Security issues
- ✅ SOLID principles

## Troubleshooting

### Import Error

```bash
# Make sure you're in the virtual environment
source .venv/bin/activate

# Reinstall
pip install -r requirements.txt
```

### API Key Error

```bash
# Check .env file exists
ls -la .env

# Verify key is set
cat .env | grep GROQ_API_KEY
```

### Permission Denied

```bash
# Make workspace directory writable
chmod 755 workspace
```

## Next Steps

Check the full [README.md](README.md) for:
- Advanced configuration
- Adding custom agents
- Integration with CI/CD
- More examples

## Example Session

```bash
$ python -m ai_dev_team "Build a weather app with React"

🚀 Initializing AI Dev Team...
✓ AI Dev Team initialized

📋 Project Requirements
Build a weather app with React

🎯 Phase 1: Planning
Orchestrator analyzing requirements... ✓

📋 Execution Plan:
Tech Stack:
  Frontend: React
  Backend: Node.js/Express
  Database: PostgreSQL

Phases:
  1. Requirements  → ProductManager
  2. Architecture  → Architect
  3. Frontend      → FrontendEngineer
  4. Backend       → BackendEngineer
  5. Quality       → CodeReviewer, QAEngineer
  6. Validation    → Evaluator

🤝 Approve this plan? [Y/n]: y

📦 Phase 1: Requirements
👤 ProductManager working... ✓
✓ ProductManager: Created requirements.md with 5 user stories

📦 Phase 2: Architecture
👤 Architect working... ✓
✓ Architect: Designed architecture with 3 components and 5 APIs

[... continues through all phases ...]

🎉 Project Execution Complete!

💰 Cost Summary:
  Total Cost: $0.0234
  Tokens: 12,450 input / 8,320 output

📁 Output: workspace/
```

Happy building! 🚀
