FILL_1_TO_N MACRO     
    MOV BL,CL           ; move CL to BL to retrieve it later
    MOV DX,0000H        ; memory pointer set to 0
    MOV AX,1000         ; first number we are saving is 1.000
SAVE_NUMBERS:
    OUT DX,AX           ; save number to memory pointed by DX
    ADD DX,2            ; DX points to next 16bit memory space
    INC AX              ; next number
    LOOP SAVE_NUMBERS   ; loops N times (CL contaains N)
    MOV CL,BL           ; retrieve CL
ENDM

PRINT_SPACE MACRO
    MOV DL,32           ; DL set to space ascii
    MOV AH,2
    INT 21H
ENDM
    

CODE    SEGMENT
    ASSUME CS:CODE,DS:CODE,SS:CODE      

PRINT_CHAR PROC
    CMP DL,10           ; compare hex to 10
    JL NUM              ; if 0-9 go to NUM
    ADD DL,7H           ; else add 7H and we then we add 30H, sum of 37H 'A'
NUM:
    ADD DL,30H          ; make ascii number
    MOV AH,2
    INT 21H
    RET
PRINT_CHAR ENDP
       
PRINT_HEX PROC
    MOV DL,AH           ; move first byte to DL
    AND DL,0F0H         ; keep only first 4 bits (hexadigit)
    ROR DL,4            ; make them lsb
    PUSH AX
    CALL PRINT_CHAR
    POP AX
    MOV DL,AH           ; move first byte to DL
    AND DL,0FH          ; keep only second 4 bits (hexadigit)
    PUSH AX
    CALL PRINT_CHAR
    POP AX
    MOV DL,AL           ; move second byte to DL
    AND DL,0F0H         ; keep only third 4 bits (hexadigit)
    ROR DL,4            ; make them lsb
    PUSH AX
    CALL PRINT_CHAR
    POP AX
    MOV DL,AL           ; move second byte to DL
    AND DL,0FH          ; keep only fourth 4 bits (hexadigit)
    CALL PRINT_CHAR
    RET
PRINT_HEX ENDP

MAIN PROC
    MOV CL,200          ; store 200 numbers
    FILL_1_TO_N         
    MOV DX,0000H        ; memory pointer set to 0
    MOV BX,0            ; we will use BX to keep the max
    MOV SI,0FFFFH       ; we will use SI to keep the min (initialise at biggest 2byte number)
    MOV CH,0            ; will use CX for loop
FIND_MIN_MAX:
    IN AX,DX            ; load number from memory
    ADD DX,2            ; DX points to next memory pair
    CMP AX,BX           ; compare current number to max
    JBE NOT_MAX         ; jump below or equal (unsigned)
    MOV BX,AX           ; make number new max
NOT_MAX:
    CMP AX,SI           ; compare current number to min
    JAE NOT_MIN         ; jump above or equal we use unsigned numbers
    MOV SI,AX           ; make number new min
NOT_MIN:
    LOOP FIND_MIN_MAX
PRINT_NOW:
    MOV AX,BX           ; move max to AX
    CALL PRINT_HEX
    PRINT_SPACE
    MOV AX,SI           ; move min to AX
    CALL PRINT_HEX    

    MOV AX,4C00H
    INT 21H
MAIN ENDP

CODE ENDS
    END MAIN
    
