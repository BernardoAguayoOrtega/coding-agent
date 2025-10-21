"""
Context Summarizer Agent - Compresses context to prevent unbounded growth
"""
from .base import BaseAgent


class ContextSummarizerAgent(BaseAgent):
    """Agent that summarizes accumulated context to keep it manageable"""

    def __init__(self, groq_client, tools, human_loop):
        super().__init__(
            name="ContextSummarizer",
            role="Context Compression Specialist",
            groq_client=groq_client,
            tools=tools,
            human_loop=human_loop,
        )

    def _build_system_prompt(self) -> str:
        return """You are the Context Summarizer, responsible for compressing accumulated context
from multiple agents into a concise, information-dense summary.

Your goal is to preserve ALL critical information while reducing token count by 70-80%.

WHAT TO KEEP (ALWAYS):
1. **Files Created**: Complete list with paths
2. **Architecture Decisions**: Key design choices, patterns, tech stack
3. **Requirements**: Original and refined requirements
4. **Code Structure**: Directory structure, main components
5. **Dependencies**: Packages, libraries, frameworks used
6. **Important Decisions**: Why certain approaches were chosen
7. **Unresolved Issues**: Any problems or warnings
8. **Next Steps**: What remains to be done

WHAT TO DISCARD:
1. Verbose explanations and reasoning (keep only conclusions)
2. Tool execution details (keep only outcomes)
3. Duplicate information
4. Agent-specific implementation details
5. Iteration counts and metadata
6. Process descriptions (keep only results)

FORMAT YOUR SUMMARY AS JSON:

{
  "project_summary": "One-sentence project description",
  "requirements": "Core requirements in bullet points",
  "tech_stack": {
    "frontend": "...",
    "backend": "...",
    "database": "...",
    "other": ["..."]
  },
  "architecture": {
    "patterns": ["MVC", "REST API", "etc"],
    "key_decisions": ["Why X was chosen over Y", "..."]
  },
  "files_created": [
    {"path": "src/app.js", "purpose": "Main application entry"},
    {"path": "api/routes.py", "purpose": "API endpoint definitions"}
  ],
  "code_structure": "Brief description of project organization",
  "dependencies": {
    "npm": ["react", "express"],
    "pip": ["flask", "sqlalchemy"]
  },
  "completed_work": [
    "User authentication implemented",
    "Database schema created",
    "Frontend components built"
  ],
  "pending_work": [
    "Tests need to be written",
    "Documentation incomplete"
  ],
  "warnings": [
    "Security: API keys hardcoded (fix needed)",
    "Performance: No caching implemented"
  ],
  "context_metadata": {
    "original_size_estimate": "~15,000 tokens",
    "compressed_size_estimate": "~3,000 tokens",
    "compression_ratio": "80%",
    "agents_summarized": ["ProductManager", "Architect", "BackendEngineer"]
  }
}

After creating the summary, respond:

DONE
SUMMARY: Compressed context from X agents, reduced by Y%

Be extremely concise but comprehensive. Every key fact must be preserved."""

    def summarize_context(self, context: dict) -> dict:
        """
        Summarize accumulated context

        Args:
            context: Full context dict from all previous agents

        Returns:
            Compressed context dict with summary
        """
        import json

        # Calculate context size
        context_str = json.dumps(context, default=str)
        original_size = len(context_str)

        # Build task description
        task = f"""Summarize the following accumulated context from the AI Dev Team workflow.

The context currently contains results from multiple agents and is approximately {original_size:,} characters.

CRITICAL: Preserve ALL essential information while reducing size by 70-80%.

Current Context to Summarize:
{json.dumps(context, indent=2, default=str)}"""

        # Execute summarization
        result = self.execute(task, context={"complexity": "medium"})

        # Extract JSON summary from result
        import re
        summary_json = None
        for msg in reversed(self.conversation_history):
            if msg["role"] == "assistant":
                json_match = re.search(r"\{.*\}", msg["content"], re.DOTALL)
                if json_match:
                    try:
                        summary_json = json.loads(json_match.group(0))
                        break
                    except json.JSONDecodeError:
                        pass

        # If parsing failed, create basic summary
        if not summary_json:
            summary_json = {
                "project_summary": context.get("requirements", "Project")[:200],
                "requirements": context.get("requirements", ""),
                "tech_stack": context.get("plan", {}).get("tech_stack", {}),
                "architecture": {},
                "files_created": [],
                "completed_work": [f"{k}: completed" for k in context.keys() if k.endswith("Engineer")],
                "context_metadata": {
                    "original_size_estimate": f"~{original_size:,} chars",
                    "note": "Fallback summary used"
                }
            }

        # Calculate compression
        summary_str = json.dumps(summary_json, default=str)
        compressed_size = len(summary_str)
        compression_ratio = (1 - compressed_size / original_size) * 100 if original_size > 0 else 0

        # Add metadata
        if "context_metadata" not in summary_json:
            summary_json["context_metadata"] = {}

        summary_json["context_metadata"].update({
            "original_size": original_size,
            "compressed_size": compressed_size,
            "compression_ratio": f"{compression_ratio:.1f}%",
            "timestamp": str(__import__('datetime').datetime.now())
        })

        return {
            "status": "summarized",
            "summary": summary_json,
            "original_size": original_size,
            "compressed_size": compressed_size,
            "compression_ratio": compression_ratio,
            "agent_result": result
        }

    def should_summarize(self, context: dict, threshold_chars: int = 10000) -> bool:
        """
        Check if context should be summarized

        Args:
            context: Current context
            threshold_chars: Character count threshold

        Returns:
            True if context exceeds threshold
        """
        import json
        context_str = json.dumps(context, default=str)
        return len(context_str) > threshold_chars
