"""
CLI interface for AI Dev Team
"""
import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.markdown import Markdown
from pathlib import Path
import json

from .config import Config
from .groq_client import GroqClient
from .tools import FileOperations, TerminalOperations, VisionOperations
from .utils import HumanLoop
from .agents import (
    OrchestratorAgent,
    ProductManagerAgent,
    ArchitectAgent,
    FrontendEngineerAgent,
    BackendEngineerAgent,
    DatabaseEngineerAgent,
    CodeReviewerAgent,
    QAEngineerAgent,
    EvaluatorAgent,
)

console = Console()


class AIDevTeam:
    """Main orchestrator for the AI development team"""

    def __init__(self, output_dir: Path, auto_approve: bool = False, verbose: bool = False):
        self.output_dir = output_dir
        self.verbose = verbose

        # Initialize systems
        console.print("[bold blue]🚀 Initializing AI Dev Team...[/bold blue]")

        self.groq_client = GroqClient()
        self.human_loop = HumanLoop(auto_approve=auto_approve)

        # Initialize tools
        self.file_ops = FileOperations(output_dir)
        self.terminal = TerminalOperations(str(output_dir))
        self.vision = VisionOperations(self.groq_client)

        self.tools = {
            "file_ops": self.file_ops,
            "terminal": self.terminal,
            "vision": self.vision,
        }

        # Initialize agents
        self.agents = {
            "Orchestrator": OrchestratorAgent(self.groq_client, self.tools, self.human_loop),
            "ProductManager": ProductManagerAgent(self.groq_client, self.tools, self.human_loop),
            "Architect": ArchitectAgent(self.groq_client, self.tools, self.human_loop),
            "FrontendEngineer": FrontendEngineerAgent(self.groq_client, self.tools, self.human_loop),
            "BackendEngineer": BackendEngineerAgent(self.groq_client, self.tools, self.human_loop),
            "DatabaseEngineer": DatabaseEngineerAgent(self.groq_client, self.tools, self.human_loop),
            "CodeReviewer": CodeReviewerAgent(self.groq_client, self.tools, self.human_loop),
            "QAEngineer": QAEngineerAgent(self.groq_client, self.tools, self.human_loop),
            "Evaluator": EvaluatorAgent(self.groq_client, self.tools, self.human_loop),
        }

        console.print("[green]✓ AI Dev Team initialized[/green]\n")

    def execute_project(self, requirements: str, image_path: str = None):
        """Execute a full project based on requirements"""

        # Show requirements
        console.print(Panel(requirements, title="📋 Project Requirements", border_style="blue"))

        # Analyze image if provided
        if image_path:
            console.print(f"\n[blue]🖼️  Analyzing design image: {image_path}[/blue]")
            image_analysis = self.vision.analyze_image(image_path)
            console.print(Panel(image_analysis, title="Image Analysis", border_style="cyan"))
            requirements += f"\n\nDesign Reference:\n{image_analysis}"

        # Phase 1: Orchestration
        console.print("\n[bold yellow]🎯 Phase 1: Planning[/bold yellow]")
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
            task = progress.add_task("Orchestrator analyzing requirements...", total=None)
            orchestrator = self.agents["Orchestrator"]
            plan_result = orchestrator.analyze_requirements(requirements)
            progress.update(task, completed=True)

        if plan_result["status"] == "success":
            plan = plan_result["plan"]
        else:
            plan = plan_result["plan"]  # Use fallback

        # Display plan
        self._display_plan(plan)

        # Request approval for plan
        approved = self.human_loop.request_approval(
            action="Execute Project Plan",
            description=f"Project: {plan.get('project_type', 'unknown')}\n"
            f"Phases: {len(plan.get('phases', []))}\n"
            f"Tech Stack: {json.dumps(plan.get('tech_stack', {}), indent=2)}",
            risk_level="low",
        )

        if not approved:
            console.print("[red]❌ Project execution cancelled by user[/red]")
            return

        # Execute phases
        context = {"requirements": requirements, "plan": plan}

        for i, phase in enumerate(plan.get("phases", []), 1):
            console.print(f"\n[bold yellow]📦 Phase {i}: {phase['name']}[/bold yellow]")
            console.print(f"[dim]{phase['description']}[/dim]")

            phase_results = {}

            for agent_name in phase["agents"]:
                if agent_name not in self.agents:
                    console.print(f"[red]⚠️  Unknown agent: {agent_name}[/red]")
                    continue

                agent = self.agents[agent_name]

                console.print(f"\n[cyan]👤 {agent_name} working...[/cyan]")

                with Progress(
                    SpinnerColumn(), TextColumn("[progress.description]{task.description}")
                ) as progress:
                    task = progress.add_task(f"{agent_name} executing...", total=None)

                    # Execute agent task
                    task_desc = f"{phase['description']}"
                    result = agent.execute(task_desc, context)

                    progress.update(task, completed=True)

                # Display result
                status_color = "green" if result["status"] == "completed" else "yellow"
                console.print(
                    f"[{status_color}]✓ {agent_name}: {result.get('summary', 'Done')}[/{status_color}]"
                )

                if self.verbose:
                    console.print(f"[dim]Iterations: {result.get('iterations', 0)}[/dim]")
                    if result.get("artifacts"):
                        console.print(f"[dim]Artifacts: {list(result['artifacts'].keys())}[/dim]")

                # Add to context for next agents
                phase_results[agent_name] = result
                context[agent_name] = result

        # Final summary
        console.print("\n" + "=" * 60)
        console.print("[bold green]🎉 Project Execution Complete![/bold green]")
        self._display_summary()

    def _display_plan(self, plan: dict):
        """Display execution plan in a nice format"""
        console.print("\n[bold]📋 Execution Plan:[/bold]")

        # Tech stack
        console.print("\n[bold]🛠️  Tech Stack:[/bold]")
        tech_table = Table()
        tech_table.add_column("Component", style="cyan")
        tech_table.add_column("Technology", style="green")

        for key, value in plan.get("tech_stack", {}).items():
            tech_table.add_row(key.title(), value)

        console.print(tech_table)

        # Phases
        console.print("\n[bold]📦 Phases:[/bold]")
        phase_table = Table()
        phase_table.add_column("#", style="cyan")
        phase_table.add_column("Phase", style="yellow")
        phase_table.add_column("Agents", style="green")
        phase_table.add_column("Description", style="dim")

        for i, phase in enumerate(plan.get("phases", []), 1):
            agents_str = ", ".join(phase.get("agents", []))
            phase_table.add_row(str(i), phase["name"], agents_str, phase["description"])

        console.print(phase_table)
        console.print()

    def _display_summary(self):
        """Display final summary with stats"""
        stats = self.groq_client.get_stats()
        approval_stats = self.human_loop.get_approval_stats()

        # Cost and usage
        console.print("\n[bold]💰 Cost Summary:[/bold]")
        cost_table = Table()
        cost_table.add_column("Metric", style="cyan")
        cost_table.add_column("Value", style="green")

        cost_table.add_row("Total Cost", f"${stats['total_cost']:.4f}")
        cost_table.add_row("Input Tokens", f"{stats['total_input_tokens']:,}")
        cost_table.add_row("Output Tokens", f"{stats['total_output_tokens']:,}")
        cost_table.add_row("Total Tokens", f"{stats['total_tokens']:,}")

        console.print(cost_table)

        # Approvals
        console.print("\n[bold]🤝 Approval Summary:[/bold]")
        approval_table = Table()
        approval_table.add_column("Metric", style="cyan")
        approval_table.add_column("Count", style="green")

        approval_table.add_row("Total Approvals", str(approval_stats["total"]))
        approval_table.add_row("Approved", str(approval_stats["approved"]))
        approval_table.add_row("Rejected", str(approval_stats["rejected"]))
        approval_table.add_row("Auto-Approved", str(approval_stats["auto"]))

        console.print(approval_table)

        # Output location
        console.print(f"\n[bold green]📁 Output directory: {self.output_dir}[/bold green]")


