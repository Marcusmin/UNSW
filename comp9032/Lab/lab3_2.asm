/*
 * lab3_1.asm
 *
 *  Created: 2019/10/20 22:56:52
 *  Author: MIN
 *	
*/

; Board settings:
; PF0:7 -> R0:C3 (KEYPAD) PORTF
; PC7:0 -> PD0:7 (LCD DATA) PORTC   
; PA4:7 -> BE:RS(LCD CTRL) PORTA
; PL7:0 -> LED9:2
  
.include "m2560def.inc"

.def num1 = r2						; define r2 to store num1 (1 byte unsigned)
.def num2 = r3						; define r3 to store num2 (1 byte unsigned)
.def row = r17						; current row number
.def col = r18						; current column number
.def rmask = r19					; mask for current row during scanning
.def cmask = r20					; mask for current column during scanning
.def temp1 = r21
.def temp2 = r22
.def num_flag  = r23				; define r23 to distinguish num1 and num2
.def button_press = r24				; to distinguish whether the key release or not

.equ LCD_RS = 7						; LCD RS bit position
.equ LCD_E  = 6						; LCD E bit position
.equ LCD_RW = 5						; LCD RW bit position
.equ LCD_BE = 4						; LCD BE bit position
.equ PORTFDIR = 0xF0				; PF7-4: output, PF3-0, input
.equ ROWMASK =0x0F					; scan from the leftmost column,
.equ INITCOLMASK = 0xEF				; scan from the top row
.equ INITROWMASK = 0x01				; for obtaining input from Port F

.macro lcd_set						; set LCD bit
	sbi PORTA, @0
.endmacro

.macro lcd_clr						; clr LCD bit
	cbi PORTA, @0
.endmacro


.macro do_lcd_command				; send a command to LCD
	ldi   r16, @0					; load the command to r16
	rcall lcd_command				; send r16 to PORTC
	rcall lcd_wait					; check LCD busy or not
.endmacro

.macro do_lcd_data					; send a data to LCD
	ldi   r16, @0					; load the data to r16
	rcall lcd_data					; send r16 to PORTC
	rcall lcd_wait					; check LCD busy or not
.endmacro

.macro do_lcd_data_num				; send a ASCII data to LCD
	mov r16, @0						; load the data
	subi r16, -'0'					; convert it to ASCII
	rcall lcd_data					; send data to PORTC
	rcall lcd_wait					; check LCD busy or not
.endmacro


RESET:

	ldi r16, low(RAMEND)			; initialize stack pointer
	out SPL, r16
	ldi r16, high(RAMEND)
	out SPH, r16
	ser r16							
	out DDRC, r16					; PORTC output (LCD data)
	out DDRA, r16					; PORTA output (LCD ctrl)
	clr r16
	out PORTC, r16
	out PORTA, r16
	ldi r16, PORTFDIR				; PF7:4/PF3:0, out/in
	out DDRF, r16

	ser r16							; PORTC is output
	STS DDRL, r16
	clr num_flag
	clr num1
	clr num2
	clr temp1

	do_lcd_command 0b00111000 		; 2x5x7
	rcall sleep_5ms

	do_lcd_command 0b00111000 		; 2x5x7
	rcall sleep_1ms

	do_lcd_command 0b00111000 		; 2x5x7
	do_lcd_command 0b00111000 		; 2x5x7

	do_lcd_command 0b00001000 		; display off
	do_lcd_command 0b00000001 		; clear display
	do_lcd_command 0b00000110 		; increment, no display shift
	do_lcd_command 0b00001110 		; Cursor on, bar, no blink

 main:
		ldi cmask, INITCOLMASK		;0xEF
		clr col

 colloop:
		cpi col, 4					; if col == 4 means all column scanned
		breq allcol
		brne continue
		
allcol:
		ser button_press			; initial the butten_press
		rjmp main					; scan again
		
continue:		
		out PORTF, cmask
		ldi temp1, 0xFF				; slow down the scan operation.
 delay:	
		dec temp1
		brne delay
		in temp1, PINF
		andi temp1, ROWMASK			;0x0F
		cpi temp1, 0xF
		breq nextcol

		ldi rmask, INITROWMASK		; initialize for row check
		clr row

 rowloop:
		cpi row, 4
		breq nextcol				; the row scan is over.
		mov temp2, temp1
		and temp2, rmask			; check un-masked bit
		breq convert				; if bit is clear, the key is pressed
		inc row						; else move to the next row
		lsl rmask
		jmp rowloop

 nextcol:							; if row scan is over
		lsl cmask
		inc col						; increase column value
		jmp colloop

 convert:
		cpi  col, 3					; if column is 3 we have a letter
		breq letters
		cpi row, 3
		breq symbols
		mov temp1, row
		lsl temp1
		add temp1, row
		add temp1, col				; input_value = 3 * row + col
		subi temp1, -1				; input += 1 -> true value
		cpi num_flag, 0				; distinguish num1 and num2 , 
		breq get_num1				; flag = 0 -> num1
		jmp get_num2				; flag != 0 -> num2

 letters:
		jmp RESET					; if letters reset

 symbols:
		cpi col, 0					; Check if we have a star
		breq star
		cpi col, 1					; or if we have zero
		breq zero

 equal:	
		cp button_press, temp1		; justify key released or not
		breq main
		mov button_press, temp1		; if we have #
		mul num1, num2				; r1: r0 = num1 * num2
		mov temp1, r1				
		cpi temp1, 0				; if r1 != 0, overfolw !
		brne overflow
		mov temp1, r0
		
		jmp display_result			; jump to display the result

 star:
		cp button_press, temp1		; justify key released or not
		breq press
		mov button_press, temp1
		ldi num_flag, 1				; make num flag 1, start getting num2
		do_lcd_data '*'				; display * on LCD
		jmp main					; scan new input

 zero:
		ldi temp1, 0				; get zero
		cpi num_flag, 0				; distinguish the zero is to num1 or num2
		breq get_num1				; if 0 to num1
		jmp get_num2				; else to num2

