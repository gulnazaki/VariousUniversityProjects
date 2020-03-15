.include "m16def.inc"
.org 0x0
	rjmp reset
.org 0x4
	rjmp ISR1
.org 0x10
	rjmp ISR_TIMER1_OVF

reset:
	ldi r26,low(RAMEND)		; initialising stack pointer
	out SPL,r26
	ldi r26,high(RAMEND)
	out SPH,r26

	ser r26				; initialize PORTB
	out DDRB, r26			; as output

	clr r26				; initialize PORTA
	out DDRA, r26			; as input

	ldi r24, (1<<ISC11)|(1<<ISC10)
	out MCUCR,r24
	ldi r24, (1<<INT1)		; we enable interruption INT1 only
	out GICR, r24
	
	ldi r24 ,(1<<TOIE1)		; enable Timer1 overflow interrupts
	out TIMSK ,r24	
	ldi r24 ,(1<<CS12) | (0<<CS11) | (1<<CS10) ; set frequency of timer at CK/1024 = 7812.5Hz
	out TCCR1B ,r24
loop:
	sei
	sbic PINA,7			; read A7, if 0 don't turn on the lights
	rjmp turn_on
	rjmp loop			; repeat
	
turn_on:
	ldi r26,0xF0			; set for 0.5 sec // 65536-3906.25 = 61629.75 -> 0xF0BE
	out TCNT1H,r26
	ldi r26,0xBE
	out TCNT1L,r26
	ser r26
	out PORTB,r26			; turn all lights on
	rjmp loop

turn_off:
	clr r26
	out PORTB,r26
	rjmp loop

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

ISR1:
	pop r26				; we don't want to store return address, we jump to turn_on

debounce0:
	ldi r26, (1<<INTF0)		; prepare debounce check for INT0
	out GIFR, r26			; write 1 to GIFR(6), making it 0
	ldi r24, low(5)
	ldi r25, high(5)
	rcall wait_msec			; wait 5 msecs
	in r26, GIFR			; check if GIFR(6) == 0
	sbrc r26,6			; if it is, serve interrupt
	rjmp debounce0			; else, repeat

	rjmp turn_on


ISR_TIMER1_OVF:
	pop r26				; we don't want to store return address, we jump to loop or turn_off
	sbis PORTB,7			; if all leds are on (checks MSB for example) change timer duration and keep PB0 on
	rjmp turn_off
	ldi r26,1			; turn on PB0
	out PORTB,r26
	ldi r26,0x95			; set for 3.5 sec // 65536-27343.75 = 38192.25 -> 0x9530
	out TCNT1H,r26
	ldi r26,0x30
	out TCNT1L,r26
	rjmp loop
