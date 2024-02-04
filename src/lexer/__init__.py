import re
from token_gen import tokens as TokenGroups
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
		Additional token_gen should not require changes to this method
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
				i = 0
				while i < len(TokenGroups.token_group_all.tokens) and remaining:
					tok:TokenTemplate = TokenGroups.token_group_all.tokens[i]

					# obviously ignore all tokens without a pattern
					if not tok.pattern:
						i += 1
						continue
					# check if the current token matches
					if (token_match := re.match("\n" if tok.pattern == r"\n" else fr"{tok.pattern}", remaining)) is not None:
						is_valid = True
						# setting up token properties
						meta = [""]
						group = token_match.group()
						if tok in TokenGroups.u_token_group_literals or tok == TokenGroups.token_group_all.get("identifiers"):
							meta[0] = group

						# create the token
						if tok == TokenGroups.token_group_all.get("identifiers") and group in BuiltIns.LIBS:
							token = Token(TokenGroups.token_group_all.get("std_identifier"), meta)
						else:
							token = Token(tok, meta)

						# extend the token list
						all_tokens.append(token)
						line_idx += len(token_match.group())
						remaining = line[line_idx:]
						break

					i += 1

				if is_valid: continue

				# make sure the lexer doesn't give a fuck about whitespaces
				if (whitespace := re.match(r"\s", remaining)) is not None:
					line_idx += len(whitespace.group())
					remaining = line[line_idx:]
					i += 1
					continue

				# in case unknown token_gen are encountered
				errors.UraniumTokenError(
					f"Encounter unknown token in {self.src_path} at {line_number + 1}:{line_idx + 1}\n" +
					f"Unknown token: {re.match(r"\S*", remaining).group()}"
				)

			line_number += 1

		return all_tokens

