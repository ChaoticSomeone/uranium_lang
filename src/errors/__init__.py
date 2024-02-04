import sys
from src.debug_logging import Logger

class UraniumError(Exception):
	"""
	UraniumError is a thing because it ensures that all classes that inherit from it
	also inherit from Python's builtin Exception
	"""
	def __init__(self, message:str="", file:str="", pseudo_exit_code:int=1, position:list[int, int, int]=[0, 0, 0], exit_code:int=1):
		Logger.log(f"Error encountered in {file} at {position[0]}:{position[1]}-{position[2]}:", "white")
		Logger.log(message, "red")
		Logger.log(f"Process finished with exit code {pseudo_exit_code}", "light_red")
		sys.exit(exit_code)


class UraniumTokenError(UraniumError):
	"""
	Occurs during tokenization of the source code
	"""
	def __init__(self, message:str="", file:str="", pseudo_exit_code:int=1, position:list[int, int, int]=[0, 0, 0], exit_code:int=1):
		super().__init__(message, file, pseudo_exit_code, position, exit_code)

class UraniumSyntaxError(UraniumError):
	"""
	Occurs when the parser encounters invalid syntax
	"""
	def __init__(self, message:str="", file:str="", pseudo_exit_code:int=1, position:list[int, int, int]=[0, 0, 0], exit_code:int=1):
		super().__init__(message, file, pseudo_exit_code, position, exit_code)


class UraniumXmlParseError(UraniumError):
	def __init__(self, message:str="", file:str="", pseudo_exit_code:int=1, position:list[int, int, int]=[0, 0, 0], exit_code:int=1):
		super().__init__(message, file, pseudo_exit_code, position, exit_code)
