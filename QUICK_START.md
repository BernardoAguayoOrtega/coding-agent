# 🚀 AI Dev Team - Quick Start Guide

## ✅ **Everything is Ready!**

Your AI Dev Team is now installed and configured.

---

## **📍 Step 1: Reload Your Terminal**

Open a **new terminal tab** or run:
```bash
source ~/.zshrc
```

---

## **🧪 Step 2: Test It Works**

```bash
aidev --help
```

You should see:
```
Usage: python -m ai_dev_team [OPTIONS] [REQUIREMENTS]

Options:
  -i, --interactive         Interactive mode
  --image PATH              Include an image for analysis
  --auto-approve            Skip approval prompts
  --max-iterations INTEGER  Max iterations per agent
  --output PATH             Output directory
  -v, --verbose             Verbose output
  --help                    Show this message and exit.
```

✅ **If you see this, you're ready!**

---

## **🎯 Step 3: Try Your First Generation**

```bash
# Go to a test directory
cd /tmp

# Generate a simple Python file
aidev "Create a hello.py file that prints Hello World" --output . --auto-approve

# Check it was created
ls -la hello.py
cat hello.py

# Run it!
python3 hello.py
```

---

## **💡 Usage Template**

```bash
aidev "YOUR REQUIREMENTS HERE" --output . --auto-approve
```

### **Key Options:**

- `--output .` → Output to current directory
- `--output ./path` → Output to specific folder
- `--auto-approve` → Skip approval prompts (faster)
- `--verbose` → See detailed logs
- `--interactive` → Multi-turn conversation mode

---

## **📚 Real Examples**

### **Example 1: Add to React App**
```bash
cd ~/Projects/my-react-app

aidev "Create a Navbar component with logo, navigation links, and mobile menu using Tailwind CSS" \
  --output ./src/components \
  --auto-approve
```

### **Example 2: Build REST API**
```bash
cd ~/Projects/my-api

aidev "Create Express routes for user CRUD operations with validation and error handling" \
  --output ./routes \
  --auto-approve
```

### **Example 3: Generate Tests**
```bash
cd ~/Projects/my-python-app

aidev "Create pytest unit tests for the Calculator class in utils/calculator.py" \
  --output ./tests \
  --auto-approve
```

### **Example 4: From Design Image**
```bash
cd ~/Projects/landing-page

aidev "Build this landing page" \
  --image design.png \
  --output ./src \
  --auto-approve
```

---

## **💰 Cost Tracking**

After each run, you'll see:
```
💰 Cost Summary:
│ Total Cost    │ $0.0054 │
│ Input Tokens  │ 5,429   │
│ Output Tokens │ 2,826   │
```

**Typical costs:**
- Simple script: $0.001 - $0.01
- REST API: $0.01 - $0.05
- Full-stack app: $0.05 - $0.20

**Very affordable!** ✨

---

## **🎮 Interactive Mode**

For multiple requests in one session:

```bash
aidev --interactive

# Then type:
Enter project requirements: Create a User model
Enter project requirements: Create a Post model
Enter project requirements: Create API routes for both
Enter project requirements: quit
```

---

## **🐛 Troubleshooting**

### **"command not found: aidev"**
```bash
source ~/.zshrc
# Or open a new terminal tab
```

### **"No module named 'ai_dev_team'"**
```bash
cd /Users/bernardo/Documents/GitHub/coding-agent
source .venv/bin/activate
pip install -e .
```

### **Need help?**
```bash
aidev --help
```

---

## **🎯 Complete Workflow**

```bash
# 1. Navigate to your project
cd ~/Projects/your-app

# 2. Generate what you need
aidev "Create authentication middleware with JWT" \
  --output ./middleware \
  --auto-approve

# 3. Review the code
ls -la middleware/
cat middleware/auth.js

# 4. Test it
npm test

# 5. Commit
git add middleware/
git commit -m "Add JWT authentication middleware"
```

---

## **📖 Documentation**

- **`START_HERE.txt`** - Quick reference
- **`HOW_TO_USE.md`** - Detailed usage guide
- **`README.md`** - Full documentation
- **`SUMMARY.md`** - Architecture overview
- **`examples/`** - Example scripts

---

## **🚀 You're Ready!**

```bash
aidev "Build something amazing" --output . --auto-approve
```

**Happy coding!** 💻✨

---

## **Pro Tips**

### ✅ **Always Specify `--output`**
```bash
aidev "..." --output . --auto-approve
```

### ✅ **Use Verbose for Debugging**
```bash
aidev "..." --output . --verbose
```

### ✅ **Review Before Committing**
```bash
git diff  # See what was changed
```

### ✅ **Iterate and Refine**
```bash
# First generation
aidev "Create login form" --output . --auto-approve

# Refine it
aidev "Add form validation and error messages to login.jsx" --output . --auto-approve
```

---

**Need help?** Check the documentation files or run `aidev --help`

🎉 **Enjoy your AI development team!**
