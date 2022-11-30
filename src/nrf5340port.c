#include "../include/ad5940lib/ad5940.h"

#include <zephyr.h>
#include <nrfx_spim.h>
#include <hal/nrf_gpio.h>

#define SCLK_PIN 6
#define MOSI_PIN 7
#define CS_PIN 11
#define MISO_PIN 25
#define RESET_PIN 26

static volatile bool ad5940_spi_xfer_done = false;
volatile static uint32_t ucInterrupted = 0;

void ad5940_spi_event_handler(nrfx_spim_evt_t const *p_event, void *p_context)
{
  if (p_event->type == NRFX_SPIM_EVENT_DONE)
  {
    ad5940_spi_xfer_done = true;
  }
}

static const nrfx_spim_t instance = NRFX_SPIM_INSTANCE(4);

static void ad5940_spi_init(void)
{
  nrfx_spim_config_t spi_cfg = {
      .bit_order = NRF_SPIM_BIT_ORDER_MSB_FIRST,
      .frequency = NRF_SPIM_FREQ_8M,
      .mode = NRF_SPIM_MODE_0,
      .ss_pin = NRFX_SPIM_PIN_NOT_USED,
      .miso_pin = 25,
      .mosi_pin = 7,
      .sck_pin = 6,
  };

  nrfx_err_t err = nrfx_spim_init(&instance, &spi_cfg, &ad5940_spi_event_handler, NULL);
  if (err != NRFX_SUCCESS)
  {
    printk("error: %d\n", err);
    if (err == NRFX_ERROR_INVALID_STATE)
    {
      printk("invalid state\n");
    }
    else if (err == NRFX_ERROR_BUSY)
    {
      printk("busy\n");
    }
    else if (err == NRFX_ERROR_NOT_SUPPORTED)
    {
      printk("not supported\n");
    }
    else if (err == NRFX_ERROR_INVALID_PARAM)
    {
      printk("invalid param\n");
    }
  }
}

void AD5940_ReadWriteNBytes(unsigned char *pSendBuffer, unsigned char *pRecvBuff, unsigned long length)
{
  nrfx_spim_xfer_desc_t desc = {
      .p_rx_buffer = pRecvBuff,
      .p_tx_buffer = pSendBuffer,
      .rx_length = length,
      .tx_length = length,
  };
  nrfx_err_t err = nrfx_spim_xfer(&instance, &desc, 0);
  if (err != NRFX_SUCCESS)
  {
    printk("error: %d\n", err);
    if (err == NRFX_ERROR_INVALID_STATE)
    {
      printk("invalid state\n");
    }
    else if (err == NRFX_ERROR_BUSY)
    {
      printk("busy\n");
    }
    else if (err == NRFX_ERROR_NOT_SUPPORTED)
    {
      printk("not supported\n");
    }
    else if (err == NRFX_ERROR_INVALID_PARAM)
    {
      printk("invalid param\n");
    }
    else if (err == NRFX_ERROR_INVALID_ADDR)
    {
      printk("invalid addr\n");
    }
  }
  while (!ad5940_spi_xfer_done)
    ;
  ad5940_spi_xfer_done = false;
}

void AD5940_CsClr(void)
{
  nrf_gpio_pin_clear(CS_PIN);
}

void AD5940_CsSet(void)
{
  nrf_gpio_pin_set(CS_PIN);
}

void AD5940_RstClr(void)
{
  nrf_gpio_pin_clear(RESET_PIN);
}

void AD5940_RstSet(void)
{
  nrf_gpio_pin_set(RESET_PIN);
}

void AD5940_Delay10us(uint32_t time)
{
  time /= 100;
  if (time == 0)
    time = 1;
  k_msleep(time);
}

uint32_t AD5940_GetMCUIntFlag(void)
{
  return ucInterrupted;
}

uint32_t AD5940_ClrMCUIntFlag(void)
{
  ucInterrupted = 0;
  return 1;
}

uint32_t
AD5940_MCUResourceInit(void *pCfg)
{
  nrf_gpio_cfg_output(CS_PIN);
  nrf_gpio_cfg_output(SCLK_PIN);
  nrf_gpio_cfg_output(MOSI_PIN);
  nrf_gpio_cfg_input(MISO_PIN, NRF_GPIO_PIN_PULLUP);

  nrf_gpio_cfg_output(RESET_PIN);

  AD5940_CsSet();
  AD5940_RstSet();

  ad5940_spi_init();

  return 0;
}