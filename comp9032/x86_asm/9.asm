assume cs:code, ds:data, ss:stack
data segment
	db 'fuck you!'
	db 02h, 71h, 24h
data ends

stack segment
	db 10 dup(0)
stack ends

code segment
start: 	
	mov ax, data
	mov ds, ax
	
	mov ax, stack
	mov ss, ax
	mov sp, 0
	
	mov cx, 3
	mov bx, 1980
	mov si, 0
	mov di, 9
	mov ax, 0B800h
	mov es, ax
s0:	push cx
	mov cx, 9
		
s:	mov al, ds:[si]
	mov es:[bx], al
	mov ah, ds:[di]
	mov es:[bx+1], ah
	add bx, 2
	inc si
	loop s
	
	add bx, 160
	mov si, 0
	inc di		
	pop cx
	loop s0
	
	mov ax,4c00h
	int 21h
code ends
end start 



