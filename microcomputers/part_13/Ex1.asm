.include "m16def.inc"
.org 0x0
	rjmp reset
.org 0x10
	rjmp ISR_TIMER1_OVF
.DSEG
_tmp_:.byte 2


.CSEG
reset:
		ldi r26,low(RAMEND)		; initialising stack pointer
		out SPL,r26
		ldi r26,high(RAMEND)
		out SPH,r26

		ldi r24,(1 << PC7) | (1 << PC6) | (1 << PC5) | (1 << PC4)
		out DDRC,r24			; initialize C as output to enable reading from keypad

		ser r24				; initialize A and D as outputs
		out DDRA,r24
		out DDRD,r24
		
		clr r24				; initialize B as input
		out DDRB,r24

		ldi r26,low(_tmp_)		; initialize _tmp_ by storing 0
		ldi r27,high(_tmp_)
		st X+,r24
		st X,r24
	
		ldi r24 ,(1<<TOIE1)		; enable Timer1 overflow interrupts
		out TIMSK ,r24	
		ldi r24 ,(1<<CS12) | (0<<CS11) | (1<<CS10) ; set frequency of timer at CK/1024 = 7812.5Hz
		out TCCR1B ,r24
		
		rcall lcd_init
		
alarm_off:					; we loop here while alarm is off
		in r26,PINB			; reading buttons PB0-7
		cpi r26,0
		brne enter_passwd		; if a button(sensor) is pressed we have to enter the password
		rjmp alarm_off
					
enter_passwd:	
		ldi r26,0x67			; set interval for 5 sec // 65536-39062.5 = 26473.5 -> 0x6769
		out TCNT1H,r26
		ldi r26,0x69
		out TCNT1L,r26
		sei				; enable interrupts (for timer)
		
		rcall scan			; scan until key is pressed
		rcall keypad_to_ascii		; convert to ascii
		push r24			; push in stack temporary because lcd_data changes r24
		rcall lcd_data
		pop r24
		cpi r24,'3'
		brne wrong1			; if '3' isn't pressed go to wrong1(1st button wrong)
		
		; if 1st number = 3 (correct)
		rcall scan			; scan until key is pressed
		rcall keypad_to_ascii		; convert to ascii
		push r24			; push in stack temporary because lcd_data changes r24
		rcall lcd_data
		pop r24
		cpi r24,'0'
		brne wrong2			; if '0' isn't pressed go to wrong2(2nd button wrong)

		; if 2nd number = 0 (also correct)
		rcall scan			; scan until key is pressed
		rcall keypad_to_ascii		; convert to ascii
		push r24			; push in stack temporary because lcd_data changes r24
		rcall lcd_data
		pop r24
		cpi r24,'3'
		brne alarm_on			; if '3' isn't pressed turn the alarm on
		
		; now the correct password has been pressed (303)		
		ldi r24 ,(0<<CS12) | (0<<CS11) | (0<<CS10) ; stop timer
		out TCCR1B ,r24
		cli				; and disable interrupts

		rcall print_off			; ALARM OFF
		
		rjmp alarm_off			; go to the initial loop

wrong1:
		rcall scan			; wait for 2 more key to be pressed
		rcall keypad_to_ascii		; print the wrong key
		rcall lcd_data
wrong2:
		rcall scan			; wait for 1 more key to be pressed
		rcall keypad_to_ascii		; print the wrong key
		rcall lcd_data
alarm_on:
		rcall print_on			; ALARM ON
on:
		ldi r24, low(400)		; set on time to 0.4 s
		ldi r25, high(400)
		ser r26
		out PORTA, r26			; turn on all LEDs
		rcall wait			; wait for 0.4 s
		
		ldi r24, low(100)		; set off time to 0.1 s
		ldi r25, high(100)
		clr r26
		out PORTA, r26			; turn off all LEDs
		rcall wait			; wait for 0.1 s
		rjmp on

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

print_on:
	rcall lcd_init
	ldi r24,'A'
	rcall lcd_data
	ldi r24,'L'
	rcall lcd_data
	ldi r24,'A'
	rcall lcd_data
	ldi r24,'R'
	rcall lcd_data
	ldi r24,'M'
	rcall lcd_data
	ldi r24,' '
	rcall lcd_data
	ldi r24,'O'
	rcall lcd_data
	ldi r24,'N'
	rcall lcd_data	
	ret

