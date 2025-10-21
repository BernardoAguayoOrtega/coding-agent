"""Code Reviewer Agent - Reviews code quality using reflection"""
from .base import BaseAgent
from ..reflection import CodeAnalyzer


class CodeReviewerAgent(BaseAgent):
    """Code Reviewer that analyzes code quality"""

    def __init__(self, groq_client, tools, human_loop):
        super().__init__(
            name="Code Reviewer",
            role="Senior Code Reviewer",
            groq_client=groq_client,
            tools=tools,
            human_loop=human_loop,
        )
        self.analyzer = CodeAnalyzer()

    def _build_system_prompt(self) -> str:
        return super()._build_system_prompt() + """

As a Code Reviewer, your responsibilities:
1. Review all code files for quality
2. Check for best practices
3. Identify security issues
4. Suggest improvements
5. Verify code meets standards

Review criteria:
- Code clarity and readability
- Proper error handling
- Security vulnerabilities
- Performance issues
- Test coverage
- Documentation

Use list_files to find code files, then read_file to review them.

For each file, provide:
- Overall assessment
- Issues found
- Suggestions for improvement

Use write_file to create code-review.md with findings.

When done, respond:
DONE
SUMMARY: Reviewed X files, found Y issues"""

    def review_code(self, directory: str = ".") -> dict:
        """Review all code in directory"""
        # List files
        file_list = self.tools["file_ops"].list_files(directory)

        # Find code files
        code_files = []
        for line in file_list.split("\n"):
            if any(ext in line for ext in [".py", ".js", ".ts", ".jsx", ".tsx"]):
                # Extract filename
                parts = line.split()
                if len(parts) >= 2:
                    code_files.append(parts[1])

        # Analyze each file
        results = []
        for filepath in code_files:
            if filepath.endswith(".py"):
                analysis = self.analyzer.analyze_python(filepath)
                results.append(analysis)
            elif filepath.endswith((".js", ".jsx", ".ts", ".tsx")):
                analysis = self.analyzer.analyze_javascript(filepath)
                results.append(analysis)

        return {"files_reviewed": len(results), "results": results}
