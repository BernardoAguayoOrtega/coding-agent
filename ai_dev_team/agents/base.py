"""
Base agent class with tool access
"""
from typing import Dict, List, Optional
import json
import re


class BaseAgent:
    """Base class for all AI agents"""

    def __init__(self, name: str, role: str, groq_client, tools: Dict, human_loop):
        self.name = name
        self.role = role
        self.groq_client = groq_client
        self.tools = tools
        self.human_loop = human_loop
        self.conversation_history = []
        self.system_prompt = self._build_system_prompt()

    def _build_system_prompt(self) -> str:
        """Build system prompt - override in subclasses"""
        return f"""You are {self.name}, a {self.role}.

You can use the following tools to accomplish tasks:

{self._get_tool_descriptions()}

When you need to use a tool, respond in this EXACT format:

TOOL: tool_name
ARGS: {{"arg1": "value1", "arg2": "value2"}}
REASONING: Why you're using this tool

CRITICAL RULES:
- BIAS TOWARD ACTION: If asked to create/write a file, do it immediately. Don't analyze first.
- For simple tasks (hello world, basic files), respond with TOOL call FIRST, then DONE.
- Always use double quotes in JSON
- filepath must be relative to output directory (e.g., "hello.py" or "src/app.js")
- For write_file, content must be a valid JSON string with escaped newlines

Example for creating a file:
TOOL: write_file
ARGS: {{"filepath": "hello.py", "content": "print('Hello World')\\n"}}
REASONING: Creating the main Python file

After using a tool, if task is complete, immediately respond:

DONE
SUMMARY: What you accomplished

Be fast and action-oriented. Don't overthink simple tasks."""

    def _get_tool_descriptions(self) -> str:
        """Get descriptions of available tools"""
        descriptions = []

        if "file_ops" in self.tools:
            descriptions.append("""
FILE OPERATIONS:
- write_file(filepath, content): Write content to a file
- read_file(filepath): Read file content
- list_files(directory): List files in directory
- create_directory(directory): Create a directory
- search_in_file(filepath, pattern): Search for pattern in file
""")

        if "terminal" in self.tools:
            descriptions.append("""
TERMINAL OPERATIONS:
- run_command(command): Execute terminal command
- install_package(package, package_manager): Install package
- run_tests(test_path, framework): Run tests
- lint_code(filepath, language): Lint code
- format_code(filepath, language): Format code
""")

        if "vision" in self.tools:
            descriptions.append("""
VISION OPERATIONS:
- analyze_image(image_path, question): Analyze image
- extract_ui_components(image_path): Extract UI from design
""")

        return "\n".join(descriptions)

    def execute(self, task: str, context: Optional[Dict] = None) -> Dict:
        """
        Execute a task

        Args:
            task: Task description
            context: Additional context from other agents

        Returns:
            Dict with results, artifacts, and status
        """
        self.conversation_history = []

        # Add context to initial message
        complexity = context.get("complexity", "medium") if context else "medium"

        initial_message = f"Task: {task}"

        # Add urgency hint for simple tasks
        if complexity == "simple":
            initial_message += "\n\n⚡ QUICK TASK: This is a simple task. Create the file immediately and mark DONE. No analysis needed."

        if context:
            initial_message += f"\n\nContext:\n{json.dumps(context, indent=2)}"

        self.conversation_history.append({"role": "user", "content": initial_message})

        # Adjust max iterations based on complexity
        complexity = context.get("complexity", "medium") if context else "medium"
        if complexity == "simple":
            max_iterations = 2  # Simple tasks: tool call + DONE
        elif complexity == "medium":
            max_iterations = 8
        else:
            max_iterations = 15  # Complex tasks may need more iterations

        artifacts = {}

        for iteration in range(max_iterations):
            # Get agent response
            response = self._get_response()

            self.conversation_history.append({"role": "assistant", "content": response})

            # Parse and execute tool call FIRST
            tool_call = self._parse_tool_call(response)

            if tool_call:
                tool_name = tool_call["tool"]
                tool_args = tool_call["args"]
                reasoning = tool_call.get("reasoning", "")

                # Execute tool with approval if needed
                result = self._execute_tool_with_approval(tool_name, tool_args, reasoning)

                # Track artifacts
                if tool_name == "write_file" and "filepath" in tool_args:
                    artifacts[tool_args["filepath"]] = "created"

                # Add result to conversation
                self.conversation_history.append(
                    {"role": "user", "content": f"Tool result:\n{result}"}
                )

            # Check if done AFTER tool execution
            if "DONE" in response:
                summary = self._extract_summary(response)
                return {
                    "status": "completed",
                    "summary": summary,
                    "artifacts": artifacts,
                    "iterations": iteration + 1,
                }

            # If no tool call and no DONE, ask agent to clarify
            if not tool_call:
                self.conversation_history.append(
                    {
                        "role": "user",
                        "content": "Please specify a tool to use or indicate you're DONE.",
                    }
                )

        return {
            "status": "max_iterations",
            "summary": "Reached maximum iterations without completion",
            "artifacts": artifacts,
            "iterations": max_iterations,
        }

    def _get_response(self) -> str:
        """Get response from Groq"""
        messages = [{"role": "system", "content": self.system_prompt}] + self.conversation_history

        # Reduce token limit for faster responses on simple tasks
        # Check if task is simple from conversation history
        context_str = str(self.conversation_history)
        if "QUICK TASK" in context_str or "simple" in context_str.lower():
            max_tokens = 512  # Quick response for simple tasks
        else:
            max_tokens = 2048  # Full response for complex tasks

        result = self.groq_client.chat(messages, temperature=0.7, max_tokens=max_tokens)

        return result["content"]

    def _parse_tool_call(self, response: str) -> Optional[Dict]:
        """Parse tool call from response"""
        # Look for TOOL: and ARGS: pattern
        tool_match = re.search(r"TOOL:\s*(\w+)", response)

        if not tool_match:
            return None

        tool_name = tool_match.group(1)
        args = {}

        # Find ARGS: and extract JSON by counting braces
        args_start = response.find("ARGS:")
        if args_start != -1:
            # Find the opening brace
            json_start = response.find("{", args_start)
            if json_start != -1:
                # Count braces to find matching closing brace
                brace_count = 0
                json_end = json_start
                for i in range(json_start, len(response)):
                    if response[i] == '{':
                        brace_count += 1
                    elif response[i] == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            json_end = i + 1
                            break

                if json_end > json_start:
                    args_str = response[json_start:json_end]
                    try:
                        args = json.loads(args_str)
                    except json.JSONDecodeError as e:
                        print(f"[ERROR] Failed to parse ARGS JSON: {e}")
                        print(f"[ERROR] Raw args: {args_str[:300]}...")

        reasoning_match = re.search(
            r"REASONING:\s*(.+?)(?=\n(?:TOOL:|ARGS:|DONE)|$)",
            response,
            re.DOTALL
        )
        reasoning = reasoning_match.group(1).strip() if reasoning_match else ""

        return {"tool": tool_name, "args": args, "reasoning": reasoning}

    def _extract_summary(self, response: str) -> str:
        """Extract summary from DONE response"""
        summary_match = re.search(r"SUMMARY:\s*(.+)", response, re.DOTALL)
        if summary_match:
            return summary_match.group(1).strip()
        return "Task completed"

    def _execute_tool_with_approval(
        self, tool_name: str, tool_args: Dict, reasoning: str
    ) -> str:
        """Execute tool with human approval if needed"""
        # Determine risk level
        risk_level = "low"
        if tool_name in ["run_command", "delete_file"]:
            risk_level = "high"
        elif tool_name in ["write_file", "create_directory"]:
            risk_level = "medium"

        # Request approval for risky actions
        if risk_level in ["high", "medium"]:
            approved = self.human_loop.request_approval(
                action=f"{tool_name}({json.dumps(tool_args)})",
                description=f"{self.name} wants to: {reasoning}",
                context={"agent": self.name, "tool": tool_name},
                risk_level=risk_level,
            )

            if not approved:
                return "❌ Action rejected by user"

        # Execute tool
        return self._execute_tool(tool_name, tool_args)

    def _execute_tool(self, tool_name: str, tool_args: Dict) -> str:
        """Execute a tool"""
        try:
            # File operations
            if tool_name in ["write_file", "read_file", "list_files", "create_directory", "search_in_file"]:
                tool_obj = self.tools.get("file_ops")
                if not tool_obj:
                    return "❌ File operations not available"

                method = getattr(tool_obj, tool_name, None)
                if not method:
                    return f"❌ Unknown file operation: {tool_name}"

                return method(**tool_args)

            # Terminal operations
            elif tool_name in ["run_command", "install_package", "run_tests", "lint_code", "format_code"]:
                tool_obj = self.tools.get("terminal")
                if not tool_obj:
                    return "❌ Terminal operations not available"

                method = getattr(tool_obj, tool_name, None)
                if not method:
                    return f"❌ Unknown terminal operation: {tool_name}"

                return method(**tool_args)

            # Vision operations
            elif tool_name in ["analyze_image", "extract_ui_components"]:
                tool_obj = self.tools.get("vision")
                if not tool_obj:
                    return "❌ Vision operations not available"

                method = getattr(tool_obj, tool_name, None)
                if not method:
                    return f"❌ Unknown vision operation: {tool_name}"

                return method(**tool_args)

            else:
                return f"❌ Unknown tool: {tool_name}"

        except Exception as e:
            return f"❌ Tool execution error: {str(e)}"
