#include <iostream>

using namespace std;

int main (int argc,char* argv[])
{
	float Dividend = 1.0;
	cout << "Dividend: ";
	cin >> Dividend;
	
	float Divisor = 1.0;
	cout << "Divisor: ";
	cin >> Divisor;
	
	float Result = (Dividend / Divisor);
	cout << Result << endl;
	
	//char StopCharacter;
	//cout << endl << "press a key adn Enter:";
	//cin >> StopCharacter;
	return 0;
}