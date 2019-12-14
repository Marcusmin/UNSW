/*
 * assignment.asm
 *
 *  Created: 2019/11/01 22:56:52
 *   Author: Weijia Min
 *	
*/

; Board settings: 
; PF0:7 -> R0:C3 (KEYPAD)
; PD0:7 (LCD DATA) -> PC7:0	   
; BE:RS(LCD CTRL) -> PA4:7
; LED8:9 -> PL4
; LED6:7 -> PE6
; LED4:5 -> PE5 
; LED2:3 -> PH11
; INPUTS PB0 -> PD RDX4

.include "m2560def.inc"

.def central = r2						; define r2 as central control
.def button_press = r4					; define r4 to justify whether the button is released or not

.def w1 = r16							; define r16 as window1 local control
.def w2 = r17							; define r17 as window2 local control
.def w3 = r18							; define r18 as window3 local control
.def w4 = r19							; define r19 as window4 local control
.def temp1 = r20						; define r20 to store temp values
.def row = r21							; current row number
.def col = r22							; current column number
.def rmask = r23						; mask for current row during scanning
.def cmask = r24						; mask for current column during scanning
.def temp2 = r25						; define r25 to store temp values


.equ LCD_RS = 7							; LCD RS bit position
.equ LCD_E  = 6							; LCD E bit position
.equ LCD_RW = 5							; LCD RW bit position
.equ LCD_BE = 4							; LCD BE bit position
.equ PORTFDIR = 0xF0					; PF7-4: output, PF3-0, input
.equ ROWMASK =0x0F						; scan from the leftmost column,
.equ INITCOLMASK = 0xEF					; scan from the top row
.equ INITROWMASK = 0x01					; for obtaining input from Port F

.macro lcd_set							; set LCD bit
	sbi PORTA, @0
.endmacro

.macro lcd_clr							; clr LCD bit
	cbi PORTA, @0
.endmacro


.macro do_lcd_command					; send a command to LCD
	push r16							; push r16 in stack
	ldi   r16, @0						; load the command to r16
	rcall lcd_command					; send r16 to PORTC
	rcall lcd_wait						; check LCD busy or not
	pop r16								; pop r16 from stack
.endmacro

.macro do_lcd_data						; send a data to LCD
	push r16							; push r16 in stack
	ldi   r16, @0						; load the data to r16
	rcall lcd_data						; send r16 to PORTC
	rcall lcd_wait						; check LCD busy or not
	pop r16								; pop r16 from stack
.endmacro

.macro do_lcd_data_num					; send a ASCII data to LCD
	push r16							; push r16 in stack
	mov r16, @0							; load the data
	subi r16, -'0'						; convert it to ASCII
	rcall lcd_data						; send data to PORTC
	rcall lcd_wait						; check LCD busy or not
	pop r16								; pop r16 from stack
.endmacro
		jmp RESET						; interrupt vectors
.org	INT0addr						; define in m2560def.inc equal 0x0002
		jmp EXT_INT0

RESET:
	ldi r16, low(RAMEND)				; initialize stack pointer
	out SPL, r16
	ldi r16, high(RAMEND)
	out SPH, r16
	ser r16
	out DDRC, r16						; PORTC output (LCD data)
	out DDRA, r16						; PORTA output (LCD ctrl)
	clr r16
	out PORTC, r16
	out PORTA, r16
	ldi r16, PORTFDIR					; PF7:4/PF3:0, out/in
	out DDRF, r16

	cbi DDRD, 0							; set port D bit 0 for input (button signals)
	sbi PORTD, 0

	ser r16								; PORTC is output
	STS DDRL, r16
	ldi temp1, (2 << ISC00)				; define in m2560def.inc equal 0
	sts EICRA, temp1					; activate failing edge interrupt request
	in temp1, EIMSK
	ori temp1, (1 << INT0)				; define in m2560def.inc equal 0
	out EIMSK, temp1					; activate INT0
	sei									; enable global interrupt					; jump to main
	clr temp1

	do_lcd_command 0b00111000 			; 2x5x7
	rcall sleep_5ms

	do_lcd_command 0b00111000 			; 2x5x7
	rcall sleep_1ms

	do_lcd_command 0b00111000 			; 2x5x7
	do_lcd_command 0b00111000 			; 2x5x7

	do_lcd_command 0b00001000 			; display off
	do_lcd_command 0b00000001 			; clear display
	do_lcd_command 0b00000110 			; increment, no display shift
	do_lcd_command 0b00001100			; set on the entire display
	do_lcd_data 'S'						; display control state
	do_lcd_data ':'	
	do_lcd_data ' '	
	do_lcd_data 'W'						; display windows' condtion
	do_lcd_data '1'	
	do_lcd_data ' '	
	do_lcd_data 'W'	
	do_lcd_data '2'	
	do_lcd_data ' '	
	do_lcd_data 'W'
	do_lcd_data '3'	
	do_lcd_data ' '	
	do_lcd_data 'W'	
	do_lcd_data '4'	
	do_lcd_command 0b11000100			; move to second line
	do_lcd_data '0'						; initialize the window condition
	do_lcd_command 0b11000111			; move to right position
	do_lcd_data '0'
	do_lcd_command 0b11001010			; move to right postion
	do_lcd_data '0'
	do_lcd_command 0b11001101			; move to right postion
	do_lcd_data '0'
	ldi temp2, 0b00001000
	sts DDRL, temp2						; activate Timer 5, 4, 3, 1
	sts DDRH, temp2
	out DDRE, temp2
	ldi temp2, 0b00100000
	out DDRB, temp2
	
	ldi temp1, (1 << CS50)
	sts TCCR5B, temp1
	ldi temp1, (1<< WGM50)|(1<<COM5A1)
	sts TCCR5A, temp1

	ldi temp1, (1 << CS40)
	sts TCCR4B, temp1
	ldi temp1, (1<< WGM40)|(1<<COM4A1)
	sts TCCR4A, temp1

	ldi temp1, (1 << CS30)
	sts TCCR3B, temp1
	ldi temp1, (1<< WGM30)|(1<<COM3A1)
	sts TCCR3A, temp1

	ldi temp1, (1 << CS10)
	sts TCCR1B, temp1
	ldi temp1, (1<< WGM10)|(1<<COM1A1)
	sts TCCR1A, temp1

	clr temp2							; clear some registers		
	clr temp1
	clr w1
	clr w2
	clr w3
	clr w4
	clr central
	jmp main
	
