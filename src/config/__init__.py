import toml
import os


"""
This file will handle compiler settings, until I switch from toml-files to
command line arguments
"""


class Config:
	check_syntax:bool = True
	write_tokens:bool = False
	new_parser:bool = False

	ignore_debug_output:bool = False
	std_lib_path:str = "/"
	reformat_cpp:bool = False
	ignore_timestamp_output:bool = False

	cpp_cmd:str = ""

	@staticmethod
	def read_config():
		with open("config.toml") as config:
			data = toml.load(config)

			dev_config = data["Dev-Settings"]
			Config.check_syntax = dev_config["check-syntax"]
			Config.write_tokens = dev_config["write-tokens"]
			Config.new_parser = dev_config["new-parser"]

			uranium_compiler_config = data["Uranium-Compiler"]
			Config.ignore_debug_output = uranium_compiler_config["no-debug-compiler-output"]
			Config.std_lib_path = os.path.expandvars(uranium_compiler_config["std-lib-path"]).replace("\\", "/")
			Config.reformat_cpp = uranium_compiler_config["reformat-cpp"]
			Config.ignore_timestamp_output = uranium_compiler_config["no-process-times"]

			cpp_compiler_config = data["CPP-Compiler"]
			Config.cpp_cmd = f"{cpp_compiler_config["compiler"]} {cpp_compiler_config["args"]}"
