/*
 * Copyright 2016-2023 NXP
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 *
 * o Redistributions of source code must retain the above copyright notice, this list
 *   of conditions and the following disclaimer.
 *
 * o Redistributions in binary form must reproduce the above copyright notice, this
 *   list of conditions and the following disclaimer in the documentation and/or
 *   other materials provided with the distribution.
 *
 * o Neither the name of NXP Semiconductor, Inc. nor the names of its
 *   contributors may be used to endorse or promote products derived from this
 *   software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
 * ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
 * ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

/**
 * @file    main.c
 * @brief   Application entry point.
 */
#include <stdio.h>
#include "board.h"
#include "peripherals.h"
#include "pin_mux.h"
#include "clock_config.h"
#include "MK22F51212.h"
#include "fsl_debug_console.h"
#include <stdint.h> /* data types */
#include <string.h> /* concat string */
#include <stdlib.h> /* malloc, calloc, free */

/* ---- SETUP ---- */
#define BITLENGTH (100) 	/* transmission time for one bit [ms] */
#define PREAMBLELENGTH (11) /* lenght of preamble in bit */
uint16_t preamble = 0b11100010010;
uint8_t preambleCounter = 0;
uint16_t dataCounter = 0;		/* holds the data bit position */
uint8_t amountOfChars = 0;
uint16_t *result = NULL;	/* contains the postprocessed data after hamming and interleaving */
void init(void);
void hamming(uint16_t *result, uint8_t length);
void interleaving(char *message, uint16_t *result, uint8_t length);
/* ---- SETUP END ---- */

int main(void) {

    /* Init board hardware. */
    BOARD_InitBootPins();
    BOARD_InitBootClocks();
    BOARD_InitBootPeripherals();
#ifndef BOARD_INIT_DEBUG_CONSOLE_PERIPHERAL
    /* Init FSL debug console. */
    BOARD_InitDebugConsole();
#endif

    /* prepare data */
	char textToTransmit[] = "PAIND2023";

	/* get number of characters in string to process */
	while(textToTransmit[amountOfChars]!='\0')
	{
		amountOfChars++;
	}

	/* allocate memory for data transmission */
	result = (uint16_t)calloc(amountOfChars, sizeof(uint16_t));

	/* generate interleaving */
	interleaving(textToTransmit, result, amountOfChars);

	/* generate hamming-code out of interleaved message */
	hamming(result, amountOfChars);

    /* enable automatic transmission of data */
    init();


    while(1) {
        __asm volatile ("nop");
    }
    return 0 ;
}

/* initialize the necessary pins and timers */
void init(void)
{
	    SIM->SCGC5 |= SIM_SCGC5_PORTB_MASK;							/* enable clock for Port B */
	    SIM->SCGC6 |= SIM_SCGC6_FTM2_MASK | SIM_SCGC6_FTM3_MASK;	/* enable clock for FTM2 (pin) & FTM3 (counter) */

	    /* pin-config GPIO */
	    PORTB->PCR[17] = PORT_PCR_MUX(1) | PORT_PCR_PE(1) | PORT_PCR_PS(1); 	/* SHDN; High = LDO ON */
	    PORTB->PCR[18] = PORT_PCR_MUX(3);										/* CTRL; High = Modulator ON = no impedance */
	    GPIOB->PDDR |= 1<<17 ;													/* define direction as OUTPUT */
	    GPIOB->PDOR |= 1<<17;													/* enable SHDN */

	    /* pin-config FTM2 */
	    FTM2->SC = FTM_SC_CLKS(1) 			/* System-clock = 120 MHz */
	        		| FTM_SC_CPWMS(0)		/* disable PWM */
					| FTM_SC_PS(0); 		/* PS:0 -> 120 MHz */
	    FTM2->MOD = 0x2; 	/* disable modulo register */
	    FTM2->CONTROLS[0].CnSC = FTM_CnSC_MSB(0) | FTM_CnSC_MSA(1) | FTM_CnSC_ELSB(0) | FTM_CnSC_ELSA(1); /* Output Compare; Toggle on match */
	    FTM2->CONTROLS[0].CnV = 0x2;	/* set compare register to 2 = 10MHz */
	    FTM2->COMBINE = 0x0;			/* be sure that this register is set to 0 */

	    /* config FTM3 */
	    FTM3->SC = FTM_SC_CLKS(2) 		/* Fixed Frequency Clock (MCGFFCLK) = 250 kHz */
	            	| FTM_SC_TOIE(1)	/* enable interrupt */
	            	| FTM_SC_CPWMS(0)	/* disable PWM */
					| FTM_SC_PS(2);		/* set prescaler to 2 = Divide CLKS by 4 */
	    FTM3->MOD = ((BITLENGTH * 250000) / 4000) - 1;	/* MOD = (Time_to_overflow * clock) / (prescaler * 1000) - 1 */
	    NVIC_SetPriority(FTM3_IRQn, 12); 				/* set priority to 12 */
	    NVIC_EnableIRQ(FTM3_IRQn); 						/* enable interrupt (Page 60 RefMan) */
}

