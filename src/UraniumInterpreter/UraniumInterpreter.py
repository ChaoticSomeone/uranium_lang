from src.UraniumParser.UraniumParser import Parser
from src.UraniumLexer.UraniumLexer import Lexer
import re, os

class Interpreter:
    cppCode = []

    @staticmethod
    def parseAndLex():
        Parser.readUraniumFile()
        Parser.tokenize()
        Parser.showTokens()
        Lexer.groupTokens()

    @staticmethod
    def translate():
        i = 0
        while i < len(Lexer.tokenGroups):
            group = Lexer.tokenGroups[i]
            for j, token in enumerate(group):
                if token == Parser.tokenTypes["KW_INT"]:
                    Interpreter.cppCode.append("int")

                elif token == Parser.tokenTypes["REQ_FUNC_MAIN"]:
                    Interpreter.cppCode.append("main")

                elif token == Parser.tokenTypes["L_PAREN"]:
                    Interpreter.cppCode.append("(")

                elif token == Parser.tokenTypes["R_PAREN"]:
                    Interpreter.cppCode.append(")")

                elif token == Parser.tokenTypes["L_BRACE"]:
                    Interpreter.cppCode.append("{")

                elif token == Parser.tokenTypes["R_BRACE"]:
                    Interpreter.cppCode.append("}")

                elif token == Parser.tokenTypes["KW_RETURN"]:
                    Interpreter.cppCode.append("return")

                elif token == Parser.tokenTypes["NEWLINE"]:
                    if Lexer.metadataGroups[i][j] is None:
                        Interpreter.cppCode.append("\n")
                    else:
                        Interpreter.cppCode.append(";\n")

                elif token == Parser.tokenTypes["INT_LIT"]:
                    Interpreter.cppCode.append(f"{Lexer.metadataGroups[i][j][0]}")

                elif token == Parser.tokenTypes["PLUS"]:
                    Interpreter.cppCode.append(f"+")

                elif token == Parser.tokenTypes["MINUS"]:
                    Interpreter.cppCode.append(f"-")

                elif token == Parser.tokenTypes["ASTERISK"]:
                    Interpreter.cppCode.append(f"*")

                elif token == Parser.tokenTypes["SLASH"]:
                    Interpreter.cppCode.append(f"/")

                elif token == Parser.tokenTypes["PERCENT"]:
                    Interpreter.cppCode.append(f"%")

            i += 1

    @staticmethod
    def compile(keepCpp:bool=False, autoExecute:bool=True):
        Interpreter.parseAndLex()
        Interpreter.translate()

        # compile from Uranium -> C++
        fullCode = ""
        for piece in Interpreter.cppCode:
            if "\n" in piece:
                fullCode += piece
            else:
                fullCode += f" {piece}"

        fname = re.search("/(.*)\.uran", Parser.filepath).group()[1:].split(".uran")[0]
        outPath = f"out/{fname}.cpp"

        with open(outPath, "w") as f:
            f.write(fullCode)


        # compile from C++ -> Executable
        os.system(f"gcc {outPath} -o out/{fname} -lm")

        if not keepCpp: os.remove(f"out/{fname}.cpp")

        if autoExecute: os.startfile(os.path.abspath(f"out/{fname}.exe"))