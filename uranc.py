from src import lexer, parser, compiler
from src.config import Config
from src.formatter import Formatter
from src.debug_logging import Logger
from src.errors import UraniumError
from token_gen.xml_parser import XmlParser
import os


def init():
	# load all the options from config.toml
	Config.read_config()
	# load the tokens
	XmlParser.generate("u")
	# init. the tokens and logger
	Logger.init()

	# we need the env. variable, thus th error
	if os.environ.get("URANIUM_PATH") is None:
		raise UraniumError("Environment variable 'URANIUM_PATH' does not exist!")

def compile(src:str) -> (compiler.UraniumCompiler, list):
	# generate a list of tokens from the source code
	uranium_lexer = lexer.UraniumLexer(src)
	tokens = uranium_lexer.tokenize()

	# run the parser
	uranium_parser = parser.UraniumParser(tokens)
	if Config.check_syntax:
		uranium_parser.check_syntax(src)
	tokens = uranium_parser.rearrange()

	# generate the final C++ code
	uranium_compiler = compiler.UraniumCompiler(tokens)
	return uranium_compiler, uranium_compiler.generate_cpp()

def write_output(dest:str, cpp_code:list):
	# start writing to output file
	with open(dest, "w") as output_file:
		# load in the template, which we need for the standard libraries
		with open("template.cpp", "r") as template:
			output_template = template.readlines()
			output_file.writelines(output_template)

		# start putting the source code together into a single string
		for snippet in cpp_code:
			final_snippet = snippet if snippet in ["\n", ";\n"] else snippet + " "
			output_file.write(final_snippet)

	# reformat the output if desired
	if Config.reformat_cpp:
		formatter = Formatter(dest)
		with open(dest, "w") as output_file:
			output_file.writelines(formatter.reformat())



if __name__ == '__main__':
	init()
	Logger.timestamp("Init took")

	# run the compiler
	src_path = "./_in/main.uran"

	if Config.new_parser:
		from src.parser.uran_ast import UraniumParser
	else:
		uranium_compiler, cpp = compile(src_path)
		Logger.timestamp("Compilation took")

		# generate some output
		cpp_path = "./_out/main.cpp"
		write_output(cpp_path, cpp)
		Logger.timestamp("Writing to output took")

		# let a C++ compiler finish the compilation
		uranium_compiler.compile(cpp_path)
		Logger.timestamp("C++ Compiler took")

		Logger.timestamp("Total time taken:", True)
