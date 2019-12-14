/*
 * lab3_1.asm
 *
 *  Created: 2019/10/18 22:56:52
 *   Author: M
 *	PF0:7 TO R0:C3 (KEYPAD)
 *	PC0:7 TO LED2:9
 */ 
 .include "m2560def.inc"

 .def num1 = r2
 .def num2 = r3
 .def numL = r4					; define r2, r3, r4 as Low, Medium, High byte of count number
 .def numM = r5
 .def numH = r6

 .def row = r16
 .def col = r17
 .def rmask = r18
 .def cmask = r19
 .def temp1 = r20
 .def temp2 = r21
 .def num_flag  = r22
 .def countL = r23				; define r17, r18, r19 as Low, Medium, High byte of cycle times
 .def countM = r24
 .def countH = r25

 .equ PORTFDIR = 0xF0
 .equ ROWMASK =0x0F 
 .equ INITCOLMASK = 0xEF
 .equ INITROWMASK = 0x01

 .macro carry
		ldi r28, 10
		mul @0, r28
		add r0, @1
		mov @0, r0
 .endmacro

 .macro	half_second_delay		; 1 cycle = 16MHz, 0.5s = 8 * 10^6 cycles
 	ldi r26, 0x01				; 1 cycle
	ldi r27, 0x00				; 1 cycle
	ldi countL, 0x37			; Low ,   count = 888887 == 0x0d9037
	ldi countM, 0x90			; Medium
	ldi countH, 0x0d			; High
	clr numL					; 1 cycle
	clr numM
	clr numH					; total 8 cycles
 loop:
	cp numL, countL				; 1 cycle
	cpc numM, countM			; 1 cycle
	cpc numH, countH			; 1 cycle
	brsh end_loop				; flase: 1 cycle ; True: 2 cycles
	add numL, r26				; 1 cycle
	adc numM, r27				; add carry 1 cycle
	adc numH, r27				; add carry 1 cycle
	rjmp loop					; 2 cycles
								; 5 cycles(final) + 9 * 888887
 end_loop:						
	nop							; 1 cycle
	nop							; 1 cycle
	nop							; 1 cycle
	nop							; 1 cycle
								; total = 8 + 9 * 888887 + 5 + 4 = 8 * 10^6 = 0.5s
.endmacro


 RESET:
		ldi temp1, PORTFDIR ; PF7:4/PF3:0, out/in
		out DDRF, temp1
		ser temp1 ; PORTC is output
		out DDRC, temp1
		out PORTC, temp1
		clr num_flag
		clr num1
		clr num2
		clr temp1

 
 main:
		ldi cmask, INITCOLMASK		;0xEF
		clr col

 colloop:
		cpi col, 4
		breq main
		out PORTF, cmask			

		ldi temp1, 0xFF ; slow down the scan operation.
 delay:	
		dec temp1
		brne delay
		in temp1, PINF
		andi temp1, ROWMASK			;0x0F
		cpi temp1, 0xF
		breq nextcol

		ldi rmask, INITROWMASK ; initialize for row check
		clr row

 rowloop:
		cpi row, 4
		breq nextcol ; the row scan is over.
		mov temp2, temp1
		and temp2, rmask ; check un-masked bit
		breq convert ; if bit is clear, the key is pressed
		inc row ; else move to the next row
		lsl rmask
		jmp rowloop

 nextcol: ; if row scan is over
		lsl cmask
		inc col ; increase column value
		jmp colloop

 convert:
		cpi  col, 3					; if column is 3 we have a letter
		breq letters
		cpi row, 3
		breq symbols
		mov temp1, row
		lsl temp1
		add temp1, row
		add temp1, col
		subi temp1, -1
		half_second_delay ;;;;;
		cpi num_flag, 0
		breq get_num1
		jmp get_num2

 letters:
		jmp RESET
		jmp main

 symbols:
		cpi col, 0 ; Check if we have a star
		breq star
		cpi col, 1 ; or if we have zero
		breq zero

 equal:
		mul num1, num2
		mov temp1, r1
		cpi temp1, 0
		brne overflow
		mov temp1, r0
		jmp display_result

 star:
		ldi num_flag, 1
		ser r28
		out PORTC, r28
		jmp main

 zero:
		ldi temp1, 0
		cpi num_flag, 0
		breq get_num1
		jmp get_num2

 get_num1:
		out PORTC, temp1
		carry num1, temp1
		jmp main

 get_num2:
		out PORTC, temp1
		carry num2, temp1
		jmp main

 overflow:
		ldi temp2, 0b01010101
		out PORTC, temp2	
		half_second_delay
		ldi temp2, 0b10101010
		out PORTC, temp2
		ldi temp2, 0b01010101
		half_second_delay
		out PORTC, temp2
		jmp RESET

 display_result:
		out PORTC, temp1				; display Result 
		jmp display_result	

		
		
