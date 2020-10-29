bits    32
global  main

extern  printf
extern  scanf

section .data
    format_d    db '%lf', 0                 ; string format
    format_p_s  db 'sqrt(%lf) = %lf ',10,0  ; string format
    start_val   dq 0.0                      ; starting value
    buff        dq 0.0                      ; temporary buffer
    off         dq 0.125                    ; single step constant

section .bss
    maxi        resq 1                      ; end value
    
section .text
    main:            
        push    maxi                        ; push end value
        push    format_d                    ; push formatted string 
        call    scanf                       ; scanf
        add     esp, 8                      ; clear stack
        fld     qword[maxi]                 ; push on stack max value
        fld     qword[off]                  ; push on stack step
        fld     qword[start_val]            ; push on stack start value
        fld     qword[buff]                 ; push on stack buffer
    begin:                                  ; loop begin
        fcomi    st3                        ; if max value is reached
        jnc     end                         ; jump out of the loop
        fsqrt                               ; if not take sqrt(buffer)
        sub     esp,8                       ; make place on stack for result
        fst     qword [esp]                 ; place it on stack
        fxch    st1                         ; exchange st0 and st1
        sub     esp,8                       ; make place on stack for the number we are taking the square root of
        fst     qword [esp]                 ; store that value on stack
        push    format_p_s                  ; push formatted string
        call    printf                      ; printf 
        add     esp, 20                     ; clear stack
        fadd    st0,st2                     ; add 0.125 to the number we are taking square root of
        fst     st1                         ; place in st0 new value to sqare root
        fxch    st1                         ; exchange st0 and st1
        jmp     begin                       ; loop again
    end:
        xor     eax, eax                    ; xor eax
        ret
