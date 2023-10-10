from src.UraniumInterpreter import Interpreter

"""
ToDo:
- Escape Sequence detection for char datatype
- Allow unspecified size for int/float
- Operators: [!=]
"""

if __name__ == '__main__':
    Interpreter.compile(keepCpp=True)