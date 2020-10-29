bits    32
global  main

extern  printf
extern  scanf

section .data
    format_d    db '%lf %lf', 0                 ; string format
    format_p_s  db 'e^x = %lf',10,0             ; string format
    series      dq 1.0                          ; series
    numerator   dq 1.0                          ; numerator
    denominator dq 1.0                          ; denominator
    counter     dq 1.0                          ; loop counter
    buffer      dq 0.0                          ; temporary buffer

section .bss
    k           resq 1                          ; k sum elements
    x           resq 1                          ; the power of e
    
section .text
    main:            
        push    x                               ; push power 
        push    k                               ; push num of elements in the sum
        push    format_d                        ; push formatted string 
        call    scanf                           ; scanf
        add     esp, 12                         ; clear stack
        fld     qword[counter]                  ; push loop counter on stack
        fld     qword[k]                        ; push num of el on stack
        fld     qword[x]                        ; push power of e on stack
        fld     qword[series]                   ; push series accumulator on stack
        fld     qword[denominator]              ; push denominator on stack
        fld     qword[numerator]                ; push numerator on stack
        fld     qword[buffer]                   ; push buffer on stack
    begin:
        fxch    st0,st6                         ; put counter in st0
        fcomi   st5                             ; compare it with k
        fxch    st0,st6                         ; put it back
        jle      end                            ; if counter>k then jump
        fxch    st1                             ; put numerator in st0
        fmul    st4                             ; multiply by x
        fxch    st1                             ; put it back
        fxch    st2                             ; put denominator in st0
        fmul    st6                             ; multiply by counter
        fxch    st2                             ; put it back
        fxch    st1                             ; put numerator in st0
        fst     st1                             ; copy st1 to st0
        fdiv    st0, st2                        ; divide numerator and denominator
        fadd    st3, st0                        ; add new element to the series
        fld1                                    ; put 1 on stack
        faddp   st7,st0                         ; add it to counter and pop st0
        jmp     begin                           ; loop again
    end:    
        fxch    st0,st3                         ; put series in st0
        sub     esp, 8                          ; make place on stack
        fst     qword [esp]                     ; put it on stack
        push    format_p_s                      ; put formatted string
        call    printf                          ; printf
        add     esp,12                          ; clear stack
        xor     eax, eax                        ; xor eax
        ret
