PRINT_STR MACRO STRING
    LEA DX,STRING		; load string(parameter) address
    MOV AH,9			; print string routine
    INT 21H
ENDM

PRINT_NUM MACRO NUM
    MOV DL,NUM			; DL <- number(parameter)		;
    ADD DL,30H			; add 30H (0's ascii code)
    MOV AH,2			; print char routine
    INT 21H
ENDM 

PRINT_NEWLINE MACRO
    MOV DL,0AH			; print chars 0AH and 0DH making a new line
    MOV AH,2
    INT 21H
    MOV DL,0DH
    MOV AH,2
    INT 21H
ENDM

READ_NUM MACRO REG
    MOV AH,8			; read char routine
    INT 21H
    CMP AL,'Q'			; end program if Q
    JE PROGRAM_END              
    MOV REG,AL              
ENDM
  
  
DATA    SEGMENT
    DEC_MSG DB "GIVE 2 DECIMAL DIGITS: $"
    OCT_MSG DB "OCTAL= $"                                      
DATA    ENDS
  
  
CODE    SEGMENT
    ASSUME CS:CODE,DS:DATA      
     
READ PROC
READ_1:
    READ_NUM BH			; char in BH
    SUB BH,30H
    CMP BH,9			
    JA READ_1 			; if >9 (no number) read again
READ_2:    
    READ_NUM BL			; second char in BL
    SUB BL,30H
    CMP BL,9			; if >9 (no number) read again
    JA READ_2                                                                                                    
WAIT_ENTER:
    READ_NUM CH			; char in CH
    CMP CH,0DH			
    JE RETURN			; if char is enter move on
    SUB CH,30H
    CMP CH,9
    JA WAIT_ENTER		; if >9 no number but no enter pressed too, read again
    MOV BH,BL			; if number keep that and the last one
    MOV BL,CH
    JMP WAIT_ENTER
RETURN:
    RET
PROGRAM_END:
    MOV AX,4C00H
    INT 21H                                                               
READ ENDP

PRINT_OCT PROC
    MOV CL,10			; multiply by 10 and add units
    MOV AL,BH
    MUL CL
    ADD AL,BL
    MOV CL,64           ; we will divide by 64 (8*8*1)
    DIV CL
    PUSH AX
    PRINT_NUM AL		; print 1st digit
    POP AX
    MOV AL,AH         	; remainder is divided next
    MOV AH,0
    MOV CL,8			; divide by 8
    DIV CL
    PUSH AX
    PRINT_NUM AL		; print 2nd digit
    POP AX
    PRINT_NUM AH   		; print 3rd digit
    RET
PRINT_OCT ENDP

MAIN PROC
START:
    MOV AX,DATA			; for using the data segment
    MOV DS,AX
    PRINT_STR DEC_MSG	; print the welcome message
    CALL READ			; read number
    PRINT_NUM BH		; print nums and a new line
    PRINT_NUM BL
    PRINT_NEWLINE
    PRINT_STR OCT_MSG	; print octal=
    CALL PRINT_OCT		; print octal form
    PRINT_NEWLINE
    JMP START     
MAIN ENDP    
     
CODE    ENDS
    END MAIN
