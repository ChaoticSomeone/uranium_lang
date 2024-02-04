from src.config import Config
from src import errors

class TokenTemplate:
	def __init__(self, pattern: str, cpp_translate: str, name: str = "", _id: str = ""):
		self.pattern = pattern
		self.cpp_translate = cpp_translate
		self.name = name if name else pattern
		self.id = _id

	def __eq__(self, other):
		if isinstance(other, TokenTemplate):
			return self.id == other.id
		elif isinstance(other, Token):
			return self.id == other.token.id

	def __str__(self):
		return f"_Token('{self.name}')"

	def __repr__(self):
		return f"_Token('{self.name}')"

	def show_as_py(self):
		return f"TokenTemplate(pattern=r'{self.pattern}', cpp_translate='{self.cpp_translate}', name='{self.name}', _id='{self.id}')"


class Token:
	def __init__(self, parent:TokenTemplate, meta:list=[], position:list[int, int, int]=[0, 0, 0]):
		self.token = parent
		self.meta = meta
		self.position = position

	def __eq__(self, other):
		if isinstance(other, TokenTemplate):
			return self.token.id == other.id
		elif isinstance(other, Token):
			return self.token.id == other.token.id

	def __str__(self):
		return f"Token('{self.token.name}'{f":{self.meta}" if len(self.meta) > 0 and self.meta[0] else ""})"

	def __repr__(self):
		return f"Token('{self.token.name}'{f":{self.meta}" if len(self.meta) > 0 and self.meta[0] else ""})"


class TokenGroup:

	def __init__(self, tokens: list, g_name: str = "", g_id: str = ""):
		self.tokens = tokens
		self.name = g_name
		self.id = g_id

		self.__idx = 0

	def __repr__(self):
		return f"TokenGroup({self.tokens})"

	def __str__(self):
		return f"TokenGroup({self.tokens})"

	def __contains__(self, item):
		if isinstance(item, TokenTemplate):
			return item in self.tokens
		elif isinstance(item, Token):
			return item.token in self.tokens

	def __add__(self, other):
		if not isinstance(other, TokenGroup):
			raise errors.UraniumTokenError(f"Cannot add type 'TokenGroup' and {type(other)}")

		return TokenGroup([*self.tokens, *other.tokens])

	def __iter__(self):
		return self

	def __next__(self):
		if self.__idx < len(self.tokens):
			result:Token = self.tokens[self.__idx]
			self.__idx += 1
			return result
		else:
			self.__idx = 0
			raise StopIteration

	def show_as_py(self):
		return "TokenGroup([" + (",".join(map(lambda x: x.show_as_py(), self.tokens))) + f"], g_name = '{self.name}', g_id = '{self.id}')"

	def get(self, id_:str) -> None|TokenTemplate:
		mapped_tokens:list = list(map(lambda tok: tok.id, self.tokens))
		if id_ not in mapped_tokens:
			return None

		return self.tokens[mapped_tokens.index(id_)]