EXT_INT0:
	sbic PIND, 0						; if pin0 of portD is clear, skip
	jmp main							; else loop 

	do_lcd_command 0b10000000			; display emergency state
	do_lcd_data '!'
	do_lcd_data '!'
	do_lcd_command 0b11000100			; display window condition
	do_lcd_data '0'
	do_lcd_command 0b11000111
	do_lcd_data '0'
	do_lcd_command 0b11001010
	do_lcd_data '0'
	do_lcd_command 0b11001101
	do_lcd_data '0'
	ldi temp1, 0
	sts OCR5AL, temp1					; clear the PWM duty cycle
	sts OCR4AL, temp1
	sts OCR3AL, temp1
	sts OCR1AL, temp1	

	stop: rjmp stop						; end

	reti								; return from emergency interrupt
	

 main:
		ldi cmask, INITCOLMASK		;0xEF
		clr col

 colloop:
		cpi col, 4
		breq allcol
		brne continue
		
allcol:
		ldi temp1, 0xff
		mov button_press, temp1
		rjmp main	
		
continue:		
		out PORTF, cmask
		ldi temp1, 0xFF					; slow down the scan operation.
 delay:	
		dec temp1
		brne delay
		in temp1, PINF
		andi temp1, ROWMASK				;0x0F
		cpi temp1, 0xF
		breq nextcol

		ldi rmask, INITROWMASK			; initialize for row check
		clr row

 rowloop:
		cpi row, 4
		breq nextcol					; the row scan is over.
		mov temp2, temp1
		and temp2, rmask				; check un-masked bit
		breq convert					; if bit is clear, the key is pressed
		inc row							; else move to the next row
		lsl rmask
		jmp rowloop

 nextcol:								; if row scan is over
		lsl cmask
		inc col							; increase column value
		jmp colloop

 convert:
		cp button_press, temp1			; justify key released or not
		breq return
		mov button_press, temp1	
		cpi col, 3						; if column is 3 we have a letter
		breq letters
		cpi row, 3
		breq symbols
		mov temp1, row
		lsl temp1
		add temp1, row
		add temp1, col					; input_value = 3 * row + col
		subi temp1, -1					; input += 1 -> true value
		; button 1 and 2 for window 1
		cpi temp1, 1					; if press '1', num1 condition, but too far, jump to num1_flag
		breq num1_flag
		cpi temp1, 2					; if press '2', num2 condition, but too far, jump to num2_flag
		breq num2_flag
		; button 3 and 4 for window 2
		cpi temp1, 3					; if press '3', num3 condition, but too far, jump to num3_flag
		breq num3_flag
		cpi temp1, 4					; if press '4', num4 condition, but too far, jump to num4_flag
		breq num4_flag
		; button 5 and 6 for window 3
		cpi temp1, 5					; if press '5', num5 condition, but too far, jump to num5_flag
		breq num5_flag
		cpi temp1, 6					; if press '6', num6 condition, but too far, jump to num6_flag
		breq num6_flag
		; button 7 and 8 for window 4
		cpi temp1, 7					; if press '7', num7 condition, but too far, jump to num7_flag
		breq num7_flag
		cpi temp1, 8					; if press '8', num8 condition, but too far, jump to num8_flag
		breq num8_flag
		
 return:
		jmp main

