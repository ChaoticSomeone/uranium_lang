#pragma once
#ifndef URAN_BUILTINS_IO_H
#define URAN_BUILTINS_IO_H

#include <iostream>
#include <string>
#include <format>

namespace uranium {
	class io {
	public:
		/**
		 * Prints out some formatted text to stdout
		 * @tparam Args type for arguments for the format placeholders
		 * @param fmt formatted string
		 * @param args arguments for the format placeholders
		 */
		template <typename... Args>
		static void print(std::string_view fmt, Args&&... args) {
			std::cout << std::vformat(fmt, std::make_format_args(args...));
		}

		/**
		 * Prints out some formatted text to stdout with an newline character at the end
		 * @tparam Args type for arguments for the format placeholders
		 * @param fmt formatted string
		 * @param args arguments for the format placeholders
		 */
		template <typename... Args>
		static void println(std::string_view fmt, Args&&... args) {
			std::cout << std::vformat(fmt, std::make_format_args(args...)) << std::endl;
		}

		/**
		 * Gets data from stdin
		 * @tparam T type to be read from stdin
		 * @param prompt prompt to be printed before the output
		 * @return data that was received from stdin
		 */
		template <typename T>
		static T read(std::string prompt="") {
			T input;
			std::cout << prompt;
			std::cin >> input;
			std::cin.clear();
			return input;
		}
	};
}

#endif
