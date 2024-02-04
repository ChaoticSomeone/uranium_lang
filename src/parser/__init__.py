from token_gen import tokens as TokenGroups

from src import errors
from src.lexer.tokens import Token, TokenTemplate
from src.config import Config
import re

class UraniumParser:
	__has_instance = False

	def __init__(self, all_tokens:list):
		if not UraniumParser.__has_instance:
			UraniumParser.__has_instance = True
			self.tokens = all_tokens

		else:
			errors.UraniumError("Class 'UraniumParser' (singleton) can only have one instance")

	def peek(self, i:int, offset:int) -> Token:
		"""
		Probably never used this in the codebase, a shame.
		Anyway, looks ahead in the token_gen list
		"""
		return self.tokens[i + offset] if i + offset < len(self.tokens) else None

	def rearrange(self) -> list:
		"""
		I would rather not explain this method.
		It rearranges the token_gen to make the transition to C++ easier, besides that I expect you
		to ignore the wizardry performed here.
		"""
		i = 0
		while i < len(self.tokens):
			tok:Token = self.tokens[i]
			# rearrange and discard token_gen for function definitions to make them fit with C++ syntax
			if tok == TokenGroups.token_group_all.get("func"):
				if self.tokens[i + 1] == TokenGroups.token_group_all.get("identifiers") and self.tokens[i + 2] == TokenGroups.token_group_all.get("l_paren"):
					j = 2
					while self.tokens[i + j] != TokenGroups.token_group_all.get("r_paren"):
						if self.tokens[i + j] in TokenGroups.u_token_group_datatypes:
							self.tokens[i + j], self.tokens[i + j - 2] = self.tokens[i + j - 2], self.tokens[i + j]
						j += 1

					offset: int = j
					if self.tokens[i + j + 1] == TokenGroups.token_group_all.get("ret_type") and self.tokens[i + j + 2] in TokenGroups.u_token_group_datatypes:
						datatype: Token = self.tokens.pop(i + j + 2)
						self.tokens.pop(i + j + 1)
						while self.tokens[i + j] != TokenGroups.token_group_all.get("func"):
							j -= 1
						self.tokens[i + j] = datatype


					elif self.tokens[i + j + 1] == TokenGroups.token_group_all.get("l_curly"):
						datatype: Token = TokenGroups.token_group_all.get("void")
						while self.tokens[i + j] != TokenGroups.token_group_all.get("func"):
							j -= 1
						self.tokens[i + j] = datatype

					i += offset

			# rearrange and discard token_gen for variable assignment to make them fit with C++ syntax
			elif tok == TokenGroups.token_group_all.get("equals"):
				if self.tokens[i - 1] in TokenGroups.u_token_group_datatypes and self.tokens[i - 2] == TokenGroups.token_group_all.get("type") and self.tokens[i - 3] == TokenGroups.token_group_all.get("identifiers"):
					self.tokens.insert(i - 3, self.tokens.pop(i - 1))
					self.tokens.pop(i - 1)

			# fix imports
			elif tok == TokenGroups.token_group_all.get("std_identifier"):
				if self.tokens[i - 1] == TokenGroups.token_group_all.get("namespace_delimiter") and self.tokens[i - 2] == TokenGroups.token_group_all.get("std_uranium") and self.tokens[i - 3] == TokenGroups.token_group_all.get("import"):
					self.tokens[i].meta[0] = f"\"{Config.std_lib_path}/{self.tokens[i].meta[0]}.h\""
					self.tokens.pop(i - 1)
					self.tokens.pop(i - 2)
					i -= 1

				elif self.tokens[i - 1] == TokenGroups.token_group_all.get("namespace_delimiter") and self.tokens[i - 2] == TokenGroups.token_group_all.get("std_uranium"):
					self.tokens[i].meta[0] = f"uranium::{re.search(r"\w*", self.tokens[i].meta[0]).group()}"
					self.tokens.pop(i - 1)
					self.tokens.pop(i - 2)
					i -= 1

			# fix if statements
			elif tok == TokenGroups.token_group_all.get("if"):
				self.tokens.insert(i + 1, Token(TokenGroups.token_group_all.get("l_paren")))
				j = 0
				while self.tokens[i + j] != TokenGroups.token_group_all.get("newline"):
					j += 1
				self.tokens.insert(i + j - 1, Token(TokenGroups.token_group_all.get("r_paren")))

			elif tok == TokenGroups.token_group_all.get("else_if"):
				self.tokens.insert(i + 1, Token(TokenGroups.token_group_all.get("l_paren")))
				j = 0
				while self.tokens[i + j] != TokenGroups.token_group_all.get("newline"):
					j += 1
				self.tokens.insert(i + j - 1, Token(TokenGroups.token_group_all.get("r_paren")))

			elif tok == TokenGroups.token_group_all.get("while"):
				self.tokens.insert(i + 1, Token(TokenGroups.token_group_all.get("l_paren")))
				j = 0
				while self.tokens[i + j] != TokenGroups.token_group_all.get("newline"):
					j += 1
				self.tokens.insert(i + j - 1, Token(TokenGroups.token_group_all.get("r_paren")))

			elif tok == TokenGroups.token_group_all.get("for"):
				# @ToDo
				self.tokens.insert(i + 1, Token(TokenGroups.token_group_all.get("l_paren")))
				j = 0
				while self.tokens[i + j] != TokenGroups.token_group_all.get("newline"):
					j += 1
				self.tokens.insert(i + j - 1, Token(TokenGroups.token_group_all.get("r_paren")))

				j = 0
				commas: int = 0
				iterator: Token | None = None
				while self.tokens[i + j] != TokenGroups.token_group_all.get("r_paren"):
					if commas == 0 and self.tokens[i + j] == TokenGroups.token_group_all.get("identifiers"):
						iterator = self.tokens[i + j]
					if commas == 2:
						meta: str = self.tokens[i + j].meta
						self.tokens[i + j] = Token(TokenGroups.token_group_all.get("ex_expr"))
						self.tokens[i + j].meta = [f"{iterator.meta[0]} += {meta[0]}"]

					if self.tokens[i + j] == TokenGroups.token_group_all.get("comma"):
						self.tokens[i + j] = Token(TokenGroups.token_group_all.get("semicolon"))
						commas += 1
					j += 1


			elif tok == TokenGroups.token_group_all.get("newline"):
				if self.tokens[i - 1] == TokenGroups.token_group_all.get("newline"):
					self.tokens.pop(i)
					i -= 1

			i += 1


		return self.tokens


	def check_syntax(self, src_path:str):
		"""
		@ToDo
		Roughly, very roughly check the validity of the syntax.
		I know, I know that I should get this fixed, but I have my
		priorities else where
		"""

		if Config.write_tokens:
			with open("tokens_log.txt", "w") as f:
				f.write("\n".join(map(lambda tok: str(tok), self.tokens)))
		'''
		parenthese:dict = {
			"L_PAREN": 0,
			"R_PAREN": 0,
			"L_CURLY": 0,
			"R_CURLY": 0
		}

		line = 1
		i = 0
		while i < len(self.tokens):
			token = self.tokens[i]
			match token:
				case TokenGroups.token_group_all.get("newling"):
					line += 1

				case TokenGroups.token_group_all.get("func"):
					if self.peek(i, 1) != TokenGroups.token_group_all.get("identifiers"):
						raise errors.UraniumSyntaxError(f"Expected identifier after keyword 'func' in line {line} of file '{src_path}'")

				case TokenGroups.token_group_all.get("identifiers"):
					# implement error checks
					pass

				case TokenGroups.token_group_all.get("type"):
					if self.peek(i, 1) not in TokenGroups.u_token_group_datatypes:
						raise errors.UraniumSyntaxError(f"Expected datatype after type delimiter ':' in line {line} of file '{src_path}'")

				case TokenGroups.token_group_all.get("l_paren"): parenthese["L_PAREN"] += 1
				case TokenGroups.token_group_all.get("r_paren"): parenthese["R_PAREN"] += 1
				case TokenGroups.token_group_all.get("l_curly"): parenthese["L_CURLY"] += 1
				case TokenGroups.token_group_all.get("r_curly"): parenthese["R_CURLY"] += 1

				case TokenGroups.token_group_all.get("ret_type"):
					if self.peek(i, 1) not in TokenGroups.u_token_group_datatypes:
						raise errors.UraniumSyntaxError(f"Expected datatype after return type specifier '->' in line {line} of file '{src_path}'")

				case TokenGroups.token_group_all.get("equals"):
					if self.peek(i, 1) not in TokenGroups.u_token_group_literals and self.peek(i, 1) not in [TokensEnum.STD_URANIUM, TokensEnum.IDENTIFIER, TokensEnum.KW_TRUE, TokensEnum.KW_FALSE, TokensEnum.SYM_PLUS, TokensEnum.SYM_MINUS, TokensEnum.SYM_L_PAREN, TokensEnum.SYM_EQUALS]:
						raise errors.UraniumSyntaxError(f"Expected identifier or literal after '=' in line {line} of file '{src_path}'")

				case TokensEnum.STD_URANIUM:
					if self.peek(i, 1) != TokensEnum.SYM_NAMESPACE_DELIMITER or self.peek(i, 2) != TokensEnum.STD_IDENTIFIER:
						raise errors.UraniumSyntaxError(f"Expected '::' and standard library after namespace 'uranium' in line {line} of file '{src_path}'")

				case TokensEnum.STD_IDENTIFIER:
					if self.peek(i, 1) not in [TokensEnum.SYM_DOT, TokensEnum.NEWLINE]:
						raise errors.UraniumSyntaxError(f"Expected '.' after standard library '{token.meta[0]}' in line {line} of file '{src_path}'")

				case TokensEnum.SYM_DOT:
					if self.peek(i, 1) != TokensEnum.IDENTIFIER:
						raise errors.UraniumSyntaxError(f"Expected identifier after '.' in line {line} of file '{src_path}'")

				case TokensEnum.KW_RETURN:
					if self.peek(i, 1) not in [TokensEnum.IDENTIFIER] and self.peek(i, 1) not in TokensEnum.LITERALS:
						raise errors.UraniumSyntaxError(f"Expected identifier or literal after keyword 'return' in line {line} of file '{src_path}'")

				case _:
					if token in TokensEnum.TYPES:
						if self.peek(i, 1) not in [TokensEnum.SYM_L_CURLY_BRACKET, TokensEnum.SYM_EQUALS, TokensEnum.SYM_COMMA, TokensEnum.SYM_R_PAREN]:
							raise errors.UraniumSyntaxError(f"Expected '{{', '=', ',' or ')' after datatype in line {line} of file '{src_path}'")

					elif token in TokensEnum.LITERALS or token in [TokensEnum.KW_FALSE, TokensEnum.KW_TRUE]:
						# implement checks for literals some time
						pass

			i += 1

		'''
		#if parenthese["L_PAREN"] != parenthese["R_PAREN"]:
		#	raise errors.UraniumSyntaxError(f"Unmatched '(' and ')' in file '{src_path}'")

		#if parenthese["L_CURLY"] != parenthese["R_CURLY"]:
		#	raise errors.UraniumSyntaxError(f"Unmatched '{{' and '}}' in file '{src_path}'")
