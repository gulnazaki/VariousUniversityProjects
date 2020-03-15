PRINT_STR MACRO STRING
    LEA DX,STRING       ; load string address
    MOV AH,9            ; orint string routine
    INT 21H
ENDM 

PRINT_NEWLINE MACRO
    MOV DL,0AH          ; print 0AH,0DH (newline)
    MOV AH,2
    INT 21H
    MOV DL,0DH
    MOV AH,2
    INT 21H
ENDM

PRINT_CHAR MACRO CHAR
    MOV DL,CHAR         ; print char (parameter = ascii code)
    MOV AH,2
    INT 21H
ENDM

READ_NUM MACRO REG
    MOV AH,8            ; read char routine
    INT 21H
    CMP AL,'='          ; end program if =
    JE PROGRAM_END
    CMP AL,0DH
    JE ENTER_PRESSED    ; jump to enter pressed if it is pressed          
    MOV REG,AL              
ENDM
  
  
DATA    SEGMENT
    START_MSG DB "Insert characters, numbers or spaces [= ends program]: ",0AH,0DH,"$"
    WAIT_MSG  DB 0AH,0DH,"14 characters already filled please press <ENTER>: $"
    ARRAY     DB 14 DUP(?)                                      
DATA    ENDS
  
  
CODE    SEGMENT
    ASSUME CS:CODE,DS:DATA      
     
READ PROC
    MOV DI,0            ; DI used as array offset
INPUT:
    READ_NUM BL         ; read a char
    CMP BL,' '          ; if it is a space go to OK
    JE OK
    CMP BL,'0'          ; if less than 0 ascii code invalid
    JL INPUT
    CMP BL,'9'          ; if it is 0-9 then OK
    JLE OK
    CMP BL,'A'          ; if less than A invalid
    JL INPUT
    CMP BL,'Z'          ; if A-Z OK
    JLE OK
    CMP BL,'a'
    JL INPUT            ; if less than a invalid
OK:
    MOV ARRAY[DI],BL    ; store in array
    PRINT_CHAR BL       ; print character
    INC DI              ; i++
    CMP DI,14           ; if we are at 14 tell the user to press enter
    JNE INPUT
    PRINT_STR WAIT_MSG
WAIT_ENTER:
    READ_NUM BL
    JMP WAIT_ENTER
ENTER_PRESSED:
    MOV CX,DI           ; we store the number of characters
    PRINT_NEWLINE
    RET
READ ENDP

PRINT_2ND_LINE PROC
    MOV DI,0            
    MOV BX,0            ; BL=BH=0, here we store the two biggest numbers' ascii code
CHECK_1:    
    MOV AL,ARRAY[DI]    ; retrieve from array
    CMP AL,' '          ; if space just skip it
    JE SKIP_1
    CMP AL,'9'          ; if more than 9 skip it
    JG SKIP_1
    CALL FIND_3RD_LINE  ; check for biggest numbers
    PRINT_CHAR AL       ; if a num print it
SKIP_1:
    INC DI              ; i++
    CMP DI,CX           ; if end of array reached print a space and go on
    JNE CHECK_1
    PRINT_CHAR ' '
    MOV DI,0
CHECK_2:
    MOV AL,ARRAY[DI]
    CMP AL,' '          ; skip space
    JE SKIP_2
    CMP AL,'Z'          ; skip more than Z
    JG SKIP_2
    CMP AL,'A'          ; skip less than A
    JL SKIP_2
    PRINT_CHAR AL
SKIP_2:
    INC DI
    CMP DI,CX
    JNE CHECK_2
    PRINT_CHAR ' '
    MOV DI,0
CHECK_3:
    MOV AL,ARRAY[DI]
    CMP AL,' '          ; skip space
    JE SKIP_3
    CMP AL,'z'          ; skip more than z
    JG SKIP_3
    CMP AL,'a'          ; skip less than a
    JL SKIP_3
    PRINT_CHAR AL
SKIP_3:
    INC DI
    CMP DI,CX
    JNE CHECK_3
    PRINT_NEWLINE
    RET
PRINT_2ND_LINE ENDP
                    
FIND_3RD_LINE PROC
    CMP AL,BL           ; we compare this number to our 2nd (in order) biggest
    JL LESS_THAN_2ND    ; if less go to LESS_THAN_2ND
    CMP AL,BH
    JL CHANGE_2ND       ; if less than the 1st change the 2nd
    MOV BH,BL           ; else "shift"
    MOV BL,AL
    JMP GO_ON
CHANGE_2ND:
    MOV BL,AL
    JMP GO_ON
LESS_THAN_2ND:
    CMP AL,BH
    JL GO_ON            ; if less than 2nd and less than 1st just leave
    MOV BH,BL           ; else "shift"
    MOV BL,AL
GO_ON:    
    RET
FIND_3RD_LINE ENDP

PRINT_3RD_LINE PROC     ; just print our numbers
    PRINT_CHAR BH
    PRINT_CHAR BL
    PRINT_NEWLINE
    RET
PRINT_3RD_LINE ENDP

MAIN PROC
START:
    MOV AX,DATA         ; data segmnent
    MOV DS,AX
    PRINT_STR START_MSG ; welcome message
    CALL READ           ; read
    CALL PRINT_2ND_LINE ; print 2nd and 3rd lines
    CALL PRINT_3RD_LINE
    JMP START
PROGRAM_END:
    MOV AX,4C00H
    INT 21H     
MAIN ENDP    
     
CODE    ENDS
    END MAIN