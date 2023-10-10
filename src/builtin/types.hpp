/// True built-in

#pragma once

#include <iostream>
#include <cmath>
#include <cstdlib>
#include <cstring>

namespace Uranium {

/* sbool ... small boolean
 * Can save up to 8 booleans in one byte */
	class sbool{
	private: char x = 0;

	public:
		sbool(int a=0, int b=0, int c=0, int d=0, int e=0, int f=0, int g=0, int h=0){
			this->x += a << 0;
			this->x += b << 1;
			this->x += c << 2;
			this->x += d << 3;
			this->x += e << 4;
			this->x += f << 5;
			this->x += g << 6;
			this->x += h << 7;
		}

		bool operator[] (size_t idx) const{
			return (bool) (this->x & (char)pow(2, idx));
		}

		static std::string toString(sbool obj){
			std::string s;
			for (int i = 0; i < 8; i++){
				s += '0' + obj[i];
			}
			return s;
		}

		friend std::ostream& operator<< (std::ostream &os, sbool &obj);
	};
	std::ostream& operator<< (std::ostream &os, sbool &obj){
		os << sbool::toString(obj);
		return os;
	}
}