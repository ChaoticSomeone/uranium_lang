import sys
from termcolor import colored
from colorama.initialise import just_fix_windows_console
just_fix_windows_console()

class UraniumError(Exception):
	def __init__(self, message:str=""):
		print(colored(message, "red"))
		sys.exit(1)

class UraniumTokenError(UraniumError):
	def __init__(self, message:str=""):
		super().__init__(message)

class UraniumSyntaxError(UraniumError):
	def __init__(self, message:str=""):
		super().__init__(message)
