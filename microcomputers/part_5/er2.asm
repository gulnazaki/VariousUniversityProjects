PRINT_CHAR MACRO CHAR
    MOV DL,CHAR             ; character's ascii code
    MOV AH,2
    INT 21H
ENDM

PRINT_ERROR MACRO
    MOV DX,100H             ; error's address
    MOV AH,9
    INT 21H
ENDM 

PRINT_NEWLINE MACRO
    PRINT_CHAR 0AH
    PRINT_CHAR 0DH
ENDM
    
READ_NUM MACRO REG
    MOV AH,8
    INT 21H
    CMP AL,0DH              ; checks if enter was pressed before it was supposed
    JE WRONG_INPUT
    SUB AL,30H              ; - 30H to find number form ascii code (in AL)
    MOV REG,AL              ; move to parameter register
ENDM

READ_ENTER MACRO
    MOV AH,8
    INT 21H
    CMP AL,0DH              ; if not enter print error and start all over
    JE SECOND_PHASE
    PRINT_NEWLINE
    PRINT_ERROR
    PRINT_NEWLINE
    JMP START
ENDM


DATA    SEGMENT
    ERROR DB    "ERROR! Enter two 2-digit numbers and then press enter$"                                      
DATA    ENDS
  
  
CODE    SEGMENT
    ASSUME CS:CODE,DS:DATA      

READ PROC
START_READING:
    READ_NUM BH             ; read first digit and store it to BH
    READ_NUM BL             ; read second digit and store it to BL
    READ_NUM CH             ; read third digit and store it to CH
    READ_NUM CL             ; read second digit and store it to CL
    RET
WRONG_INPUT:
    PRINT_ERROR
    PRINT_NEWLINE
    JMP START_READING
READ ENDP

PRINT_A PROC
    PRINT_CHAR 'Z'
    PRINT_CHAR '='
    ADD BH,30H              ; first digit's ascii code
    PRINT_CHAR BH
    SUB BH,30H              ; digit's value
    ADD BL,30H
    PRINT_CHAR BL
    SUB BL,30H
    PRINT_CHAR ' '
    PRINT_CHAR 'W'
    PRINT_CHAR '='
    ADD CH,30H              ; first digit's ascii code
    PRINT_CHAR CH
    SUB CH,30H              ; digit's value
    ADD CL,30H
    PRINT_CHAR CL
    SUB CL,30H
    RET
PRINT_A ENDP

PRINT_B PROC
    PRINT_CHAR 'Z'
    PRINT_CHAR '+'
    PRINT_CHAR 'W'
    PRINT_CHAR '='
    MOV AL,BH               ; moves number to AL to print it
    CALL PRINT_HEX_NUM
    PRINT_CHAR ' '
    PRINT_CHAR 'Z'
    PRINT_CHAR '-'
    PRINT_CHAR 'W'
    PRINT_CHAR '='   
    MOV AL,BL               ; moves number to AL to print it
    CALL PRINT_HEX_NUM
    PRINT_NEWLINE
    RET
PRINT_B ENDP

PRINT_HEX_NUM PROC
    CALL IS_NEGATIVE?
    MOV AH,0                ; helps at division
    MOV CL,16               ; we divide by 16
    DIV CL
    MOV DL,AL               ; move first hexdigit to DL to print
    CMP DL,10               ; compare to 10
    JL NUM1                 ; if 0-9 go to NUM1
    ADD DL,7H               ; else add 7H and we then we add 30H, sum of 37H 'A'
NUM1:
    ADD DL,30H              ; make ascii number
    MOV DH,AH               ; remainder stored in DH temporarily
    MOV AH,2
    INT 21H
    MOV DL,DH               ; move second hexdigit to DL to print
    CMP DL,10               ; compare to 10
    JL NUM2                 ; if 0-9 go to NUM2
    ADD DL,7H               ; else add 7H and we then we add 30H, sum of 37H 'A'
NUM2:
    ADD DL,30H              ; make ascii number
    MOV AH,2
    INT 21H
    RET
PRINT_HEX_NUM ENDP

IS_NEGATIVE? PROC
    ROL AL,1                 ; rotate AL left to see if negative
    JNC POSITIVE            ; if first bit is 0 we are okay
    ROR AL,1  
    NEG AL
    PUSH AX
    PRINT_CHAR '-'
    POP AX
    ROL AL,1
POSITIVE:
    ROR AL,1
    RET
IS_NEGATIVE? ENDP

CREATE_FIRST_NUMBER PROC
    MOV AL,BH               ; move first digit to AL
    MOV DL,10               ; we will multiply by 10
    MUL DL
    ADD BL,AL               ; first number created
    RET
CREATE_FIRST_NUMBER ENDP

CREATE_SECOND_NUMBER PROC            
    MOV AL,CH               ; move first digit to AL
    MOV DL,10               ; we will multiply by 10
    MUL DL
    ADD CL,AL               ; first number created
    RET
CREATE_SECOND_NUMBER ENDP

MAIN PROC
START:
    CALL READ
    CALL PRINT_A
    READ_ENTER    
SECOND_PHASE:
    PRINT_NEWLINE
    CALL CREATE_FIRST_NUMBER   ; create first number and store it in BL
    CALL CREATE_SECOND_NUMBER  ; create second number and store it in CL
    MOV BH,BL
    ADD BH,CL               ; BH contains sum
    SUB BL,CL               ; BL contains difference
    CALL PRINT_B
    JMP START
    
    MOV AX,4C00H
    INT 21H
MAIN ENDP

CODE    ENDS
    END MAIN
    
