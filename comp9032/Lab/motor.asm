;
; Lab4_Task3.asm

; Created: 2018/10/09 13:22:00
; Function: Write an AVR assembly language program that measures the speed of the motor 
; (based on the number of holes that are detected by the shaft encoder) and displays the speed on LCD. 
; The motor speed can be adjusted by the POT (potentiometer).


.include "m2560def.inc"

.macro  OneSecondDelay					;  One Second Delay

		ldi r19, 0
startm:
		ldi r17, low(0xffff)			; load 0xff to r17
		ldi r18, high(0xffff)			; load 0xff to r18
		clr r29 
		clr r28
loop:
		cp r28,  r17 
		cpc r29, r18
		brsh done 
		adiw r29:r28, 1 
		nop
		rjmp loop 
done:
		cpi r19, 30
		inc r19
		brlo startm
.endmacro


.macro do_lcd_command				; execute command to LCD
		ldi r16, @0
		rcall lcd_command
		rcall lcd_wait
.endmacro

.macro do_lcd_data					; display data on LCD
		mov r16, @0
		rcall lcd_data
		rcall lcd_wait
.endmacro

.def 	temp = r16
.def    unit = r20
.def    ten = r21
.def    hundred = r22
.def    thousand = r23					; set thousand/hundred/ten/unit for display speed
.def    count = r24						; count for calcuate holes

										; set up interrupt vectors
	jmp RESET
.org 	INT0addr						; defined in m2560def.inc
	jmp EXT_INT0

RESET:
	
		clr r26							; clear registers
		clr thousand
		clr unit
		clr ten
		clr hundred

		ldi temp, (2 << ISC00)			; set INT0 as falling edge triggered interrupt
		sts EICRA, temp					; store temp to data space

		in temp, EIMSK					; enable INT0
		ori temp, (1<<INT0)				; logical or with immediate
		out EIMSK, temp					; store temp to I/o register

		;lcd reset
		ldi r16, low(RAMEND)			; load 0xff to r16
		out SPL, r16					; 0xff to SPL
		ldi r16, high(RAMEND)			; load 0x21 to r16
		out SPH, r16					; 0x21 to SPH

		ser r16							; set r16
		out DDRF, r16					; set PORTF as output
		out DDRA, r16					; set PORTA as output
		clr r16							; clear r16
		out PORTF, r16					; PORTF to 0
		out PORTA, r16					; PORTA to 0

		do_lcd_command 0b00111000		; 2x5x7
		rcall sleep_5ms
		do_lcd_command 0b00111000		; 2x5x7
		rcall sleep_1ms
		do_lcd_command 0b00111000		; 2x5x7
		do_lcd_command 0b00111000		; 2x5x7
		
		do_lcd_command 0b00001000		; display off
		do_lcd_command 0b00000001		; clear display
		do_lcd_command 0b00000110		; increment, no display shift
		do_lcd_command 0b00001110		; display on/off, Cursor display on/off, cursor blink on/off


		sei								; enable Global Interrupt
		jmp main

EXT_INT0:               

		cpi count, 4					; The wheel has 4 holes, so if count is 4, the motor runs one whole circle.
		brne count_plus_1
		clr count
	
		cpi unit, 9						; check the value of unit position, if got 9, ten position plus 1, clear unit posion
		brne unit_plus_1
		clr unit

		cpi ten, 9					    ; check the value of ten position, if got 9, hundred position plus 1, clear ten posion
		brne ten_plus_1
		clr ten

		cpi hundred, 9					; check the value of hundred position, if got 9, thousand position plus 1, clear hundred posion
		brne hundred_plus_1
		clr hundred

		cpi  thousand, 9                ; check the value of thousand position, if got 9, clear thousand posion
		brne thousand_plus_1
		clr  thousand
		jmp  end_ext

thousand_plus_1:					
		inc thousand					; thousand increased by 1
		jmp end_ext

hundred_plus_1:
		inc hundred						; hundred increased by 1
		jmp end_ext

ten_plus_1:
		inc ten							; ten increased by 1
		jmp end_ext

