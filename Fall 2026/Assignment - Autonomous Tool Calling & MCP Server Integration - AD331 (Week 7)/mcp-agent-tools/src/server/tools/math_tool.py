"""Safe deterministic mathematical expression evaluator."""

import ast
import json
import operator


OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _evaluate(node: ast.AST) -> float:
    if isinstance(node, ast.Expression):
        return _evaluate(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        if abs(node.value) > 1_000_000_000:
            raise ValueError("Number is too large")
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
        result = OPERATORS[type(node.op)](_evaluate(node.left), _evaluate(node.right))
        if abs(result) > 1_000_000_000:
            raise ValueError("Result is too large")
        return result
    if isinstance(node, ast.UnaryOp) and type(node.op) in OPERATORS:
        return OPERATORS[type(node.op)](_evaluate(node.operand))
    raise ValueError("Unsupported expression")


def calculate_expression(expression: str) -> str:
    """Evaluate approved arithmetic without eval() or exec()."""
    if len(expression) > 200:
        return json.dumps({"error": "Expression is too long."})
    try:
        tree = ast.parse(expression, mode="eval")
        result = _evaluate(tree)
        return json.dumps({"result": result})
    except (SyntaxError, ValueError, TypeError, ZeroDivisionError, OverflowError) as exc:
        return json.dumps({"error": f"Unsafe or invalid expression: {exc}"})
