from src.config import Config
from src import errors

class Formatter:
	"""
	This formatter is so flawed, that I won't even bother to explain
	"""


	__has_instance = False

	def __init__(self, cpp_path:str):
		if not Formatter.__has_instance:
			Formatter.__has_instance = True

			self.cpp_path = cpp_path
			with open(cpp_path, "r") as source_file:
				self.cpp = source_file.readlines()

		else:
			raise errors.UraniumError("Class 'Formatter' (singleton) can only have one instance")

	def reformat(self, indent_size:int=4) -> list:
		i = 0
		indent = 0

		while i < len(self.cpp):
			line:str = self.cpp[i]

			if "{" in line and not "}" in line:
				i += 1
				indent += indent_size
				continue

			elif "}" in line and not "{" in line:
				indent -= indent_size

			self.cpp[i] = f"{" " * indent}{self.cpp[i]}"
			i += 1

		return self.cpp
