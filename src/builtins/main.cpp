#include "io.h"

int main() {
	std::string a = uranium::io::read<std::string>(">>");
	uranium::io::println("{}", a);
    return 0;
}
