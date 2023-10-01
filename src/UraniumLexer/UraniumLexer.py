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
                if Parser.tokens[i + 1] not in [Parser.tokenTypes["IDENTIFIER"], Parser.tokenTypes["L_ANGLE"], Parser.tokenTypes["ELLIPSIS"]]:
                    UraniumError("SyntaxError", "Unexpected Token at int keyword!")
                if Parser.tokens[i+1] == Parser.tokenTypes["ELLIPSIS"]:
                    i += 1
                    continue
                if Parser.tokens[i + 1] == Parser.tokenTypes["L_ANGLE"] and Parser.tokens[i + 2] == Parser.tokenTypes["INT_LIT"] and Parser.tokens[i + 3] == Parser.tokenTypes["R_ANGLE"]:
                    if not Parser.tokenMetaData[i+2][0] in [1,2,4,8,16]:
                       UraniumError("SyntaxError", "Invalid integer literal at int keyword!")
                    Parser.tokenMetaData[i] = Parser.tokenMetaData[i + 2]
                    for j in range(1,3):
                        Parser.tokens.pop(i+j)
                        Parser.tokenMetaData.pop(i+j)
                    Parser.tokens.pop(i+1)
                    Parser.tokenMetaData.pop(i+1)

            # check if 'float' keyword is used correctly
            if token == Parser.tokenTypes["KW_FLOAT"]:
                if Parser.tokens[i + 1] not in [Parser.tokenTypes["IDENTIFIER"], Parser.tokenTypes["L_ANGLE"], Parser.tokenTypes["ELLIPSIS"]]:
                    UraniumError("SyntaxError", "Unexpected Token at float keyword!")
                if Parser.tokens[i+1] == Parser.tokenTypes["ELLIPSIS"]:
                    i += 1
                    continue
                if Parser.tokens[i + 1] == Parser.tokenTypes["L_ANGLE"] and Parser.tokens[i + 2] == Parser.tokenTypes["INT_LIT"] and Parser.tokens[i + 3] == Parser.tokenTypes["R_ANGLE"]:
                    if not Parser.tokenMetaData[i+2][0] in [4,8,16]:
                       UraniumError("SyntaxError", "Invalid integer literal at float keyword!")
                    Parser.tokenMetaData[i] = Parser.tokenMetaData[i + 2]
                    for j in range(1,3):
                        Parser.tokens.pop(i+j)
                        Parser.tokenMetaData.pop(i+j)
                    Parser.tokens.pop(i+1)
                    Parser.tokenMetaData.pop(i+1)

            # check if 'char' keyword is used correctly
            if token == Parser.tokenTypes["KW_CHAR"]:
                if Parser.tokens[i + 1] not in [Parser.tokenTypes["IDENTIFIER"], Parser.tokenTypes["ELLIPSIS"]]:
                    UraniumError("SyntaxError", "Unexpected Token at keyword char!")

            # check if 'bool' keyword is used correctly
            if token == Parser.tokenTypes["KW_BOOL"]:
                if Parser.tokens[i + 1] not in [Parser.tokenTypes["IDENTIFIER"], Parser.tokenTypes["ELLIPSIS"]]:
                    UraniumError("SyntaxError", "Unexpected Token at keyword bool!")

            # check if 'true' keyword is used correctly
            if token == Parser.tokenTypes["KW_TRUE"]:
                if Parser.tokens[i + 1] not in [Parser.tokenTypes["NEWLINE"], Parser.tokenTypes["ELLIPSIS"]]:
                    UraniumError("SyntaxError", "Unexpected Token at keyword true!")

            # check if 'false' keyword is used correctly
            if token == Parser.tokenTypes["KW_FALSE"]:
                if Parser.tokens[i + 1] not in [Parser.tokenTypes["NEWLINE"], Parser.tokenTypes["ELLIPSIS"]]:
                    UraniumError("SyntaxError", "Unexpected Token at keyword false!")

            # check if 'return' keyword is used correctly
            if token == Parser.tokenTypes["KW_RETURN"]:
                if Parser.tokens[i + 1] not in [*Parser.literals.values(), Parser.tokenTypes["IDENTIFIER"], Parser.tokenTypes["KW_TRUE"], Parser.tokenTypes["KW_FALSE"], Parser.tokenTypes["ELLIPSIS"]]:
                    UraniumError("SyntaxError", "Unexpected Token keyword return!")


            # check if integer literals are used correctly
            if token == Parser.tokenTypes["INT_LIT"]:
                if Parser.tokens[i + 1] in [Parser.tokenTypes["NEWLINE"], *Parser.arithmetics.values(), Parser.tokenTypes["ELLIPSIS"]]:
                    i += 1
                    continue
                else:
                    UraniumError("SyntaxError", f"Unexpected token at integer literal!")

            # check if float literals are used correctly
            if token == Parser.tokenTypes["FLOAT_LIT"]:
                if Parser.tokens[i + 1] in [Parser.tokenTypes["NEWLINE"], *Parser.arithmetics.values(), Parser.tokenTypes["ELLIPSIS"]]:
                    i += 1
                    continue
                else:
                    UraniumError("SyntaxError", f"Unexpected token at float literal!")

            # check if char literals are used correctly
            if token == Parser.tokenTypes["CHAR_LIT"]:
                if Parser.tokens[i + 1] in [Parser.tokenTypes["NEWLINE"], Parser.tokenTypes["ELLIPSIS"]]:
                    i += 1
                    continue
                else:
                    UraniumError("SyntaxError", f"Unexpected token at char literal!")

            # check if plus signs are used correctly
            if token == Parser.tokenTypes["PLUS"]:
                if Parser.tokens[i + 1] in [Parser.tokenTypes["INT_LIT"], Parser.tokenTypes["FLOAT_LIT"], Parser.tokenTypes["ELLIPSIS"]]:
                    i += 1
                    continue
                else:
                    UraniumError("SyntaxError", f"Unexpected token at plus sign!")

            # check if minus signs are used correctly
            if token == Parser.tokenTypes["MINUS"]:
                if Parser.tokens[i + 1] in [Parser.tokenTypes["INT_LIT"], Parser.tokenTypes["FLOAT_LIT"], Parser.tokenTypes["ELLIPSIS"]]:
                    i += 1
                    continue
                else:
                    UraniumError("SyntaxError", f"Unexpected token at minus sign!")

            # check if asterisk is used correctly
            if token == Parser.tokenTypes["ASTERISK"]:
                if Parser.tokens[i + 1] in [Parser.tokenTypes["INT_LIT"], Parser.tokenTypes["FLOAT_LIT"], Parser.tokenTypes["MINUS"], Parser.tokenTypes["PLUS"], Parser.tokenTypes["ELLIPSIS"]]:
                    i += 1
                    continue
                else:
                    UraniumError("SyntaxError", f"Unexpected token at asterisk sign!")

            # check if slash is used correctly
            if token == Parser.tokenTypes["SLASH"]:
                if Parser.tokens[i + 1] in [Parser.tokenTypes["INT_LIT"], Parser.tokenTypes["FLOAT_LIT"], Parser.tokenTypes["MINUS"], Parser.tokenTypes["PLUS"], Parser.tokenTypes["ELLIPSIS"]]:
                    i += 1
                    continue
                else:
                    UraniumError("SyntaxError", f"Unexpected token at slash sign!")

            # check if percent sign is used correctly
            if token == Parser.tokenTypes["PERCENT"]:
                if Parser.tokens[i + 1] in [Parser.tokenTypes["INT_LIT"], Parser.tokenTypes["MINUS"], Parser.tokenTypes["PLUS"], Parser.tokenTypes["ELLIPSIS"]]:
                    i += 1
                    continue
                else:
                    UraniumError("SyntaxError", f"Unexpected token at percent sign!")

            # check if equals sign is used correctly
            if token == Parser.tokenTypes["EQUALS"]:
                if Parser.tokens[i + 1] in [*Parser.literals.values(), Parser.tokenTypes["MINUS"], Parser.tokenTypes["PLUS"], Parser.tokenTypes["KW_TRUE"], Parser.tokenTypes["KW_FALSE"], Parser.tokenTypes["ELLIPSIS"]]:
                    i += 1
                    continue
                else:
                    UraniumError("SyntaxError", f"Unexpected token at equals sign!")

            # check if identifiers are used correctly
            if token == Parser.tokenTypes["IDENTIFIER"]:
                if Parser.tokens[i + 1] in [Parser.tokenTypes["EQUALS"], Parser.tokenTypes["NEWLINE"], Parser.tokenTypes["L_PAREN"], Parser.tokenTypes["ELLIPSIS"]]:
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

        # group tokens by line
        j = 0
        for i, token in enumerate(Parser.tokens):

            currentGroup.append(token)
            currentMdGroup.append(Parser.tokenMetaData[i])

            if token == Parser.tokenTypes["NEWLINE"] or i == len(Parser.tokens) - 1:
                currentMdGroup[j-1] = ";"

                Lexer.tokenGroups.append(currentGroup)
                Lexer.metadataGroups.append(currentMdGroup)
                currentGroup = []
                currentMdGroup = []
                j = 0

            j += 1

        # ellipsis (line continuation) implementation
        i = 0
        while i < len(Lexer.tokenGroups):
            j = 0
            while j < len(Lexer.tokenGroups[i]):
                if Lexer.tokenGroups[i][j] == Parser.tokenTypes["ELLIPSIS"]:
                    Lexer.tokenGroups[i].pop(len(Lexer.tokenGroups[i])-1)
                    Lexer.tokenGroups[i].extend(Lexer.tokenGroups[i+1])
                    Lexer.tokenGroups.pop(i+1)

                    Lexer.metadataGroups[i].pop(len(Lexer.metadataGroups[i])-1)
                    Lexer.metadataGroups[i].extend(Lexer.metadataGroups[i+1])
                    Lexer.metadataGroups.pop(i+1)
                    break
                j += 1
            i += 1