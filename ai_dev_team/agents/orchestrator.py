"""
Orchestrator Agent - Analyzes requirements and divides work among specialized agents
"""
from .base import BaseAgent


class OrchestratorAgent(BaseAgent):
    """Orchestrator that analyzes requirements and creates execution plan"""

    def __init__(self, groq_client, tools, human_loop):
        super().__init__(
            name="Orchestrator",
            role="Project Orchestrator and Task Coordinator",
            groq_client=groq_client,
            tools=tools,
            human_loop=human_loop,
        )

    def _build_system_prompt(self) -> str:
        return """You are the Orchestrator, responsible for analyzing project requirements and creating an execution plan.

Your job:
1. Analyze the user's requirements
2. Break down the project into logical phases
3. Assign tasks to specialized agents:
   - ProductManager: Refine requirements and create specs
   - Architect: Design system architecture
   - FrontendEngineer: Build UI components
   - BackendEngineer: Build APIs and server logic
   - DatabaseEngineer: Design database schema
   - CodeReviewer: Review code quality
   - QAEngineer: Test functionality
   - Evaluator: Final validation

4. Create a detailed execution plan

Respond in JSON format:

{
  "project_type": "fullstack_web_app | api | frontend_only | etc",
  "tech_stack": {
    "frontend": "React | Vue | etc",
    "backend": "Node.js | Python | etc",
    "database": "PostgreSQL | MongoDB | etc"
  },
  "phases": [
    {
      "name": "Requirements",
      "agents": ["ProductManager"],
      "description": "Refine and document requirements"
    },
    {
      "name": "Architecture",
      "agents": ["Architect"],
      "description": "Design system architecture"
    },
    {
      "name": "Implementation",
      "agents": ["DatabaseEngineer", "BackendEngineer", "FrontendEngineer"],
      "description": "Build the application"
    },
    {
      "name": "Quality",
      "agents": ["CodeReviewer", "QAEngineer"],
      "description": "Review and test"
    },
    {
      "name": "Validation",
      "agents": ["Evaluator"],
      "description": "Final validation"
    }
  ]
}

After creating the plan, respond with:

DONE
SUMMARY: Created execution plan with N phases"""

    def analyze_requirements(self, requirements: str) -> dict:
        """Analyze requirements and create execution plan"""
        result = self.execute(f"Analyze these requirements and create an execution plan:\n\n{requirements}")

        # Parse JSON plan from summary
        import json
        import re

        # Try to extract JSON from the conversation
        for msg in reversed(self.conversation_history):
            if msg["role"] == "assistant":
                # Look for JSON object
                json_match = re.search(r"\{.*\}", msg["content"], re.DOTALL)
                if json_match:
                    try:
                        plan = json.loads(json_match.group(0))
                        return {
                            "status": "success",
                            "plan": plan,
                            "summary": result.get("summary", ""),
                        }
                    except json.JSONDecodeError:
                        pass

        # Fallback: create a default plan
        return {
            "status": "fallback",
            "plan": self._create_default_plan(),
            "summary": "Created default execution plan",
        }

    def _create_default_plan(self) -> dict:
        """Create a default full-stack execution plan"""
        return {
            "project_type": "fullstack_web_app",
            "tech_stack": {
                "frontend": "React",
                "backend": "Node.js/Express",
                "database": "PostgreSQL",
            },
            "phases": [
                {
                    "name": "Requirements",
                    "agents": ["ProductManager"],
                    "description": "Refine and document requirements",
                },
                {
                    "name": "Architecture",
                    "agents": ["Architect"],
                    "description": "Design system architecture",
                },
                {
                    "name": "Database",
                    "agents": ["DatabaseEngineer"],
                    "description": "Design database schema",
                },
                {
                    "name": "Backend",
                    "agents": ["BackendEngineer"],
                    "description": "Build API and server logic",
                },
                {
                    "name": "Frontend",
                    "agents": ["FrontendEngineer"],
                    "description": "Build user interface",
                },
                {
                    "name": "Quality",
                    "agents": ["CodeReviewer", "QAEngineer"],
                    "description": "Review and test code",
                },
                {
                    "name": "Validation",
                    "agents": ["Evaluator"],
                    "description": "Final validation",
                },
            ],
        }
