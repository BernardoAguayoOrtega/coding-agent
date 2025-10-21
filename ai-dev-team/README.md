# AI Dev Team 🤖

**Your own AI software development team in a single CLI tool**

A multi-agent system powered by Groq that acts as a complete full-stack development team. Give it requirements, and watch as specialized AI agents collaborate to build your project.

## ✨ Features

- 🎯 **Orchestrator Agent** - Analyzes requirements and divides work intelligently
- 👔 **Product Manager** - Clarifies requirements and creates specifications
- 🏗️ **Software Architect** - Designs system architecture and patterns
- 💻 **Frontend Engineer** - Builds UI with React, Vue, or your choice
- ⚙️ **Backend Engineer** - Creates APIs and server-side logic
- 🗄️ **Database Engineer** - Designs schemas and queries
- 🔍 **Code Reviewer** - Reviews code quality with reflection techniques
- 🧪 **QA Engineer** - Tests and finds edge cases
- ✅ **Evaluator Agent** - Validates all outputs for quality

### Advanced Capabilities

- 🔄 **Reflection System** - Automatic code quality evaluation
- 🖥️ **Terminal Integration** - Full file system and command execution
- 🖼️ **Vision Support** - Can view and analyze images/screenshots
- 🤝 **Human-in-the-Loop** - Requests approval for critical actions
- 💰 **Cost Tracking** - Monitors API usage (typically $0.001-0.01 per task)

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or navigate to the ai-dev-team directory
cd ai-dev-team

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your Groq API key
# Get one free at: https://console.groq.com/keys
nano .env  # or use your favorite editor
```

### 3. Run Your First Project

```bash
# Start the AI dev team
python -m ai_dev_team.cli "Build a todo app with React frontend and Flask backend"

# Or use interactive mode
python -m ai_dev_team.cli --interactive
```

## 📖 Usage Examples

### Full-Stack Web App

```bash
python -m ai_dev_team.cli "Create a blog platform with:
- React frontend with Tailwind CSS
- Node.js/Express backend
- PostgreSQL database
- User authentication
- CRUD for blog posts
- Responsive design"
```

### API Development

```bash
python -m ai_dev_team.cli "Build a REST API for a bookstore:
- FastAPI framework
- SQLite database
- Endpoints for books, authors, customers
- JWT authentication
- OpenAPI documentation"
```

### With Image Reference

```bash
python -m ai_dev_team.cli "Recreate this design" --image screenshot.png
```

## 🎮 CLI Options

```bash
python -m ai_dev_team.cli [OPTIONS] "your requirements"

Options:
  -i, --interactive       Interactive mode for multi-turn conversation
  --image PATH           Include an image for the agents to analyze
  --no-reflection        Disable code quality reflection
  --auto-approve         Skip human approval prompts (autonomous mode)
  --max-iterations N     Maximum agent iterations (default: 50)
  --output DIR           Output directory (default: ./workspace)
  -v, --verbose          Show detailed logs
  --help                 Show help message
```

## 🏗️ Architecture

### Agent Flow

```
User Requirements
    ↓
[Orchestrator] → Analyzes and creates work plan
    ↓
[Product Manager] → Refines requirements
    ↓
[Architect] → Designs system
    ↓
[Frontend Engineer] → Builds UI
[Backend Engineer] → Builds API
[Database Engineer] → Designs schema
    ↓
[Code Reviewer] → Reviews with reflection
    ↓
[QA Engineer] → Tests functionality
    ↓
[Evaluator] → Final validation
    ↓
Completed Project ✅
```

### Agent Communication

Agents communicate through a shared context that includes:
- **Requirements** - Original and refined specifications
- **Architecture** - System design decisions
- **Code** - All generated files
- **Feedback** - Code review and QA findings
- **Actions** - File operations, terminal commands

### Reflection System

Each code file is automatically analyzed using:
1. **Linter** - Syntax and style (PEP8, ESLint)
2. **Best Practices** - Framework conventions
3. **SOLID Principles** - Design patterns
4. **DRY** - Code duplication detection
5. **Security** - Common vulnerabilities
6. **Performance** - Optimization opportunities

### Human-in-the-Loop

You'll be asked to approve:
- Critical file operations (delete, overwrite)
- Code with quality issues flagged by reflection
- Terminal commands that could affect system
- Major architectural decisions
- Deployment actions

## 💰 Cost Estimation

Using Groq's pricing (as of 2024):
- Simple CRUD app: ~$0.002 - $0.01
- Full-stack app: ~$0.01 - $0.05
- Complex system: ~$0.05 - $0.20

**Why so cheap?** Groq's inference is incredibly fast and affordable compared to alternatives.

## 🛠️ Configuration

Edit `.env` file:

```bash
# Use faster but smaller model for cost savings
GROQ_MODEL=mixtral-8x7b-32768

