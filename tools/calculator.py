import ast
import operator

def calculate(expression: str) -> dict:
    """
    Safely evaluate a math expression.
    Example: "2 + 2" -> 4
    Works with Python 3.8+
    """
    try:
        # Safe operators we allow
        operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.USub: operator.neg,
        }
        
        def eval_expr(node):
            # Python 3.8+ uses ast.Constant instead of ast.Num
            if isinstance(node, ast.Constant):  # number
                return node.value
            elif isinstance(node, ast.BinOp):  # binary operation
                return operators[type(node.op)](eval_expr(node.left), eval_expr(node.right))
            elif isinstance(node, ast.UnaryOp):  # unary operation
                return operators[type(node.op)](eval_expr(node.operand))
            else:
                raise ValueError("Unsupported operation")
        
        node = ast.parse(expression, mode='eval')
        result = eval_expr(node.body)
        
        return {
            "success": True,
            "result": result,
            "expression": expression
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "expression": expression
        }