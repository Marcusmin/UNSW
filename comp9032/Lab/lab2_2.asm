/*
 * lab2_2.asm
 *
 *  Created: 2019/10/12 17:39:47
 *   Author: Min
 */
 .include "m2560def.inc" 
 .def numL = r2					; define r2, r3, r4 as Low, Medium, High byte of count number
 .def numM = r3
 .def numH = r4
 .def countL = r17				; define r17, r18, r19 as Low, Medium, High byte of cycle times
 .def countM = r18
 .def countH = r19
 .def LED1 = r22				; define r22, r23, r24 as LED 1 2 3
 .def LED2 = r23
 .def LED3 = r24

 .equ PATTERN1 = 0b00100010		; LED display pattern
 .equ PATTERN2 = 0b01000100
 .equ PATTERN3 = 0b10001000 

 .macro	half_second_delay		; 1 cycle = 16MHz, 0.5s = 8 * 10^6 cycles
 	ldi r20, 0x01				; 1 cycle
	ldi r21, 0x00				; 1 cycle
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
	add numL, r20				; 1 cycle
	adc numM, r21				; add carry 1 cycle
	adc numH, r21				; add carry 1 cycle
	rjmp loop					; 2 cycles
								; 5 cycles(final) + 9 * 888887
 end_loop:						
	nop							; 1 cycle
	nop							; 1 cycle
	nop							; 1 cycle
	nop							; 1 cycle
								; total = 8 + 9 * 888887 + 5 + 4 = 8 * 10^6 = 0.5s
.endmacro

.macro display					; display LED
	out PORTC, @0				; send pattern to output portC
	sbis PIND, 0				; check if the bit is set
	rjmp end					; if yes skip the next instruction and continue displaying	
.endmacro

main:
	cbi DDRD, 0					; set port D bit 0 for input (button signals)
	sbi PORTD, 0				; activate the pull up
	ser r16
	out DDRC, r16				; set Port C for output
	ldi LED1, PATTERN1			; load the display pattern
	ldi LED2, PATTERN2
	ldi LED3, PATTERN3


display_1:
	display LED1				; display 0b00100010 in lab bar
	half_second_delay			; wait one second

check_1:
	sbic PIND,0					; check if that bit is clear ; if yes skip the next instruction
	rjmp display_2				; rjmp to display_2
	rjmp check_1				; loop justify input

display_2:
	display LED2				; display 0b01000100 in lab bar
	half_second_delay			; wait one second

check_2:
	sbic PIND,0					; check if that bit is clear ; if yes skip the next instruction
	rjmp display_3				; rjmp to display_3
	rjmp check_2				; loop justify input

display_3:
	display LED3				; display 0b10001000 in lab bar
	half_second_delay			; wait one second

check_3:
	sbic PIND,0					; check if that bit is clear ; if yes skip the next instruction
	rjmp display_1				; rjmp to display_1
	rjmp check_3				; loop justify input

end:
	rjmp end

