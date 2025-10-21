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

CRITICAL: Detect task complexity and create appropriate plans!

SIMPLE TASKS (1-2 files, basic scripts, hello world, single component):
- Use ONLY the implementation agent (BackendEngineer OR FrontendEngineer)
- Skip ProductManager, Architect, CodeReviewer, QAEngineer, Evaluator
- 1 phase: Implementation

MEDIUM TASKS (multiple files, small features, CRUD operations):
- Use implementation agent + Evaluator
- 2 phases: Implementation, Validation

COMPLEX TASKS (full applications, multiple features, database):
- Use all relevant agents
- Multiple phases: Requirements, Architecture, Implementation, Quality, Validation

Examples:
- "create hello world" → SIMPLE → Just BackendEngineer
- "create a login form" → SIMPLE → Just FrontendEngineer
- "create a REST API with 3 endpoints" → MEDIUM → BackendEngineer + Evaluator
- "build a todo app with database" → COMPLEX → Full team

Available agents:
- ProductManager: Refine requirements (COMPLEX only)
- Architect: Design architecture (COMPLEX only)
- FrontendEngineer: Build UI components
- BackendEngineer: Build APIs and scripts
- DatabaseEngineer: Design database schema (COMPLEX only)
- CodeReviewer: Review code quality (COMPLEX only)
- QAEngineer: Test functionality (COMPLEX only)
- Evaluator: Final validation (MEDIUM/COMPLEX only)

Respond in JSON format:

{
  "project_type": "simple_script | single_component | api | fullstack_web_app | etc",
  "complexity": "simple | medium | complex",
  "tech_stack": {
    "backend": "Python | Node.js | etc" (if applicable),
    "frontend": "React | Vue | etc" (if applicable)
  },
  "phases": [
    {
      "name": "Implementation",
      "agents": ["BackendEngineer"],
      "description": "Create the hello world script"
    }
  ]
}

After creating the plan, respond with:

DONE
SUMMARY: Created [simple|medium|complex] execution plan with N phases"""

    def analyze_requirements(self, requirements: str) -> dict:
        """Analyze requirements and create execution plan"""
        import json
        import re
        
        # FAST PATH: Detect simple tasks instantly without LLM
        req_lower = requirements.lower()
        simple_patterns = [
            'hello world', 'create file', 'write file', 'make file',
            'simple script', 'basic', 'quick', 'test file'
        ]
        
        # Check if it's obviously simple
        if any(pattern in req_lower for pattern in simple_patterns) or len(requirements.split()) < 15:
            # Detect language/type
            if 'react' in req_lower or 'jsx' in req_lower or 'component' in req_lower:
                agent = 'FrontendEngineer'
                tech = 'React'
            elif 'html' in req_lower or 'css' in req_lower:
                agent = 'FrontendEngineer'
                tech = 'HTML'
            else:
                agent = 'BackendEngineer'
                tech = 'Python'
            
            return {
                "status": "fast_path",
                "plan": {
                    "project_type": "simple_script",
                    "complexity": "simple",
                    "tech_stack": {"language": tech},
                    "phases": [{
                        "name": "Implementation",
                        "agents": [agent],
                        "description": requirements
                    }]
                },
                "summary": "Fast-tracked simple task",
            }
        
        # Complex task - use LLM
        result = self.execute(f"Analyze these requirements and create an execution plan:\n\n{requirements}")

        # Try to extract JSON from the conversation
        for msg in reversed(self.conversation_history):
            if msg["role"] == "assistant":
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

        # Fallback
        return {
            "status": "fallback",
            "plan": self._create_default_plan(),
            "summary": "Created default execution plan",
        }

    def _create_default_plan(self) -> dict:
        """Create a default simple execution plan"""
        return {
            "project_type": "simple_script",
            "complexity": "simple",
            "tech_stack": {
                "backend": "Python",
            },
            "phases": [
                {
                    "name": "Implementation",
                    "agents": ["BackendEngineer"],
                    "description": "Create the requested files",
                },
            ],
        }
