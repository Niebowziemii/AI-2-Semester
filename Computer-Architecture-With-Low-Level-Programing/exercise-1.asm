bits    32
global  main

extern  printf
extern  scanf

section .data
    format_s   db '%1023[0-9a-zA-Z ]', 0
    format_p   db '%s',0
    input      times 1024 db 0
    output     times 1024 db 0

section .text
    main:
        push    input           ; push argument
        push    format_s        ; push formatted string
        call    scanf           ; scanf
        add     esp, 8          ; clear stack
        lea     esi, [input]    ; get input address
        lea     edi, [output]   ; get output address
        times 1024 movsb        ; move 1024 bytes from esi to edi
        push    output          ; push argument
        push    format_p        ; push formatted string
        call    printf          ; printf
        add     esp, 8          ; clear stack
        xor     eax, eax        ; clear eax
        ret                     ; return
