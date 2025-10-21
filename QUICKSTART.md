# Quick Start - 3 Simple Steps

Get your AI development team running in under 2 minutes.

## Step 1: Install (30 seconds)

```bash
cd /path/to/coding-agent

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Configure (30 seconds)

```bash
# Add your Groq API key to .env
echo "GROQ_API_KEY=your_key_here" > .env
```

Get a free API key at: **https://console.groq.com/keys**

## Step 3: Build Something! (1 minute)

```bash
# Simple test
python -m ai_dev_team "Create a Python hello world script"

# Full application
python -m ai_dev_team "Build a todo app with React and Flask"

# Interactive mode
python -m ai_dev_team --interactive
```

## That's It!

Your code will be in the `workspace/` directory.

**Typical cost:** $0.001 - $0.05 per project
**Typical time:** 10 seconds - 3 minutes

## Optional: Use From Anywhere

```bash
# Add alias to your shell
echo 'alias aidev="source /path/to/coding-agent/.venv/bin/activate && python -m ai_dev_team"' >> ~/.zshrc
source ~/.zshrc

# Now use from any directory
cd ~/Projects/my-app
aidev "Add user authentication" --output ./src --auto-approve
```

## Need More Help?

- **Full Documentation:** See [README.md](README.md)
- **Examples:** Check `/examples` directory
- **Troubleshooting:** See README's troubleshooting section

## Common Commands

```bash
# Generate in current directory
aidev "..." --output . --auto-approve

# Skip approvals (autonomous mode)
aidev "..." --auto-approve

# See detailed logs
aidev "..." --verbose

# Use with design mockup
aidev "Build this UI" --image design.png

# Get help
aidev --help
```

Happy building! 🚀
