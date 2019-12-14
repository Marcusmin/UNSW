assume cs:code, ds:data
data segment
	db 'welcome to a', 0
data ends
code segment
start:	mov dh, 10
		mov dl, 10
		mov cl, 2
		mov ax, data
		mov ds, ax
		mov si, 0
		mov es, 
		
		mov cx, offset do7end - offset do7
		 
		
		int 7ch
		mov ax, 4c00h
		int 21h
do7:	mov ax, 0b800h
		mov es, ax
		mov di, 0
		add di, dh * 160
		add di, dl * 36
		mov si, 0
		mov cx, 10
		
	s:	
		mov ax, cs
		mov ds, ax
		mov al, [si]
		mov es:[di], al
		mov es:[di+1], cl
		inc si
		add di, 2
		loop s
		
		mov ax, 4c00h
		int 21h

do7end:	nop
		
code ends
end start





