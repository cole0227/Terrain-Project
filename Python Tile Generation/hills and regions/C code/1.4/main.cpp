// step 1 of generation
//curently generates random numbers from seed consistently
//step 2: simplify the process with a separate file.
//step 3: figure out how to reset and control the random.
//next step is to start making features logically and repeatably

#include <iostream>
#include "seed.h"
using namespace std;

void GenNums(int num,int max)
{
	int i = 1;
	while(i <= num)
	{
		int rnd = SeedShine(max);
		
		//cout << rnd << "\n";

		
		i++;
	}
	
}

int mountainNum;

void GetNewSeed(void)
{
	long long unsigned int newseed = 7;
	cout << "Seed of the Universe: ";
	cin >> newseed;
	cout << "\n";
	SetSeed(newseed);
}

void AskMountains(void)
{
	mountainNum = SeedShine(2)+2;
	cout << "How many mountains? " << mountainNum << "\n";
}

int main()
{
	//GenNums(30,2);
	
	GetNewSeed();
	
	int i = 100;
	while(i>1)
	{
		AskMountains();
		i--;
	}
	return 0;
}
