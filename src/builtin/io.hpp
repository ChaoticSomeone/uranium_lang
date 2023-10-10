/// Built-in Library

#pragma once

#include <iostream>

namespace Uranium{
	class io{
	public:
		// Function for retrieving an integer from stdin
		static void getInput(int &a, std::string prompt=""){
			std::string buf;
			bool isInt;

			do{
				buf = "";
				isInt = true;

				std::cout << prompt;
				std::cin >> buf;

				for (char c : buf){
					if (!isdigit(c)){
						isInt = false;
						break;
					}
				}
			} while (!isInt);

			a = stoi(buf);
		}

		// Function for retrieving a float from stdin
		static void getInput(float &a, std::string prompt=""){
			std::string buf;
			bool isFloat;
			int dotCount;

			do{
				buf = "";
				isFloat = true;
				dotCount = 0;

				std::cout << prompt;
				std::cin >> buf;

				for (char c : buf){
					if (c == '.'){
						dotCount++;
					}
					else if (!isdigit(c)){
						isFloat = false;
						break;
					}

					if (dotCount > 1){
						isFloat = false;
						break;
					}
				}
			} while (!isFloat);

			a = stof(buf);
		}

		// Function for retrieving a bool from stdin
		static void getInput(bool &a, std::string prompt=""){
			std::string buf;
			do{
				buf = "";

				std::cout << prompt;
				std::cin >> buf;
			} while (buf != "true" && buf != "false" && buf != "1" && buf != "0");

			a = buf == "true" || buf == "1";
		}

		// Function for retrieving a char from stdin
		static void getInput(char &a, std::string prompt=""){
			std::string buf;
			do{
				buf = "";

				std::cout << prompt;
				std::cin >> buf;
			} while (buf.length() != 1);

			a = buf[0];
		}

		// Function for retrieving a string from stdin
		static void getInput(std::string &a, std::string prompt=""){
			std::string buf;
			std::cout << prompt;
			getline(std::cin, buf);
			a = buf;
		}


		// prints to stdin
		template <typename T>
		static void print(T fmt){
			std::cout << fmt;
		}

		// prints to stdin with a newline character at the end
		template <typename T>
		static void println(T fmt){
			std::cout << fmt << std::endl;
		}
	};
}