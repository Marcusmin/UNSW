/*
 * lab2_1.asm
 *
 *  Created: 2019/10/2 11:02:37
 *   Author: M
 */ 
 .include "m2560def.inc"
 .def aL = r16					; define aL as register r16
 .def aH = r17					; define aH as register r17
 .def bL = r18					; define bL as register r18
 .def bH = r19					; define bH as register r19
 .def temp1 = r20				; define temp1 as register r20
 .def temp2 = r21				; define temp2 as register r21

 .macro remainder				; a: @0, @1
 loop:							; b: @2, @3
	cp @0, @2					; compare aH:aL to bH:bL
	cpc @1, @3
	breq zero					; if a == b, the remainder wii be 0
	brlo remainer				; if a < b, the remainder wii be a
	sub @0, @2					; aL = aL - bL
	sbc @1, @3					; aH = aH - bH
	rjmp loop					; loop until a <= b
 zero:
	clr @0						; make a = 0
	clr @1
 remainer:						; the result of remainder will be stored in aH:aL
	nop
 .endmacro

 .macro a_swap_b				; a: @0, @1
	clr @2						; temp: @2, @3
	clr @3						; b: @4, @5
	mov @2, @0					; swap a and b
	mov @3, @1
	mov @0, @4
	mov @1, @5
	mov @4, @2
	mov @5, @3
 .endmacro

 .cseg
	num_a:	.dw	400				; num_a & num_b in program memory
	num_b:	.dw	100

 main:
	ldi ZL, low(num_a<<1)		; initial Z to num_a address   
	ldi ZH, high(num_a<<1)
	lpm aL, Z+					; load num_a into aH:aL
	lpm aH, Z
	ldi ZL, low(num_b<<1)		; initial Z to num_b address  
	ldi ZH, high(num_b<<1)
	lpm bL, Z+					; load num_b into bH:bL
	lpm bH, Z
	rcall gcd					; r25: r24 as return value
 end:
	rjmp end

 gcd:
	; prologue			
	push bL						; save conflict registers on stack
	push bH
	push aL
	push aH
	push temp1					
	push temp2
	push YL						; save Y on the stack
	push YH	
	in YL, SPL					; load SP into Y
	in YH, SPH
	sbiw Y,4					; let Y point to the top of the stack frame
	out SPL, YL					; update SP make it points to new stack top
	out SPH, YH
	std Y+1, bL					; get the parameter
	std Y+2, bH
	std Y+3, aL
	std Y+4, aH
	; end of prologue

	; gcd function body
	clr temp1
	clr temp2				
	cp bL, temp1				; compare b with 0
	cpc bH, temp2
	brne bne0					; if b != 0, branch to bne0
	mov r24, aL					; else return a to r25:r24
	mov r25, aH
	rjmp gcd_end				; jump to gcd_end (epilogue)
bne0:
	remainder aL, aH, bL, bH				; reaminder stored in aH:aL, a = a%b
	a_swap_b aL, aH, temp1, temp2, bL, bH	; swap a, b
	rcall gcd					; call gcd(b, a%b)
	; gcd function end	

gcd_end:			
	; epilogue
	adiw Y, 4					; deallocate the stack frame
	out SPH, YH					; restore SP
	out SPL, YL
	pop YH						; restore Y
	pop YL
	pop temp2					; restore conflict registers
	pop temp1
	pop aH
	pop aL
	pop bH
	pop bL
	ret
	; end of epilogue

			
		

	