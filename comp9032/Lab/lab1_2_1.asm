/*
 * comp 9032 lab1_1 for minimun code size
 *
 *  Created: 2019/9/21 19:00:30
 *   Author: Weijia Min
 */ 
 /*
 int main(void){
	int a, b; 
	while (a!=b){ 
		if (a>b)
			a = a - b;
		else
			b = b - a;
	}
	return 0; 
}
 */

 .def aL = r16				; define aL as register r16
 .def aH = r17				; define aH as register r17
 .def bL = r18				; define bL as register r18
 .def bH = r19				; define bH as register r19


 ldi aL,  low(1000)
 ldi aH,  high(1000)
 ldi bL,  low(400)
 ldi bH,  high(400)

 loop:
		cp	aL, bL			; compare low byte of a to low byte of b		1 words
		cpc aH, bH			; compare high byte of a to high byte of b		1 words
		breq end			; if a == b branch to end						1 words 
		brlo else			; if a < b branch to else						1 words 
		sub aL, bL			; aL = aL - bL									1 words
		sbc aH, bH			; aH = aH - bH									1 words
		rjmp loop			; back to the loop								1 words
 else:
		sub	bL, aL			; bL = bL - aL									1 words
		sbc bH, aH			; bH = bH - aH									1 words
		rjmp loop			; back to the loop								1 words
 end:
		rjmp end			;												1 words
							;										total: 11 words


