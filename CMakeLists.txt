# SPDX-License-Identifier: Apache-2.0

cmake_minimum_required(VERSION 3.20.0)
find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})
project(multi-modal-neural-interface)

add_compile_definitions(CHIPSEL_594X)

target_include_directories(app PRIVATE include)

target_sources(app PRIVATE src/main.c src/nrf5340port.c include/ad5940lib/ad5940.h include/ad5940lib/ad5940.c)