print_off:	
	rcall lcd_init
	ldi r24,'A'
	rcall lcd_data
	ldi r24,'L'
	rcall lcd_data
	ldi r24,'A'
	rcall lcd_data
	ldi r24,'R'
	rcall lcd_data
	ldi r24,'M'
	rcall lcd_data
	ldi r24,' '
	rcall lcd_data
	ldi r24,'O'
	rcall lcd_data
	ldi r24,'F'
	rcall lcd_data	
	ldi r24,'F'
	rcall lcd_data

	ldi r24,low(1000)			; we wait 1 sec and flush the screen
	ldi r25,high(1000)
	rcall wait
	rcall lcd_init
	ret

keypad_to_ascii:
		movw r26,r24
		ldi r24 ,'*'
		sbrc r26 ,0
		ret
		ldi r24 ,'0'
		sbrc r26 ,1
		ret
		ldi r24 ,'#'
		sbrc r26 ,2
		ret
		ldi r24 ,'D' 
		sbrc r26 ,3
		ret
		ldi r24 ,'7'
		sbrc r26 ,4
		ret
		ldi r24 ,'8'
		sbrc r26 ,5
		ret
		ldi r24 ,'9'
		sbrc r26 ,6
		ret
		ldi r24 ,'C'
		sbrc r26 ,7
		ret
		ldi r24 ,'4'
		sbrc r27 ,0
		ret
		ldi r24 ,'5'
		sbrc r27 ,1
		ret
		ldi r24 ,'6'
		sbrc r27 ,2
		ret
		ldi r24 ,'B'
		sbrc r27 ,3
		ret
		ldi r24 ,'1'
		sbrc r27 ,4
		ret
		ldi r24 ,'2'
		sbrc r27 ,5
		ret
		ldi r24 ,'3'
		sbrc r27 ,6
		ret
		ldi r24 ,'A'
		sbrc r27 ,7
		ret
		clr r24
		ret
		
		
ISR_TIMER1_OVF:
		pop r26				; remove return address from stack
		rjmp alarm_on			; and turn the alarm on

write_2_nibbles:
		push r24
		in r25 ,PIND
		andi r25 ,0x0f
		andi r24 ,0xf0
		add r24 ,r25
		out PORTD ,r24
		sbi PORTD ,PD3
		cbi PORTD ,PD3
		pop r24
		swap r24
		andi r24 ,0xf0
		add r24 ,r25
		out PORTD ,r24
		sbi PORTD ,PD3
		cbi PORTD ,PD3
		ret

lcd_data:
		sbi PORTD ,PD2
		rcall write_2_nibbles
		ldi r24 ,43
		ldi r25 ,0
		rcall wait_usec
		ret

lcd_command:
		cbi PORTD ,PD2
		rcall write_2_nibbles
		ldi r24 ,39
		ldi r25 ,0
		rcall wait_usec
		ret

lcd_init:
		ldi r24 ,40
		ldi r25 ,0
		rcall wait

		ldi r24 ,0x30
		out PORTD ,r24
		sbi PORTD ,PD3
		cbi PORTD ,PD3
		ldi r24 ,39
		ldi r25 ,0
		rcall wait_usec
		
		ldi r24 ,0x30
		out PORTD ,r24
		sbi PORTD ,PD3
		cbi PORTD ,PD3
		ldi r24 ,39
		ldi r25 ,0
		rcall wait_usec

		ldi r24 ,0x20
		out PORTD ,r24
		sbi PORTD ,PD3
		cbi PORTD ,PD3
		ldi r24 ,39
		ldi r25 ,0
		rcall wait_usec
		
		ldi r24 ,0x28
		rcall lcd_command

		ldi r24 ,0x0e
		rcall lcd_command
		
		ldi r24 ,0x01
		rcall lcd_command
		
		ldi r24 ,low(1530)
		ldi r25 ,high(1530)
		rcall wait_usec

		ldi r24 ,0x06
		rcall lcd_command
		ret
