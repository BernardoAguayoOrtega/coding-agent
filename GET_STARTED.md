# 🚀 Get Started in 60 Seconds

## You're Already Set Up! ✅

Everything is installed and configured with your Groq API key.

## Quick Test (30 seconds)

```bash
# 1. Activate virtual environment
source .venv/bin/activate

# 2. Run a simple test
python -m ai_dev_team "Create a Python script that prints Hello World"
```

## What Just Happened?

1. **Orchestrator** analyzed your request
2. **Product Manager** created specs
3. **Architect** designed the solution
4. **Backend Engineer** wrote the code
5. **Code Reviewer** checked quality
6. **QA Engineer** verified it works
7. **Evaluator** gave final approval

All in ~30 seconds for ~$0.002!

## Your First Real Project (2 minutes)

```bash
python -m ai_dev_team "Build a REST API for a task manager with:
- FastAPI framework
- SQLite database
- CRUD endpoints for tasks
- Each task has: title, description, status, due_date
- OpenAPI documentation"
```

**Output**: Complete working API in `workspace/` directory!

## What Makes This Special?

### 🤝 Human-in-the-Loop
You'll be asked to approve:
```
🤝 Human Approval Required
─────────────────────────────
write_file(main.py, ...)

The agent wants to: Create the main API file

Risk: MEDIUM

Approve this action? [Y/n]:
```

### 🔍 Automatic Quality Checks
Every file is analyzed:
```
📊 Code Quality Analysis
═══════════════════════
✅ Overall Score: 85/100
✅ Syntax: PASSED
✅ Complexity: Average 6.5 (good)
⚠️ Best Practices: 2 issues
  - Consider adding docstrings
  - Line too long at 42
```

### 💰 Cost Tracking
```
💰 Session Cost: $0.0234
📊 Tokens: 12,450 input / 8,320 output
```

## Advanced Examples

### Full-Stack App
```bash
python -m ai_dev_team "Build a blog with React frontend, Node.js backend, and MongoDB"
```

### From Design Mockup
```bash
python -m ai_dev_team "Recreate this UI" --image design.png
```

### Autonomous Mode (No Approvals)
```bash
python -m ai_dev_team "Build a calculator app" --auto-approve
```

### Interactive Session
```bash
python -m ai_dev_team --interactive

# Then type multiple requests:
> "Create a user authentication system"
> "Add password reset functionality"
> "Create email templates"
```

## Check Your Output

```bash
cd workspace
ls -la
```

You'll find:
- Complete source code
- Requirements files
- Documentation
- Tests (if requested)

## Example Output Structure

```
workspace/
├── src/
│   ├── main.py
│   ├── models.py
│   ├── routes.py
│   └── database.py
├── tests/
│   └── test_api.py
├── requirements.txt
├── README.md
└── api-spec.md
```

## Tips for Best Results

### ✅ Be Specific
```bash
"Build a REST API with FastAPI, PostgreSQL, JWT auth, and CRUD for users and posts"
```

### ❌ Too Vague
```bash
"Make an API"
```

### ✅ Include Details
- Framework preferences
- Database choice
- Authentication method
- Specific features needed
- Any design requirements

## Real-World Example

**Requirement:**
```bash
python -m ai_dev_team "Build a weather dashboard with:
- React frontend with Tailwind CSS
- Fetches data from OpenWeatherMap API
- Shows current weather and 5-day forecast
- Search by city name
- Display temperature, humidity, wind speed
- Responsive design for mobile
- Error handling for API failures
- Loading states"
```

**Result:**
- Complete React app with components
- API integration configured
- Beautiful UI with Tailwind
- Responsive design
- Error handling
- README with setup instructions
- Cost: ~$0.03
- Time: ~2 minutes

## Troubleshooting

### Nothing happens?
```bash
# Make sure venv is activated
source .venv/bin/activate

# Check installation
python test_install.py
```

### Cost concerns?
- Simple scripts: < $0.01
- REST APIs: $0.01 - $0.05
- Full-stack apps: $0.05 - $0.20

You can track in real-time!

### Want faster/cheaper?
Edit `.env`:
```
GROQ_MODEL=mixtral-8x7b-32768
```

## What Can You Build?

- ✅ Web applications (React, Vue, vanilla JS)
- ✅ REST APIs (FastAPI, Flask, Express)
- ✅ CLI tools (Python, Node.js)
- ✅ Automation scripts
- ✅ Database schemas
- ✅ Authentication systems
- ✅ CRUD applications
- ✅ Dashboards and admin panels
- ✅ From mockup to code

## Ready? Let's Build!

```bash
source .venv/bin/activate

python -m ai_dev_team "Build something amazing"
```

## Need Inspiration?

Check `examples/` directory:
```bash
cd examples
./01_simple_script.sh    # Python calculator
./02_rest_api.sh         # Bookstore API
./03_fullstack_todo.sh   # Complete todo app
./04_with_image.sh       # From design mockup
```

## Documentation

- **README.md** - Complete documentation
- **QUICKSTART.md** - 3-minute guide
- **SUMMARY.md** - What you built
- **This file** - Get started now!

---

## Your AI Dev Team Awaits! 🤖

**9 specialized agents** ready to build whatever you need.

**Cost:** Pennies per project

**Speed:** Minutes, not hours

**Quality:** Automatic code review and testing

**Your input:** Just describe what you want

Let's build! 🚀
