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

        i = 0
        while i < len(Parser.tokens):
            token = Parser.tokens[i]

            # check if 'int' keyword is used correctly
            if token == Parser.tokenTypes["KW_INT"]:
                if Parser.tokens[i + 1] not in [Parser.tokenTypes["REQ_FUNC_MAIN"]]:
                    UraniumError("SyntaxError", "Expected identifier 'main'!")

            # check if integer literals are used correctly
            if token == Parser.tokenTypes["INT_LIT"]:
                if Parser.tokens[i + 1] in [Parser.tokenTypes["NEWLINE"], *Parser.arithmetics.values()]:
                    i += 1
                    continue
                else:
                    UraniumError("SyntaxError", f"Unexpected token!")

            # check if plus signs are used correctly
            if token == Parser.tokenTypes["PLUS"]:
                if Parser.tokens[i + 1] in [Parser.tokenTypes["INT_LIT"]]:
                    i += 1
                    continue
                else:
                    UraniumError("SyntaxError", f"Unexpected token!")

            # check if minus signs are used correctly
            if token == Parser.tokenTypes["MINUS"]:
                if Parser.tokens[i + 1] in [Parser.tokenTypes["INT_LIT"]]:
                    i += 1
                    continue
                else:
                    UraniumError("SyntaxError", f"Unexpected token!")

            # check if asterisk is used correctly
            if token == Parser.tokenTypes["ASTERISK"]:
                if Parser.tokens[i + 1] in [Parser.tokenTypes["INT_LIT"], Parser.tokenTypes["MINUS"], Parser.tokenTypes["PLUS"]]:
                    i += 1
                    continue
                else:
                    UraniumError("SyntaxError", f"Unexpected token!")

            # check if slash is used correctly
            if token == Parser.tokenTypes["SLASH"]:
                if Parser.tokens[i + 1] in [Parser.tokenTypes["INT_LIT"], Parser.tokenTypes["MINUS"], Parser.tokenTypes["PLUS"]]:
                    i += 1
                    continue
                else:
                    UraniumError("SyntaxError", f"Unexpected token!")

            # check if percent sign is used correctly
            if token == Parser.tokenTypes["PERCENT"]:
                if Parser.tokens[i + 1] in [Parser.tokenTypes["INT_LIT"], Parser.tokenTypes["MINUS"], Parser.tokenTypes["PLUS"]]:
                    i += 1
                    continue
                else:
                    UraniumError("SyntaxError", f"Unexpected token!")


            i += 1


    @staticmethod
    def groupTokens():
        Lexer.errorChecks()

        currentGroup = []
        currentMdGroup = []
        j = 0
        for i, token in enumerate(Parser.tokens):

            currentGroup.append(token)
            currentMdGroup.append(Parser.tokenMetaData[i])

            if token == Parser.tokenTypes["NEWLINE"] or i == len(Parser.tokens) - 1:

                keywordCount = [TT in Parser.keywords.values() or TT == Parser.tokenTypes["REQ_FUNC_MAIN"] for TT in currentGroup].count(True)
                if keywordCount == 1: currentMdGroup[j-1] = ";"

                Lexer.tokenGroups.append(currentGroup)
                Lexer.metadataGroups.append(currentMdGroup)
                currentGroup = []
                currentMdGroup = []
                j = 0

            j += 1