.include "m16def.inc"

.def input = r26
.def min = r27
.def secs = r28
.def t = r29
.def u = r30


reset:
		ldi r24, low(RAMEND)	; initialising stack pointer
		out SPL, r24
		ldi r24, high(RAMEND)
		out SPH, r24

		ser r24			; initialize D as output
		out DDRD, r24

		clr r24			; initialize B as input
		out DDRB, r24

		rcall lcd_init		; initialize LCD screen

initialize_counter:			; initialize timer
		ldi min, 0
		ldi secs, 0
		rcall print_time

check_input:				; check PORTB
		sbic PINB, 7		; if PD7 is pressed, stop counting and return to zero
		rjmp initialize_counter
		sbis PINB, 0		; start counting if PD0 is pressed
		rjmp check_input

count:
		rcall print_time	; print mins and secs
		ldi r24, low(1000)
		ldi r25, high(1000)
		rcall wait_msec		; wait for 1 second
		inc secs		; increase seconds counter
		cpi secs, 60		; when it reaches 60,
		brne check_input
		inc min			; increase minutes counter
		ldi secs, 0		; and set seconds counter to 0
		cpi min, 60		; when minutes counter reaches 60,
		breq initialize_counter ; start counting from 0 again
		rjmp check_input


; ---------------------------------------- ROUTINES ----------------------------------------

; converts hex number in r24 to dec, and stores tens in t and units in u
hex2ascii:
		ldi t, 0x30		; add 0x30 for ascii code
		ldi u, 0x30
tens:
		cpi r24, 10
		brlt units
		inc t
		subi r24, 10
		rjmp tens
units:
		add u, r24
		ret


; prints minutes and seconds
print_time:
		rcall set_address	; reset DDRAM address to print new number
		mov r24, min
		rcall hex2ascii		; tens in t, units in u
		mov r24, t
		rcall LCD_data		; print tens of minutes
		mov r24, u
		rcall LCD_data		; print units of minutes
		ldi r24, ' '
		rcall LCD_data		; print ' '
		ldi r24, 'M'
		rcall LCD_data		; print 'M'
		ldi r24, 'I'
		rcall LCD_data		; print 'I'
		ldi r24, 'N'
		rcall LCD_data		; print 'N'
		ldi r24, ':'
		rcall LCD_data		; print ':'
		mov r24, secs
		rcall hex2ascii		; tens in t, units in u
		mov r24, t
		rcall LCD_data		; print tens of seconds
		mov r24, u
		rcall LCD_data		; print units of seconds
		ldi r24, ' '
		rcall LCD_data		; print ' '
		ldi r24, 'S'
		rcall LCD_data		; print 'S'
		ldi r24, 'E'
		rcall LCD_data		; print 'E'
		ldi r24, 'C'
		rcall LCD_data		; print 'C'
		ret


; sends byte to the LCD screen controller, 4 bits at a time
write_2_nibbles:
		push r24
		in r25, PIND
		andi r25, 0x0f
		andi r24, 0xf0
		add r24, r25
		out PORTD, r24
		sbi PORTD, PD3
		cbi PORTD, PD3
		pop r24
		swap r24
		andi r24, 0xf0
		add r24, r25
		out PORTD, r24
		sbi PORTD, PD3
		cbi PORTD, PD3
		ret


; sends byte of data to the LCD screen controller
lcd_data:
		sbi PORTD, PD2
		rcall write_2_nibbles
		ldi r24, 43
		ldi r25, 0
		rcall wait_usec
		ret


; sends an instruction to the LCD screen controller
lcd_command:
		cbi PORTD, PD2
		rcall write_2_nibbles
		ldi r24, 39
		ldi r25, 0
		rcall wait_usec
		ret


; initializes LCD screen
lcd_init:
		ldi r24, 40
		ldi r25, 0
		rcall wait_msec

		ldi r24, 0x30
		out PORTD, r24
		sbi PORTD, PD3
		cbi PORTD, PD3
		ldi r24, 39
		ldi r25, 0
		rcall wait_usec

		ldi r24, 0x30
		out PORTD, r24
		sbi PORTD, PD3
		cbi PORTD, PD3
		ldi r24, 39
		ldi r25, 0
		rcall wait_usec

		ldi r24, 0x20
		out PORTD, r24
		sbi PORTD, PD3
		cbi PORTD, PD3
		ldi r24, 39
		ldi r25, 0
		rcall wait_usec

		ldi r24, 0x28
		rcall lcd_command

		ldi r24, 0x0c
		rcall lcd_command

		ldi r24, 0x01
		rcall lcd_command
		
		ldi r24, low(1530)
		ldi r25, high(1530)
		rcall wait_usec

		ldi r24, 0x06
		rcall lcd_command
		ret


; sets DDRAM address to 00H, to print new number
set_address:
		ldi r24 ,0x80
		rcall lcd_command
		ldi r24 ,low(39)
		ldi r25, 0
		rcall wait_usec
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
