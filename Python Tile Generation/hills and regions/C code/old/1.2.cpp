// step 1 of generation
#include <iostream>
using namespace std;

	int* seed;
	int** seed2 = &seed;
int main ()
{

	cout << *seed2 << "\n";
	return 0;
}