.include "m16def.inc"
.org 0

reset:
	ldi r24, low(RAMEND)		; initialising stack pointer
	out SPL, r24
	ldi r24, high(RAMEND)
	out SPH, r24

	ser r26
	out DDRB, r26			; PORTB is output
	clr r26
	out DDRA, r26			; PORTA is input

flash:
	in r26, PINA			; store input in r26
	mov r27, r26			; and r27
	andi r26,0b00001111		; x1 = (PA0-PA3) -> r26
	lsr r27				; x2 = (PA4-PA7) -> r27
	lsr r27
	lsr r27
	lsr r27
	inc r26				; x1 + 1 -> r26
	inc r27				; x2 + 1 -> r27
	ldi r28, 200
	mul r26, r28			; 200 * (x1 + 1) -> r1:r0

	rcall on			; switch LEDS on
	mov r24, r0
	mov r25, r1
	rcall wait_msec			; delay for r1:r0 mseconds

	rcall off			; switch LEDS off
	mul r27, r28			; 200 * (x2 + 1) -> r1:r0
	mov r24, r0
	mov r25, r1
	rcall wait_msec			; delay for r1:r2 mseconds
	rjmp flash			; repeat

on:
	ser r26				; 11111111 -> r26
	out PORTB, r26			; switch LEDS on
	ret

off:
	clr r26				; 00000000 -> r26
	out PORTB, r26			; switch LEDS off
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