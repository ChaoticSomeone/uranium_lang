from src import lexer, parser, compiler
from src.config import Config
from src.lexer.tokens import print_token_list, TokensEnum
from src.formatter import Formatter
from src.debug_logging import Logger
from src.errors import UraniumError
import os

def init():
	Config.read_config()
	TokensEnum.load_tokens()
	Logger.init()

	if os.environ.get("URANIUM_PATH") is None:
		raise UraniumError("Environment variable 'URANIUM_PATH' does not exist!")

def compile(src:str) -> (compiler.UraniumCompiler, list):
	uranium_lexer = lexer.UraniumLexer(src)
	tokens = uranium_lexer.tokenize()

	uranium_parser = parser.UraniumParser(tokens)
	if Config.check_syntax:
		uranium_parser.check_syntax(src)
	tokens = uranium_parser.rearrange()
	print_token_list(tokens, end="####################\n")

	uranium_compiler = compiler.UraniumCompiler(tokens)
	return uranium_compiler, uranium_compiler.generate_cpp()

def write_output(dest:str, cpp_code:list):
	with open(dest, "w") as output_file:
		with open("template.cpp", "r") as template:
			output_template = template.readlines()
			output_file.writelines(output_template)

		for snippet in cpp_code:
			final_snippet = snippet if snippet in ["\n", ";\n"] else snippet + " "
			output_file.write(final_snippet)

	if Config.reformat_cpp:
		formatter = Formatter(dest)
		with open(dest, "w") as output_file:
			output_file.writelines(formatter.reformat())

if __name__ == '__main__':
	init()
	Logger.timestamp("Init took")

	src_path = "./_in/main.uran"
	uranium_compiler, cpp = compile(src_path)
	Logger.timestamp("Compilation took")

	cpp_path = "./_out/main.cpp"
	write_output(cpp_path, cpp)
	Logger.timestamp("Writing to output took")

	uranium_compiler.compile(cpp_path)
	Logger.timestamp("C++ Compiler took")

	Logger.timestamp("Total time taken:", True)