.macro carry						; @0: num1 or num2
	ldi r28, 10						; @1: input value from keypad
	mul @0, r28						; new_num = old_num * 10 + input
	ldi r30, 0
	cp r1, r30						; check whether the input is 8 bits or not
	brne input_overflow				; if larger than 8 bits, jump to overflow procedure
	rjmp move
input_overflow:						; if overflow during carrying, e.g. 333
	jmp overflow					; jump to overflow
move:
	add r0, @1						; units add tens
	brcs input_overflow				; if overfolw while adding
	mov @0, r0
.endmacro

 get_num1:
		cp button_press, temp1		; justify key released or not
		breq press
		mov button_press, temp1
		do_lcd_data_num temp1		; display input on lcd
		carry num1, temp1			; new_num = old_num * 10 + input
		jmp main					; scan new input

 get_num2:
		cp button_press, temp1		; justify key released or not
		breq press
		mov button_press, temp1		
		do_lcd_data_num temp1		; display input on lcd
		carry num2, temp1			; new_num = old_num * 10 + input
		jmp main					; scan new input

 press:								; if not release back to scanning
	jmp main

 overflow:							 
		do_lcd_command 0b00000001	; clear display
		do_lcd_data 'o'				; display 'overflow!'
		do_lcd_data 'v'
		do_lcd_data 'e'
		do_lcd_data 'r'
		do_lcd_data 'f'
		do_lcd_data 'l'
		do_lcd_data 'o'
		do_lcd_data 'w'
		do_lcd_data '!'
		ldi temp2, 0b10101010		; flash 3 times
		sts PORTL, temp2
		rcall sleep_ns
		ldi temp2, 0b01010101
		sts PORTL, temp2
		rcall sleep_ns
		ldi temp2, 0b10101010
		sts PORTL, temp2
		rcall sleep_ns
		jmp end

.macro print_digit					; @0: 10 or 100,  display tens or hundreds
		clr r30						; as counter
first_check:						; first check avoid the situation: 1(0)3 rather than 103
		cpi temp1, @0				; if the hundreds exist but the tens is 0
		brlo less					
second_check:						
		cpi temp1, @0				; compare the reuslt with 10 or 100
		brlo print					; if < 10 or 100
		subi temp1, @0				; result -= 10 or 100
		inc r30						; counter++
		rjmp second_check			; rjmp loop
less:
		do_lcd_data '0'				; display zero on LCD
		rjmp finish
print:								; display the hundreds or tens
		do_lcd_data_num r30
finish:
		nop
.endmacro

 display_result:
		do_lcd_command 0b00000001   ; clear display
		do_lcd_command 0b00001100	; no cursor
		cpi temp1, 10				; if result < 10, branch to less_10 part
		brlo less_10
		cpi temp1, 100				; if result < 100, branch to less_100 part
		brlo less_100		
		print_digit 100				; display the hundreds
		print_digit 10				; display the tens
		do_lcd_data_num temp1		; display the units
		rjmp end

less_100:							; display the tens
		print_digit 10				; and then display the units

less_10:							; directly display the result
		do_lcd_data_num temp1	
			
end:
		rjmp end
					 


; Send a command to the LCD (r16)

lcd_command:

	out PORTC, r16
	Nop								; delay to meet timing(Set up time)

	lcd_set LCD_E					; turn on the enbale pin
	nop								; delay to meet timing (Enable pulse width)
	nop
	Nop

	lcd_clr LCD_E					; turn off the enable pin
	nop								; delay to meet timing (Enable cycle time)
	nop			
	nop
	ret

lcd_data:

	out PORTC, r16
	lcd_set LCD_RS				; RS = 1, RW = 0 for a data write
	nop							; delay to meet timing (Set up time)
	nop
	Nop

	lcd_set LCD_E				; turn on the enable pin
	nop							; delay to meet timing (Enable pulse width)
	nop
	Nop

	lcd_clr LCD_E				; turn off the enable pin
	nop							; delay to meet timing (Enable cycle time)
	nop
	nop
	lcd_clr LCD_RS				; clear RS
	ret


lcd_wait:						; Check LCD and wait until LCD is not busy

	push r16
	clr r16
	out DDRC, r16				; PORTC input
	out PORTC, r16				; pull-up resistor
	lcd_set LCD_RW				; RW = 1

lcd_wait_loop:

	nop							; delay to meet set-up time
	lcd_set LCD_E				; turn on the enable pin
	nop							; delay to meet timing (Data delay time)
	nop
    nop
	in r16, PINC				; read value from LCD
	lcd_clr LCD_E				; turn off the enable pin
	sbrc r16, 7					; if the busy flag is set
	rjmp lcd_wait_loop			; repeat command read
	lcd_clr LCD_RW				; else RW = 0
	ser r16
	out DDRC, r16				; make PORTC an output port again
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

sleep_ns:
	
	push r24
	push r25
	push r26
	ldi r26, 0XF
	ldi r25, 0xFF
	ldi r24, 0xFF

delayloop:

	subi r24, 1
	sbci r25, 0
	sbci r26, 0
	brne delayloop
	pop r26
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






	