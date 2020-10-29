bits    32
global  main

extern  printf
extern  scanf

section .data
    format_d    db '%d', 0
    format_p_s  db '%d ',0
section .bss
    array       resd 100
    buff        resd 1

section .text
    main:
        mov     esi, 0                          ; clear size of array register
    scan_begin:
        lea     eax, [array+4*esi]              ; reach address of array element
        push    eax                             ; push argument
        push    format_d                        ; push formatted string
        call    scanf                           ; scanf
        add     esp, 8                          ; update stack
        cmp     eax, 1                          ; check if scanf raise error
        jne     scan_end                        ; end scanf if so
        cmp     esi, 100                        ; check if size not exceeded
        jge     scan_end                        ; end scanf if so
        inc     esi                             ; increase array size
        jmp     scan_begin                      ; jump if good
    scan_end:
        mov     edi, esi                        ; set first index(lesser)
    outer_begin:
        cmp     edi, 0                          ; check if greater than or equal zero
        jl      outer_end                       ; jump if less
        mov     ecx, esi                        ; set second index(bigger)
        sub     ecx, 1                          ; set second index(bigger)
        mov     ebx, ecx                        ; set second index(bigger)
    loop_begin:
        cmp     ebx, 0                          ; check if greater or equal zero
        jl      loop_end                        ; jump if not
        mov     eax, dword [array+4*(ebx-1)]    ; first into eax
        mov     edx, dword [array+4*ebx]        ; second into edx
        cmp     eax, edx                        ; if they are in the good order
        jl      end_if                          ; jump out
        mov     [array+4*(ebx-1)], edx          ; if not - exchange
        mov     [array+4*ebx], eax              ; if not - exchange
    end_if:                   
        dec     ebx                             ; decrement second index
        jmp     loop_begin                      ; loop again
    loop_end:
        dec     edi                             ; decrement first index
        jmp     outer_begin                     ; loop again
    outer_end:
        mov     ebx, 0                          ; clear array pointer
    print_begin:
        lea     eax, [array+ebx]                ; reach address of array element
        push    dword [eax]                     ; push argument
        push    format_p_s                      ; push formatted string
        call    printf                          ; printf
        add     esp, 8                          ; update stack
        add     ebx, 4                          ; move array pointer
        dec     esi                             ; decrement size
        cmp     esi, 0                          ; check if end of the array
        jne     print_begin                     ; print next number if there is one
    print_end:
        xor     eax, eax                        ; clear eax
        ret
