from src.UraniumParser import Parser
from src.UraniumLexer import Lexer
from src.UraniumInterpreter import Interpreter

if __name__ == '__main__':
    Parser.readUraniumFile()
    Parser.tokenize()
    Parser.showTokens()
    Lexer.groupTokens()