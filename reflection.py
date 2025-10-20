"""
Reflection System - Sistema de reflexión para mejorar la calidad del código
Implements multiple reflection techniques for code quality evaluation
"""

import re
import subprocess
import ast
import json
from typing import Dict, List, Tuple, Optional, Any
from pathlib import Path
from dataclasses import dataclass
from enum import Enum


class ReflectionType(Enum):
    LINTER = "linter"
    BEST_PRACTICES = "best_practices" 
    SIMPLICITY = "simplicity"
    SOLID = "solid"
    DRY = "dry"
    TDD = "tdd"


@dataclass
class ReflectionResult:
    """Resultado de una reflexión sobre código."""
    reflection_type: ReflectionType
    score: float  # 0-100
    issues: List[str]
    suggestions: List[str]
    passed: bool
    details: Dict[str, Any]


class CodeReflector:
    """Sistema principal de reflexión de código."""
    
    def __init__(self, language: str = "es"):
        self.language = language
        self.messages = self._load_messages()
    
    def _load_messages(self) -> Dict:
        """Carga mensajes en el idioma seleccionado."""
        if self.language == "es":
            return {
                "linter_check": "Verificando código con linter...",
                "analyzing_patterns": "Analizando patrones de código...",
                "checking_simplicity": "Evaluando simplicidad...",
                "solid_evaluation": "Evaluando principios SOLID...",
                "dry_analysis": "Analizando principio DRY...",
                "tdd_check": "Verificando cobertura de tests...",
                "reflection_complete": "Reflexión completada",
                "issues_found": "Problemas encontrados",
                "suggestions": "Sugerencias de mejora"
            }
        else:
            return {
                "linter_check": "Checking code with linter...",
                "analyzing_patterns": "Analyzing code patterns...", 
                "checking_simplicity": "Evaluating simplicity...",
                "solid_evaluation": "Evaluating SOLID principles...",
                "dry_analysis": "Analyzing DRY principle...",
                "tdd_check": "Checking test coverage...",
                "reflection_complete": "Reflection completed",
                "issues_found": "Issues found",
                "suggestions": "Improvement suggestions"
            }
    
    def reflect_on_code(self, code: str, file_path: str = "", reflection_types: List[ReflectionType] = None) -> List[ReflectionResult]:
        """
        Ejecuta reflexiones sobre el código proporcionado.
        
        Args:
            code: Código a analizar
            file_path: Ruta del archivo (opcional)
            reflection_types: Tipos de reflexión a ejecutar (por defecto: todos)
        
        Returns:
            Lista de resultados de reflexión
        """
        if reflection_types is None:
            reflection_types = list(ReflectionType)
        
        results = []
        
        for reflection_type in reflection_types:
            try:
                if reflection_type == ReflectionType.LINTER:
                    result = self._reflect_linter(code, file_path)
                elif reflection_type == ReflectionType.BEST_PRACTICES:
                    result = self._reflect_best_practices(code)
                elif reflection_type == ReflectionType.SIMPLICITY:
                    result = self._reflect_simplicity(code)
                elif reflection_type == ReflectionType.SOLID:
                    result = self._reflect_solid(code)
                elif reflection_type == ReflectionType.DRY:
                    result = self._reflect_dry(code)
                elif reflection_type == ReflectionType.TDD:
                    result = self._reflect_tdd(code, file_path)
                
                results.append(result)
            except Exception as e:
                # Si falla una reflexión, crear resultado de error
                results.append(ReflectionResult(
                    reflection_type=reflection_type,
                    score=0,
                    issues=[f"Error en reflexión: {e}"],
                    suggestions=["Revisar el código manualmente"],
                    passed=False,
                    details={"error": str(e)}
                ))
        
        return results
    
    def _reflect_linter(self, code: str, file_path: str) -> ReflectionResult:
        """Reflexión usando linter (flake8/pylint)."""
        print(f"🔍 {self.messages['linter_check']}")
        
        issues = []
        suggestions = []
        score = 100
        
        try:
            # Análisis AST básico
            tree = ast.parse(code)
            
            # Verificar importaciones no utilizadas
            imports = []
            used_names = set()
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.Name):
                    used_names.add(node.id)
            
            # Verificar líneas muy largas
            lines = code.split('\n')
            long_lines = [(i+1, line) for i, line in enumerate(lines) if len(line) > 88]
            
            if long_lines:
                issues.extend([f"Línea {num} muy larga ({len(line)} caracteres)" for num, line in long_lines])
                suggestions.append("Dividir líneas largas en múltiples líneas")
                score -= len(long_lines) * 5
            
            # Verificar funciones muy largas
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_lines = node.end_lineno - node.lineno + 1 if hasattr(node, 'end_lineno') else 0
                    if func_lines > 50:
                        issues.append(f"Función '{node.name}' muy larga ({func_lines} líneas)")
                        suggestions.append(f"Dividir función '{node.name}' en funciones más pequeñas")
                        score -= 10
        
        except SyntaxError as e:
            issues.append(f"Error de sintaxis: {e}")
            score = 0
        
        return ReflectionResult(
            reflection_type=ReflectionType.LINTER,
            score=max(0, score),
            issues=issues,
            suggestions=suggestions,
            passed=score >= 80,
            details={"lines_checked": len(code.split('\n'))}
        )
    
    def _reflect_best_practices(self, code: str) -> ReflectionResult:
        """Reflexión sobre mejores prácticas."""
        print(f"📋 {self.messages['analyzing_patterns']}")
        
        issues = []
        suggestions = []
        score = 100
        
        try:
            tree = ast.parse(code)
            
            # Verificar docstrings
            functions_without_docstring = []
            classes_without_docstring = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if not ast.get_docstring(node):
                        functions_without_docstring.append(node.name)
                elif isinstance(node, ast.ClassDef):
                    if not ast.get_docstring(node):
                        classes_without_docstring.append(node.name)
            
            if functions_without_docstring:
                issues.append(f"Funciones sin docstring: {', '.join(functions_without_docstring)}")
                suggestions.append("Agregar docstrings a todas las funciones")
                score -= len(functions_without_docstring) * 5
            
            if classes_without_docstring:
                issues.append(f"Clases sin docstring: {', '.join(classes_without_docstring)}")
                suggestions.append("Agregar docstrings a todas las clases")
                score -= len(classes_without_docstring) * 10
            
            # Verificar nomenclatura
            bad_names = []
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if not re.match(r'^[a-z_][a-z0-9_]*$', node.name):
                        bad_names.append(f"función '{node.name}'")
                elif isinstance(node, ast.ClassDef):
                    if not re.match(r'^[A-Z][a-zA-Z0-9]*$', node.name):
                        bad_names.append(f"clase '{node.name}'")
            
            if bad_names:
                issues.append(f"Nomenclatura incorrecta: {', '.join(bad_names)}")
                suggestions.append("Usar snake_case para funciones y PascalCase para clases")
                score -= len(bad_names) * 5
        
        except SyntaxError:
            score = 0
            issues.append("No se puede analizar: error de sintaxis")
        
        return ReflectionResult(
            reflection_type=ReflectionType.BEST_PRACTICES,
            score=max(0, score),
            issues=issues,
            suggestions=suggestions,
            passed=score >= 70,
            details={}
        )
    
    def _reflect_simplicity(self, code: str) -> ReflectionResult:
        """Reflexión sobre simplicidad (KISS principle)."""
        print(f"⭐ {self.messages['checking_simplicity']}")
        
        issues = []
        suggestions = []
        score = 100
        
        try:
            tree = ast.parse(code)
            
            # Calcular complejidad ciclomática básica
            complexity_issues = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    complexity = self._calculate_complexity(node)
                    if complexity > 10:
                        complexity_issues.append((node.name, complexity))
                        issues.append(f"Función '{node.name}' muy compleja (complejidad: {complexity})")
                        suggestions.append(f"Simplificar función '{node.name}' dividiéndola en funciones más pequeñas")
                        score -= (complexity - 10) * 5
            
            # Verificar anidamiento excesivo
            max_depth = self._get_max_nesting_depth(tree)
            if max_depth > 4:
                issues.append(f"Anidamiento muy profundo (nivel {max_depth})")
                suggestions.append("Reducir anidamiento usando return temprano o funciones auxiliares")
                score -= (max_depth - 4) * 10
            
            # Verificar número de parámetros
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    param_count = len(node.args.args)
                    if param_count > 5:
                        issues.append(f"Función '{node.name}' tiene demasiados parámetros ({param_count})")
                        suggestions.append(f"Reducir parámetros de '{node.name}' o usar objetos/dataclasses")
                        score -= (param_count - 5) * 5
        
        except SyntaxError:
            score = 0
            issues.append("No se puede analizar: error de sintaxis")
        
        return ReflectionResult(
            reflection_type=ReflectionType.SIMPLICITY,
            score=max(0, score),
            issues=issues,
            suggestions=suggestions,
            passed=score >= 75,
            details={"max_nesting_depth": max_depth if 'max_depth' in locals() else 0}
        )
    
    def _reflect_solid(self, code: str) -> ReflectionResult:
        """Reflexión sobre principios SOLID."""
        print(f"🏗️ {self.messages['solid_evaluation']}")
        
        issues = []
        suggestions = []
        score = 100
        
        try:
            tree = ast.parse(code)
            
            # S - Single Responsibility: verificar clases con muchos métodos
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
                    if len(methods) > 10:
                        issues.append(f"Clase '{node.name}' tiene demasiadas responsabilidades ({len(methods)} métodos)")
                        suggestions.append(f"Dividir clase '{node.name}' siguiendo Single Responsibility Principle")
                        score -= 15
            
            # O - Open/Closed: buscar modificaciones directas vs extensiones
            # L - Liskov Substitution: verificar jerarquías de herencia
            # I - Interface Segregation: verificar interfaces grandes
            # D - Dependency Inversion: verificar dependencias concretas vs abstracciones
            
            # Verificar acoplamiento alto (muchas importaciones)
            imports_count = len([node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))])
            if imports_count > 15:
                issues.append(f"Demasiadas dependencias ({imports_count} importaciones)")
                suggestions.append("Reducir dependencias y mejorar la arquitectura")
                score -= 10
        
        except SyntaxError:
            score = 0
            issues.append("No se puede analizar: error de sintaxis")
        
        return ReflectionResult(
            reflection_type=ReflectionType.SOLID,
            score=max(0, score),
            issues=issues,
            suggestions=suggestions,
            passed=score >= 70,
            details={}
        )
    
    def _reflect_dry(self, code: str) -> ReflectionResult:
        """Reflexión sobre principio DRY (Don't Repeat Yourself)."""
        print(f"🔄 {self.messages['dry_analysis']}")
        
        issues = []
        suggestions = []
        score = 100
        
        # Buscar código duplicado a nivel de líneas
        lines = [line.strip() for line in code.split('\n') if line.strip()]
        line_counts = {}
        
        for line in lines:
            if len(line) > 20:  # Solo líneas significativas
                line_counts[line] = line_counts.get(line, 0) + 1
        
        duplicated_lines = {line: count for line, count in line_counts.items() if count > 1}
        
        if duplicated_lines:
            for line, count in list(duplicated_lines.items())[:3]:  # Top 3
                issues.append(f"Línea duplicada {count} veces: '{line[:50]}...'")
                suggestions.append("Extraer código común a funciones reutilizables")
                score -= count * 5
        
        # Buscar patrones duplicados en funciones
        try:
            tree = ast.parse(code)
            function_bodies = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    body_str = ast.dump(node)
                    function_bodies.append((node.name, body_str))
            
            # Verificar similitud entre funciones (básico)
            for i, (name1, body1) in enumerate(function_bodies):
                for name2, body2 in function_bodies[i+1:]:
                    similarity = self._calculate_similarity(body1, body2)
                    if similarity > 0.7:
                        issues.append(f"Funciones muy similares: '{name1}' y '{name2}'")
                        suggestions.append(f"Refactorizar '{name1}' y '{name2}' para compartir lógica común")
                        score -= 20
        
        except SyntaxError:
            score = 50
            issues.append("No se puede analizar completamente: error de sintaxis")
        
        return ReflectionResult(
            reflection_type=ReflectionType.DRY,
            score=max(0, score),
            issues=issues,
            suggestions=suggestions,
            passed=score >= 75,
            details={"duplicated_lines_count": len(duplicated_lines)}
        )
    
    def _reflect_tdd(self, code: str, file_path: str) -> ReflectionResult:
        """Reflexión sobre Test-Driven Development."""
        print(f"🧪 {self.messages['tdd_check']}")
        
        issues = []
        suggestions = []
        score = 50  # Empezar en 50 porque TDD es opcional
        
        try:
            tree = ast.parse(code)
            
            # Verificar si hay funciones de test
            test_functions = []
            regular_functions = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if node.name.startswith('test_') or 'test' in node.name.lower():
                        test_functions.append(node.name)
                    elif not node.name.startswith('_'):
                        regular_functions.append(node.name)
            
            if not test_functions and regular_functions:
                issues.append("No se encontraron tests para las funciones implementadas")
                suggestions.append("Agregar tests unitarios para validar el comportamiento")
                score = 20
            elif test_functions:
                test_ratio = len(test_functions) / (len(regular_functions) + len(test_functions))
                if test_ratio < 0.3:
                    issues.append(f"Pocas funciones de test ({len(test_functions)} tests, {len(regular_functions)} funciones)")
                    suggestions.append("Aumentar cobertura de tests")
                    score = 60
                else:
                    score = 90
                    suggestions.append("Buena cobertura de tests detectada")
            
            # Verificar imports de testing
            has_test_imports = False
            for node in ast.walk(tree):
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    module_name = getattr(node, 'module', None) or (node.names[0].name if node.names else '')
                    if any(test_lib in module_name.lower() for test_lib in ['unittest', 'pytest', 'test']):
                        has_test_imports = True
                        score += 10
                        break
            
            if test_functions and not has_test_imports:
                issues.append("Tests encontrados pero sin imports de frameworks de testing")
                suggestions.append("Usar unittest, pytest u otro framework de testing")
        
        except SyntaxError:
            score = 0
            issues.append("No se puede analizar: error de sintaxis")
        
        return ReflectionResult(
            reflection_type=ReflectionType.TDD,
            score=max(0, min(100, score)),
            issues=issues,
            suggestions=suggestions,
            passed=score >= 60,
            details={"test_functions": len(test_functions) if 'test_functions' in locals() else 0}
        )
    
    def _calculate_complexity(self, node: ast.FunctionDef) -> int:
        """Calcula complejidad ciclomática básica."""
        complexity = 1
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1
            elif isinstance(child, ast.With, ast.AsyncWith):
                complexity += 1
        
        return complexity
    
    def _get_max_nesting_depth(self, tree: ast.AST) -> int:
        """Calcula la profundidad máxima de anidamiento."""
        def get_depth(node, current_depth=0):
            max_depth = current_depth
            for child in ast.iter_child_nodes(node):
                if isinstance(child, (ast.If, ast.While, ast.For, ast.With, ast.Try)):
                    child_depth = get_depth(child, current_depth + 1)
                    max_depth = max(max_depth, child_depth)
                else:
                    child_depth = get_depth(child, current_depth)
                    max_depth = max(max_depth, child_depth)
            return max_depth
        
        return get_depth(tree)
    
    def _calculate_similarity(self, str1: str, str2: str) -> float:
        """Calcula similitud básica entre dos strings."""
        if not str1 or not str2:
            return 0.0
        
        # Simple similarity based on common characters
        set1, set2 = set(str1), set(str2)
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        
        return intersection / union if union > 0 else 0.0


