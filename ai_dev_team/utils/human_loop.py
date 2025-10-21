"""
Human-in-the-Loop system for approvals and feedback
"""
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from typing import Optional
from ..config import Config

console = Console()


class HumanLoop:
    """Interactive approval and feedback system"""

    def __init__(self, auto_approve: bool = None):
        self.auto_approve = auto_approve if auto_approve is not None else Config.AUTO_APPROVE
        self.approval_log = []

    def request_approval(
        self,
        action: str,
        description: str,
        context: Optional[dict] = None,
        risk_level: str = "medium",
    ) -> bool:
        """
        Request human approval for an action

        Args:
            action: Action to approve
            description: Description of what will happen
            context: Additional context
            risk_level: low, medium, high

        Returns:
            True if approved, False otherwise
        """
        if self.auto_approve and risk_level == "low":
            self.approval_log.append(
                {"action": action, "approved": True, "auto": True}
            )
            return True

        # Display request
        risk_colors = {"low": "green", "medium": "yellow", "high": "red"}
        color = risk_colors.get(risk_level, "yellow")

        console.print()
        console.print(
            Panel(
                f"[bold]{action}[/bold]\n\n{description}\n\n[{color}]Risk: {risk_level.upper()}[/{color}]",
                title="🤝 Human Approval Required",
                border_style=color,
            )
        )

        if context:
            console.print("[dim]Context:[/dim]")
            for key, value in context.items():
                console.print(f"  [dim]{key}:[/dim] {value}")
            console.print()

        # Get approval
        approved = Confirm.ask("Approve this action?", default=True)

        self.approval_log.append(
            {"action": action, "approved": approved, "auto": False}
        )

        if approved:
            console.print("[green]✓ Approved[/green]")
        else:
            console.print("[red]✗ Rejected[/red]")

        console.print()
        return approved

    def request_feedback(self, question: str, default: Optional[str] = None) -> str:
        """
        Request human feedback

        Args:
            question: Question to ask
            default: Default answer

        Returns:
            User's response
        """
        console.print()
        console.print(Panel(question, title="💭 Feedback Needed", border_style="blue"))

        response = Prompt.ask("Your response", default=default or "")

        console.print()
        return response

    def request_choice(
        self, question: str, choices: list, default: Optional[str] = None
    ) -> str:
        """
        Request human choice from options

        Args:
            question: Question to ask
            choices: List of choices
            default: Default choice

        Returns:
            Selected choice
        """
        console.print()
        console.print(Panel(question, title="🎯 Choice Required", border_style="cyan"))

        for i, choice in enumerate(choices, 1):
            console.print(f"  {i}. {choice}")

        console.print()
        choice_str = " / ".join(choices)
        response = Prompt.ask(f"Select ({choice_str})", choices=choices, default=default)

        console.print()
        return response

    def show_info(self, message: str, title: str = "ℹ️  Information"):
        """Display information to user"""
        console.print()
        console.print(Panel(message, title=title, border_style="blue"))
        console.print()

    def show_warning(self, message: str):
        """Display warning to user"""
        console.print()
        console.print(Panel(message, title="⚠️  Warning", border_style="yellow"))
        console.print()

    def show_error(self, message: str):
        """Display error to user"""
        console.print()
        console.print(Panel(message, title="❌ Error", border_style="red"))
        console.print()

    def show_success(self, message: str):
        """Display success message"""
        console.print()
        console.print(Panel(message, title="✅ Success", border_style="green"))
        console.print()

    def get_approval_stats(self) -> dict:
        """Get approval statistics"""
        total = len(self.approval_log)
        if total == 0:
            return {"total": 0, "approved": 0, "rejected": 0, "auto": 0}

        approved = sum(1 for log in self.approval_log if log["approved"])
        rejected = total - approved
        auto = sum(1 for log in self.approval_log if log.get("auto", False))

        return {"total": total, "approved": approved, "rejected": rejected, "auto": auto}
