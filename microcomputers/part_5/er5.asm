PRINT_NUM MACRO CHAR
    MOV DL,CHAR
    ADD DL,30H
    PUSH AX
    MOV AH,2
    INT 21H
    POP AX
ENDM

PRINT_. MACRO
    MOV DL,'.'
    PUSH AX
    MOV AH,2
    INT 21H
    POP AX
ENDM

PRINT_NEWLINE MACRO
    MOV DL,0AH
    MOV AH,2
    INT 21H
    MOV DL,0DH
    MOV AH,2
    INT 21H
ENDM

PRINT_CELSIUS MACRO
    MOV DL,248
    MOV AH,2
    INT 21H
    MOV DL,'C'
    MOV AH,2
    INT 21H
ENDM

PRINT_START MACRO
    LEA DX,START_MSG
    MOV AH,9
    INT 21H
ENDM

PRINT_ERROR MACRO
    LEA DX,ERROR_MSG
    MOV AH,9
    INT 21H
ENDM
  
  
DATA    SEGMENT
    START_MSG DB    "START(Y,N): $"
    ERROR_MSG DB    "ERROR$"
DATA    ENDS
   
   
CODE    SEGMENT
    ASSUME CS:CODE,DS:DATA      

READ_Y_OR_N PROC
READ_Y:
    MOV AH,8
    INT 21H
    CMP AL,'N'              ; if N is pressed quit
    JE PROGRAM_END
    CMP AL,'Y'              ; if Y is not pressed wait for next button
    JNE READ_Y
    MOV DL,AL               ; we will print Y also
    MOV AH,2
    INT 21H
    RET
PROGRAM_END:
    MOV AX,4C00H
    INT 21H
READ_Y_OR_N ENDP

READ_HEX PROC
READ:
    MOV AH,8
    INT 21H
    CMP AL,'N'              ; if character is N end program
    JE PROGRAM_END
    CMP AL,'0'              ; if character is less than 0           
    JL READ                 ; ignore and read again
    CMP AL,'F'              ; if character is bigger than F
    JG READ                 ; ignore and read again
    CMP AL,'9'              ; if character is bigger than 9 we do an additional check
    JLE NUM                 ; else it's a number and we go on
    CMP AL,'A'
    JL READ
    SUB AL,7H               ; it's a valid char (A-F) we subtract 7 and later 30 for value
NUM:
    SUB AL,30H              ; we subtract 30H to find the digit's value
    ADD BL,AL               ; we want result in BL
    RET
PROGRAM_END_N:
    MOV AX,4C00H
    INT 21H
READ_HEX ENDP

PRINT_TEMPERATURE PROC
    CMP BX,7FFH             ; if temperature is more than 400 convert second way
    JG PRINT_B
    CALL PRINT_1
    RET
PRINT_B:
    CALL PRINT_2    
    RET
PRINT_TEMPERATURE ENDP

PRINT_1 PROC
    CMP BX,7FFH
    JE T_400
    CMP BX,0
    JE T_0
    MOV DX,0                ; division help
    MOV AX,BX               ; division
    MOV CX,512              ; divide by 512 to keep the quotient (512 = 2047/400 * 100)
    DIV CX
    PUSH DX
    PRINT_NUM AL
    POP DX
    MOV AX,DX
    MOV DX,0
    MOV BX,10
    MUL BX
    DIV CX
    PUSH DX
    PRINT_NUM AL
    POP DX
    MOV AX,DX
    MOV DX,0
    MOV BX,10
    MUL BX
    DIV CX
    PUSH DX
    PRINT_NUM AL
    PRINT_.
    POP DX
    MOV AX,DX
    MOV DX,0
    MOV BX,10
    MUL BX
    DIV CX
    PRINT_NUM AL 
    RET                            
T_400:
    PRINT_NUM 4             ; print 400.0
    PRINT_NUM 0
    PRINT_NUM 0
    PRINT_.
    PRINT_NUM 0 
    RET
T_0:
    PRINT_NUM 0             ; print 0.0
    PRINT_.
    PRINT_NUM 0
    RET
PRINT_1 ENDP

PRINT_2 PROC
    CMP BX,0BFDH            
    JE T_1200
    SUB BX,7FFH             ; we subtract voltage that corresponds to 400 celsius
    MOV DX,0                ; division help
    MOV AX,BX               ; division
    MOV CX,128              ; divide by 128 to keep the quotient (128 = 1023/800 * 100)
    DIV CX
    ADD AL,4                ; we add 400 actually because we subtracted before
    CMP AL,10
    JL SKIP_FIRST
    PUSH DX
    PRINT_NUM 1
    POP DX
    SUB AL,10
SKIP_FIRST:    
    PUSH DX
    PRINT_NUM AL
    POP DX
    MOV AX,DX
    MOV DX,0
    MOV BX,10
    MUL BX
    DIV CX
    PUSH DX
    PRINT_NUM AL
    POP DX
    MOV AX,DX
    MOV DX,0
    MOV BX,10
    MUL BX
    DIV CX
    PUSH DX
    PRINT_NUM AL
    PRINT_.
    POP DX
    MOV AX,DX
    MOV DX,0
    MOV BX,10
    MUL BX
    DIV CX
    PRINT_NUM AL 
    RET
T_1200:
    PRINT_NUM 1             ; print 1200.0
    PRINT_NUM 2           
    PRINT_NUM 0
    PRINT_NUM 0
    PRINT_.
    PRINT_NUM 0 
    RET
PRINT_2 ENDP

MAIN PROC
    MOV AX,DATA
    MOV DS,AX
    PRINT_START             ; print welcome message: START(Y,N):
    CALL READ_Y_OR_N        ; if Y continue else quit program
    PRINT_NEWLINE
START:
    MOV BX,0
    CALL READ_HEX                
    ROL BX,4                ; we rotate BX 4 bits left (multiply by 16)
    CALL READ_HEX
    ROL BX,4                ; rotate BX 4 bits left (multiply by 16 again)
    CALL READ_HEX           ; now BX contains our 3 digit hex
    CMP BX,0BFDH            ; if temperature is over 1200 print error and start again
    JA ERROR
    CALL PRINT_TEMPERATURE                     
    PRINT_CELSIUS
    PRINT_NEWLINE 
    JMP START
ERROR:
    PRINT_ERROR
    PRINT_NEWLINE
    JMP START
MAIN ENDP

CODE    ENDS
    END MAIN
    
