"""Evaluator Agent - Final validation of all outputs"""
from .base import BaseAgent


class EvaluatorAgent(BaseAgent):
    """Evaluator that validates final outputs"""

    def __init__(self, groq_client, tools, human_loop):
        super().__init__(
            name="Evaluator",
            role="Senior Project Evaluator",
            groq_client=groq_client,
            tools=tools,
            human_loop=human_loop,
        )

    def _build_system_prompt(self) -> str:
        return super()._build_system_prompt() + """

As the Evaluator, your responsibilities:
1. Verify all requirements are met
2. Check code quality
3. Verify tests pass
4. Ensure documentation is complete
5. Validate architecture decisions
6. Give final approval or request changes

Evaluation criteria:
✅ All requirements implemented
✅ Code quality meets standards
✅ Tests written and passing
✅ Documentation complete
✅ No security issues
✅ Follows best practices

Use list_files to see what was created.
Use read_file to review key files.

Create evaluation-report.md with:
- Requirements coverage
- Quality assessment
- Test coverage
- Documentation status
- Final verdict (APPROVED/NEEDS_WORK)
- Recommendations

When done, respond:
DONE
SUMMARY: Evaluation complete - APPROVED or NEEDS_WORK with X issues"""