@click.command()
@click.argument("requirements", required=False)
@click.option("-i", "--interactive", is_flag=True, help="Interactive mode")
@click.option("--image", type=click.Path(exists=True), help="Include an image for analysis")
@click.option("--auto-approve", is_flag=True, help="Skip approval prompts")
@click.option("--max-iterations", type=int, default=50, help="Max iterations per agent")
@click.option("--output", type=click.Path(), default="workspace", help="Output directory")
@click.option("-v", "--verbose", is_flag=True, help="Verbose output")
def main(requirements, interactive, image, auto_approve, max_iterations, output, verbose):
    """
    AI Dev Team - Your own AI software development team

    Examples:
        ai-dev-team "Build a todo app with React and Flask"
        ai-dev-team --interactive
        ai-dev-team "Recreate this design" --image mockup.png
    """
    try:
        # Set config
        Config.MAX_ITERATIONS = max_iterations
        Config.VERBOSE = verbose
        Config.AUTO_APPROVE = auto_approve

        # Initialize team
        output_path = Path(output)
        team = AIDevTeam(output_path, auto_approve=auto_approve, verbose=verbose)

        if interactive:
            console.print("[bold blue]🔄 Interactive Mode[/bold blue]")
            console.print("Type 'quit' to exit\n")

            while True:
                req = click.prompt("Enter project requirements")

                if req.lower() in ["quit", "exit", "q"]:
                    console.print("[yellow]👋 Goodbye![/yellow]")
                    break

                img_path = None
                if click.confirm("Include an image?", default=False):
                    img_path = click.prompt("Image path")

                team.execute_project(req, img_path)

                if not click.confirm("\nStart another project?", default=False):
                    break

        elif requirements:
            team.execute_project(requirements, image)

        else:
            console.print("[red]❌ Please provide requirements or use --interactive mode[/red]")
            console.print("\nExamples:")
            console.print('  ai-dev-team "Build a todo app with React and Flask"')
            console.print("  ai-dev-team --interactive")

    except KeyboardInterrupt:
        console.print("\n[yellow]👋 Interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]❌ Error: {str(e)}[/red]")
        if verbose:
            import traceback
            console.print(traceback.format_exc())


if __name__ == "__main__":
    main()
