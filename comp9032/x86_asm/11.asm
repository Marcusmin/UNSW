assume cs:code, ds:data

data segment
	db 'hello my lover', 0
data ends

code segment
	start:	mov ax, data
			mov ds, ax
			mov si, 0
			call letterc
			
			mov ax, 4c00h
			int 21h
	letterc:
			push cx
			pushf
			mov cx, 0
	s:		mov cl, [si]
			jcxz ok
			cmp cl, 'a'
			ja next
			cmp cl, 'z'
			jb next
			and cl, 0dfh
			mov [si], cl
	next:	inc si
			jmp short s			
	ok:		popf
			pop cx
			ret
	
code ends
end start
