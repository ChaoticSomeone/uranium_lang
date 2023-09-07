import re

class Parser:
    tokenTypes = {}
    code = ""
    tokens = []
    tokenMetaData = []
    idx = 0
    oldIdx = 0
    ids = []

    @staticmethod
    def initParser():
        enumTT = enumerate([
            "UNKNOWN_TOKEN",
            "DT_INT",
            "REQ_FUNC_MAIN",
            "IDENTIFIER",
            "L_PAREN",
            "R_PAREN",
            "L_BRACE",
            "R_BRACE",
            "RETURN",
            "INT_LIT",
            "NEWLINE"
        ])
        for i, TT in enumTT:
            Parser.tokenTypes[TT] = i

    @staticmethod
    def readUraniumFile(filepath:str="uranium/main.uran") -> str:
        Parser.initParser()
        with open(filepath, "r") as f:
            lines = f.readlines()
        Parser.code = "".join(lines)
        return Parser.code

    @staticmethod
    def tokenize():
        while Parser.idx < len(Parser.code):
            c = Parser.advance()

            if re.search("^int", Parser.code[Parser.idx-1:]) and Parser.peek(2).isspace():
                Parser.tokens.append(Parser.tokenTypes["DT_INT"])
                Parser.idx += 2
                Parser.tokenMetaData.append(None)


            elif re.search("^main", Parser.code[Parser.idx-1:]) and not Parser.peek(3).isalnum():
                Parser.tokens.append(Parser.tokenTypes["REQ_FUNC_MAIN"])
                Parser.ids.append("main")
                Parser.idx += 3
                Parser.tokenMetaData.append(None)

            elif re.search("^return", Parser.code[Parser.idx-1:]):
                Parser.tokens.append(Parser.tokenTypes["RETURN"])
                Parser.idx += 5
                Parser.tokenMetaData.append(None)

            elif c == "(":
                Parser.tokens.append(Parser.tokenTypes["L_PAREN"])
                Parser.tokenMetaData.append(None)

            elif c == ")":
                Parser.tokens.append(Parser.tokenTypes["R_PAREN"])
                Parser.tokenMetaData.append(None)

            elif c == "{":
                Parser.tokens.append(Parser.tokenTypes["L_BRACE"])
                Parser.tokenMetaData.append(None)

            elif c == "}":
                Parser.tokens.append(Parser.tokenTypes["R_BRACE"])
                Parser.tokenMetaData.append(None)

            elif c == "\n":
                Parser.tokens.append(Parser.tokenTypes["NEWLINE"])
                Parser.tokenMetaData.append(None)

            elif c.isspace():
                continue

            elif num := re.search("^\d+", Parser.code[Parser.idx-1:]):
                if num is not None and num.group().isdecimal():
                    Parser.tokens.append(Parser.tokenTypes["INT_LIT"])
                    l = len(num.group())
                    if l > 1: Parser.idx += l - 1
                    Parser.tokenMetaData.append([int(num.group())])


            else:
                Parser.tokens.append(Parser.tokenTypes["UNKNOWN_TOKEN"])
                Parser.tokenMetaData.append(None)

    @staticmethod
    def peek(offset:int=0) -> str: return Parser.code[Parser.idx + offset]

    @staticmethod
    def advance() -> str:
        Parser.oldIdx = Parser.idx
        Parser.idx += 1
        return Parser.code[Parser.idx - 1]

    @staticmethod
    def advanceUntil(character:str) -> str:
        val = Parser.code[Parser.idx:].split(character, 1)[0]
        Parser.oldIdx = Parser.idx
        Parser.idx += len(val)
        return val

    @staticmethod
    def peekUntil(character:str) -> str:
        return Parser.code[Parser.idx:].split(character, 1)[0]

    @staticmethod
    def rollback(): Parser.idx = Parser.oldIdx

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