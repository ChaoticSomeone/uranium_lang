import re

class Parser:
    keywords = {}
    arithmetics = {}
    tokenTypes = {}
    braceLikes = {}
    literals = {}
    comparisons = {}

    ids = []
    tokenMetaData = []
    tokens = []

    code = ""
    filepath = ""

    idx = 0
    oldIdx = 0

    @staticmethod
    def initParser():
        enumTT = enumerate([
            "UNKNOWN_TOKEN",

            "KW_INT",
            "KW_FLOAT",
            "KW_CHAR",
            "KW_RETURN",
            "KW_BOOL",
            "KW_TRUE",
            "KW_FALSE",

            "IDENTIFIER",
            "INT_LIT",
            "FLOAT_LIT",
            "CHAR_LIT",

            "L_PAREN",
            "R_PAREN",
            "L_BRACE",
            "R_BRACE",
            "L_ANGLE",
            "R_ANGLE",

            "COMP_EQ",
            "COMP_LE",
            "COMP_GE",
            "COMP_NE",

            "PLUS",
            "MINUS",
            "ASTERISK",
            "SLASH",
            "PERCENT",
            "EQUALS",
            "ELLIPSIS",
            "NEWLINE"
        ])

        for i, TT in enumTT:
            Parser.tokenTypes[TT] = i
            if re.search("^KW_", TT) is not None:
                Parser.keywords[TT] = i
            if TT in ["PLUS", "MINUS", "ASTERISK", "SLASH", "PERCENT"]:
                Parser.arithmetics[TT] = i
            if TT in ["L_PAREN", "R_PAREN", "L_BRACE", "R_BRACE", "L_ANGLE", "R_ANGLE"]:
                Parser.braceLikes[TT] = i
            if re.search("_LIT$", TT) is not None:
                Parser.literals[TT] = i
            if re.search("^COMP_", TT) is not None:
                Parser.comparisons[TT] = i


    @staticmethod
    def readUraniumFile(filepath:str="uranium/main.uran") -> str:
        Parser.filepath = filepath
        Parser.initParser()
        with open(filepath, "r") as f:
            lines = f.readlines()
        Parser.code = "".join(lines)
        return Parser.code

    @staticmethod
    def tokenize():
        isMultiLineCom:bool = False
        while Parser.idx < len(Parser.code):
            c = Parser.code[Parser.idx]

            # Isolate the tokenizing process while in a multi-line comment
            if isMultiLineCom:
                if (com := re.search("^\*/\s*\n", Parser.code[Parser.idx:])) is not None:
                    isMultiLineCom = False
                    Parser.idx += len(com.group())
                else:
                    Parser.idx += 1
                continue


            if re.search("^int(\s+|<)", Parser.code[Parser.idx:]):
                Parser.tokens.append(Parser.tokenTypes["KW_INT"])
                Parser.idx += 3
                Parser.tokenMetaData.append(None)

            elif re.search("^float(\s+|<)", Parser.code[Parser.idx:]):
                Parser.tokens.append(Parser.tokenTypes["KW_FLOAT"])
                Parser.idx += 5
                Parser.tokenMetaData.append(None)

            elif re.search("^char(\s+)", Parser.code[Parser.idx:]):
                Parser.tokens.append(Parser.tokenTypes["KW_CHAR"])
                Parser.idx += 4
                Parser.tokenMetaData.append(None)

            elif re.search("^bool(\s+)", Parser.code[Parser.idx:]):
                Parser.tokens.append(Parser.tokenTypes["KW_BOOL"])
                Parser.idx += 4
                Parser.tokenMetaData.append(None)

            elif re.search("^true(\s+)", Parser.code[Parser.idx:]):
                Parser.tokens.append(Parser.tokenTypes["KW_TRUE"])
                Parser.idx += 4
                Parser.tokenMetaData.append(None)

            elif re.search("^false(\s+)", Parser.code[Parser.idx:]):
                Parser.tokens.append(Parser.tokenTypes["KW_FALSE"])
                Parser.idx += 5
                Parser.tokenMetaData.append(None)

            elif re.search("^return(\s+)", Parser.code[Parser.idx:]):
                Parser.tokens.append(Parser.tokenTypes["KW_RETURN"])
                Parser.idx += 6
                Parser.tokenMetaData.append(None)

            elif re.search("^\.\.\.", Parser.code[Parser.idx:]):
                Parser.tokens.append(Parser.tokenTypes["ELLIPSIS"])
                Parser.idx += 3
                Parser.tokenMetaData.append(None)

            elif com := re.search("^//[^\n]*\n", Parser.code[Parser.idx:]):
                if com is not None: Parser.idx += len(com.group())

            elif com := re.search("^/\*", Parser.code[Parser.idx:]):
                if com is not None:
                    Parser.idx += 2
                    isMultiLineCom = True
                    continue

            elif c == "(":
                Parser.tokens.append(Parser.tokenTypes["L_PAREN"])
                Parser.idx += 1
                Parser.tokenMetaData.append(None)

            elif c == ")":
                Parser.tokens.append(Parser.tokenTypes["R_PAREN"])
                Parser.idx += 1
                Parser.tokenMetaData.append(None)

            elif c == "{":
                Parser.tokens.append(Parser.tokenTypes["L_BRACE"])
                Parser.idx += 1
                Parser.tokenMetaData.append(None)

            elif c == "}":
                Parser.tokens.append(Parser.tokenTypes["R_BRACE"])
                Parser.idx += 1
                Parser.tokenMetaData.append(None)

            elif c == "<":
                if Parser.code[Parser.idx+1] == "=":
                    Parser.tokens.append(Parser.tokenTypes["COMP_LE"])
                    Parser.idx += 2
                else:
                    Parser.tokens.append(Parser.tokenTypes["L_ANGLE"])
                    Parser.idx += 1
                Parser.tokenMetaData.append(None)

            elif c == ">":
                if Parser.code[Parser.idx + 1] == "=":
                    Parser.tokens.append(Parser.tokenTypes["COMP_GE"])
                    Parser.idx += 2
                else:
                    Parser.tokens.append(Parser.tokenTypes["R_ANGLE"])
                    Parser.idx += 1
                Parser.tokenMetaData.append(None)

            elif c == "\n":
                Parser.tokens.append(Parser.tokenTypes["NEWLINE"])
                Parser.idx += 1
                Parser.tokenMetaData.append(None)

            elif c.isspace():
                Parser.idx += 1
                continue

            elif re.search("^\+", Parser.code[Parser.idx:]):
                Parser.tokens.append(Parser.tokenTypes["PLUS"])
                Parser.idx += 1
                Parser.tokenMetaData.append(None)

            elif re.search("^-", Parser.code[Parser.idx:]):
                Parser.tokens.append(Parser.tokenTypes["MINUS"])
                Parser.idx += 1
                Parser.tokenMetaData.append(None)

            elif re.search("^\*", Parser.code[Parser.idx:]):
                Parser.tokens.append(Parser.tokenTypes["ASTERISK"])
                Parser.idx += 1
                Parser.tokenMetaData.append(None)

            elif re.search("^/", Parser.code[Parser.idx:]):
                Parser.tokens.append(Parser.tokenTypes["SLASH"])
                Parser.idx += 1
                Parser.tokenMetaData.append(None)

            elif re.search("^%", Parser.code[Parser.idx:]):
                Parser.tokens.append(Parser.tokenTypes["PERCENT"])
                Parser.idx += 1
                Parser.tokenMetaData.append(None)

            elif re.search("^=", Parser.code[Parser.idx:]):
                if Parser.code[Parser.idx+1] == "=":
                    Parser.tokens.append(Parser.tokenTypes["COMP_EQ"])
                    Parser.idx += 2
                else:
                    Parser.tokens.append(Parser.tokenTypes["EQUALS"])
                    Parser.idx += 1
                Parser.tokenMetaData.append(None)

            elif num := re.search("^\d+\.\d+", Parser.code[Parser.idx:]):
                if num is not None:
                    Parser.tokens.append(Parser.tokenTypes["FLOAT_LIT"])
                    l = len(num.group())
                    Parser.idx += l
                    Parser.tokenMetaData.append([float(num.group())])

            elif num := re.search("^\d+", Parser.code[Parser.idx:]):
                if num is not None and num.group().isdecimal():
                    Parser.tokens.append(Parser.tokenTypes["INT_LIT"])
                    l = len(num.group())
                    Parser.idx += l
                    Parser.tokenMetaData.append([int(num.group())])

            elif char := re.search("^\'(\S| )\'", Parser.code[Parser.idx:]):
                if char is not None:
                    Parser.tokens.append(Parser.tokenTypes["CHAR_LIT"])
                    l = len(char.group())
                    Parser.idx += l
                    Parser.tokenMetaData.append([char.group()])

            # must be last
            elif identifier := re.search("^[a-zA-Z_](([a-zA-Z_]|\d)*)", Parser.code[Parser.idx:]):
                if identifier is not None:
                    Parser.tokens.append(Parser.tokenTypes["IDENTIFIER"])
                    l = len(identifier.group())
                    Parser.idx += l
                    Parser.tokenMetaData.append([identifier.group()])
                    Parser.ids.append(identifier.group())

            else:
                Parser.tokens.append(Parser.tokenTypes["UNKNOWN_TOKEN"])
                Parser.idx += 1
                Parser.tokenMetaData.append(None)



    @staticmethod
    def showTokens(doShowMetaData=True):
        tts = [list(Parser.tokenTypes.items())[i][0] for i in Parser.tokens]
        i = 0

        while i < len(tts):
            if doShowMetaData:
                print(f"{tts[i]:<15}: {Parser.tokenMetaData[i]}")
            else:
                if i < len(tts) - 1:
                    print(f"{tts[i]}, ", end="")
                else:
                    print(tts[i])
            i += 1