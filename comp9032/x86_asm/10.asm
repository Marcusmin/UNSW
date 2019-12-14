assume cs:code

data segment
	db 'fuck you!',0
data ends

code segment
start:	mov dh,8
		mov dl,3
		mov cl,2
		mov ax,data
		mov ds,ax
		mov si,0
		call show_str
		
		mov ax,4c00h
		int 21h
show_str:	
			mov ax, 0B800h
			mov es, ax
			mov di, 0
			mov cx, 3
			
			mov al, 160
			mul dh
			add di, ax
			
			mov al, 2
			mul dl
			add di, ax
		s:	push cx
			mov cx, 9
		s0:	mov al, [si]
			mov es:[di], al
			mov es:[di+1], cl
			add di, 2
			inc si
			loop s0
			mov si, 0
			add di, 142
			pop cx
			loop s
			ret
			
			

code ends
end start





