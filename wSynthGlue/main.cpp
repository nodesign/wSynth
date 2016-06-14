#include <linux/soundcard.h>
#include <unistd.h>
#include <fcntl.h>
#include <stdio.h>
#include <string>
#include <sstream>
#include <iostream>

using namespace std;

int main(void) {
   char* device =  "/dev/midi1" ;
   unsigned char data[3] = {0,0,0};

   // step 1: open the OSS device for writing
   int fd = open(device, O_WRONLY, 0);
   if (fd < 0) {
      printf("Error: cannot open %s\n", device);
      return 1;
   }

    while(true)
    {
        for (string line; getline(cin, line);)
        {
			
			// get string. Example: 144 60 127
			istringstream iss(line);
			// split and convert to int
			int a, b, c;
			iss >> a >> b >> c;
			
			// convert int to char
			data[0] = a;
			data[1] = b;
			data[2] = c;
			
			// print output for debuging
			cout << a << " " << b  << " " << c << endl;

			// step 2: write the MIDI information to the OSS device
			write(fd, data, sizeof(data));
			
        }
    }
	
   return 0;
}

