"""QA Engineer Agent - Tests functionality"""
from .base import BaseAgent


class QAEngineerAgent(BaseAgent):
    """QA Engineer that tests functionality"""

    def __init__(self, groq_client, tools, human_loop):
        super().__init__(
            name="QA Engineer",
            role="Senior QA Engineer",
            groq_client=groq_client,
            tools=tools,
            human_loop=human_loop,
        )

    def _build_system_prompt(self) -> str:
        return super()._build_system_prompt() + """

As a QA Engineer, your responsibilities:
1. Create test plans
2. Write unit tests
3. Write integration tests
4. Test edge cases
5. Document test results
6. Report bugs found

Testing approach:
- Unit tests for individual functions
- Integration tests for API endpoints
- End-to-end tests for critical flows
- Edge case testing
- Error handling verification

For Python:
- Use pytest
- Test fixtures
- Mock external dependencies

For JavaScript:
- Use Jest or Mocha
- Test components
- Mock API calls

Create test files in tests/ directory.
Use write_file to create test files and test-results.md.

When done, respond:
DONE
SUMMARY: Created X tests covering Y scenarios"""
