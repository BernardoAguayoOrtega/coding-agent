"""
Terminal operation tools for AI agents
"""
import subprocess
from typing import Optional


class TerminalOperations:
    """Tools for executing terminal commands"""

    DANGEROUS_COMMANDS = ["rm -rf", "dd ", "mkfs", "> /dev/", ":(){ :|:& };:"]

    def __init__(self, work_dir: str):
        self.work_dir = work_dir

    def run_command(self, command: str, timeout: int = 60) -> str:
        """
        Execute a terminal command

        Args:
            command: Command to execute
            timeout: Timeout in seconds (default: 60)

        Returns:
            Command output or error message
        """
        # Security check
        if any(dangerous in command for dangerous in self.DANGEROUS_COMMANDS):
            return f"🚫 Dangerous command blocked: {command}"

        try:
            result = subprocess.run(
                command,
                shell=True,
                check=False,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=self.work_dir,
            )

            output = result.stdout.strip()
            stderr = result.stderr.strip()

            if result.returncode == 0:
                if output:
                    return f"✅ Command succeeded:\n{output}"
                else:
                    return "✅ Command executed successfully (no output)"
            else:
                error_msg = stderr if stderr else output
                return f"❌ Command failed (exit code {result.returncode}):\n{error_msg}"

        except subprocess.TimeoutExpired:
            return f"⏱️ Command timed out after {timeout} seconds"
        except Exception as e:
            return f"❌ Error executing command: {str(e)}"

    def install_package(self, package: str, package_manager: str = "pip") -> str:
        """
        Install a package

        Args:
            package: Package name
            package_manager: Package manager (pip, npm, yarn)

        Returns:
            Installation result
        """
        managers = {
            "pip": f"pip install {package}",
            "npm": f"npm install {package}",
            "yarn": f"yarn add {package}",
        }

        if package_manager not in managers:
            return f"❌ Unknown package manager: {package_manager}"

        command = managers[package_manager]
        return self.run_command(command, timeout=300)  # 5 min timeout

    def run_tests(self, test_path: str = ".", framework: str = "pytest") -> str:
        """
        Run tests

        Args:
            test_path: Path to test files
            framework: Test framework (pytest, unittest, jest)

        Returns:
            Test results
        """
        commands = {
            "pytest": f"pytest {test_path} -v",
            "unittest": f"python -m unittest discover {test_path}",
            "jest": f"npm test -- {test_path}",
        }

        if framework not in commands:
            return f"❌ Unknown test framework: {framework}"

        command = commands[framework]
        return self.run_command(command, timeout=300)

    def lint_code(self, filepath: str, language: str = "python") -> str:
        """
        Lint code file

        Args:
            filepath: Path to file
            language: Programming language

        Returns:
            Linting results
        """
        linters = {
            "python": f"pylint {filepath}",
            "javascript": f"eslint {filepath}",
            "typescript": f"eslint {filepath}",
        }

        if language not in linters:
            return f"❌ No linter configured for {language}"

        command = linters[language]
        return self.run_command(command)

    def format_code(self, filepath: str, language: str = "python") -> str:
        """
        Format code file

        Args:
            filepath: Path to file
            language: Programming language

        Returns:
            Formatting result
        """
        formatters = {
            "python": f"black {filepath}",
            "javascript": f"prettier --write {filepath}",
            "typescript": f"prettier --write {filepath}",
        }

        if language not in formatters:
            return f"❌ No formatter configured for {language}"

        command = formatters[language]
        return self.run_command(command)
