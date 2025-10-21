"""
Code quality analysis and reflection
"""
import ast
import re
from pathlib import Path
from typing import Dict, List
from radon.complexity import cc_visit
from radon.metrics import mi_visit


class CodeAnalyzer:
    """Analyze code quality using multiple techniques"""

    def __init__(self):
        self.results = {}

    def analyze_python(self, filepath: str) -> Dict:
        """
        Analyze Python code quality

        Args:
            filepath: Path to Python file

        Returns:
            Analysis results
        """
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                code = f.read()

            results = {
                "filepath": filepath,
                "language": "python",
                "syntax": self._check_syntax(code),
                "complexity": self._check_complexity(code),
                "maintainability": self._check_maintainability(code),
                "best_practices": self._check_best_practices(code),
                "security": self._check_security(code),
            }

            # Calculate overall score
            scores = []
            if results["syntax"]["passed"]:
                scores.append(100)
            if results["complexity"]["average_complexity"] < 10:
                scores.append(80)
            elif results["complexity"]["average_complexity"] < 15:
                scores.append(60)
            else:
                scores.append(40)

            results["overall_score"] = sum(scores) / len(scores) if scores else 0
            results["passed"] = results["overall_score"] >= 60

            return results

        except Exception as e:
            return {
                "filepath": filepath,
                "error": str(e),
                "passed": False,
                "overall_score": 0,
            }

    def _check_syntax(self, code: str) -> Dict:
        """Check Python syntax"""
        try:
            ast.parse(code)
            return {"passed": True, "issues": []}
        except SyntaxError as e:
            return {
                "passed": False,
                "issues": [f"Syntax error at line {e.lineno}: {e.msg}"],
            }

    def _check_complexity(self, code: str) -> Dict:
        """Check code complexity"""
        try:
            complexity = cc_visit(code)
            complexities = [block.complexity for block in complexity]

            if not complexities:
                return {"average_complexity": 0, "max_complexity": 0, "issues": []}

            avg = sum(complexities) / len(complexities)
            max_c = max(complexities)

            issues = []
            for block in complexity:
                if block.complexity > 15:
                    issues.append(
                        f"High complexity ({block.complexity}) in {block.name}"
                    )

            return {
                "average_complexity": round(avg, 2),
                "max_complexity": max_c,
                "issues": issues,
            }

        except Exception:
            return {"average_complexity": 0, "max_complexity": 0, "issues": []}

    def _check_maintainability(self, code: str) -> Dict:
        """Check maintainability index"""
        try:
            mi = mi_visit(code, multi=True)

            if not mi:
                return {"maintainability_index": 0, "rank": "C", "issues": []}

            avg_mi = sum(mi) / len(mi)
            rank = "A" if avg_mi > 20 else "B" if avg_mi > 10 else "C"

            issues = []
            if avg_mi < 10:
                issues.append("Low maintainability - consider refactoring")

            return {
                "maintainability_index": round(avg_mi, 2),
                "rank": rank,
                "issues": issues,
            }

        except Exception:
            return {"maintainability_index": 0, "rank": "C", "issues": []}

    def _check_best_practices(self, code: str) -> Dict:
        """Check Python best practices"""
        issues = []

        # Check for docstrings
        if '"""' not in code and "'''" not in code:
            issues.append("Missing docstrings")

        # Check line length
        long_lines = [
            i + 1 for i, line in enumerate(code.split("\n")) if len(line) > 100
        ]
        if long_lines:
            issues.append(f"Lines too long (>100 chars): {len(long_lines)} lines")

        # Check naming conventions
        if re.search(r"def [A-Z]", code):
            issues.append("Function names should be lowercase with underscores")

        if re.search(r"class [a-z]", code):
            issues.append("Class names should use CapWords convention")

        # Check for print statements (should use logging)
        print_count = code.count("print(")
        if print_count > 3:
            issues.append(
                f"Excessive print statements ({print_count}) - consider using logging"
            )

        return {"issues": issues, "passed": len(issues) == 0}

    def _check_security(self, code: str) -> Dict:
        """Check for common security issues"""
        issues = []

        # Check for eval/exec
        if "eval(" in code or "exec(" in code:
            issues.append("Dangerous: eval/exec usage detected")

        # Check for shell=True
        if 'shell=True' in code:
            issues.append("Security risk: subprocess with shell=True")

        # Check for SQL injection risks
        if re.search(r'f".*SELECT.*FROM', code) or re.search(r"f'.*SELECT.*FROM", code):
            issues.append("Potential SQL injection risk - use parameterized queries")

        # Check for hardcoded secrets
        if re.search(r'password\s*=\s*["\']', code, re.I):
            issues.append("Possible hardcoded password detected")

        if re.search(r'api[_-]?key\s*=\s*["\']', code, re.I):
            issues.append("Possible hardcoded API key detected")

        return {"issues": issues, "passed": len(issues) == 0}

    def analyze_javascript(self, filepath: str) -> Dict:
        """Analyze JavaScript code - basic analysis"""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                code = f.read()

            issues = []

            # Basic checks
            if code.count("var ") > code.count("let ") + code.count("const "):
                issues.append("Prefer let/const over var")

            if "eval(" in code:
                issues.append("Dangerous: eval usage detected")

            if code.count("console.log") > 5:
                issues.append("Excessive console.log statements")

            passed = len(issues) == 0
            score = 80 if passed else 60

            return {
                "filepath": filepath,
                "language": "javascript",
                "issues": issues,
                "passed": passed,
                "overall_score": score,
            }

        except Exception as e:
            return {"filepath": filepath, "error": str(e), "passed": False}

    def format_results(self, results: Dict) -> str:
        """Format analysis results for display"""
        output = [f"\n{'='*60}"]
        output.append(f"📊 Code Quality Analysis: {results.get('filepath', 'unknown')}")
        output.append('=' * 60)

        if "error" in results:
            output.append(f"❌ Error: {results['error']}")
            return "\n".join(output)

        # Overall score
        score = results.get("overall_score", 0)
        emoji = "✅" if score >= 80 else "⚠️" if score >= 60 else "❌"
        output.append(f"\n{emoji} Overall Score: {score:.1f}/100")

        # Syntax
        if "syntax" in results:
            syntax = results["syntax"]
            if syntax["passed"]:
                output.append("\n✅ Syntax: PASSED")
            else:
                output.append("\n❌ Syntax: FAILED")
                for issue in syntax.get("issues", []):
                    output.append(f"  - {issue}")

        # Complexity
        if "complexity" in results:
            comp = results["complexity"]
            avg = comp.get("average_complexity", 0)
            emoji = "✅" if avg < 10 else "⚠️" if avg < 15 else "❌"
            output.append(f"\n{emoji} Complexity:")
            output.append(f"  Average: {avg}")
            output.append(f"  Max: {comp.get('max_complexity', 0)}")
            for issue in comp.get("issues", []):
                output.append(f"  - {issue}")

        # Maintainability
        if "maintainability" in results:
            maint = results["maintainability"]
            output.append(f"\n📈 Maintainability:")
            output.append(f"  Index: {maint.get('maintainability_index', 0)}")
            output.append(f"  Rank: {maint.get('rank', 'C')}")
            for issue in maint.get("issues", []):
                output.append(f"  - {issue}")

        # Best practices
        if "best_practices" in results:
            bp = results["best_practices"]
            if bp.get("passed", False):
                output.append("\n✅ Best Practices: PASSED")
            else:
                output.append("\n⚠️ Best Practices: Issues Found")
                for issue in bp.get("issues", []):
                    output.append(f"  - {issue}")

        # Security
        if "security" in results:
            sec = results["security"]
            if sec.get("passed", False):
                output.append("\n🔒 Security: PASSED")
            else:
                output.append("\n⚠️ Security: Issues Found")
                for issue in sec.get("issues", []):
                    output.append(f"  - {issue}")

        # Generic issues (for non-Python)
        if "issues" in results and not "syntax" in results:
            output.append("\n⚠️ Issues Found:")
            for issue in results["issues"]:
                output.append(f"  - {issue}")

        output.append('=' * 60)

        return "\n".join(output)
