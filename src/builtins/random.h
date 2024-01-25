#pragma once
#ifndef BUILTINS_RANDOM_H
#define BUILTINS_RANDOM_H

#include <random>
#include <string>

namespace uranium {
	class random {
	private:
		/**
		 * Generates a random character
		 * (private method because Uranium Lang has no char type)
		 * @param noWhitespaces can whitespaces be generated?
		 * @return a random ascii character
		 */
		static char randchar(bool noWhitespaces=true) {
			std::random_device rd;
			std::mt19937 gen(rd());
			std::uniform_int_distribution<char> dist(noWhitespaces ? 33 : 1, 126);
			return dist(gen);
		}

	public:
		/**
		 * generates a random integer
		 * @tparam T integer type to be generated
		 * @param min minimal value (inclusive)
		 * @param max maximum value (inclusive)
		 * @return a random integer
		 */
		template <typename T>
		static T randint(T min, T max) {
			std::random_device rd;
			std::mt19937 gen(rd());
			std::uniform_int_distribution<T> dist(min, max);
			return dist(gen);
		}

		/**
		 * generates a random floating-point number
		 * @tparam T floating-point type to be generated
		 * @param min minimal value (inclusive)
		 * @param max maximum value (inclusive)
		 * @return a random float
		 */
		template <typename T>
		static T randfloat(T min, T max) {
			std::random_device rd;
			std::mt19937 gen(rd());
			std::uniform_real_distribution<T> dist(min, max);
			return dist(gen);
		}

		/**
		 * generates a random string
		 * @param length the length of the resulting string
		 * @param noWhitespaces can whitespaces be generated?
		 * @return a random string
		 */
		static std::string randstring(int length, bool noWhitespaces=true) {
			std::string result;
			for (int i = 0; i < length; i++) {
				result += randchar(noWhitespaces);
			}
			return result;
		}

		/**
		 * generates a random boolean value
		 * @return a random boolean
		 */
		static bool randbool() {
			std::random_device rd;
			std::mt19937 gen(rd());
			std::uniform_int_distribution<int> dist(0, 1);
			return (bool) dist(gen);
		}
	};
}
#endif
