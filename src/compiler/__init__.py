import os
from token_gen import tokens as TokenGroups
from src import errors
from src.lexer.tokens import TokenTemplate, Token
from src.config import Config

class UraniumCompiler:
	__has_instance:bool = False

	def __init__(self, all_tokens:list):
		if not UraniumCompiler.__has_instance:
			UraniumCompiler.__has_instance = True
			self.tokens:list = all_tokens

		else:
			errors.UraniumError("Class 'UraniumCompiler' (singleton) can only have one instance")

	# allows to look ahead while iterating token_gen (probably didn't use this often)
	def peek(self, i:int, offset:int) -> Token:
		return self.tokens[i + offset] if i + offset < len(self.tokens) else None


	"""
	This version of generate_cpp, handles token_gen by itself,
	most token_gen added won't change the code of this method
	"""
	def generate_cpp(self) -> list:
		output:list = []
		i = 0
		while i < len(self.tokens):
			token:Token = self.tokens[i]

			# determine if we need a semicolon
			if token == TokenGroups.token_group_all.get("newline"):
				output.append(";\n" if not self.peek(i, - 1) in [TokenGroups.token_group_all.get("l_curly"), TokenGroups.token_group_all.get("std_identifier")] else "\n")
				if self.peek(i, 1) == TokenGroups.token_group_all.get("newline"):
					i += 1

			# token_gen which cannot be expressed by some constant string are handled here
			elif token in TokenGroups.u_token_group_literals or token in [*TokenGroups.u_token_group_identifiers, TokenGroups.token_group_all.get("ex_expr")]:
				output.append(f"{token.meta[0]}")

			# token_gen which can be expressed by a constant string are handled here
			else:
				if isinstance(token, Token):
					output.append(f"{token.token.cpp_translate}")
				elif isinstance(token, TokenTemplate):
					output.append(f"{token.cpp_translate}")

			i += 1

		return output


	def compile(self, cpp_path:str):
		command = f"{Config.cpp_cmd} {cpp_path}"
		os.system(command)
