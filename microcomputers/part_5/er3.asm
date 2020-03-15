PRINT_NEWLINE MACRO
    MOV DL,0AH
    MOV AH,2
    INT 21H
    MOV DL,0DH
    MOV AH,2
    INT 21H
ENDM
  
  
CODE    SEGMENT
    ASSUME CS:CODE      

PRINT_NUM PROC
    ADD DL,30H              ; create ascii code
    PUSH AX
    MOV AH,2
    INT 21H
    POP AX
    RET
PRINT_NUM ENDP

PRINT_DEC PROC
    PUSH BX                 ; save number
    MOV AH,0                ; will use AX for division
    MOV AL,BL               ; move number to AL
    MOV CL,100              ; we will divide by 10
    DIV CL
    MOV DL,AL               ; quotient stored in DL
    CALL PRINT_NUM
    MOV AL,AH               ; remainder is divided next
    MOV AH,0
    MOV CL,10
    DIV CL
    MOV DL,AL
    CALL PRINT_NUM
    MOV DL,AH
    CALL PRINT_NUM
    POP BX                  ; restore number 
    MOV DL,'='              ; we print =
    MOV AH,2
    INT 21H
    RET
PRINT_DEC ENDP

PRINT_OCT PROC
    PUSH BX                 ; save number
    MOV AH,0                ; will use AX for division
    MOV AL,BL               ; move number to AL
    MOV CL,64               ; we will divide by 64 (8*8*1)
    DIV CL
    MOV DL,AL               ; quotient stored in DL
    CALL PRINT_NUM
    MOV AL,AH               ; remainder is divided next
    MOV AH,0
    MOV CL,8
    DIV CL
    MOV DL,AL
    CALL PRINT_NUM
    MOV DL,AH
    CALL PRINT_NUM
    POP BX                  ; restore number 
    MOV DL,'='              ; we print =
    MOV AH,2
    INT 21H   
    RET
PRINT_OCT ENDP

PRINT_BIN PROC
    PUSH BX                 ; save number
    MOV CX,8                ; we will loop 8 times (1 for each digit)
ALL_DIGITS:
    MOV DL,0                ; set DL to 0 in each loop
    ROL BL,1                ; rotate number left and if msb 1 carry flag is set
    ADC DL,0                ; we add zero plus Carry flag to DL (setting it)
    CALL PRINT_NUM
    LOOP ALL_DIGITS
    POP BX                  ; restore number
    RET
PRINT_BIN ENDP

HEX_KEYB PROC
READ:
    MOV AH,8
    INT 21H
    CMP AL,'T'              ; if character is T end program
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
    MOV BL,AL               ; we want result in BL
    RET
PROGRAM_END:
    MOV AX,4C00H
    INT 21H
HEX_KEYB ENDP

MAIN PROC
START:
    CALL HEX_KEYB           ; routine reads a hex (0-F) and stores it in BL
    MOV BH,BL               ; move first digit to BH
    ROL BH,4                ; we multiply with 16 (4 left shifts)
    CALL HEX_KEYB
    ADD BL,BH               ; we add the two digits and create a byte hex in BL
    CALL PRINT_DEC
    CALL PRINT_OCT  
    CALL PRINT_BIN
    PRINT_NEWLINE
    JMP START
MAIN ENDP

CODE    ENDS
    END MAIN
    
