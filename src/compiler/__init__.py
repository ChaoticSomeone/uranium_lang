import os

from src import errors
from src.lexer.tokens import _Token, Token, TokensEnum
from src.config import Config

class UraniumCompiler:
	__has_instance:bool = False

	def __init__(self, all_tokens:list):
		if not UraniumCompiler.__has_instance:
			UraniumCompiler.__has_instance = True
			self.tokens:list = all_tokens

		else:
			errors.UraniumError("Class 'UraniumCompiler' (singleton) can only have one instance")

	# allows to look ahead while iterating tokens (probably didn't use this often)
	def peek(self, i:int, offset:int) -> Token:
		return self.tokens[i + offset] if i + offset < len(self.tokens) else None


	"""
	This version of generate_cpp, handles tokens by itself,
	most tokens added won't change the code of this method
	"""
	def generate_cpp(self) -> list:
		output:list = []
		i = 0
		while i < len(self.tokens):
			token:Token = self.tokens[i]

			# determine if we need a semicolon
			if token == TokensEnum.NEWLINE:
				output.append(";\n" if not self.peek(i, - 1) in [TokensEnum.SYM_L_CURLY_BRACKET, TokensEnum.STD_IDENTIFIER] else "\n")
				if self.peek(i, 1) == TokensEnum.NEWLINE:
					i += 1

			# tokens which cannot be expressed by some constant string are handled here
			elif token in TokensEnum.LITERALS or token in [TokensEnum.STD_IDENTIFIER, TokensEnum.IDENTIFIER, TokensEnum.EXTERNAL_EXPR]:
				output.append(f"{token.meta[0]}")

			# tokens which can be expressed by a constant string are handled here
			else:
				if isinstance(token, Token):
					output.append(f"{token.token.cpp_translate}")
				elif isinstance(token, _Token):
					output.append(f"{token.cpp_translate}")

			i += 1

		return output


	def compile(self, cpp_path:str):
		command = f"{Config.cpp_cmd} {cpp_path}"
		os.system(command)
