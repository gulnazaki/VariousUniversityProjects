.include "m16def.inc"


reset:
	ldi r24, low(RAMEND)		; initialising stack pointer
	out SPL, r24
	ldi r24, high(RAMEND)
	out SPH, r24
loop:
	rcall temp
	push r24					; LSByte
	push r25					; MSByte
	ser r24						; set ports A, B, C as outputs
	out DDRA, r24
	out DDRB, r24
	out DDRC, r24
	pop r25						; MSByte -> r25
	pop r24						; LSByte -> r24
	out PORTA, r24				; print LSByte in PORTA
	out PORTB, r24				; print LSByte in PORTB
	out PORTC, r25				; print MSByte in PORTC
;	ldi r24 ,low(2000)
;	ldi r25 ,high(2000)
;	rcall wait_msec
	rjmp loop



; ---------------------------------------- ROUTINES ----------------------------------------

temp:
	rcall one_wire_reset		; initialize device
	cpi r24, 0					; if one_wire_reset returns 0,
	breq no_dev					; jump to no_dev
	ldi r24, 0xCC				; there is only 1 device
	rcall one_wire_transmit_byte
	ldi r24, 0x44				; send instruction that initiates temperature conversion
	rcall one_wire_transmit_byte
wait:
	rcall one_wire_receive_bit
	sbrs r24,0					; if conversion is complete, the device transmits 1-bit
	rjmp wait
	rcall one_wire_reset		; initialize device
	cpi r24, 0					; if one_wire_reset returns 0,
	breq no_dev					; jump to no_dev
	ldi r24, 0xCC				; there is only 1 device
	rcall one_wire_transmit_byte
	ldi r24, 0xBE				; send instructiopn that reads temperature
	rcall one_wire_transmit_byte
	rcall one_wire_receive_byte
	push r24					; receive LSByte of temperature and push to stack
	rcall one_wire_receive_byte
	mov r25, r24				; receive MSByte of temperature and move to r25
	pop r24						; pop LSByte of temperature to r24
	cpi r25, 0xFF
	brne pos					; if sign is not negative, jump to pos
	com r24						; else calculate complement of 2
	inc r24
pos:
	lsr r24						; shift right -> divide by 2
;	lsr r24						; DELETE THIS LINE
	sbrc r25,0					; if sign is positive skip next instruction
	com r24						; else calculate complement of 1
	ret
no_dev:							; if no device is found,
	ldi r25, 0x80				; store 0x8000 in r25:r24
	ldi r24, 0
	ret
	
	
wait_usec:
	sbiw r24,1					; subtracting 1 from r25:r24 (2 cycles)
	nop
	nop
	nop
	nop
	brne wait_usec				; instructions till now take 8 cycles = 1usec
	ret							; if 25:r24 usecs have passed return


wait_msec:
	push r24					; pushing r25:r24 in stack / all instructions take 1msec=1000usec
	push r25
	ldi r24, low(998)
	ldi r25, high(998)
	rcall wait_usec
	pop r25						; poping r25:r24
	pop r24
	sbiw r24,1					; subtract 1 from delay in msecs
	brne wait_msec
	ret							; if we are finished return


one_wire_receive_byte:
	ldi r27 ,8
	clr r26
loop_:
	rcall one_wire_receive_bit
	lsr r26
	sbrc r24 ,0
	ldi r24 ,0x80
	or r26 ,r24
	dec r27
	brne loop_
	mov r24 ,r26
	ret


one_wire_receive_bit:
	sbi DDRA ,PA4
	cbi PORTA ,PA4				; generate time slot
	ldi r24 ,0x02
	ldi r25 ,0x00
	rcall wait_usec
	cbi DDRA ,PA4				; release the line
	cbi PORTA ,PA4
	ldi r24 ,10					; wait 10 us
	ldi r25 ,0
	rcall wait_usec
	clr r24						; sample the line
	sbic PINA ,PA4
	ldi r24 ,1
	push r24
	ldi r24 ,49					; delay 49 us to meet the standards
	ldi r25 ,0					; for a minimum of 60 usec time slot
	rcall wait_usec				; and a minimum of 1 usec recovery time
	pop r24
	ret


one_wire_transmit_byte:
	mov r26 ,r24
	ldi r27 ,8
_one_more_:
	clr r24
	sbrc r26 ,0
	ldi r24 ,0x01
	rcall one_wire_transmit_bit
	lsr r26
	dec r27
	brne _one_more_
	ret


one_wire_transmit_bit:
	push r24					; save r24
	sbi DDRA ,PA4
	cbi PORTA ,PA4				; generate time slot
	ldi r24 ,0x02
	ldi r25 ,0x00
	rcall wait_usec
	pop r24						; output bit
	sbrc r24 ,0
	sbi PORTA ,PA4
	sbrs r24 ,0
	cbi PORTA ,PA4
	ldi r24 ,58					; wait 58 usec for the
	ldi r25 ,0					; device to sample the line
	rcall wait_usec
	cbi DDRA ,PA4				; recovery time
	cbi PORTA ,PA4
	ldi r24 ,0x01
	ldi r25 ,0x00
	rcall wait_usec
	ret


one_wire_reset:
	sbi DDRA ,PA4				; PA4 configured for output
	cbi PORTA ,PA4				; 480 usec reset pulse
	ldi r24 ,low(480)
	ldi r25 ,high(480)
	rcall wait_usec
	cbi DDRA ,PA4				; PA4 configured for input
	cbi PORTA ,PA4
	ldi r24 ,100				; wait 100 usec for devices
	ldi r25 ,0					; to transmit the presence pulse
	rcall wait_usec
	in r24 ,PINA				; sample the line
	push r24
	ldi r24 ,low(380)			; wait for 380 usec
	ldi r25 ,high(380)
	rcall wait_usec
	pop r25						; return 0 if no device was
	clr r24						; detected or 1 else
	sbrs r25 ,PA4
	ldi r24 ,0x01
	ret
