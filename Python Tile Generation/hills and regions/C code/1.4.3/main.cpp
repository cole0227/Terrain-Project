// step 1 of generation
//curently generates random numbers from seed consistently	DONE
//step 2: simplify the process with a separate file.		DONE
//step 3: figure out how to reset and control the random.	-ISH
//step 4: is to start making features logically and repeatably	
//
//need mersenne twister to generate the new random.		DONE
//also need a matrix of pointers leading to points in 3-space.	DONE
// to generate fractal terrain by random midpoint displacement,	DONE
// but with non-static major gridlines and variations in both z	TODO
// and up to the width of one NEW grid tile in any direction.	TODO
//output terrain in easy-to-visualize manner			TODO
//figure out how to drop to terrain despite bat-shit crazy 	TODO
// algorithms 

#include <iostream>
#include "mersenne.h"
#include <cmath>
using namespace std;

void MersenneTest(int maximum, int iterations)
{
	int num = 125;
	//cout << "seed: ";
	//cin >> num;
	Minit(num);

	int k1=0;
	int k2=0;
	int k3=0;
	int k4=0;
	//cout << "0%\n";
	for (int i = 1; i <= iterations;i++)
	{
		int j = Mget(maximum);
		//if (i%((int)(iterations*0.05))==0) cout << (i/(iterations*0.01)) << "%\n";
		//cout << j << " ";
		if      (j<(maximum*0.25)) k1++;
		else if (j<(maximum*0.5)) k2++;
		else if (j<(maximum*0.75)) k3++;
		else k4++;
	}
	//cout << "100%\n";
	cout << k1 << ":" << k2 << ":" << k3 << ":" << k4 << "\n";
}

void Grid()
{
	const int size = 65;
	//needs to be in format 2^n+1

	int num = 0;
	cout << "Seed: ";
	cin >> num;
	Minit(num);
	
	struct point
	{double x;
	 double y;
	 double z;};
	 
	double map[size][size];
	//main loop for terrain generation follows
	for(int level=size-1; level>0; level/=2 )
	//level of detail at which I am working 2^level
	{
		for( int x1=0; x1<size ; x1+=level )//east-west
		{
			for( int y1=0; y1<size ; y1+=level )// North-south
			{
				double z1 = (Mget(90)+10);
				z1 += 0.4*(level+1-size);
				//z1 += (Mget(90)+10)*(level)/(size-1); //smooth as a baby's bottom
				//z1 /= 2;
				//was done last round or this is the first round
				if(level==size-1)
				{
					map[x1][y1] = z1;
					//cout << map[x1][y1] << "A ";
				} else if( (x1%(2*level)!=0 && y1%(2*level)!=0) )
				{
					z1 += (	map[x1-level][y1-level] + map[x1+level][y1-level] +
						map[x1-level][y1+level] + map[x1+level][y1+level] ) / 4;
					map[x1][y1] = z1;
					//cout << (int)map[x1][y1] << "B ";
				} else if( x1%(2*level)!= 0 )
				{
					z1 += ( map[x1-level][y1] + map[x1+level][y1] )/2 ;
					map[x1][y1] = z1;
					//cout << (int)map[x1][y1] << "C ";
				} else if( y1%(2*level)!= 0 )
				{
					z1 += ( map[x1][y1-level] + map[x1][y1+level] )/2 ;
					map[x1][y1] = z1;
					//cout << (int)map[x1][y1] << "D ";
					//cout << map[x1][y1-level] << " " << map[x1][y1+level] << " " << level << "\n";
				} else {
					//cout << "..E ";
				}
				//cout << "[" << x1 << "," << y1 << "]";
			}
			//cout << "\n";
		}
		//cout << "\n";
	}
	
	//trys to level things off
	int z = 0;
	for (int x=1;x<size-1;x++)
	{
		for (int y=1;y<size-1;y++)
		{
			if(map[x][y] < map[x][y+1] && map[x][y] < map[x][y-1] &&
			   map[x][y] < map[x+1][y] && map[x][y] < map[x-1][y]) {
			   	z++;
			   	if ((int)map[x][y]%2==0) {
			   		map[x][y]=map[x-1][y];
			   	} else {
			   		map[x][y]=map[x][y-1];
			   	}
			   }
			//cout << (int)map[x][y] << " ";
		}
		//cout << "\n";
	}
	//cout << "\n";
	for (int x=0;x<size;x++)
	{
		for (int y=0;y<size;y++)
		{
			cout << (int)map[x][y] << " ";
		}
		cout << "\n";
	}
	cout << "\n";
	for (int x=0;x<size;x++)
	{
		for (int y=0;y<size;y++)
		{
			if        (map[x][y]>200){
				cout << "4";
			} else if (map[x][y]>150){
				cout << "3";
			} else if (map[x][y]>100){
				cout << "2";
			} else if (map[x][y]>50){
				cout << "1";
			} else {
				cout << "0";
			}
		}
		cout << "\n";
	}
	cout << "Minima Removed:" << z << "\n";
}

void BasicMersenneTest()
{
	Minit(6);
	int i = 0;
	while (i < 1500) {cout << Mget(10) << " "; i++; }
}

int main()
{
	//MersenneTest(10,1000000);
	//MersenneTest(100,1000000);
	//MersenneTest(1000,1000000);
	//BasicMersenneTest();
	Grid();
	return 0;
}
