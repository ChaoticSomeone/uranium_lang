import os
import re
from src.errors import UraniumXmlParseError
from src.debug_logging import Logger
import xmltodict

def read_xml() -> dict:
	files:list = list(filter(lambda file: file.endswith(".xml"), os.listdir(".")))
	token_files:dict = {file: {} for file in files}

	for file in files:
		with open(file, "rt") as f:
			contents:str = f.read()

		token_files[file] = xmltodict.parse(contents)

	return token_files



import json
token_xml:dict = read_xml()
print(json.dumps(token_xml, indent=4))


