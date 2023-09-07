from src.UraniumParser.UraniumParser import Parser
from sys import exit
from termcolor import colored

class UraniumError:
    def __init__(self, err, msg, color="red"):
        print(colored(f"{err}: {msg}", color))
        exit(1)

class Lexer:
    tokenGroups = []
    metadataGroups = []

    @staticmethod
    def errorChecks():

        # check if main function exists
        if Parser.tokenTypes["REQ_FUNC_MAIN"] not in Parser.tokens:
            UraniumError("CompileError", "No entry point for execution found!")
        # check if there's exactly one main function
        if Parser.tokens.count(Parser.tokenTypes["REQ_FUNC_MAIN"]) > 1:
            UraniumError("CompileError", "Redefinition of function 'main'!")

        # check if all parentheses are complete
        if Parser.tokens.count(Parser.tokenTypes["L_PAREN"]) != Parser.tokens.count(Parser.tokenTypes["R_PAREN"]):
            UraniumError("SyntaxError", "Amount of opening parentheses does not match the amount of closing parentheses!")

        # check if all braces are complete
        if Parser.tokens.count(Parser.tokenTypes["L_BRACE"]) != Parser.tokens.count(Parser.tokenTypes["R_BRACE"]):
            UraniumError("SyntaxError", "Amount of opening braces does not match the amount of closing braces!")

        for i, token in enumerate(Parser.tokens):
            # check if 'int' keyword is used correctly
            if token == Parser.tokenTypes["DT_INT"]:
                if Parser.tokens[i + 1] not in [Parser.tokenTypes["REQ_FUNC_MAIN"]]:
                    UraniumError("SyntaxError", "Expected identifier 'main'!")

            # check if 'return' keyword is used correctly
            if token == Parser.tokenTypes["RETURN"]:
                if Parser.tokens[i + 1] not in [Parser.tokenTypes["INT_LIT"]]:
                    UraniumError("SyntaxError", "Expected integer literal!")
                if Parser.tokens[i + 2] != Parser.tokenTypes["NEWLINE"]:
                    UraniumError("SyntaxError", "Expected newline")

    @staticmethod
    def groupTokens():
        Lexer.errorChecks()

        currentGroup = []
        currentMdGroup = []
        for i, token in enumerate(Parser.tokens):
            currentGroup.append(token)
            currentMdGroup.append(Parser.tokenMetaData[i])
            if token == Parser.tokenTypes["NEWLINE"] or i == len(Parser.tokens) - 1:
                Lexer.tokenGroups.append(currentGroup)
                Lexer.metadataGroups.append(currentMdGroup)
                currentGroup = []
                currentMdGroup = []