num1_flag:
		jmp num1						; jump to num1 condition

num2_flag:
		jmp num2						; jump to num2 condition

num3_flag:
		jmp num3						; jump to num3 condition

num4_flag:
		jmp num4						; jump to num4 condition

num5_flag:
		jmp num5						; jump to num5 condition
			
num6_flag:
		jmp num6						; jump to num6 condition

num7_flag:
		jmp num7						; jump to num7 condition

num8_flag:
		jmp num8						; jump to num8 condition

 letters:								; if press letters, RESET
		jmp RESET
		
 returnSymbols:							; scan again
		jmp main
star1:									; if press start, jup to star
		jmp star	

 symbols:
		cpi col, 0						; Check if we have a star
		breq star1
		cpi col, 1						; or if we have zero
		breq return

 equal:	
		/*
		ldi temp1, 1
		mov central, temp1
		*/
		ldi temp1, 0					; if press '=', central control off
		mov central, temp1				; clear cenral control signal
				
		do_lcd_command 0b10000000		; display central control state	
		do_lcd_data 'C'
		do_lcd_command 0b11000100
		do_lcd_data '0'					; display central conrol window state
		do_lcd_command 0b11000111
		do_lcd_data '0'
		do_lcd_command 0b11001010
		do_lcd_data '0'
		do_lcd_command 0b11001101
		do_lcd_data '0'	
		clr w1							; clear windows condition level, make them 0
		clr w2
		clr w3
		clr w4
		ldi temp1, 0
		sts OCR5AL, temp1				; clear windows PWM duty cycle, make shake off
		sts OCR4AL, temp1
		sts OCR3AL, temp1
		sts OCR1AL, temp1				
		jmp main


star:									
		ldi temp1, 1					; if press '*', central control on
		mov central, temp1				; set cenral control signal
		
		do_lcd_command 0b10000000		; display central control state	
		do_lcd_data 'C'
		do_lcd_command 0b11000100
		do_lcd_data '3'					; display central conrol window state
		do_lcd_command 0b11000111
		do_lcd_data '3'
		do_lcd_command 0b11001010
		do_lcd_data '3'
		do_lcd_command 0b11001101
		do_lcd_data '3'
		ldi temp1, 0xff					; clear windows PWM duty cycle, make shake fully on
		sts OCR5AL, temp1
		sts OCR4AL, temp1
		sts OCR3AL, temp1
		sts OCR1AL, temp1	
		jmp main						; scan new input

 return1:
		jmp main
; press button '1'
 num1:
		ldi temp1, 0					; justify whether in central control
		cp central, temp1
		brne return1					; if yes, wait for scanning new input
		do_lcd_command 0b10000000		; else, change control state to 'L'
		do_lcd_data 'L'
		cpi w1, 3						; if opaqe level == 3, wait for scanning new input, cannot increase anymroe
		breq return1			
		inc w1							; else w1++, opaqe level increase
		do_lcd_command 0b11000100		; move to w1 condition number postiion
		do_lcd_data_num w1				; change w1 condition number
		rjmp led_1A2					; jump to change w1 opaque level
; window 1 opaque level
 led_1A2:
		ldi temp1, 85					; full duty cycle is 255, 85 = 255/3, 4 level
		mul w1, temp1					; duty cycle mul w1 condition number
		mov temp1, r0					
		sts OCR5AL, temp1				; change the Timer PWM duty cycle
		CLR temp1
		sts OCR5AH, temp1				; clear high position of Timer PWM duty cycle
		jmp main						; jump to change w1 opaque level

 return2:
		jmp main
; press button '2'
 num2:
		ldi temp1, 0					; justify whether in central control
		cp central, temp1
		brne return2					; if yes, wait for scanning new input
		do_lcd_command 0b10000000		; else, change control state to 'L'
		do_lcd_data 'L'
		cpi w1, 0						; if opaqe level == 0, wait for scanning new input, cannot decrease anymore
		breq return2
		dec w1							; else w1--, opaqe level decrease
		do_lcd_command 0b11000100		; move to w1 condition number postiion
		do_lcd_data_num w1				; change w1 condition number
		rjmp led_1A2

return3:
		jmp main