unit_plus_1:
		inc unit						; unit increased by 1
		jmp end_ext

count_plus_1:
		inc count						; count increased by 1
		jmp end_ext

end_ext:
		reti

main:
		OneSecondDelay					; One second delay
		do_lcd_command 0b00000001		; clear display
	
		subi unit, -'0'                 ; add the value of every position to '0' to get speed
		subi ten, -'0'
		subi hundred, -'0'
		subi thousand, -'0'

		do_lcd_data thousand            ; display speed 
		do_lcd_data hundred
		do_lcd_data ten
		do_lcd_data unit

		ldi r30, 'r'                    ; display "rps"
		do_lcd_data r30 
		ldi r30, 'p'
		do_lcd_data r30 
		ldi r30, 's'
		do_lcd_data r30 

		clr unit                        ; clear unit
		clr ten							; clear ten
		clr hundred						; clear hundred
		clr thousand					; clear thousand
		rjmp main						; jump to main

.equ LCD_RS = 7						; 7 bit in PORTA
.equ LCD_E  = 6						; 6 bit in PORTA
.equ LCD_RW = 5						; 5 bit in PORTA
.equ LCD_BE = 4						; 4 bit in PORTA

.macro	lcd_set
		sbi PORTA, @0				; set bit in I/O register
.endmacro

.macro	lcd_clr
		cbi PORTA, @0				; clear bit in I/O register
.endmacro

; Send a command to the LCD (r16)

lcd_command:
		out PORTF, r16				; store data in r16 to PortF(connect to LCD)
		nop
		lcd_set LCD_E				; set bit 6 in PORTA(connect to LCD control)
		nop							; delay to meet timing
		nop
		nop
		lcd_clr LCD_E				; clear bit 6 in PORTA(connect to LCD control)
		nop
		nop
		nop
		ret	

lcd_data:
		out PORTF, r16				; store data in r16 to PortF(connect to LCD)
		lcd_set LCD_RS				; set bit 7 in PORTA(connect to LCD control)
		nop
		nop
		nop
		lcd_set LCD_E				; set bit 6 in PORTA(connect to LCD control)
		nop
		nop
		nop
		lcd_clr LCD_E				; clear bit 6 in PORTA(connect to LCD control)
		nop
		nop
		nop
		lcd_clr LCD_RS			    ; clear bit 7 in PORTA(connect to LCD control)
		ret

lcd_wait:
		push r16					; save r16
		clr r16						; clear r16
		out DDRF, r16				; set PortF as input
		out PORTF, r16				; clear PortF
		lcd_set LCD_RW				; set bit 5 in PORTA(connect to LCD control)

lcd_wait_loop:
		nop
		lcd_set LCD_E				; set bit 6 in PORTA(connect to LCD control)
		nop
		nop
		nop
		
		in r16, PINF				; load data from PINF to r16
		lcd_clr LCD_E				; set bit 6 in PORTA(connect to LCD control)
		sbrc r16, 7					; Skip if Bit in Register is Cleared
		rjmp lcd_wait_loop

		lcd_clr LCD_RW				; clear bit 5 in PORTA(connect to LCD control)
		ser r16						; set r16
		out DDRF, r16				; set PORTF as output
		pop r16
		ret

.equ F_CPU = 16000000
.equ DELAY_1MS = F_CPU / 4 / 1000 - 4
; 4 cycles per iteration - setup/call-return overhead

sleep_1ms:							; 1 ms delay
		push r24
		push r25
		ldi r25, high(DELAY_1MS)	; load high DELAY_1MS to r25
		ldi r24, low(DELAY_1MS)     ; load low DELAY_1MS to r25

delayloop_1ms:						; 1 ms delayloop 
		sbiw r25:r24, 1				; substract 1 from r25:r24
		brne delayloop_1ms			; if r25:r24 not equal 0, jump to delayloop_1ms
		pop r25
		pop r24
		ret

sleep_5ms:							; 5ms delay
		rcall sleep_1ms
		rcall sleep_1ms
		rcall sleep_1ms
		rcall sleep_1ms
		rcall sleep_1ms
		ret



