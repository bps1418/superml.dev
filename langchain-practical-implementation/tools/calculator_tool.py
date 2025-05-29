from langchain.tools import Tool

def safe_calculate(expr: str) -> str:
    try:
        result = eval(expr, {"__builtins__": None}, {})
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {e}"

calculator_tool = Tool(
    name="Calculator",
    func=safe_calculate,
    description="Performs basic arithmetic calculations."
)