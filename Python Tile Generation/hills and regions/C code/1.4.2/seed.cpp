#include <stdlib.h>

long long unsigned int seed = rand();

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
	
	return temp+1;
}

void SetSeed(long long unsigned int newSeed)
{
	seed = newSeed;
}

long long unsigned int GetSeed(void)
{
	return seed;
}
void ResetSeed(void)
{
	seed = rand();
}