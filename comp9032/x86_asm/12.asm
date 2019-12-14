assume cs:code

code segment

start:	mov ax, 0
		mov es, ax
		mov di, 200h
		mov ax, cs
		mov ds, ax
		mov si, offset do0
		mov cx, offset do0end - offset do0
		cld
		rep movsb
		
		mov ax, 0
		mov es, ax
		mov word ptr es:[0*4], 200h
		mov word ptr es:[0*4+2], 0
		int 0h
		mov ax, 4c00h
		int 21h
		
do0:	jmp short do0start
		db 'wrong'

do0start:	mov ax, 0b800h
			mov es, ax
			mov di, 160*12+36*2
			mov ax, cs
			mov ds, ax
			mov si, 202h
			mov cx, 5
		s:	mov al, [si]
			mov es:[di], al
			inc si
			add di, 2
			loop s
			
			mov ax, 4c00h
			int 21h		

do0end:	nop

code ends
end start
