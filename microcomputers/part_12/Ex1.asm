.include "m16def.inc"

.def temp = r26
.def input = r27
.def ANDin = r28
.def output = r29

reset:
	ldi temp,low(RAMEND)				; initialise stack pointer
	out SPL,temp
	ldi temp,high(RAMEND)
	out SPH,temp

	ser temp					; PORTB = output
	out DDRB,temp
	clr temp					; PORTA, PORTC = input
	out DDRA,temp
	out DDRC,temp

main:
	in input,PINA					; read dip switches
	rcall make_output
	in input,PINC					; read PC0-7 and reverse PB0-7 accordingly (XOR)				
	eor output,input
	out PORTB,output				; open leds
	rjmp main

make_output:
	mov temp,input					; read input
	lsr input					; shift right
	eor temp,input					; xor and store at temp
	andi temp,1					; we keep only the lsb (logic xor of PA0 and PA1)
	mov ANDin,temp					; keep it as AND input for later

	lsr input					; shift right to keep the next lsb every time
	mov temp,input
	lsr input
	or temp,input					; logic OR
	andi temp,1					; we care only about PA2 and PA3
	and ANDin,temp					; AND with previous input
	mov output,ANDin				; store as output
	lsl temp					; shift left and append with OR
	or output,temp

	lsr input
	mov temp,input
	lsr input
	or temp,input					; logic OR and com meaning NOR
	com temp
	andi temp,1
	lsl temp					; shift left twice to make it PB2
	lsl temp
	or output,temp

	lsr input
	mov temp,input
	lsr input
	eor temp,input					; logic XOR and com meaning NXOR
	com temp
	andi temp,1
	lsl temp					; we store output at PB3
	lsl temp
	lsl temp
	or output,temp

	ret
