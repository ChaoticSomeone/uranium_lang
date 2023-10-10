/// Built-in library

#pragma once

#include <random>
#include <string>

namespace Uranium{
	class random{
	public:
		template <typename T>
		static T randint(T min, T max){
			std::random_device rd;
			std::mt19937 gen(rd());
			std::uniform_int_distribution<T> dist(min, max);
			return dist(gen);
		}

		template <typename T>
		static T randfloat(T min, T max){
			std::random_device rd;
			std::mt19937 gen(rd());
			std::uniform_real_distribution<T> dist(min, max);
			return dist(gen);
		}

		static char randchar(bool noWhitespaces=true){
			std::random_device rd;
			std::mt19937 gen(rd());
			std::uniform_int_distribution<char> dist(noWhitespaces ? 33 : 1, 126);
			return dist(gen);
		}

		static std::string randstring(int length, bool noWhitespaces=true){
			std::string ret;
			for (int i = 0; i < length; i++){
				ret += randchar(noWhitespaces);
			}
			return ret;
		}
	};
}