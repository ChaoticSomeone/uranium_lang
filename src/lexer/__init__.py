import re

from src import errors
from src.lexer.tokens import *
from src.builtins import BuiltIns

class UraniumLexer:
	__has_instance = False

	def __init__(self, src_filepath:str):
		if not UraniumLexer.__has_instance:
			UraniumLexer.__has_instance = True

			self.src_path = src_filepath
			with open(src_filepath, "r") as source_file:
				self.src = source_file.readlines()

		else:
			raise errors.UraniumError("Class 'UraniumLexer' (singleton) can only have one instance")


	def tokenize(self) -> list:
		"""
		This method is able to tokenize the source code autonomous.
		Additional tokens should not require changes to this method
		"""
		all_tokens = []

		line_number = 0
		while line_number < len(self.src):
			# extract the relevant contents of the current line
			line = self.src[line_number]
			newline_tmp = re.search(r"\n$", line) is not None
			line = line.strip()  # make sure we don't have leading and trailing whitespaces
			line += "\n" if newline_tmp else ""
			line_idx = 0
			while line_idx < len(line):
				# extract the part of the line, that we still need to iterate over
				remaining = line[line_idx:]
				is_valid = False

				# ignore all characters in a single-line-comment
				if (comment := re.match(r"//.*", remaining)) is not None:
					line_idx += len(comment.group())
					remaining = line[line_idx:]

				# generate appropriate tokens and add metadata if needed
				for tok in TokensEnum.ALL_TOKENS:
					# check if the current token matches
					if (token_match := re.match(tok.pattern, remaining)) is not None:
						# setting up token properties
						meta = [""]
						group = token_match.group()
						if tok in TokensEnum.LITERALS or tok == TokensEnum.IDENTIFIER:
							meta[0] = group

						# create the token
						if tok == TokensEnum.IDENTIFIER and group in BuiltIns.LIBS:
							token = Token(TokensEnum.STD_IDENTIFIER, meta)
						else:
							token = Token(tok, meta)

						# extend the tokens list
						all_tokens.append(token)
						line_idx += len(token_match.group())
						remaining = line[line_idx:]
						is_valid = True
						break

				if is_valid: continue

				# make sure the lexer doesn't give a fuck about whitespaces
				if (whitespace := re.match(r"\s", remaining)) is not None:
					line_idx += len(whitespace.group())
					continue

				# in case unknown tokens are encountered
				errors.UraniumTokenError(
					f"Encounter unknown token in {self.src_path} at {line_number + 1}:{line_idx + 1}\n" +
					f"Unknown token: {re.match(r"\S*", remaining).group()}"
				)

			line_number += 1

		return all_tokens

