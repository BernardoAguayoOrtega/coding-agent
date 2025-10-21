"""Product Manager Agent - Refines requirements and creates specifications"""
from .base import BaseAgent


class ProductManagerAgent(BaseAgent):
    """Product Manager that refines requirements"""

    def __init__(self, groq_client, tools, human_loop):
        super().__init__(
            name="Product Manager",
            role="Product Manager and Requirements Specialist",
            groq_client=groq_client,
            tools=tools,
            human_loop=human_loop,
        )

    def _build_system_prompt(self) -> str:
        return super()._build_system_prompt() + """

As a Product Manager, your responsibilities:
1. Clarify vague requirements
2. Create detailed user stories
3. Define acceptance criteria
4. Document functional and non-functional requirements
5. Create a product specification document

Use write_file to create a requirements.md document.

When done, respond:
DONE
SUMMARY: Created product specification with X user stories"""
