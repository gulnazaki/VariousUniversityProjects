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
    

CODE    SEGMENT
    ASSUME CS:CODE,DS:CODE,SS:CODE   
        
PRINT_NUMBER PROC
    CMP AX,0            ; if quotient is 0 don't print anything
    JE SKIP_NUMBER
PRINT_ANYWAY:
    PUSH DX             ; we save remainder temporarily
    MOV DX,AX           ; move to print
    ADD DL,30H          ; add ascii code
    MOV AH,2            
    INT 21H
    POP DX              ; restore remainder
    MOV BL,1            ; flag set to 1 (digit printed)
    JMP RESTORE
SKIP_NUMBER:
    CMP BL,1            ; is flag 1?
    JE PRINT_ANYWAY
RESTORE:
    MOV AX,DX           ; move remainder to A to divide again
    MOV DX,0            ; set DX to zero
    RET
PRINT_NUMBER ENDP    
       
MAIN PROC
    MOV CL,200          ; store 200 numbers
    FILL_1_TO_N         
    MOV DX,0000H        ; memory pointer set to 0
    MOV BX,0            ; sum of evens set to 0
    MOV SI,0            ; number of evens set to 0
    MOV CH,0            ; we may use CH if there is an overflow  
ADD_EVENS:
    IN AX,DX            ; get number from memory pointed by DX
    ADD DX,2            ; DX points to next 16bit memory space
    RCR AX,1            ; rotates number right setting carry to lsb
    JC SKIP             ; if carry = 1 number is odd
    RCL AX,1            ; restore number
    INC SI              ; evens++
    ADD BX,AX           ; sum += even
    JNC SKIP
    INC CH              ; if overflow increase CH holding most significant byte
SKIP:
    DEC CL              ; CL--
    JNZ ADD_EVENS    
CALCULATE_MEAN:
    MOV DH,0
    MOV DL,CH           ; msword of sum in DL
    MOV AX,BX           ; lsword of sum in AX
    MOV CX,SI           ; move number of evens to CX
    DIV CX              ; divide with number of evens and quotient is stored in AX, remainder in DX
    SUB CX,DX           ; we subtract remainder from divisor
    CMP DX,CX           ; we compare divisor-remainder with remainder (remainder<divisor/2)
    JL SHOW_RESULT      ; no need to "round"
    INC AL              ; increase quotient
SHOW_RESULT:
    MOV DX,0            ; we use it for division by 16-bit numbers
    MOV CX,10000        ; biggest 16bit number is 65535 so we divide by 10.000
    DIV CX
    MOV BL,0            ; flag set to 0 (no digit printed yet)              
    CALL PRINT_NUMBER
    MOV CX,1000
    DIV CX
    CALL PRINT_NUMBER    
    MOV CX,100
    DIV CX
    CALL PRINT_NUMBER 
    MOV CX,10
    DIV CX
    CALL PRINT_NUMBER
    CALL PRINT_NUMBER   ; print last digit
    MOV AX,4C00H
    INT 21H
MAIN ENDP

CODE ENDS
    END MAIN
    