# Disable verbose logging
VERBOSE=false

# Auto-approve for autonomous operation
AUTO_APPROVE=true

# Limit iterations for budget control
MAX_ITERATIONS=30
```

## 📁 Project Structure

```
ai-dev-team/
├── ai_dev_team/
│   ├── agents/          # Agent definitions
│   │   ├── base.py      # Base agent class
│   │   ├── orchestrator.py
│   │   ├── product_manager.py
│   │   ├── architect.py
│   │   ├── frontend_engineer.py
│   │   ├── backend_engineer.py
│   │   ├── database_engineer.py
│   │   ├── code_reviewer.py
│   │   ├── qa_engineer.py
│   │   └── evaluator.py
│   ├── tools/           # Agent tools
│   │   ├── file_ops.py  # File operations
│   │   ├── terminal.py  # Command execution
│   │   └── vision.py    # Image analysis
│   ├── reflection/      # Code quality
│   │   └── analyzer.py
│   ├── utils/
│   │   └── human_loop.py
│   ├── config.py
│   ├── groq_client.py
│   └── cli.py           # Main CLI
├── workspace/           # Generated projects (gitignored)
├── .env                 # Your configuration (gitignored)
├── .env.example
├── requirements.txt
└── README.md
```

## 🤔 How It Works

1. **You provide requirements** - Via CLI or interactive mode
2. **Orchestrator analyzes** - Breaks down into agent-specific tasks
3. **Agents collaborate** - Each specialist does their part
4. **Reflection validates** - Code quality is automatically checked
5. **Evaluator confirms** - Final validation before delivery
6. **You approve** - Human-in-the-loop for critical decisions
7. **Project delivered** - Ready-to-run code in workspace/

## 🎯 Best Practices

### Writing Good Requirements

✅ **Good:**
```
Build a task management app with:
- User authentication (email/password)
- Create, edit, delete tasks
- Task categories and tags
- Due dates and reminders
- React frontend, Node.js backend
- MongoDB database
```

❌ **Too Vague:**
```
Make me an app
```

### Using Images

```bash
# Reference a design mockup
python -m ai_dev_team.cli "Build this UI" --image design.png

# Debug with screenshot
python -m ai_dev_team.cli "Fix the layout issue shown here" --image bug.png
```

## 🐛 Troubleshooting

### API Key Issues

```bash
# Verify your API key is set
echo $GROQ_API_KEY

# Or check .env file
cat .env
```

### Permission Errors

```bash
# Make sure workspace directory is writable
mkdir -p workspace
chmod 755 workspace
```

### Agent Not Following Requirements

- Be more specific in requirements
- Use `--verbose` to see agent reasoning
- Provide reference images if applicable

## 🚀 Advanced Usage

### Custom Agent Flow

Edit `ai_dev_team/agents/orchestrator.py` to customize how work is divided among agents.

### Adding New Agents

1. Create new file in `ai_dev_team/agents/`
2. Extend `BaseAgent` class
3. Define system prompt and tools
4. Register in orchestrator

### Integration with CI/CD

```bash
# Generate code without human approval
python -m ai_dev_team.cli "..." --auto-approve --output ./build
```

## 📊 Monitoring

Cost tracking is automatic:

```
💰 Session Cost: $0.0234
📊 Tokens Used: 12,450 input / 8,320 output
⏱️  Time: 45s
```

## 🤝 Contributing

This is your personal dev team! Feel free to:
- Add new agent types
- Improve reflection techniques
- Enhance tool capabilities
- Add framework-specific templates

## 📝 License

MIT License - Build whatever you want!

## 🙏 Credits

- **Groq** - For blazing fast, affordable LLM inference
- **Llama 3.3** - Meta's powerful language model
- Built with inspiration from AutoGPT, GPT-Engineer, and DevGPT

---

**Made with ❤️ for developers who want to build faster**

Need help? Open an issue or check the examples in `examples/` directory.
