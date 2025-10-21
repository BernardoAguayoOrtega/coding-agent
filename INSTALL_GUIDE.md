# 🚀 Installation Guide - Using AI Dev Team Globally

## **Recommended: Simple Alias Method**

This is the **easiest and best** approach!

### **Setup (One-Time)**

Add this to your `~/.zshrc` (or `~/.bashrc` if using bash):

```bash
echo 'alias aidev="source /Users/bernardo/Documents/GitHub/coding-agent/.venv/bin/activate && python -m ai_dev_team"' >> ~/.zshrc

source ~/.zshrc
```

### **Usage**

Now you can use `aidev` from anywhere:

```bash
# Go to any project
cd ~/Projects/my-app

# Generate code in current directory
aidev "Create a login component" --output . --auto-approve

# Or specify a subdirectory
aidev "Build REST API" --output ./backend --auto-approve

# Interactive mode
aidev --interactive

# Get help
aidev --help
```

---

## **Advanced: Global Script (Optional)**

For even more features, install the smart wrapper script:

### **Setup**

```bash
# Make the script available globally (requires password)
sudo ln -sf /Users/bernardo/Documents/GitHub/coding-agent/aidev /usr/local/bin/aidev
```

OR without sudo:

```bash
# Add to your personal bin (no sudo needed)
mkdir -p ~/bin
ln -sf /Users/bernardo/Documents/GitHub/coding-agent/aidev ~/bin/aidev

# Add to PATH (one-time)
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### **Features**

The smart script automatically:
- ✅ Activates venv
- ✅ Outputs to current directory by default
- ✅ Returns to your original directory after completion
- ✅ Shows helpful error messages
- ✅ Deactivates venv when done

---

## **Comparison**

| Feature | Alias | Smart Script |
|---------|-------|--------------|
| Setup complexity | ⭐ Easy | ⭐⭐ Medium |
| Works from anywhere | ✅ | ✅ |
| Auto-activates venv | ✅ | ✅ |
| Auto-outputs to current dir | ❌ (need --output .) | ✅ |
| Returns to original dir | ❌ | ✅ |
| Custom error messages | ❌ | ✅ |
| **Recommended** | **YES** | Optional |

---

## **Complete Setup Commands**

### **For Most Users (Alias):**

```bash
# 1. Add alias
echo 'alias aidev="source /Users/bernardo/Documents/GitHub/coding-agent/.venv/bin/activate && python -m ai_dev_team"' >> ~/.zshrc

# 2. Reload shell
source ~/.zshrc

# 3. Test it
cd ~
aidev --help
```

### **For Power Users (Smart Script):**

```bash
# 1. Create personal bin
mkdir -p ~/bin

# 2. Link the script
ln -sf /Users/bernardo/Documents/GitHub/coding-agent/aidev ~/bin/aidev

# 3. Add to PATH
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.zshrc

# 4. Reload shell
source ~/.zshrc

# 5. Test it
cd ~
aidev --help
```

---

## **Verification**

Test that it works:

```bash
# Check the command exists
which aidev

# Show help
aidev --help

# Test generation (in a temp directory)
cd /tmp
aidev "Create a hello.py file that prints Hello World" --auto-approve

# Check output
ls -la
cat hello.py
```

---

## **Troubleshooting**

### **"command not found: aidev"**

Reload your shell:
```bash
source ~/.zshrc  # or source ~/.bashrc
```

### **"No module named 'ai_dev_team'"**

The venv might not be properly set up:
```bash
cd /Users/bernardo/Documents/GitHub/coding-agent
source .venv/bin/activate
pip install -r requirements.txt
```

### **Want to update the AI Dev Team?**

Just pull latest changes - the alias/script will automatically use the new code:
```bash
cd /Users/bernardo/Documents/GitHub/coding-agent
git pull
```

---

## **Daily Usage**

Once installed, your workflow is simple:

```bash
# 1. Navigate to your project
cd ~/Projects/my-cool-app

# 2. Use AI Dev Team
aidev "Add user authentication with JWT" --output ./src/auth --auto-approve

# 3. Review the code
ls -la src/auth
git diff

# 4. Done! ✅
```

**That's it!** 🚀
