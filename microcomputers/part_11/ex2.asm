.include "m16def.inc"
.org 0x0
	rjmp reset
.org 0x2
	rjmp ISR0

reset:
	ldi r26,low(RAMEND)		; initialising stack pointer
	out SPL,r26
	ldi r26,high(RAMEND)
	out SPH,r26

	ser r26				; initialize PORTB
	out DDRB, r26			; and PORTC
	out DDRC, r26			; as outputs

	clr r26				; initialize PORTA
	out DDRA, r26			; as input

	clr r27				; initialize intr counter
	clr r26					; initialize counter

	ldi r24, (1<<ISC01)|(1<<ISC00)
	out MCUCR,r24
	ldi r24, (1<<INT0)		; we enable interruption INT0 only
	out GICR, r24	

	sei				; enable interrupts

count:
	out PORTB, r26			; show counter value
	ldi r24, low(200)		; call wait_msec
	ldi r25, high(200)		; to make program sleep
	rcall wait_msec			; for ~0.2 sec
	inc r26				; increase counter
	rjmp count			; repeat

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

wait_usec:
	sbiw r24,1			; subtracting 1 from r25:r24 (2 cycles)
	nop
	nop
	nop
	nop
	brne wait_usec			; instructions till now take 8 cycles = 1usec
	ret				; if 25:r24 usecs have passed return

;;; interrupt service routine ;;;

ISR0:
	push r26			; store counter
	in r26, SREG			; and SREG
	push r26

debounce0:
	ldi r26, (1<<INTF0)		; prepare debounce check for INT0
	out GIFR, r26			; write 1 to GIFR(6), making it 0
	ldi r24, low(5)
	ldi r25, high(5)
	rcall wait_msec			; wait 5 msecs
	in r26, GIFR			; check if GIFR(6) == 0
	sbrc r26,6			; if it is, serve interrupt
	rjmp debounce0			; else, repeat

	in r26, PINA		; read PORTA
	clr r28				; initialize PORTC display
	ldi r27,8			; set counter = 8

loop:
	lsl r26				; move MSBit of r26 to Carry
	brcc to_next_loop	; if C = 0, go on
	lsl r28				; else shift display left
	inc r28				; and add 1
to_next_loop:
	dec r27
	cpi r27,0			; if counter = 0
	brne loop			; we are done
	
	out PORTC, r28			; display result in PORTC

	pop r26				; restore SREG
	out SREG, r26
	pop r26				; and counter
	reti