def format_reflection_results(results: List[ReflectionResult], language: str = "es") -> str:
    """Formatea los resultados de reflexión para mostrar al usuario."""
    if language == "es":
        output = "📊 RESULTADOS DE REFLEXIÓN DE CÓDIGO\n"
        output += "=" * 50 + "\n\n"
        
        overall_score = sum(r.score for r in results) / len(results) if results else 0
        output += f"🎯 Puntuación General: {overall_score:.1f}/100\n\n"
        
        for result in results:
            status = "✅ PASÓ" if result.passed else "❌ FALLÓ"
            output += f"🔍 {result.reflection_type.value.upper()} - {status} ({result.score}/100)\n"
            
            if result.issues:
                output += "   Problemas encontrados:\n"
                for issue in result.issues:
                    output += f"   • {issue}\n"
            
            if result.suggestions:
                output += "   Sugerencias:\n"
                for suggestion in result.suggestions:
                    output += f"   💡 {suggestion}\n"
            
            output += "\n"
    else:
        output = "📊 CODE REFLECTION RESULTS\n"
        output += "=" * 50 + "\n\n"
        
        overall_score = sum(r.score for r in results) / len(results) if results else 0
        output += f"🎯 Overall Score: {overall_score:.1f}/100\n\n"
        
        for result in results:
            status = "✅ PASSED" if result.passed else "❌ FAILED"
            output += f"🔍 {result.reflection_type.value.upper()} - {status} ({result.score}/100)\n"
            
            if result.issues:
                output += "   Issues found:\n"
                for issue in result.issues:
                    output += f"   • {issue}\n"
            
            if result.suggestions:
                output += "   Suggestions:\n"
                for suggestion in result.suggestions:
                    output += f"   💡 {suggestion}\n"
            
            output += "\n"
    
    return output
