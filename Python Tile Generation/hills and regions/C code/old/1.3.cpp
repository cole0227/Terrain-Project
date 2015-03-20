// step 1 of generation
//;curently generates random numbers from seed consistently
//step 2: simplify the process with a separate file 
#include <iostream>
using namespace std;

	long long unsigned int seed;
	static int seeds[25];
	seeds[0]  = 12345678;
	seeds[1]  = 87654321;
	seeds[2]  = 11111111;
	seeds[3]  = 22222222;
	seeds[4]  = 33333333;
	seeds[5]  = 44444444;
	seeds[6]  = 55555555;
	seeds[7]  = 66666666;
	seeds[8]  = 77777777;
	seeds[9]  = 88888888;
	seeds[10] = 11223344;
	seeds[11] = 55667788;
	seeds[12] = 88776655;
	seeds[13] = 44332211;
	seeds[14] = 11335577;
	seeds[15] = 22446688;
	seeds[16] = 77553311;
	seeds[17] = 88664422;
	seeds[18] = 10000000;
	seeds[19] = 20000000;
	seeds[20] = 30000000;
	seeds[21] = 40000000;
	seeds[22] = 50000000;
	seeds[23] = 60000000;
	seeds[24] = 70000000;
	seeds[25] = 80000000;

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
		if(i%3==0 && temp == 0) temp--;
		i--;
	}
	temp += mod/2 - 1;
	temp %= mod;
	return temp;
}

int SeedShine(int mod)
{
	int temp = SeedMod(SeedPeel(),mod);
	while ((temp + (mod-1)/2)%mod > 0)
	{
		SeedMod(SeedPeel(),mod);
		temp--;
	}
	temp = SeedMod(SeedPeel(),mod);
//	int common = (mod-1)/2;
//	while(temp != common)
//	{
//		temp = SeedMod(SeedPeel(),mod);
//	}
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
	while(i <= 100)
	{
		int rnd = SeedShine(10);
//		cout << rnd << "\n";
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