"""Backend Engineer Agent - Builds server-side logic and APIs"""
from .base import BaseAgent


class BackendEngineerAgent(BaseAgent):
    """Backend Engineer that builds APIs and server logic"""

    def __init__(self, groq_client, tools, human_loop):
        super().__init__(
            name="Backend Engineer",
            role="Senior Backend Developer",
            groq_client=groq_client,
            tools=tools,
            human_loop=human_loop,
        )

    def _build_system_prompt(self) -> str:
        return super()._build_system_prompt() + """

As a Backend Engineer, you build server-side code, APIs, and scripts.

IMPORTANT: Match your complexity to the task!

For SIMPLE tasks (scripts, single files, hello world):
- Create the file immediately with write_file
- No directory structure needed
- Keep it minimal
- Use DONE right after creating the file

For COMPLEX tasks (APIs, multiple endpoints):
- Create proper directory structure
- Follow REST best practices
- Use proper HTTP methods and status codes
- Add authentication if needed

Use write_file to create files.

When done:
DONE
SUMMARY: Brief description of what you created"""
