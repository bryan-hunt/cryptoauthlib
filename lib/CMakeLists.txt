cmake_minimum_required(VERSION 2.6.4)
project(cryptoauth)

# Various Options for Build
option(ATCA_HAL_KIT_HID "Include the HID HAL Driver")
option(ATCA_HAL_I2C "Include the I2C Hal Driver - Linux & MCU only")
option(ATCA_PRINTF "Enable Debug print statements in library")
option(ATCA_PKCS11 "Build PKCS11 Library")

# Collect Library Sources
file(GLOB LIB_SRC RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} "*.c")
file(GLOB ATCACERT_SRC RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} "atcacert/*.c")
file(GLOB BASIC_SRC RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} "basic/*.c")
file(GLOB_RECURSE CRYPTO_SRC RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} "crypto/*.c")
file(GLOB HOST_SRC RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} "host/*.c")
file(GLOB JWT_SRC RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} "jwt/*.c")
file(GLOB PKCS11_SRC RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} "pkcs11/*.c")

# Add the basic sources to the library
add_library(cryptoauth SHARED
${LIB_SRC}
${ATCACERT_SRC}
${BASIC_SRC}
${CRYPTO_SRC}
${HOST_SRC}
${JWT_SRC}
hal/atca_hal.c )

if(WIN32)
target_sources(cryptoauth PUBLIC hal/hal_win_timer.c)
set(HID_SRC ../third_party/hidapi/windows/hid.c)
elseif(APPLE)
target_sources(cryptoauth PUBLIC hal/hal_linux_timer.c)
set(HID_SRC ../third_party/hidapi/mac/hid.c)
elseif(UNIX)
target_sources(cryptoauth PUBLIC hal/hal_linux_timer.c)
find_library(HAS_LIBUSB libusb)
if(HAS_LIBUSB)
set(HID_SRC ../third_party/hidapi/libusb/hid.c)
else()
set(HID_SRC ../third_party/hidapi/linux/hid.c)
endif()
set(TWI_SRC hal/hal_linux_i2c_userspace.c)
else()
set(HID_SRC )
endif()

if(ATCA_HAL_KIT_HID)
add_definitions(-DATCA_HAL_KIT_HID)
target_sources(cryptoauth PUBLIC hal/kit_protocol.c hal/hal_all_platforms_kit_hidapi.c ${HID_SRC})
endif(ATCA_HAL_KIT_HID)

if(ATCA_HAL_I2C)
add_definitions(-DATCA_HAL_I2C)
target_sources(cryptoauth PUBLIC ${TWI_SRC})
endif(ATCA_HAL_I2C)

# Add Remaining Sources depending on target library type
if(ATCA_PKCS11)
target_sources(cryptoauth PUBLIC ${PKCS11_SRC} ${ATCACERT_DEF_SRC})
set_target_properties(cryptoauth PROPERTIES OUTPUT_NAME "ateccx08pkcs11")
endif(ATCA_PKCS11)

if(ATCA_PRINTF)
add_definitions(-DATCAPRINTF)
endif(ATCA_PRINTF)

include_directories(cryptoauth PUBLIC ${CMAKE_CURRENT_SOURCE_DIR} ../third_party/hidapi/hidapi)

if(WIN32)
set_target_properties(cryptoauth PROPERTIES WINDOWS_EXPORT_ALL_SYMBOLS true)
target_link_libraries(cryptoauth setupapi.lib)
endif(WIN32)

if(UNIX)
if(HAS_LIBUSB)
target_link_libraries(cryptoauth usb-1.0)
endif()
target_link_libraries(cryptoauth udev rt)
endif(UNIX)


