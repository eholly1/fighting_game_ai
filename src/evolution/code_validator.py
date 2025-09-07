#!/usr/bin/env python3
"""
Code Validator for Evolutionary Training

Validates LLM-generated agent code for safety, syntax, and constraints
before execution in the tournament system.
"""
import ast
import re
import sys
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class ValidationResult:
    """Result of code validation"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    metrics: Dict[str, int]
    cleaned_code: Optional[str] = None

class CodeValidator:
    """
    Validates and cleans LLM-generated agent code

    Ensures code is safe, syntactically correct, and meets constraints
    """

    def __init__(self, max_lines: int = 1400, max_chars: int = 40000):
        """
        Initialize code validator

        Args:
            max_lines: Maximum number of lines allowed
            max_chars: Maximum number of characters allowed
        """
        self.max_lines = max_lines
        self.max_chars = max_chars

        # Dangerous patterns to detect
        self.dangerous_patterns = [
            r'import\s+os',
            r'import\s+sys',
            r'import\s+subprocess',
            r'import\s+socket',
            r'import\s+urllib',
            r'import\s+requests',
            r'import\s+pickle',
            r'import\s+marshal',
            r'import\s+eval',
            r'import\s+exec',
            r'from\s+os\s+import',
            r'from\s+sys\s+import',
            r'from\s+subprocess\s+import',
            r'eval\s*\(',
            r'exec\s*\(',
            r'compile\s*\(',
            r'open\s*\(',
            r'file\s*\(',
            r'input\s*\(',
            r'raw_input\s*\(',
            r'globals\s*\(',
            r'locals\s*\(',
            r'vars\s*\(',
            r'dir\s*\(',
            r'hasattr\s*\(',
            r'getattr\s*\(',
            r'setattr\s*\(',
            r'delattr\s*\(',
        ]

        # Required patterns
        self.required_patterns = [
            r'def\s+get_action\s*\(',  # Must have get_action function
        ]

        # Allowed imports
        self.allowed_imports = {
            'numpy', 'np', 'random', 'math', 'time'
        }

    def validate_code(self, code: str, agent_id: str = "unknown") -> ValidationResult:
        """
        Validate agent code comprehensively

        Args:
            code: Python code string to validate
            agent_id: Identifier for the agent (for error reporting)

        Returns:
            ValidationResult with validation status and details
        """
        errors = []
        warnings = []
        metrics = {}

        # Clean the code first
        cleaned_code = self._clean_code(code)

        # 1. Basic metrics
        lines = cleaned_code.split('\n')
        metrics['lines'] = len(lines)
        metrics['chars'] = len(cleaned_code)
        metrics['non_empty_lines'] = len([line for line in lines if line.strip()])

        # 2. Length constraints
        if metrics['lines'] > self.max_lines:
            errors.append(f"Code too long: {metrics['lines']} lines (max {self.max_lines})")

        if metrics['chars'] > self.max_chars:
            errors.append(f"Code too long: {metrics['chars']} chars (max {self.max_chars})")

        # 3. Syntax validation
        syntax_valid, syntax_error = self._validate_syntax(cleaned_code)
        if not syntax_valid:
            errors.append(f"Syntax error: {syntax_error}")

        # 4. Security validation
        security_issues = self._validate_security(cleaned_code)
        errors.extend(security_issues)

        # 5. Required patterns
        missing_requirements = self._validate_requirements(cleaned_code)
        errors.extend(missing_requirements)

        # 6. Import validation
        import_issues = self._validate_imports(cleaned_code)
        errors.extend(import_issues)

        # 7. Complexity warnings
        complexity_warnings = self._check_complexity(cleaned_code)
        warnings.extend(complexity_warnings)

        # 8. Code quality suggestions
        quality_warnings = self._check_code_quality(cleaned_code)
        warnings.extend(quality_warnings)

        is_valid = len(errors) == 0

        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings,
            metrics=metrics,
            cleaned_code=cleaned_code if is_valid else None
        )

    def _clean_code(self, code: str) -> str:
        """Clean and normalize code"""
        # Remove markdown code blocks if present
        if "```python" in code:
            code = code.split("```python")[1].split("```")[0]
        elif "```" in code:
            code = code.split("```")[1].split("```")[0]

        # Remove leading/trailing whitespace
        code = code.strip()

        # Normalize line endings
        code = code.replace('\r\n', '\n').replace('\r', '\n')

        # Remove excessive blank lines (max 2 consecutive)
        lines = code.split('\n')
        cleaned_lines = []
        blank_count = 0

        for line in lines:
            if line.strip() == '':
                blank_count += 1
                if blank_count <= 2:
                    cleaned_lines.append(line)
            else:
                blank_count = 0
                cleaned_lines.append(line)

        return '\n'.join(cleaned_lines)

    def _validate_syntax(self, code: str) -> Tuple[bool, Optional[str]]:
        """Validate Python syntax"""
        try:
            ast.parse(code)
            return True, None
        except SyntaxError as e:
            return False, f"Line {e.lineno}: {e.msg}"
        except Exception as e:
            return False, str(e)

    def _validate_security(self, code: str) -> List[str]:
        """Check for dangerous patterns"""
        issues = []

        for pattern in self.dangerous_patterns:
            matches = re.findall(pattern, code, re.IGNORECASE)
            if matches:
                issues.append(f"Dangerous pattern detected: {pattern}")

        return issues

    def _validate_requirements(self, code: str) -> List[str]:
        """Check for required patterns"""
        issues = []

        for pattern in self.required_patterns:
            if not re.search(pattern, code):
                issues.append(f"Missing required pattern: {pattern}")

        return issues

    def _validate_imports(self, code: str) -> List[str]:
        """Validate import statements"""
        issues = []

        try:
            tree = ast.parse(code)

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name not in self.allowed_imports:
                            issues.append(f"Disallowed import: {alias.name}")

                elif isinstance(node, ast.ImportFrom):
                    if node.module and node.module not in self.allowed_imports:
                        issues.append(f"Disallowed import from: {node.module}")

        except Exception as e:
            issues.append(f"Could not parse imports: {e}")

        return issues

    def _check_complexity(self, code: str) -> List[str]:
        """Check code complexity and suggest improvements"""
        warnings = []

        lines = code.split('\n')

        # Check nesting depth
        max_indent = 0
        for line in lines:
            if line.strip():
                indent = len(line) - len(line.lstrip())
                max_indent = max(max_indent, indent // 4)  # Assuming 4-space indents

        if max_indent > 4:
            warnings.append(f"Deep nesting detected (level {max_indent}). Consider refactoring.")

        # Check function length
        in_function = False
        function_lines = 0

        for line in lines:
            stripped = line.strip()
            if stripped.startswith('def '):
                in_function = True
                function_lines = 1
            elif in_function:
                if stripped and not line.startswith(' ') and not line.startswith('\t'):
                    # End of function
                    if function_lines > 50:
                        warnings.append(f"Long function detected ({function_lines} lines). Consider breaking into smaller functions.")
                    in_function = False
                    function_lines = 0
                else:
                    function_lines += 1

        return warnings

    def _check_code_quality(self, code: str) -> List[str]:
        """Check code quality and readability"""
        warnings = []

        lines = code.split('\n')

        # Check for very long lines
        for i, line in enumerate(lines, 1):
            if len(line) > 120:
                warnings.append(f"Line {i} is very long ({len(line)} chars). Consider breaking it up.")

        # Check for magic numbers
        magic_number_pattern = r'\b(?<![\w.])[0-9]+\.?[0-9]*(?![\w.])\b'
        magic_numbers = re.findall(magic_number_pattern, code)

        # Filter out common acceptable numbers
        acceptable_numbers = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '100', '0.0', '1.0'}
        problematic_numbers = [num for num in set(magic_numbers) if num not in acceptable_numbers]

        if len(problematic_numbers) > 5:
            warnings.append(f"Many magic numbers detected. Consider using named constants.")

        # Check for meaningful variable names
        short_var_pattern = r'\b[a-z]\b'
        short_vars = re.findall(short_var_pattern, code)
        if len(set(short_vars)) > 3:
            warnings.append("Consider using more descriptive variable names instead of single letters.")

        return warnings

def create_safe_execution_environment():
    """Create a restricted execution environment for agent code"""
    import numpy as np
    import random
    import math

    safe_builtins = {
        # Basic types
        'int': int,
        'float': float,
        'bool': bool,
        'str': str,
        'list': list,
        'dict': dict,
        'tuple': tuple,
        'set': set,

        # Basic functions
        'len': len,
        'range': range,
        'enumerate': enumerate,
        'zip': zip,
        'sum': sum,
        'min': min,
        'max': max,
        'abs': abs,
        'round': round,
        'sorted': sorted,
        'reversed': reversed,

        # Math functions
        'pow': pow,

        # Type checking
        'isinstance': isinstance,
        'type': type,

        # Exceptions (for proper error handling)
        'Exception': Exception,
        'ValueError': ValueError,
        'TypeError': TypeError,
        'IndexError': IndexError,
        'KeyError': KeyError,
    }

    safe_globals = {
        '__builtins__': safe_builtins,
        'np': np,
        'numpy': np,
        'random': random,
        'math': math,
    }

    return safe_globals

def test_code_validator():
    """Test the code validator with various code samples"""
    validator = CodeValidator()

    # Test 1: Valid code
    valid_code = """
