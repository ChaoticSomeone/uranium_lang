import time
from termcolor import colored
from colorama.initialise import just_fix_windows_console
from src.config import Config
just_fix_windows_console()

class Logger:
	_t1:float = 0
	_t2:float = 0
	_tt1:float = 0

	@staticmethod
	def init():
		Logger._t1 = time.time()
		Logger._tt1 = Logger._t1

	@staticmethod
	def timestamp(message:str="", use_total_time:bool=False):
		if message:
			if not Config.ignore_timestamp_output:
				Logger._t2 = time.time()
				dt:float = Logger._t2 - (Logger._tt1 if use_total_time else Logger._t1)
				print(colored(f"{message} {dt:.5f} seconds", "green" if dt < 3 else "red"))
				Logger._t1 = Logger._t2

	@staticmethod
	def log(message:str="", fg:str="white", bg:str="on_black"):
		if message:
			print(colored(message, fg, bg))

