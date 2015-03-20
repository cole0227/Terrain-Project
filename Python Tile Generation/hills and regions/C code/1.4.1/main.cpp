// step 1 of generation
//curently generates random numbers from seed consistently
//step 2: simplify the process with a separate file.
//step 3: figure out how to reset and control the random.
//step 4: is to start making features logically and repeatably

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

void Mountains(void)
{
	mountainNum = SeedShine(2)+2;
	cout << "How many mountains? " << mountainNum << "\n";
	//radius should vary between 200 and 500 meters
	//height will be automatically determined by radius
	//and steepness in that area
	//I will soon have to decide if this is for 2d or 3d
	//or not, If I am careful.
	//define everything in meters, and hope for the best.
	//the map must be divided into 900m square, with each 
	//square knowing the height of its center, and the 
	//slope of the area around.
	//slope is at this stage fairly small, no more than 
	//land tends to rise and fall, so 15 degrees maximum.
	//then pick a direction at random for the slope.
	//after three levels of this at 900, 200, and 44
	//meters should give a fair amount of play.
	//this forms the basis for a water table covering a
	//specific percentage of the map between 30 and 50.
	//it could be forced to form an island, by adding a
	//hemispherical layer to the process.
	//mountains and hills use the slope of nearby areas to
	//find the rate at which they should modify the terrain
	//map with their hillyness.
	
}

int main()
{
	//GenNums(30,2);
	
	GetNewSeed();
	
	int i = 100;
	while(i>1)
	{
		Mountains();
		i--;
	}
	return 0;
}
