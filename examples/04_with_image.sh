#!/bin/bash
# Example 4: Build from image mockup

source ../.venv/bin/activate

# Place your design mockup in examples/design.png
python -m ai_dev_team "Recreate this exact UI design with React and Tailwind CSS" \
  --image examples/design.png
