assume cs:code, ds:a, es:b, ss:d
a segment
	db 1,2,3,4,5,6,7,8
a ends

b segment
	db 1,2,3,4,5,6,7,8
b ends

d segment
	db 1,2,3,4,5,6,7,8
d ends

code segment
start:
	mov cx, 8
	mov ax, a
	mov ds, ax
	mov ax, b
	mov es, ax
	mov ax, d
	mov ss, ax
	mov bx, 0
s:	mov al, ds:[bx]
	add al, es:[bx]
	mov ss:[bx], al
	inc bx
	loop s
	
	mov ax, 4c00H
	int 21H
code ends
end start
