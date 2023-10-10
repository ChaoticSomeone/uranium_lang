#include "io.hpp"
#include "types.hpp"
#include "random.hpp"
#include <any>

int main(){
	std::any a = std::any();
	a.emplace<Uranium::sbool>(Uranium::sbool{1,0,1});
	std::cout << Uranium::sbool::toString(std::any_cast<Uranium::sbool>(a));
	return 0;
}