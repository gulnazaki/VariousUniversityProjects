#include <mega16.h>				// mega16 header file

void main(void)
{
	unsigned char A,B,C,D,E,F,X0,X1,X2,temp;

	DDRA = 0xFF;					// PORTA is output
	DDRC = 0;						// PORTC is input
	PORTC = 0xFF;					// enable pull-up for input

	while(1)
	{
		temp = PINC;				// read PORTC
		temp >> 2;					// rotate temp 2 bits right 
		A = temp & 1;				// A is lsb and so on...
		temp >> 1;
		B = temp & 1;
		temp >> 1;		
		C = temp & 1;
		temp >> 1;
		D = temp & 1;
		temp >> 1;
		E = temp & 1;
		temp >> 1;
		F = temp & 1;

		X0 = (A&B) | (C&(~D)&(~E)&F);
		X1 = (A&B&(~C)&D) | ((~D)&E&(~F));
		X2 = X0 | X1;

		X2 << 1;						// shift X2 left
		X2 += X1;						// add X1
		X2 << 1;						// shift left again
		X2 += X0; 						// all 3 bits contained here 

		PORTA = X2;
	}
}