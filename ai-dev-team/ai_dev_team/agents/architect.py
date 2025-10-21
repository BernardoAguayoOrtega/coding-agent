"""Software Architect Agent - Designs system architecture"""
from .base import BaseAgent


class ArchitectAgent(BaseAgent):
    """Software Architect that designs system architecture"""

    def __init__(self, groq_client, tools, human_loop):
        super().__init__(
            name="Software Architect",
            role="Senior Software Architect",
            groq_client=groq_client,
            tools=tools,
            human_loop=human_loop,
        )

    def _build_system_prompt(self) -> str:
        return super()._build_system_prompt() + """

As a Software Architect, your responsibilities:
1. Design overall system architecture
2. Choose appropriate design patterns
3. Define component structure
4. Create database schema design
5. Define API contracts
6. Document architectural decisions

Use write_file to create:
- architecture.md: System architecture documentation
- api-spec.md: API endpoints and contracts

Focus on:
- Scalability
- Maintainability
- Security
- Performance

When done, respond:
DONE
SUMMARY: Created architecture with X components and Y APIs"""
