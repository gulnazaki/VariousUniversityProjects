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

UPDATE_RESULT MACRO
    PUSH AX                     ; else result = result*10 + AL
    MOV AX,BX
    POP BX
    MUL CL
    ADD AX,BX                   ; AX = updated result
    MOV BX,AX                   ; store result in BX
ENDM

EXIT MACRO                      ; exits program
    MOV AX, 4C00H
    INT 21H
ENDM

STACK SEGMENT
    DB 10 DUB(?)
STACK ENDS

CODE SEGMENT
    ASSUME CS:CODE, SS:STACK
     
START:
    MOV CH,0                    ; our digits counter
    MOV CL,10                   ; a multiplier we will use
    MOV AX,0                    ; initialise accumulator
    MOV BX,0                    ; initialise are result storage
    
READ_FIRST:
    CALL DEC_KEYB               ; read first dec digit
    CMP AL,'Q'                  ; check if termination is in order
    JE EXIT_PROGRAM
    
    CMP AL,'+'
    JE TO_SECOND                ; if we read '+', we go to next number
    CMP AL,'-'
    JE TO_SECOND                ; same for '-' 
    
    UPDATE_RESULT               ; else, update result
    
    JMP READ_FIRST
    
TO_SECOND:
    PUSH AX                     ; store +/- in stack for later
    MOV CH,0                    ; reset digits counter
    MOV DX,BX                   ; store 1st number in DX to use BX for the second
    MOV BX,0                    ; initialise result storage
    
READ_SECOND:
    CALL DEC_KEYB
    CMP AL,'Q'
    JE EXIT_PROGRAM
    
    CMP AL,'='
    JE CALCULATE
    
    UPDATE_RESULT
    
    JMP READ_SECOND

;;; at this point, first number is in DX and second in BX ;;;

CALCULATE:
    POP AX                      ; restore +/-
    MOV AX,DX
    CALL PRINT_DEC_NUM
    MOV AX,BX
    CALL PRINT_DEC_NUM
    
    
    ;JMP START
    
EXIT_PROGRAM:    
    EXIT                        ; return to OS    

;;; routines ;;;

DEC_KEYB PROC NEAR              ; reads digit+checks if it's valid (0-9) and prints it
IGNORE:
    READ                        ; read digit
    CMP AL,'+'                  ; if we read a '+'
    JE PRINT_SYMBOL             ; we return
    CMP AL,'-'                  ; same for '-'
    JE PRINT_SYMBOL
    CMP AL,'='                  ; same for '='
    JE PRINT_SYMBOL
    CMP AL,'Q'                  ; same fo 'Q'
    JE RETURN
    SUB AL,30H                  ; check if 0<=digit<=9
    CMP AL,0
    JB IGNORE                   ; if digit<0 ignore and read next
    CMP AL,9
    JA IGNORE                   ; if digit>9 ignore and read next
PRINT_DIGIT:
    INC CH                      ; digits counter--
    CMP CH,3                    ; if we have read more than 3 digits, no more allowed
    JG IGNORE
    ADD AL,30H
    PRINT_CHAR AL
    SUB AL,30H
    JMP RETURN
PRINT_SYMBOL:
    CMP CH,0                    ; the first input we will read must be a digit
    JE IGNORE
    PRINT_CHAR AL
RETURN:
    MOV AH,0                    ; 00-AL->AX
    RET                         ; return number in AL
DEC_KEYB ENDP

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
