.INCLUDE "m16def.inc"			; we are using mega16
.DEF cntr=R14
.DEF leds=R15
.DEF mode=R16

.MACRO Delay	
	mov cntr,@0					; parameter passed to cntr
delay_loop:
	cpi cntr,0					; compare cntr with 0
	breq main					; if cntr is 0 then stop delay
	rcall Delay10
	dec cntr					; cntr--
	rjmp delay_loop
.ENDMACRO

start:
	clr mode					; mode = 0x00
	out DDRD,mode				; we set PORTD as input
	dec mode					; mode = 0xFF
	out DDRB,mode				; we set PORTB as output (leds)
	out PORTD,mode				; pull-up enabled (input)

main:
	ser leds					; we will open all leds
	in mode,PIND				; read PORTD
	rol mode					; MSB
	brcs pattern1				; if MSB = 1 use first pattern
	rjmp pattern2				; else use second pattern

pattern1:
	out PORTB,leds				; open leds
	Delay(50)					; wait 0.5 sec
	clr leds					; close leds
	out PORTB,leds
	Delay(150)					; wait 1,5 sec
	rjmp main

pattern 2:
	out PORTB,leds				; open leds
	Delay(150)					; wait 1.5 sec
	clr leds					; close leds
	out PORTB,leds
	Delay(50)					; wait 0,5 sec
	rjmp main
