// step 1 of generation
//;curently generates random numbers from seed consistently
#include <iostream>
using namespace std;

	long long unsigned int seed;
	int lastSeed = 0;


int SeedPeel(void)
{
	lastSeed++;
	return (seed % lastSeed);
}

int SeedMod(int seed,int mod)
{
	int temp = seed;
	int i = 3;
	while(i >= 1)
	{
		temp %= (mod+i);
		//if(i%2==0) temp--;
		i--;
	}
	temp += mod/2 - 1;
	temp %= mod;
	return temp;
}

int main ()
{

	cout << "Seed: ";
	cin >> seed; // Give it n, then generate n-1 numbers :P
	cout << "\n";
	
	int i0 = 0;
	int i1 = 0;
	int i2 = 0;
	int i3 = 0;
	int i4 = 0;
	int i5 = 0;
	int i6 = 0;
	int i7 = 0;
	int i8 = 0;
	int i9 = 0;
	
	int i = 1;
	while(i < 10000)
	{
		int rnd = SeedMod(SeedPeel(),10);
		//cout << rnd << "\n";
		if(rnd == 0) i0++;
		if(rnd == 1) i1++;
		if(rnd == 2) i2++;
		if(rnd == 3) i3++;
		if(rnd == 4) i4++;
		if(rnd == 5) i5++;
		if(rnd == 6) i6++;
		if(rnd == 7) i7++;
		if(rnd == 8) i8++;
		if(rnd == 9) i9++;
		i++;
	}
	
	cout << "key:" << i0 << "\n";
	cout << "key:" << i1 << "\n";
	cout << "key:" << i2 << "\n";
	cout << "key:" << i3 << "\n";
	cout << "key:" << i4 << "\n";
	cout << "key:" << i5 << "\n";
	cout << "key:" << i6 << "\n";
	cout << "key:" << i7 << "\n";
	cout << "key:" << i8 << "\n";
	cout << "key:" << i9 << "\n";

	return 0;
}