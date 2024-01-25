from src import errors
from src.lexer.tokens import Token, TokensEnum
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
		return self.tokens[i + offset] if i + offset < len(self.tokens) else None

	def rearrange(self) -> list:
		i = 0

		while i < len(self.tokens):
			match self.tokens[i]:
				# rearrange and discard tokens for function definitions to make them fit with C++ syntax
				case TokensEnum.KW_FUNC:
					if self.tokens[i + 1] == TokensEnum.IDENTIFIER and self.tokens[i + 2] == TokensEnum.SYM_L_PAREN:
						j = 2
						while self.tokens[i + j] != TokensEnum.SYM_R_PAREN:
							if self.tokens[i + j] in TokensEnum.TYPES:
								self.tokens[i + j], self.tokens[i + j - 2] = self.tokens[i + j - 2], self.tokens[i + j]
							j += 1

						offset:int = j
						if self.tokens[i + j + 1] == TokensEnum.SYM_RET_TYPE and self.tokens[i + j + 2] in TokensEnum.TYPES:
							datatype:Token = self.tokens.pop(i + j + 2)
							self.tokens.pop(i + j + 1)
							while self.tokens[i + j] != TokensEnum.KW_FUNC:
								j -= 1
							self.tokens[i + j] = datatype


						elif self.tokens[i + j + 1] == TokensEnum.SYM_L_CURLY_BRACKET:
							datatype:Token = TokensEnum.EXTERNAL_VOID
							while self.tokens[i + j] != TokensEnum.KW_FUNC:
								j -= 1
							self.tokens[i + j] = datatype

						i += offset

				# rearrange and discard tokens for variable assignment to make them fit with C++ syntax
				case TokensEnum.SYM_EQUALS:
					if self.tokens[i - 1] in TokensEnum.TYPES and self.tokens[i - 2] == TokensEnum.SYM_TYPE and self.tokens[i - 3] == TokensEnum.IDENTIFIER:
						self.tokens.insert(i - 3, self.tokens.pop(i - 1))
						self.tokens.pop(i - 1)

				# fix imports
				case TokensEnum.STD_IDENTIFIER:
					if self.tokens[i - 1] == TokensEnum.SYM_NAMESPACE_DELIMITER and self.tokens[i - 2] == TokensEnum.STD_URANIUM and self.tokens[i - 3] == TokensEnum.KW_IMPORT:
						self.tokens[i].meta[0] = f"\"{Config.std_lib_path}/{self.tokens[i].meta[0]}.h\""
						self.tokens.pop(i - 1)
						self.tokens.pop(i - 2)
						i -= 1

					elif self.tokens[i - 1] == TokensEnum.SYM_NAMESPACE_DELIMITER and self.tokens[i - 2] == TokensEnum.STD_URANIUM:
						self.tokens[i].meta[0] = f"uranium::{re.search(r"\w*", self.tokens[i].meta[0]).group()}"
						self.tokens.pop(i - 1)
						self.tokens.pop(i - 2)
						i -= 1


				case TokensEnum.NEWLINE:
					if self.tokens[i - 1] == TokensEnum.NEWLINE:
						self.tokens.pop(i)
						i -= 1

			for composite in TokensEnum.composites2:
				if self.tokens[i] == composite[0] and self.tokens[i + 1] == composite[1]:
					match composite:
						case TokensEnum.OP_EQUALS_COMP:
							self.tokens[i] = TokensEnum.OP_EQUALS
							self.tokens.pop(i + 1)
						case TokensEnum.OP_LESS_EQUALS_COMP:
							self.tokens[i] = TokensEnum.OP_LESS_EQUALS
							self.tokens.pop(i + 1)
						case TokensEnum.OP_GREATER_EQUALS_COMP:
							self.tokens[i] = TokensEnum.OP_GREATER_EQUALS
							self.tokens.pop(i + 1)
						case TokensEnum.OP_NOT_EQUAL_COMP:
							self.tokens[i] = TokensEnum.OP_NOT_EQUAL
							self.tokens.pop(i + 1)

			i += 1


		return self.tokens


	def check_syntax(self, src_path:str):
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
				case TokensEnum.NEWLINE:
					line += 1

				case TokensEnum.KW_FUNC:
					if self.peek(i, 1) != TokensEnum.IDENTIFIER:
						raise errors.UraniumSyntaxError(f"Expected identifier after keyword 'func' in line {line} of file '{src_path}'")

				case TokensEnum.IDENTIFIER:
					# implement error checks
					pass
					#if self.peek(i, 1) not in [TokensEnum.SYM_TYPE, TokensEnum.SYM_L_PAREN, TokensEnum.NEWLINE]:
					#	raise errors.UraniumSyntaxError(f"Expected '(' or ':' after identifier '{token.meta[0]}' in line {line} of file '{src_path}'")

				case TokensEnum.SYM_TYPE:
					if self.peek(i, 1) not in TokensEnum.TYPES:
						raise errors.UraniumSyntaxError(f"Expected datatype after type delimiter ':' in line {line} of file '{src_path}'")

				case TokensEnum.SYM_L_PAREN: parenthese["L_PAREN"] += 1
				case TokensEnum.SYM_R_PAREN: parenthese["R_PAREN"] += 1
				case TokensEnum.SYM_L_CURLY_BRACKET: parenthese["L_CURLY"] += 1
				case TokensEnum.SYM_R_CURLY_BRACKET: parenthese["R_CURLY"] += 1

				case TokensEnum.SYM_RET_TYPE:
					if self.peek(i, 1) not in TokensEnum.TYPES:
						raise errors.UraniumSyntaxError(f"Expected datatype after return type specifier '->' in line {line} of file '{src_path}'")

				case TokensEnum.SYM_EQUALS:
					if self.peek(i, 1) not in TokensEnum.LITERALS and self.peek(i, 1) not in [TokensEnum.STD_URANIUM, TokensEnum.IDENTIFIER, TokensEnum.KW_TRUE, TokensEnum.KW_FALSE, TokensEnum.SYM_PLUS, TokensEnum.SYM_MINUS, TokensEnum.SYM_L_PAREN]:
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


		if parenthese["L_PAREN"] != parenthese["R_PAREN"]:
			raise errors.UraniumSyntaxError(f"Unmatched '(' and ')' in file '{src_path}'")

		if parenthese["L_CURLY"] != parenthese["R_CURLY"]:
			raise errors.UraniumSyntaxError(f"Unmatched '{{' and '}}' in file '{src_path}'")
