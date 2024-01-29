import toml
import os

class Config:
	check_syntax:bool = True

	ignore_debug_output:bool = False
	std_lib_path:str = "/"
	reformat_cpp:bool = False
	ignore_timestamp_output:bool = False

	cpp_cmd:str = ""

	@staticmethod
	def read_config():
		with open("config.toml") as config:
			data = toml.load(config)

			Config.check_syntax = data["Dev-Settings"]["check-syntax"]

			uranium_compiler_config = data["Uranium-Compiler"]
			Config.ignore_debug_output = uranium_compiler_config["no-debug-compiler-output"]
			Config.std_lib_path = os.path.expandvars(uranium_compiler_config["std-lib-path"]).replace("\\", "/")
			Config.reformat_cpp = uranium_compiler_config["reformat-cpp"]
			Config.ignore_timestamp_output = uranium_compiler_config["no-process-times"]

			cpp_compiler_config = data["CPP-Compiler"]
			Config.cpp_cmd = f"{cpp_compiler_config["compiler"]} {cpp_compiler_config["args"]}"
