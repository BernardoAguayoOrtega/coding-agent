# ✅ Fixed! How to Use `aidev` Command

## **Setup Complete!**

The `aidev` alias is now installed in your `~/.zshrc` file.

---

## **Important: Reload Your Shell First**

After adding the alias, you need to reload your terminal:

```bash
# Option 1: Source zshrc
source ~/.zshrc

# Option 2: Start a new terminal tab/window
# Cmd+T for new tab
```

---

## **Verify It Works**

```bash
aidev --help
```

You should see:
```
Usage: python -m ai_dev_team [OPTIONS] [REQUIREMENTS]

  AI Dev Team - Your own AI software development team

Options:
  -i, --interactive         Interactive mode
  --image PATH              Include an image for analysis
  --auto-approve            Skip approval prompts
  --max-iterations INTEGER  Max iterations per agent
  --output PATH             Output directory
  -v, --verbose             Verbose output
  --help                    Show this message and exit.
```

---

## **Usage Examples**

### **1. Generate in Current Directory**

```bash
cd ~/Projects/my-app
aidev "Create a login component" --output . --auto-approve
```

### **2. Generate in Specific Folder**

```bash
cd ~/Projects/blog
aidev "Build REST API" --output ./backend --auto-approve
```

### **3. Interactive Mode**

```bash
aidev --interactive
```

Then type your requests:
```
Enter project requirements: Create a navbar component
Enter project requirements: Add dark mode toggle
Enter project requirements: quit
```

### **4. With Image/Design**

```bash
aidev "Build this UI" --image mockup.png --output ./src --auto-approve
```

### **5. Verbose Mode (See Details)**

```bash
aidev "Create a Python calculator" --output . --verbose --auto-approve
```

---

## **Complete Workflow Example**

```bash
# 1. Go to your project
cd ~/Projects/my-react-app

# 2. Use aidev to add a feature
aidev "Create a UserProfile component with avatar, name, email, and edit button using Tailwind CSS" --output ./src/components --auto-approve

# 3. Check what was created
ls -la src/components

# 4. Review the code
cat src/components/UserProfile.jsx

# 5. Test it
npm start
```

---

## **Tips**

### **Always Include `--output`**

The alias doesn't auto-output to current directory, so specify it:

```bash
# ✅ Good
aidev "..." --output . --auto-approve

# ❌ Will output to workspace/ in AI Dev Team directory
aidev "..." --auto-approve
```

### **Use `--auto-approve` for Speed**

Skip approval prompts:
```bash
aidev "..." --output . --auto-approve
```

### **Check Costs After Each Run**

You'll see:
```
💰 Cost Summary:
│ Total Cost    │ $0.0054 │
```

---

## **Troubleshooting**

### **"command not found: aidev"**

You need to reload your shell:
```bash
source ~/.zshrc
```

Or open a new terminal tab/window.

### **"No module named 'ai_dev_team'"**

The virtual environment isn't set up:
```bash
cd /Users/bernardo/Documents/GitHub/coding-agent
source .venv/bin/activate
pip install -r requirements.txt
```

### **Output going to wrong directory**

Make sure to specify `--output`:
```bash
aidev "..." --output . --auto-approve
```

---

## **What the Alias Does**

When you run `aidev`, it:
1. ✅ Activates the virtual environment
2. ✅ Runs the AI Dev Team with your requirements
3. ✅ Uses Groq API (fast & cheap!)
4. ✅ Shows cost tracking
5. ✅ Generates code where you specify

---

## **Quick Reference**

```bash
# Basic usage
aidev "YOUR REQUIREMENTS" --output . --auto-approve

# With all options
aidev "YOUR REQUIREMENTS" \
  --output ./path \
  --auto-approve \
  --verbose \
  --max-iterations 100

# Interactive
aidev --interactive

# Help
aidev --help
```

---

## **Ready to Build! 🚀**

```bash
# Try it now
cd /tmp
aidev "Create a hello.py file that prints Hello World" --output . --auto-approve
cat hello.py
python hello.py
```

**Happy coding!** 💻✨
