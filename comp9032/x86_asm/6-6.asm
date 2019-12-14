assume cs:code

a segment

    dw 1,2,3,4,5,6,7,8,9,0ah,0bh,0ch,0dh,0eh,0fh,0ffh

a ends

 

b segment

    dw 0,0,0,0,0,0,0,0

b ends

code segment

start:

    mov ax,a

    mov ds,ax        ;ds指向a段

 

    mov ax,b

    mov ss,ax        ;ss指向了b段

    mov sp,16        ;初始化栈顶，ss：sp指向了栈顶，意味着b段是个栈结构了。

 

    mov bx,0

    mov cx,8        

s:

    push ds:[bx] ;直接将a段中的字单元内存压栈即可。这样在栈中的存储结构就是逆序的

    add bx,2

    loop s

 

    mov ax,4c00h

    int 21h

code ends

end start