; press nutton '3'
 num3:
		ldi temp1, 0					; justify whether in central control
		cp central, temp1
		brne return3					; if yes, wait for scanning new input
		do_lcd_command 0b10000000		; else, change control state to 'L'
		do_lcd_data 'L'
		cpi w2, 3						; if opaqe level == 3, wait for scanning new input, cannot increase anymore
		breq return3
		inc w2							; else w2++, opaqe level decrease
		do_lcd_command 0b11000111		; move to w2 condition number postiion
		do_lcd_data_num w2				; change w2 condition number
		jmp led_3A4
; window 2 opaque level 
 led_3A4:
		ldi temp1, 85
		mul w2, temp1
		mov temp1, r0
		sts OCR4AL, temp1
		CLR temp1
		STS OCR4AH, temp1
	
		jmp main

 return4:
		jmp main
; press nutton '4'
 num4:
		ldi temp1, 0
		cp central, temp1
		brne return4
		do_lcd_command 0b10000000
		do_lcd_data 'L'
		cpi w2, 0
		breq return4
		dec w2
		do_lcd_command 0b11000111
		do_lcd_data_num w2
		jmp led_3A4				

return5:
		jmp main

 num5:
		ldi temp1, 0
		cp central, temp1
		brne return5
		do_lcd_command 0b10000000
		do_lcd_data 'L'
		cpi w3, 3
		breq return5
		inc w3
		do_lcd_command 0b11001010
		do_lcd_data_num w3
		jmp led_5A6

led_5A6:
		ldi temp1, 85
		mul w3, temp1
		mov temp1, r0
		sts OCR3AL, temp1
		CLR temp1
		STS OCR3Ah, temp1
		jmp main

 return6:
		jmp main

 num6:
		ldi temp1, 0
		cp central, temp1
		brne return6
		do_lcd_command 0b10000000
		do_lcd_data 'L'
		cpi w3, 0
		breq return6
		dec w3
		do_lcd_command 0b11001010
		do_lcd_data_num w3
		jmp led_5A6
		
return7:
		jmp main

 num7:
		ldi temp1, 0
		cp central, temp1
		brne return7
		do_lcd_command 0b10000000
		do_lcd_data 'L'
		cpi w4, 3
		breq return7
		inc w4
		do_lcd_command 0b11001101
		do_lcd_data_num w4
		jmp led_7A8

led_7A8:
		ldi temp1, 85
		mul w4, temp1
		mov temp1, r0
		sts OCR1AL, temp1
		CLR temp1
		STS OCR1Ah, temp1
		jmp main

 return8:
		jmp main

 num8:
		ldi temp1, 0
		cp central, temp1
		brne return8
		do_lcd_command 0b10000000
		do_lcd_data 'L'
		cpi w4, 0
		breq return8
		dec w4
		do_lcd_command 0b11001101
		do_lcd_data_num w4
		jmp led_7A8		

 



 press:								; if not release back to scanning
	jmp main

 
; Send a command to the LCD (r16)

lcd_command:

	out PORTC, r16
	Nop

	lcd_set LCD_E
	nop
	nop
	Nop

	lcd_clr LCD_E
	nop
	nop
	nop
	ret

lcd_data:

	out PORTC, r16
	lcd_set LCD_RS
	nop
	nop
	Nop

	lcd_set LCD_E
	nop
	nop
	Nop

	lcd_clr LCD_E
	nop
	nop
	nop
	lcd_clr LCD_RS
	ret

lcd_wait:

	push r16
	clr r16
	out DDRC, r16
	out PORTC, r16
	lcd_set LCD_RW

lcd_wait_loop:

	nop
	lcd_set LCD_E
	nop
	nop
    nop
	in r16, PINC
	lcd_clr LCD_E
	sbrc r16, 7
	rjmp lcd_wait_loop
	lcd_clr LCD_RW
	ser r16
	out DDRC, r16
	pop r16
	ret

.equ F_CPU = 16000000
.equ DELAY_1MS = F_CPU / 4 / 1000 - 4
; 4 cycles per iteration - setup/call-return overhead

sleep_1ms:
	
	push r24
	push r25
	ldi r25, high(DELAY_1MS)
	ldi r24, low(DELAY_1MS)

delayloop_1ms:

	sbiw r25:r24, 1
	brne delayloop_1ms
	pop r25
	pop r24
	ret

sleep_5ms:

	rcall sleep_1ms
	rcall sleep_1ms
	rcall sleep_1ms
	rcall sleep_1ms
	rcall sleep_1ms
	ret

sleep_25ms:

	rcall sleep_5ms
	rcall sleep_5ms
	rcall sleep_5ms
	rcall sleep_5ms
	rcall sleep_5ms
	ret

sleep_100ms:

	rcall sleep_25ms
	rcall sleep_25ms
	rcall sleep_25ms
	rcall sleep_25ms
	ret

sleep_500ms:

	rcall sleep_100ms
	rcall sleep_100ms
	rcall sleep_100ms
	rcall sleep_100ms
	ret





	