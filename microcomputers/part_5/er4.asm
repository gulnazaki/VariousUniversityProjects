PRINT_NEWLINE MACRO
    MOV DL,0AH
    MOV AH,2
    INT 21H
    MOV DL,0DH
    MOV AH,2
    INT 21H
ENDM
  
  
DATA    SEGMENT
    TABLE DB    20 DUP(?)  ; we declare a 20 byte table to store characters
DATA    ENDS
   
   
CODE    SEGMENT
    ASSUME CS:CODE,DS:DATA      

READ_CHAR PROC
READ:
    MOV AH,8
    INT 21H
    CMP AL,'='              ; if = is pressed terminate program
    JE PROGRAM_END
    CMP AL,0DH              ; if ENTER is pressed don't print and just return 0
    JE ENTER_PRESSED
    CMP AL,'0'              ; if char less than 0 then ignore and read again
    JL READ
    CMP AL,'z'              ; if char above(unsigned) than z read again
    JA READ
    CMP AL,'9'              ; if char is 9 or below we are ok
    JLE OK
    CMP AL,'a'              ; else check if less than a then read again
    JL READ
OK:
    MOV AH,2
    MOV DL,AL
    INT 21H
    MOV AL,DL               ; after we print we store to AL to return ascii code
    RET
ENTER_PRESSED:
    MOV AL,0                ; we return 0
    RET
PROGRAM_END:
    MOV AX,4C00H
    INT 21H
READ_CHAR ENDP

PRINT_CHAR PROC
    CMP DL,'9'
    JLE NUM
    SUB DL,20H              ; convert to uppercase
NUM:
    MOV AH,2                ; just print
    INT 21H
    RET
PRINT_CHAR ENDP

MAIN PROC
    MOV AX,DATA
    MOV DS,AX
START:
    MOV CX,20               ; we will read 20 chars max            
    MOV DI,0                ; first table element
READ_LOOP:
    CALL READ_CHAR
    CMP AL,0                ; if ENTER was pressed READ_CHAR returns 0 so break the loop
    JE PRINT_UPPER
    MOV TABLE[DI],AL        ; we store character in table
    INC DI                  ; DI points to next table element
    LOOP READ_LOOP
PRINT_UPPER:
    PRINT_NEWLINE
    MOV CX,DI               ; we will loop for number of characters
    MOV DI,0                ; we iterate to first table element again
PRINT_LOOP:
    MOV DL,TABLE[DI]        ; we move char we want to print to DL
    CALL PRINT_CHAR
    INC DI                  ; DI points to next element
    LOOP PRINT_LOOP
    PRINT_NEWLINE     
    JMP START
MAIN ENDP

CODE    ENDS
    END MAIN
    
