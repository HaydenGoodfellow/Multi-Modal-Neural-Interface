/*
 * Copyright (c) 2016 Intel Corporation
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr.h>
#include <device.h>
#include <devicetree.h>
#include <drivers/gpio.h>
#include <drivers/spi.h>

/* 1000 msec = 1 sec */
#define SLEEP_TIME_MS 1000

/* The devicetree node identifier for the "led0" alias. */
#define LED0_NODE DT_ALIAS(led0)

#define MY_SPI_MASTER DT_NODELABEL(my_spi_master)

// SPI master functionality
const struct device *spi_dev;

struct spi_cs_control spim_cs = {
		.gpio = SPI_CS_GPIOS_DT_SPEC_GET(DT_NODELABEL(reg_my_spi_master)),
		.delay = 0,
};

static void spi_init(void)
{
	spi_dev = DEVICE_DT_GET(MY_SPI_MASTER);
	if (!device_is_ready(spi_dev))
	{
		printk("SPI master device not ready!\n");
	}
	if (!device_is_ready(spim_cs.gpio.port))
	{
		printk("SPI master chip select device not ready!\n");
	}
}

static const struct spi_config spi_cfg = {
		.operation = SPI_WORD_SET(8) | SPI_TRANSFER_MSB |
								 SPI_MODE_CPHA,
		.frequency = 500000,
		.slave = 0,
		.cs = &spim_cs,
};

static int spi_write_test_msg(uint8_t *i, int n)
{
	static uint8_t counter = 0;
	static uint8_t rx_buffer[4];

	const struct spi_buf tx_buf = {
			.buf = i,
			.len = n * sizeof(uint8_t)};
	const struct spi_buf_set tx = {
			.buffers = &tx_buf,
			.count = 1};

	struct spi_buf rx_buf = {
			.buf = rx_buffer,
			.len = sizeof(rx_buffer),
	};
	const struct spi_buf_set rx = {
			.buffers = &rx_buf,
			.count = 1};

	// Update the TX buffer with a rolling counter
	printk("SPI TX: 0x%.2x, 0x%.2x\n", i[0], i[1], i[2]);

	int ret = gpio_pin_configure_dt(&spim_cs, GPIO_ACTIVE_LOW);
	if (ret < 0)
	{
		return;
	}

	// Start transaction
	int error = spi_transceive(spi_dev, &spi_cfg, &tx, &rx);
	if (error != 0)
	{
		printk("SPI transceive error: %i\n", error);
		return error;
	}

	ret = gpio_pin_configure_dt(&spim_cs, GPIO_ACTIVE_HIGH);
	if (ret < 0)
	{
		return;
	}

	printk("SPI RX: 0x%.2x, 0x%.2x, 0x%.2x, 0x%.2x\n", rx_buffer[0], rx_buffer[1], rx_buffer[2], rx_buffer[3]);
	return 0;
}

/*
 * A build error on this line means your board is unsupported.
 * See the sample documentation for information on how to fix this.
 */
static const struct gpio_dt_spec led = GPIO_DT_SPEC_GET(LED0_NODE, gpios);

void main(void)
{
	int ret;

	if (!device_is_ready(led.port))
	{
		return;
	}

	ret = gpio_pin_configure_dt(&led, GPIO_OUTPUT_ACTIVE);
	if (ret < 0)
	{
		return;
	}

	spi_init();

	printk("SPI master/slave example started\n");

	uint8_t tx_buffer[3];
	tx_buffer[0] = 0x20;
	tx_buffer[1] = 0x04;
	tx_buffer[2] = 0x00;

	spi_write_test_msg(tx_buffer, 3);

	k_sleep(K_MSEC(1));

	uint8_t tx_buffer2[2];
	tx_buffer2[0] = 0x6D;
	tx_buffer2[1] = 0xff;

	spi_write_test_msg(tx_buffer2, 2);
}