def get_action(state):
    import numpy as np
    distance = state[22]
    relative_pos = state[23]

    if distance < 0.15:
        return 4  # punch
    elif distance < 0.3:
        if relative_pos > 0:
            return 2  # move right
        else:
            return 1  # move left
    else:
        return 9  # projectile
"""

    result = validator.validate_code(valid_code, "test_valid")
    print(f"Valid code test: {'✅ PASS' if result.is_valid else '❌ FAIL'}")
    if result.errors:
        print(f"  Errors: {result.errors}")

    # Test 2: Invalid code (dangerous import)
    dangerous_code = """
import os
def get_action(state):
    os.system("rm -rf /")  # Very dangerous!
    return 0
"""

    result = validator.validate_code(dangerous_code, "test_dangerous")
    print(f"Dangerous code test: {'✅ PASS' if not result.is_valid else '❌ FAIL'}")
    if result.errors:
        print(f"  Errors detected: {len(result.errors)}")

    # Test 3: Missing get_action function
    missing_function_code = """
def some_other_function():
    return 42
"""

    result = validator.validate_code(missing_function_code, "test_missing")
    print(f"Missing function test: {'✅ PASS' if not result.is_valid else '❌ FAIL'}")

    print(f"\n📊 Code Validator Tests Complete")

if __name__ == "__main__":
    test_code_validator()
