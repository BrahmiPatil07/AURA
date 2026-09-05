import os
import json
import ast
import operator

from dotenv import load_dotenv
from groq import Groq

from memory import add_message, get_memory
from tools import get_current_time
from document_tool import read_document


load_dotenv()

client = Groq(api_key=os.environ["GROQ_API_KEY"])


def calculator(expression):
    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
    }

    def evaluate(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value

        if isinstance(node, ast.BinOp) and type(node.op) in operators:
            left = evaluate(node.left)
            right = evaluate(node.right)
            return operators[type(node.op)](left, right)

        if isinstance(node, ast.UnaryOp) and type(node.op) in (ast.USub, ast.UAdd):
            value = evaluate(node.operand)
            return -value if isinstance(node.op, ast.USub) else value

        raise ValueError("Invalid mathematical expression.")

    try:
        tree = ast.parse(expression, mode="eval")
        return evaluate(tree.body)
    except Exception:
        return "Could not calculate that expression."


tools = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Calculate mathematical expressions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The mathematical expression to calculate."
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get the current date and time.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_document",
            "description": "Read a local TXT, PDF, or DOCX document from the documents folder.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "The name of the document to read."
                    }
                },
                "required": ["filename"]
            }
        }
    },
    {
        "type": "browser_search"
    }
]


def execute_tool(tool_call):
    arguments = json.loads(tool_call.function.arguments)

    if tool_call.function.name == "calculator":
        return calculator(arguments["expression"])

    if tool_call.function.name == "get_current_time":
        return get_current_time()

    if tool_call.function.name == "read_document":
        return read_document(arguments["filename"])

    return "Unknown tool."