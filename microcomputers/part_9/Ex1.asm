READ MACRO                      ; reads one character from keyboard
    MOV AH,8                    ; and stores its ASCII code in AL
    INT 21H
ENDM

PRINT_CHAR MACRO CHAR           ; prints CHAR character
    PUSH AX                     ; store AX,DX
    PUSH DX
    MOV DL,CHAR                 ; print CHAR
    MOV AH, 2
    INT 21H
    POP DX                      ; recover AX,DX
    POP AX
ENDM

PRINT_STR MACRO STR             ; prints STR string
    PUSH AX                     ; store AX,DX
    PUSH DX
    MOV DX, OFFSET STR          ; print STR
    MOV AH,9
    INT 21H
    POP DX                      ; recover AX,DX
    POP AX
ENDM

PRINT_DEC MACRO                 ; prints decimal digit stored in DL
    PUSH AX                     ; store AX
    ADD DL, 30H                 ; print digit
    MOV AH,2
    INT 21H
    POP AX                      ; recover AX
ENDM

EXIT MACRO                      ; exits program
    MOV AX, 4C00H
    INT 21H
ENDM

DATA SEGMENT
    INPUT_PROMPT DB "GIVE 3 HEX DIGITS: $"
    RESULT_PROMPT DB "Decimal: $"
    NL DB 0AH, 0DH, '$'
DATA ENDS

STACK SEGMENT
    DB 10 DUB(?)
STACK ENDS

CODE SEGMENT
    ASSUME CS:CODE, SS:STACK, DS:DATA
     
START:
    MOV AX,DATA
    MOV DS,AX
    
    PRINT_STR INPUT_PROMPT      ; print input prompt
    
    CALL HEX_KEYB               ; read first (valid) hex digit from keyboard
    MOV BL,10H                  ; BL = 16
    MUL BL                      ; now, AL = 16*(first digit)
    MOV CH,AL                   ; store {16*(first digit)} in CH
    
    CALL HEX_KEYB               ; read second (valid) hex digit from keyboard
    ADD CH,AL                   ; create the quantity: 16*(first digit)+(second digit)
    PRINT_CHAR '.'              ; print a dot
    
    CALL HEX_KEYB               ; read the last (valid) hex digit from keyboard
    MOV CL,AL                   ; now H1H0 in CH and H(-1) in CL
    
CHECK_IF_DONE:
    CMP CL,3                    ; if CL = 3, then
    JNE PRINT_RESULT            ; we may need to terminate, else we move on
    CMP CH,192                  ; if CH = 192 (=C0 in hex), we are done
    JE EXIT_PROGRAM  

PRINT_RESULT:    
    PRINT_STR NL                ; print a new line
    PRINT_STR RESULT_PROMPT     ; print result prompt
    MOV DL,0                    ; we initialise counter for routine to call
    MOV AH,0
    MOV AL,CH
    CALL PRINT_DEC_NUM          ; and print them
    PRINT_CHAR '.'              ; print a dot
        
    MOV AH,0                    ; now AH = 0, AL = H(-1)
    MOV AL,CL
    MOV BX,625                  ; result will be H(-1)*625*0.01 (4 digits to be printed)
    MUL BX

    MOV DL,0                    ; counter = 0 (we will pretend we have a regular 4-digit number to print)
    CMP CL,1                    ; if H(-1)=0 or 1, first digit after dot will be zero
    JG PRINT_THEM_ALREADY
    PRINT_CHAR '0'
PRINT_THEM_ALREADY:
    CALL PRINT_DEC_NUM          ; print the remaining 3 digits   
    
    PRINT_STR NL                ; print a new line
    JMP START                   ; repeat forever
    

EXIT_PROGRAM:    
    EXIT                        ; return to OS    

;;; routines ;;;

HEX_KEYB PROC NEAR              ; reads digit+checks if it's valid (0-9 or A-F) and prints it
IGNORE:
    READ                        ; read digit
    SUB AL,30H                  ; check if 0<=digit<=9
    CMP AL,0
    JB IGNORE                   ; if digit<0 ignore and read next
    CMP AL,9
    JBE RETURN_DIGIT            ; if 0<=digit<=9 -> RETURN
    SUB AL,7                    ; check if A=10<=digit<=F=15
    CMP AL,10
    JB IGNORE                   ; if digit>9 but not A,B,C,D,E,F ignore and read next
    CMP AL,15
    JNBE IGNORE
RETURN_LETTER:
    ADD AL,55
    PRINT_CHAR AL               ; prints what it read
    SUB AL,55
    JMP RETURN
RETURN_DIGIT:
    ADD AL,30H
    PRINT_CHAR AL
    SUB AL,30H
RETURN:
    MOV AH,0                    ; 00-AL->AX
    RET                         ; return number in AL
HEX_KEYB ENDP

PRINT_DEC_NUM PROC NEAR         ; prints big dec numbers (with thousands) in AX
    PUSH AX
    PUSH CX
    MOV DL,0
COUNT_THOUSANDS:
    CMP AX,1000
    JB PRINT_THOUSANDS
    INC DL
    SUB AX,1000
    JMP COUNT_THOUSANDS
PRINT_THOUSANDS:
    CMP DL,0                    ; if we have no thousands, print nothing
    JE SKIP_PRINT
    PRINT_DEC
SKIP_PRINT:
    MOV DL,0
COUNT_HUNDREDS:                 
    CMP AX,100                  ; if AX < 100, then print hundreds (stored in DL)
    JB PRINT_HUNDREDS
    INC DL                      ; else counter++
    SUB AX,100
    JMP COUNT_HUNDREDS
PRINT_HUNDREDS:
    PRINT_DEC        
    MOV DL,0                    ; same for decs
COUNT_DECS:
    CMP AX,10
    JB PRINT_DECS
    INC DL
    SUB AX,10
    JMP COUNT_DECS
PRINT_DECS:
    PRINT_DEC
    MOV DL,AL
    PRINT_DEC                   ; print units
    POP CX
    POP AX
    RET
PRINT_DEC_NUM ENDP

CODE ENDS

    END START                   ; inform the assembler that program starts from START tag
