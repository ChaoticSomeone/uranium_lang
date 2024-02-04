import os
from typing import Literal
import xmltodict
from src.errors import UraniumXmlParseError
from src.lexer.tokens import TokenGroup, Token, TokenTemplate

class XmlParser:

	@staticmethod
	def read_xml() -> dict:
		files:list = list(filter(lambda file: file.endswith(".xml"), os.listdir("./token_gen/")))
		token_files:dict = {file: {} for file in files}

		for file in files:
			with open("./token_gen/" + file, "rt") as f:
				contents:str = f.read()

			token_files[file] = xmltodict.parse(contents)

		return token_files

	@staticmethod
	def get_token_property(token_element:dict, key:str) -> str:
		return "" if token_element is None or token_element.get(key) is None or token_element.get(key) == '""' else token_element.get(key)

	@staticmethod
	def get_token_group(root, group:str) -> (str, str, list):
		xml: dict = root.get(group)

		# get all fields and check for a bit of validity
		token_group: dict = xml.get("TokenGroup")
		if token_group is None:
			raise UraniumXmlParseError("Missing root tag 'TokenGroup'")

		g_id: str = token_group.get("@Id")
		if g_id is None:
			raise UraniumXmlParseError("Missing required attribute 'Id' in TokenGroup tag")

		g_name: str = token_group.get("@Name")
		if g_name is None:
			raise UraniumXmlParseError("Missing required attribute 'Name' in TokenGroup tag")

		tokens: list = token_group.get("Token")
		if tokens is None:
			tokens = []

		# generate token_gen
		tokens_of_group: list = []

		for tok in tokens:
			new_token: TokenTemplate = TokenTemplate(
				pattern = XmlParser.get_token_property(tok, "Pattern"),
				cpp_translate = XmlParser.get_token_property(tok.get("Translations"), "CPP"),
				name = XmlParser.get_token_property(tok, "@Name"),
				_id = XmlParser.get_token_property(tok, "@Id")
			)
			tokens_of_group.append(new_token)

		return g_id, g_name, tokens_of_group


	@staticmethod
	def generate(xml_type:Literal["u", "x"]):
		# read the xml file and turn it into a dict
		token_xml:dict = XmlParser.read_xml()

		# store all token_gen and token groups
		all_tokens:list = []
		groups:list = []
		for key in token_xml:
			group_id, group_name, group_tokens = XmlParser.get_token_group(token_xml, key)
			groups.append(TokenGroup(group_tokens, group_name, group_id))
			all_tokens.extend(group_tokens)

		# write everything to a python file for use later
		with open("token_gen/tokens.py", "wt") as f:
			all_groups:str = ""
			content:str = "# This file is generated dynamically during installation, thus no quality assurance can be made\n# !! Please leave this file unchanged !!\n"
			content += "from src.lexer.tokens import Token, TokenGroup, TokenTemplate\n"
			for g in groups:
				name:str = f"{xml_type}_token_group_{g.id}"
				content += f"{name} = {g.show_as_py()}\n"
				all_groups += f"{name} + "
			content += f"token_group_all = {all_groups[:-2]}\ntoken_group_all.name = 'All'\ntoken_group_all.id = 'all'\n"
			f.write(content)