/* generate the hamming code (16,8)
 * this results in the expansion of an 8 bit interleaved value
 * into a 16 bit value */
void hamming(uint16_t *result, uint8_t amountOfChars)
{
    char hA[16] = { 0 };
    /* fill array with redundant data */
    hA[13] = 0;
    hA[14] = 1;
    hA[15] = 0;
    for (uint8_t i = 0; i < amountOfChars; i++) {
        hA[3] = (result[i] 	& (1 << 7))  	? 	1 : 0;
        hA[5] = (result[i] 	& (1 << 6))  	? 	1 : 0;
        hA[6] = (result[i] 	& (1 << 5))  	? 	1 : 0;
        hA[7] = (result[i] 	& (1 << 4))  	? 	1 : 0;
        hA[9] = (result[i] 	& (1 << 3))  	? 	1 : 0;
        hA[10] = (result[i] 	& (1 << 2)) 	? 	1 : 0;
        hA[11] = (result[i] 	& (1 << 1)) 	? 	1 : 0;
        hA[12] = (result[i] 	& 1)        	? 	1 : 0;
        hA[1] = ((hA[3] ^ hA[5] ^ hA[7] ^ hA[9]  ^ hA[11] ^ hA[13] ^ hA[15]) & 1)   ? 1 : 0;
        hA[2] = ((hA[3] ^ hA[6] ^ hA[7] ^ hA[10] ^ hA[11] ^ hA[14] ^ hA[15]) & 1)   ? 1 : 0;
        hA[4] = ((hA[5] ^ hA[6] ^ hA[7] ^ hA[12] ^ hA[13] ^ hA[14] ^ hA[15]) & 1)   ? 1 : 0;
        hA[8] = ((hA[9] ^ hA[10] ^ hA[11] ^ hA[12] ^ hA[13] ^ hA[14] ^ hA[15]) & 1) ? 1 : 0;
        hA[0] = ((hA[1] ^ hA[2] ^ hA[3] ^ hA[4] ^ hA[5] ^ hA[6] ^ hA[7] ^ hA[8] ^ hA[9] ^ hA[10] ^ hA[11] ^ hA[12] ^ hA[13] ^ hA[14] ^ hA[15]) & 1) ? 1 : 0;
        /* store hamming-data into output */
        for(uint8_t j = 0; j < 16; j++){
        	result[i] &= hA[j] << (15-j);
        }
        printf("%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d\n", hA[0], hA[1], hA[2], hA[3], hA[4], hA[5], hA[6], hA[7], hA[8], hA[9], hA[10], hA[11], hA[12], hA[13], hA[14], hA[15]);
    }
}

/* interlaves the bits of a message
 * every ASCII character gets split up into 8 individual bits */
void interleaving(char *message, uint16_t *result, uint8_t length)
{
	for(uint16_t i = 0; i < length; i++)
	{
		for(uint8_t j = 0; j < 8; j++)
		{
			result[i] |= ((message[j] >> i) & 1) << j; /* starts at MSB of each ASCII-character */
		}
		printf("%X", result[i]);
	}
}

/* turns the pin on / off every BITLENGTH ms */
void FTM3_IRQHandler(void)
{
	FTM3->SC ^= FTM_SC_TOF_MASK;	/* reactivate Interrupt for next call */
	/* transmit preamble */
	if(preambleCounter < PREAMBLELENGTH)
	{
		if((preamble & (1 << (PREAMBLELENGTH - preambleCounter - 1))))
		{
			FTM2->SC = 1 << 3; /* turn ON the high frequency PORTB, PIN 18 */
		}
		else
		{
			FTM2->SC &= 0b1110111; /* turn OFF the high frequency PORTB, PIN 18 */
		}
		preambleCounter++;
	}
	/* transmit payload */
	else
	{
		if(result[dataCounter / 16] & (1 << (dataCounter % 16)))
		{
			FTM2->SC = 1 << 3; /* turn ON the high frequency PORTB, PIN 18 */
		}
		else
		{
			FTM2->SC &= 0b1110111; /* turn OFF the high frequency PORTB, PIN 18 */
		}
		dataCounter++;
	}

//	FTM2->SC ^= 1 << 3;				/* toggle on and off the high frequency PORTB, PIN 18, depending on the last state */
}
