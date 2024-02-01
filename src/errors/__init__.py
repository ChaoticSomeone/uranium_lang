import sys
from termcolor import colored
from colorama.initialise import just_fix_windows_console
just_fix_windows_console()


class UraniumError(Exception):
	"""
	UraniumError is a thing because it ensures that all classes that inherit from it
	also inherit from Python's builtin Exception
	"""
	def __init__(self, message:str=""):
		print(colored(message, "red"))
		sys.exit(1)


class UraniumTokenError(UraniumError):
	"""
	Occurs during tokenization of the source code
	"""
	def __init__(self, message:str=""):
		super().__init__(message)

class UraniumSyntaxError(UraniumError):
	"""
	Occurs when the parser encounters invalid syntax
	"""
	def __init__(self, message:str=""):
		super().__init__(message)


class UraniumXmlParseError(UraniumError):
	def __init__(self, message:str=""):
		super().__init__(message)
