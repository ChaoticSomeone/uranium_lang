from src.config import Config

# a class that helps with managing different tokens
class _Token:
	next_id:int = 0

	def __init__(self, pattern:str, cpp_translate:str, name:str="", has_pattern:bool=True):
		self.pattern = pattern
		self.cpp_translate = cpp_translate
		self.name = pattern if name == "" else name
		self.id = _Token.next_id
		self.has_pattern = has_pattern
		_Token.next_id += 1

	def __eq__(self, other):
		if isinstance(other, _Token):
			return self.id == other.id
		elif  isinstance(other, Token):
			return self.id == other.token.id

	def __str__(self):
		return f"Token('{self.name}')"

	def __repr__(self):
		return f"Token('{self.name}')"


class Token:
	def __init__(self, parent:_Token,  meta:list=[]):
		self.token = parent
		self.meta = meta

	def __eq__(self, other):
		if isinstance(other, _Token):
			return self.token.id == other.id
		elif  isinstance(other, Token):
			return self.token.id == other.token.id

	def __str__(self):
		return f"Token('{self.token.name}'{f":{self.meta}" if len(self.meta[0]) != 0 else ""})"

	def __repr__(self):
		return f"Token('{self.token.name}'{f":{self.meta}" if len(self.meta[0]) != 0 else ""})"


# this class allows us to group "similar" tokens
class _TokenGroup:
	def __init__(self, start:_Token, end:_Token):
		self.start = start.id
		self.end = end.id

	def __contains__(self, item):
		if isinstance(item, _Token):
			return self.start <= item.id <= self.end
		elif isinstance(item, Token):
			return self.start <= item.token.id <= self.end

	def get_all(self) -> range:
		return range(self.start, self.end + 1)


# just treat this one as an enum
# contains all the different tokens
class TokensEnum:
	# misc
	NEWLINE = _Token(r"\n", "","newline")

	STD_URANIUM = _Token(r"uranium", "", "uranium std")

	# keywords
	KW_FUNC = _Token(r"func", "")
	KW_RETURN = _Token(r"return", "return")
	KW_IMPORT = _Token(r"import", "#include")
	KW_IF = _Token(r"if", "if")
	KW_TRUE = _Token(r"true", "true")
	KW_FALSE = _Token(r"false", "true")

	KEYWORDS = _TokenGroup(KW_FUNC, KW_FALSE)

	# datatypes and datatype keywords
	TYPE_INT = _Token(r"int", "int")
	TYPE_FLOAT = _Token(r"float", "float")
	TYPE_STRING = _Token(r"string", "std::string")
	TYPE_BOOL = _Token(r"bool", "bool")

	TYPES = _TokenGroup(TYPE_INT, TYPE_BOOL)

	# literals
	LIT_FLOAT = _Token(r"\d*\.\d+", "", "float literal")
	LIT_INT = _Token(r"\d+", "", "int literal")
	LIT_STRING = _Token(r"\".*\"", "", "string literal")

	LITERALS = _TokenGroup(LIT_FLOAT, LIT_STRING)

	# symbols
	SYM_L_PAREN = _Token(r"\(", "(", "(")
	SYM_R_PAREN = _Token(r"\)", ")", ")")
	SYM_L_CURLY_BRACKET = _Token(r"\{", "{", "{")
	SYM_R_CURLY_BRACKET = _Token(r"\}", "}", "}")
	SYM_NAMESPACE_DELIMITER = _Token(r"::", "/", "namespace delimiter")
	SYM_COMMA = _Token(r",", ",", "comma")
	SYM_DOT = _Token(r"\.", "::", "dot")
	SYM_L_ANGLE = _Token(r"<", "<")
	SYM_R_ANGLE = _Token(r">", ">")
	SYM_EXCLAMATION = _Token(r"!", "!")
	SYM_RET_TYPE = _Token(r"->", "")									# ignored by the compiler
	SYM_TYPE = _Token(r":", "", "type delimiter")			# ignored by the compiler
	SYM_PLUS = _Token(r"\+", "+", "plus")
	SYM_MINUS = _Token(r"-", "-", "minus")
	SYM_ASTERISK = _Token(r"\*", "*", "asterisk")
	SYM_SLASH = _Token(r"/", "/", "slash")
	SYM_PERCENT = _Token(r"%", "%", "modulo")
	SYM_EQUALS = _Token(r"=", "=", "equals")

	SYMBOLS = _TokenGroup(SYM_L_PAREN, SYM_EQUALS)

	# not part of Uranium
	EXTERNAL_VOID = _Token(r"void", "void", "void")

	EXTERNALS = _TokenGroup(EXTERNAL_VOID, EXTERNAL_VOID)

	# composite operators (2 characters)
	OP_EQUALS = _Token("", "==", "logical equals", False)
	OP_EQUALS_COMP = [SYM_EQUALS, SYM_EQUALS]

	OP_LESS_EQUALS = _Token("", "<=", "less equals", False)
	OP_LESS_EQUALS_COMP = [SYM_L_ANGLE, SYM_EQUALS]

	OP_GREATER_EQUALS = _Token("", "<=", "less equals", False)
	OP_GREATER_EQUALS_COMP = [SYM_R_ANGLE, SYM_EQUALS]

	OP_NOT_EQUAL = _Token("", "!=", "not equal", False)
	OP_NOT_EQUAL_COMP = [SYM_EXCLAMATION, SYM_EQUALS]

	composites2 = [
		OP_EQUALS_COMP,
		OP_LESS_EQUALS_COMP,
		OP_GREATER_EQUALS_COMP,
		OP_NOT_EQUAL_COMP
	]

	# other misc
	IDENTIFIER = _Token(r"[a-zA-Z_]\w*", "", "identifier")
	STD_IDENTIFIER = _Token("", "", "uranium std identifier", False)

	# literally all tokens from above
	ALL_TOKENS = []


	@staticmethod
	def load_tokens():
		TokensEnum.ALL_TOKENS = list(filter(lambda x: isinstance(x, _Token) and x.has_pattern, TokensEnum.__dict__.values()))



def print_token_list(tokens:list, end:str="\n") -> None:
	if not Config.ignore_debug_output:
		for token in tokens:
			print(token)
		print(end)
