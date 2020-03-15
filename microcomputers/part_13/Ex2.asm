.include "m16def.inc"

.def count = r26
.def sign = r27
.def numb = r28
.def h = r29		; hundreds
.def t = r30		; tens
.def u = r31		; units


reset:
		ldi r24, low(RAMEND)	; initialising stack pointer
		out SPL, r24
		ldi r24, high(RAMEND)
		out SPH, r24

		ser r24			; initialize D as output
		out DDRD, r24

		clr r24			; initialize A as input
		out DDRA, r24

		rcall lcd_init		; initialize LCD screen

loop:
		in numb, PINA		; read input from PORTA
		push numb		; store input

		rcall set_address	; initialize DDRAM address to 00H
		ldi count, 7		; initialize digit counter

print_dig:
		ldi r24, 0x30		; digit to be printed is 0 (in ascii)
		sbrc numb, 6		; if bit in position 6 is 0 skip next instruction
		ldi r24, 0x31		; digit to be printed is 1 (in ascii)
		rcall lcd_data		; print digit
		lsl numb		; shift number left to print next bit
		dec count		; next bit
		brne print_dig		; repeat for all 7 bits

		pop numb		; recover input number
		ldi sign, '+'		; initialize sign
		sbrc numb, 7		; if 1st bit is 0 skip conversion
		rcall negative		; else convert to negative
		cpi numb, 0		; if number is 0 don't use sign
		brne not_zero
		ldi sign, ' '
not_zero:
		andi numb, 0x7F		; keep 7 LSBs
		rcall hex_2_ascii	; convert to BCD (ascii)

		ldi r24, '='
		rcall lcd_data		; print '='
		mov r24, sign
		rcall lcd_data		; print sign '+' or '-'
		mov r24, h
		rcall lcd_data		; print hundreds
		mov r24, t
		rcall lcd_data		; print tens
		mov r24, u
		rcall lcd_data		; print units
		rjmp loop


; ---------------------------------------- ROUTINES ----------------------------------------

; if number is negative
negative:
		ldi sign, '-'		; negative sign
		com numb		; one's complement
		ret


; converts hex number in numb to dec, and stores hundreds in h, tens in t, units in u
hex_2_ascii:
		ldi h, 0x30		; add 0x30 for ascii code
		ldi t, 0x30
		ldi u, 0x30
hundreds:
		cpi numb, 100
		brlt tens
		inc h
		subi numb, 100
		rjmp hundreds
tens:
		cpi numb, 10
		brlt units
		inc t
		subi numb, 10
		rjmp tens
units:
		add u, numb
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
