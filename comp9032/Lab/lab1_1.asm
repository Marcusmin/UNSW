/*
 * lab1_1.asm
 *
 *  Created: 2019/9/21 20:06:10
 *   Author: Min & Ricky 
 */ 
 .include "m2560def.inc"
 .def	code1 = r16				; define code1 as r16 
 .def	code2 = r17				; define code2 as r17
 .def	num1 = r18				; define num1 as r18
 .def	num2 = r19				; define num2 as r19
 .def	temp = r20				; define temp as r20

 .macro convert
	cpi @0, 0b10000000			; whether the digital is hexadecimal number
	brsh hexD					; if hexadecimal number branch to hexD
	subi @0, 0x30				; if it is decimal number, subtract 0x30 (0's Hex)
	rjmp transfer				; banrch to transfer
	hexD:						; hexadecimal digital 0 ~ 9 stream
		subi @0, 0b10000000		; subtract the signal hex
		clr temp				
		ldi temp, 0x40			
		cp  temp, @0			; whether the digital is A to F
		brlo hexA				; if the digital is A to F, brach to HexA
		subi @0, 0x30			; if the digital is 0 to 9, subtract 0x30 (0's Hex)
		rjmp transfer			; banrch to transfer
	hexA:						; hexadecimal (A to F) stream
		clr temp
		ldi temp, 0xA			; load 'A' bin value
		subi @0, 0x41			; subtract 0x41 (A's Hex)
		add @0, temp			; add 'A' bin value into the difference between number and 'A' 
	transfer:
		mov @1, @0				; move bin number
 .endmacro

 main:
	ldi code1, 0b10111000
	ldi code2, 0b11000010
	convert code1, num1			; macro running, convert hex or dec to bin
	convert code2, num2
	ldi temp, 1					; temp = 1, loop counter

 loop:							; the first number left shift 4 bits
	cpi temp, 5					; compare temp and 5
	brge sum					; if temp >= 5, branch to sum
	inc temp					; temp++
	lsl num1					; left shift 1 bit
	rjmp loop					; jump to loop

 sum:
	add num1, num2				; make 2 nums into one
								; result = 1st number's left four bits + 2nd number's right four bits
 end:
	rjmp end

