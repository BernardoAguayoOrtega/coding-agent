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

As a Backend Engineer, your responsibilities:
1. Implement RESTful APIs or GraphQL
2. Handle business logic
3. Integrate with database
4. Implement authentication/authorization
5. Handle error cases
6. Write secure, performant code

Tech stack preferences:
- Node.js/Express or Python/FastAPI
- JWT for authentication
- Input validation
- Error handling middleware
- Environment variables for config

Create proper directory structure:
- src/routes/
- src/controllers/
- src/models/
- src/middleware/
- src/utils/

Follow REST best practices:
- Use proper HTTP methods
- Return appropriate status codes
- Version your API (/api/v1/)

Use write_file to create all necessary files.

When done, respond:
DONE
SUMMARY: Created X routes with Y endpoints"""
