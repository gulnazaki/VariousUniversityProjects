.include "m16def.inc"

.DSEG
_tmp_:.byte 2


.CSEG
reset:
		ldi r26,low(RAMEND)		; initialising stack pointer
		out SPL,r26
		ldi r26,high(RAMEND)
		out SPH,r26

		ldi r24 ,(1 << PC7) | (1 << PC6) | (1 << PC5) | (1 << PC4)
		out DDRC ,r24			; initialize C as output to enable reading from keypad

		ser r24
		out DDRB, r24			; initialize B as output

		ldi r26 ,low(_tmp_)		; initialize _tmp_ by storing 0
		ldi r27 ,high(_tmp_)
		clr r24
		st X+, r24
		st X, r24

loop:
		; 0 -> keypad state = 0x00 - 0x02
		; 3 -> keypad state = 0x40 - 0x00
		rcall scan			; scan until key is pressed
		cpi r25,0
		brne wrong1			; if 1st byte is not 0, the 1st number is wrong
		cpi r24,2
		brne wrong1			; if 2nd byte is not 2, the 1st number is wrong

		; if 1st byte = 0 and 2nd byte = 2, 1st number = 0 (correct)
		rcall scan			; scan until key is pressed
		cpi r25,0x40
		brne wrong			; if 1st byte is not 0x40, the 2nd number is wrong
		cpi r24,0
		brne wrong			; if 2nd byte is not 0, the 2nd number is wrong

		; if 1st byte = 0x40 and 2nd byte = 0, 2nd number = 3 (both correct)
		ser r24
		out PORTB, r24			; turn on all LEDs
		ldi r24, low(4000)		; wait for 4 s
		ldi r25, high(4000)
		rcall wait
		clr r24
		out PORTB, r24			; turn off all LEDs
		rjmp loop			; wait for new numbers

; first number is wrong
wrong1:
		rcall scan			; wait for 1 more key to be pressed
wrong:
		ldi r24, low(250)		; set waiting time to 0.25 s
		ldi r25, high(250)
		ldi r22,8			; initialize counter
blink:
		ser r23
		out PORTB, r23			; turn on all LEDs
		rcall wait			; wait for 0.25 s
		clr r23
		out PORTB, r23			; turn off all LEDs
		rcall wait			; wait for 0.25 s
		dec r22				; decrease counter
		cpi r22, 0
		brne blink
		rjmp loop			; after 8 repetitions, stop and wait for new number

; routine that waits for (r25:r24), without changing (r25:r24)
wait:
		push r24
		push r25
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
		pop r25
		pop r24
		ret				; if we are finished return

wait_usec:
		sbiw r24,1			; subtracting 1 from r25:r24 (2 cycles)
		nop
		nop
		nop
		nop
		brne wait_usec			; instructions till now take 8 cycles = 1usec
		ret				; if 25:r24 usecs have passed return

; routine that checks a line (line number in r24) and returns state of keys in 4 LSDs of r24
scan_row:
		ldi r25 ,0x08			; initialize with '0000 1000'
back_:
		lsl r25				; shift r25 left as many times
		dec r24				; as the number of the line
		brne back_
		out PORTC,r25			; chosen line is set to 1
		nop
		nop				; delay so that new state is written to PINC
		in r24 ,PINC			; return positions of pressed keys
		andi r24 ,0x0f			; only the four LSBs are useful
		clr r25					; make sure that, after the scan,
		out PORTC,r25			; all LEDs of PORTC are off
		ret

; routine that scans keypad and returns state of all keys in r25:r24
scan_keypad:
		ldi r24 ,0x01
		rcall scan_row			; check first line of keypad
		swap r24			; swap bytes (4LSBs <-> 4MSBs)
		mov r27 ,r24			; store in 4 MSBs of r27
		ldi r24 ,0x02
		rcall scan_row			; check second line of keypad
		add r27 ,r24			; store in 4 LSBs of r27
		ldi r24 ,0x03
		rcall scan_row			; check third line of keypad
		swap r24			; swap bytes (4LSBs <-> 4MSBs)
		mov r26 ,r24			; store in 4 MSBs of r26
		ldi r24 ,0x04
		rcall scan_row			; check fourth line of keypad
		add r26 ,r24			; store in 4 LSBs of r26
		movw r24 ,r26			; move result from r27:r26 to r25:r24
		ret

; scans keypad and returns just pressed keys in r25:r24, avoiding bouncing
scan_keypad_rising_edge:
		mov r22 ,r24			; store given time duration in r22
		rcall scan_keypad		; check for any pressed key
		push r24			; push keyboard state to the stack
		push r25
		mov r24 ,r22			; wait to avoid bouncing
		ldi r25 ,0
		rcall wait
		rcall scan_keypad		; check again for pressed key
		pop r23				; pop first keyboard state
		pop r22
		and r24 ,r22			; see what is still pressed (not a result from bouncing)
		and r25 ,r23
		ldi r26 ,low(_tmp_)		; load previous result from RAM
		ldi r27 ,high(_tmp_)
		ld r23 ,X+
		ld r22 ,X
		st X,r24			; store next result to RAM
		st -X,r25
		com r23				; (next) and (prev)' -> keys just pressed
		com r22
		and r24 ,r22			; store just pressed keys in r25:r24
		and r25 ,r23
		ret

; routine that scans keypad continuously until a key is pressed, then returns keypad state in r24
scan:
		ldi r24,7			; debouncing time
		call scan_keypad_rising_edge	; scan keypad
		cpi r25, 0
		brne scan_complete		; if key is pressed return
		cpi r24, 0
		breq scan			; else scan again
scan_complete:
		ret
