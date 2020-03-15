.INCLUDE "m16def.inc"
.DEF A=R16
.DEF B=R17
.DEF C=R18
.DEF D=R19
.DEF E=R20
.DEF F=R21
.DEF X0=R22
.DEF X1=R23
.DEF X2=R24
.DEF temp=R22

.MACRO Read_input
	in temp,PINC				; input
	lsr temp
	lsr temp
	ldi A,1						; A = 0b00000001
	andi A,temp					; A reg set to A
	lsr temp
	ldi B,1						
	andi B,temp					
	lsr temp
	ldi C,1						
	andi C,temp					
	lsr temp
	ldi D,1						
	andi D,temp					
	lsr temp
	ldi E,1						
	andi E,temp					
	lsr temp
	ldi F,1						
	andi F,temp	
.ENDMACRO

start:
	clr temp					; temp = 0x00
	out DDRC					; use PORTC as input
	dec temp					; temp = 0xFF
	out PORTC					; pull-up enabled for PORTC
	out DDRA					; use PORTA as output

main:
	Read_input
	
	mov X0,A 					; we store first term in X0
	and X0,B
	mov temp,C 					; second term in temp
	com D 						; D'
	and temp,D 					
	com D 						; restore D
	com E 						; E'
	and temp,E 				
	com E 						; restore E
	and temp,F 
	or X0,temp

	mov X1,A 				 	; first term in X1
	and X1,B
	com C 						; C'
	and X1,C 					
	and X1,D
	com D 						; D'
	mov temp,D 					; second term in temp
	and temp,E
	com F 						; F'
	and temp,F 
	or X1,temp

	mov X2,X1			
	or X2,X0
	lsl X2						; shift left X2 (2nd LSB)
	add X2,X1					; add X1 (becomes LSB)
	lsl X2						; shift left X2 (becomes 3rd LSB) and X1 becomes 2nd
	add X2,X0					; add X0 (LSB)
	out PORTA,X2				; output (X0 -> pin0, X1 -> pin1, X2 -> pin2)

	rjmp main