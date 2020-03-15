.include "m16def.inc"
.org 0

reset:
	ldi r24,low(RAMEND)		; initialising stack pointer
	out SPL,r24
	ldi r24,high(RAMEND)
	out SPH,r24

	ser r26				; we will use port B as output
	out DDRB,r26

	clr r26				; and port A as input
	out DDRA,r26

	ldi r26,1			; load 0b00000001 to r26

go_left:
	rcall allowed			; checks if PA0 button is pressed and only then LED moves
	out PORTB, r26			; if pressed display our bit
	ldi r24, low(500)
	ldi r25, high(500)
	rcall wait_msec			; wait 0.5 sec
	lsl r26				; shift left our bit ("moving" to the left)
	sbrs r26,7			; if MSB is on (LED goes all the way left) go right
	rjmp go_left

go_right:
	rcall allowed			; checks if PA0 button is pressed and only then LED moves
	out PORTB, r26			; if pressed display our bit
	ldi r24, low(500)
	ldi r25, high(500)
	rcall wait_msec			; wait 0.5 sec
	lsr r26				; shift right our bit ("moving" to the right)
	sbrs r26,0			; if LSB is on (LED goes all the way right) go left
	rjmp go_right
	rjmp go_left

allowed:
	in r27,PINA			; r27 <- input
	sbrs r27,0			; if PA0 is pressed go to return and continue / else loop there
	rjmp allowed
	ret

wait_usec:
	sbiw r24,1			; subtracting 1 from r25:r24 (2 cycles)
	nop
	nop
	nop
	nop
	brne wait_usec			; instructions till now take 8 cycles = 1usec
	ret				; if 25:r24 usecs have passed return
wait_msec:
	push r24			; pushing r25:r24 in stack / all instructions take 1msec=1000usec
	push r25
	ldi r24, low(998)
	ldi r25, high(998)
	rcall wait_usec
	pop r25				; poping r25:r24
	pop r24
	sbiw r24,1			; subtract 1 from delay in msecs
	brne wait_msec
	ret				; if we are finished return