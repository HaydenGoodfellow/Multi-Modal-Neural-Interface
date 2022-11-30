/*
 * Copyright (c) 2016 Intel Corporation
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr.h>
#include <device.h>
#include <devicetree.h>
#include "../include/ad5940lib/ad5940.h"

/* 1000 msec = 1 sec */
#define SLEEP_TIME_MS 1000

// #define MY_SPI_MASTER DT_NODELABEL(my_spi_master)

// static int spi_write_test_msg(uint8_t *i, int n)
// {
// 	static uint8_t counter = 0;
// 	static uint8_t rx_buffer[4];

// 	// Update the TX buffer with a rolling counter
// 	printk("SPI TX: 0x%.2x, 0x%.2x\n", i[0], i[1], i[2]);

// 	printk("SPI RX: 0x%.2x, 0x%.2x, 0x%.2x, 0x%.2x\n", rx_buffer[0], rx_buffer[1], rx_buffer[2], rx_buffer[3]);
// 	return 0;
// }

/*
 * A build error on this line means your board is unsupported.
 * See the sample documentation for information on how to fix this.
 */
void main(void)
{
	AD5940_MCUResourceInit(0);

	printk("resource init\n");

	AD5940_HWReset();

	printk("hw reset\n");

	AD5940_Initialize();
	printk("initialize\n");

	unsigned long temp = AD5940_ReadReg(REG_AFECON_ADIID);
	printk("Read ADIID register, got: 0x%04lx\n", temp);

	return;
}
