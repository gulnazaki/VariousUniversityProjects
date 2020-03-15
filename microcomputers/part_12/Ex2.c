#include <avr/io.h>

unsigned char input, output, f0, f1, f2;
unsigned char abc, cd, d, e, de, dnot_enot;

int main(void) {

	DDRC = 0xff;		// PORTC is set as output		
	PORTC = 0x00;
	DDRA = 0x00;		// PORTA is set as input

	while(1) {
		input = PINA & 0x1f;		// we only need 5 LSBs

		/* calculation of some middle-way results */
		abc = (input & 1) & ((input & 2) >> 1) & ((input & 4) >> 2);	// A*B*C
		cd = ((input & 4) >> 2) & ((input & 8) >> 3);					// C*D
		d = (input & 8) >> 3;											// D
		e = (input & 16) >> 4;											// E		
		de = d & e;														// D*E
		dnot_enot = (!d) & (!e);										// D'*E'

		/* calculation of f0, f1 and f2 */
		f0 = !(abc | cd | de);
		f1 = abc | dnot_enot;
		f2 = f0 | f1;

		/* formation of output */
		output = (f0 << 5) | (f1 << 6) | (f2 << 7);

		/* print output on PORTC */
		PORTC = output;
	}
	return 0;
}
