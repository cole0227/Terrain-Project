// This is a mersenne Twister, to reliably generate random numbers.

int MT [624];
int index = 0;

void initializeGenerator(int seed) {
     MT[0] = seed;
     for (int i=1; i<=623;i++) { // loop over each other element
         MT[i] = (1812433253 * (MT[i-1] ^ (MT[i-1] >> 30)) + i); // 0x6c078965
	 MT[i] &= 0xffffffffUL;
     }
 }

// Generate an array of 624 untempered numbers
 void generateNumbers() {
     for (int i=0; i<=623;i++) {
         int y = MT[i];
         y &= 0x80000000UL;
         y |= 0x7fffffffUL & (MT[(i+1) % 624]);
         MT[i] = MT[(i + 397) % 624] ^ (y >> 1);
         if ((y % 2) == 1) { // y is odd
             MT[i] = MT[i] ^ (2567483615); // 0x9908b0df
         }
     }
 }
 
 // Extract a tempered pseudorandom number based on the index-th value,
 // calling generateNumbers() every 624 numbers
 int extractNumber() {
     if (index == 0) {
         generateNumbers();
     }
     
     int y = MT[index];
     y = y ^ ( y >> 11);
     y = y ^ ( y << 7 & (2636928640)); // 0x9d2c5680
     y = y ^ ( y << 15 & (4022730752)); // 0xefc60000
     y = y ^ ( y >> 18);
     
     index = (index + 1) % 624;
     return y;
 }
