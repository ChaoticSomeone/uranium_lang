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
                if Parser.tokens[i + 1] not in [Parser.tokenTypes["IDENTIFIER"], Parser.tokenTypes["L_ANGLE"]]:
                    UraniumError("SyntaxError", "Unexpected Token at int keyword!")

            # check if 'float' keyword is used correctly
            if token == Parser.tokenTypes["KW_FLOAT"]:
                if Parser.tokens[i + 1] not in [Parser.tokenTypes["IDENTIFIER"], Parser.tokenTypes["L_ANGLE"]]:
                    UraniumError("SyntaxError", "Unexpected Token at float keyword!")

            # check if 'char' keyword is used correctly
            if token == Parser.tokenTypes["KW_CHAR"]:
                if Parser.tokens[i + 1] not in [Parser.tokenTypes["IDENTIFIER"]]:
                    UraniumError("SyntaxError", "Unexpected Token at keyword char!")

            # check if 'return' keyword is used correctly
            if token == Parser.tokenTypes["KW_RETURN"]:
                if Parser.tokens[i + 1] not in [*Parser.literals.values(), Parser.tokenTypes["IDENTIFIER"]]:
                    UraniumError("SyntaxError", "Unexpected Token keyword return!")


            # check if integer literals are used correctly
            if token == Parser.tokenTypes["INT_LIT"]:
                if Parser.tokens[i + 1] in [Parser.tokenTypes["NEWLINE"], Parser.tokenTypes["R_ANGLE"], *Parser.arithmetics.values()]:
                    i += 1
                    continue
                else:
                    UraniumError("SyntaxError", f"Unexpected token at integer literal!")

            # check if float literals are used correctly
            if token == Parser.tokenTypes["FLOAT_LIT"]:
                if Parser.tokens[i + 1] in [Parser.tokenTypes["NEWLINE"], *Parser.arithmetics.values()]:
                    i += 1
                    continue
                else:
                    UraniumError("SyntaxError", f"Unexpected token at float literal!")

            # check if char literals are used correctly
            if token == Parser.tokenTypes["CHAR_LIT"]:
                if Parser.tokens[i + 1] in [Parser.tokenTypes["NEWLINE"]]:
                    i += 1
                    continue
                else:
                    UraniumError("SyntaxError", f"Unexpected token at char literal!")

            # check if plus signs are used correctly
            if token == Parser.tokenTypes["PLUS"]:
                if Parser.tokens[i + 1] in [Parser.tokenTypes["INT_LIT"], Parser.tokenTypes["FLOAT_LIT"]]:
                    i += 1
                    continue
                else:
                    UraniumError("SyntaxError", f"Unexpected token at plus sign!")

            # check if minus signs are used correctly
            if token == Parser.tokenTypes["MINUS"]:
                if Parser.tokens[i + 1] in [Parser.tokenTypes["INT_LIT"], Parser.tokenTypes["FLOAT_LIT"]]:
                    i += 1
                    continue
                else:
                    UraniumError("SyntaxError", f"Unexpected token at minus sign!")

            # check if asterisk is used correctly
            if token == Parser.tokenTypes["ASTERISK"]:
                if Parser.tokens[i + 1] in [Parser.tokenTypes["INT_LIT"], Parser.tokenTypes["FLOAT_LIT"], Parser.tokenTypes["MINUS"], Parser.tokenTypes["PLUS"]]:
                    i += 1
                    continue
                else:
                    UraniumError("SyntaxError", f"Unexpected token at asterisk sign!")

            # check if slash is used correctly
            if token == Parser.tokenTypes["SLASH"]:
                if Parser.tokens[i + 1] in [Parser.tokenTypes["INT_LIT"], Parser.tokenTypes["FLOAT_LIT"], Parser.tokenTypes["MINUS"], Parser.tokenTypes["PLUS"]]:
                    i += 1
                    continue
                else:
                    UraniumError("SyntaxError", f"Unexpected token at slash sign!")

            # check if percent sign is used correctly
            if token == Parser.tokenTypes["PERCENT"]:
                if Parser.tokens[i + 1] in [Parser.tokenTypes["INT_LIT"], Parser.tokenTypes["MINUS"], Parser.tokenTypes["PLUS"]]:
                    i += 1
                    continue
                else:
                    UraniumError("SyntaxError", f"Unexpected token at percent sign!")

            # check if equals sign is used correctly
            if token == Parser.tokenTypes["EQUALS"]:
                if Parser.tokens[i + 1] in [*Parser.literals.values(), Parser.tokenTypes["MINUS"], Parser.tokenTypes["PLUS"]]:
                    i += 1
                    continue
                else:
                    UraniumError("SyntaxError", f"Unexpected token at equals sign!")

            # check if left angle is used correctly
            if token == Parser.tokenTypes["L_ANGLE"]:
                if not Parser.tokens[i + 1] in [Parser.tokenTypes["INT_LIT"], Parser.tokenTypes["R_ANGLE"]]:
                    UraniumError("SyntaxError", f"Unexpected token at left angle!")

            # check if right angle is used correctly
            if token == Parser.tokenTypes["R_ANGLE"]:
                if not Parser.tokens[i + 1] in [Parser.tokenTypes["IDENTIFIER"]]:
                    UraniumError("SyntaxError", f"Unexpected token at right angle!")

            # check if identifiers are used correctly
            if token == Parser.tokenTypes["IDENTIFIER"]:
                if Parser.tokens[i + 1] in [Parser.tokenTypes["EQUALS"], Parser.tokenTypes["NEWLINE"], Parser.tokenTypes["L_PAREN"]]:
                    i += 1
                    continue
                else:
                    UraniumError("SyntaxError", f"Unexpected token at identifier!")


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

                keywordCount = [TT in Parser.keywords.values() for TT in currentGroup].count(True)
                if keywordCount == 1: currentMdGroup[j-1] = ";"

                Lexer.tokenGroups.append(currentGroup)
                Lexer.metadataGroups.append(currentMdGroup)
                currentGroup = []
                currentMdGroup = []
                j = 0

            j += 1