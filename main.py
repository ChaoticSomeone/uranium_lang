from src.UraniumInterpreter import Interpreter

"""
ToDo:
- Escape Sequence detection for char datatype
- Fix size specifiers / work on implementation
"""

if __name__ == '__main__':
    Interpreter.compile(keepCpp=True)