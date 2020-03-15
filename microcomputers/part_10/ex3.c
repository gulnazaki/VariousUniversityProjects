#include <avr/io.h>

// function that calculates position of input's most significant 1-bit
unsigned char mostsign1 (unsigned char input) {
	if (input & 16)
		return 5;
	else if (input & 8)
		return 4;
	else if (input & 4)
		return 3;
	else if (input & 2)
		return 2;
	else if (input & 1)
		return 1;
	else					// ignore all other bits
		return 0;
}

int main(void) {
	unsigned char msb1, msb2, output;
	DDRA = 0xFF;				// set PortA as output port
	DDRC = 0x00;				// set PortC as input port
	output = 0x80;				// initialize output
	msb1 = mostsign1(PINC);			// read input and save position of most significant 1-bit
	while (1) {
		msb2 = mostsign1(PINC);		// read new input and save position of most significant 1-bit
		// if the switch with the highest priority has been turned off, change output accordingly:
		if (msb2 < msb1) {
			if (msb1 == 5)
				output = 0x80;
			else if (msb1 == 4)
				output = output << 2 | output >> 6;
			else if (msb1 == 3)
				output = output >> 2 | output << 6;
			else if (msb1 == 2)
				output = output << 1 | output >> 7;
			else if (msb1 == 1)
				output = output >> 1 | output << 7;
		}
		msb1 = msb2;
		PORTA = output;			 // change display
	}
	return 0;
}