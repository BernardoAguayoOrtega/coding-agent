"""Frontend Engineer Agent - Builds user interfaces"""
from .base import BaseAgent


class FrontendEngineerAgent(BaseAgent):
    """Frontend Engineer that builds UIs"""

    def __init__(self, groq_client, tools, human_loop):
        super().__init__(
            name="Frontend Engineer",
            role="Senior Frontend Developer",
            groq_client=groq_client,
            tools=tools,
            human_loop=human_loop,
        )

    def _build_system_prompt(self) -> str:
        return super()._build_system_prompt() + """

As a Frontend Engineer, your responsibilities:
1. Build React/Vue/etc components
2. Implement responsive design
3. Handle state management
4. Integrate with backend APIs
5. Ensure accessibility
6. Write clean, maintainable code

Tech stack preferences:
- React with functional components and hooks
- CSS Modules or Tailwind CSS
- TypeScript for type safety
- Axios or Fetch for API calls

Create proper directory structure:
- src/components/
- src/pages/
- src/services/
- src/utils/

Use write_file to create all necessary files.

When done, respond:
DONE
SUMMARY: Created X components and Y pages"""
