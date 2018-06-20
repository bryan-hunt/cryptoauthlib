/**
 * \file
 * \brief ATCA Constants typically used for debugging
 *
 * \copyright (c) 2017 Microchip Technology Inc. and its subsidiaries.
 *            You may use this software and any derivatives exclusively with
 *            Microchip products.
 *
 * \page License
 *
 * (c) 2017 Microchip Technology Inc. and its subsidiaries. You may use this
 * software and any derivatives exclusively with Microchip products.
 *
 * THIS SOFTWARE IS SUPPLIED BY MICROCHIP "AS IS". NO WARRANTIES, WHETHER
 * EXPRESS, IMPLIED OR STATUTORY, APPLY TO THIS SOFTWARE, INCLUDING ANY IMPLIED
 * WARRANTIES OF NON-INFRINGEMENT, MERCHANTABILITY, AND FITNESS FOR A
 * PARTICULAR PURPOSE, OR ITS INTERACTION WITH MICROCHIP PRODUCTS, COMBINATION
 * WITH ANY OTHER PRODUCTS, OR USE IN ANY APPLICATION.
 *
 * IN NO EVENT WILL MICROCHIP BE LIABLE FOR ANY INDIRECT, SPECIAL, PUNITIVE,
 * INCIDENTAL OR CONSEQUENTIAL LOSS, DAMAGE, COST OR EXPENSE OF ANY KIND
 * WHATSOEVER RELATED TO THE SOFTWARE, HOWEVER CAUSED, EVEN IF MICROCHIP HAS
 * BEEN ADVISED OF THE POSSIBILITY OR THE DAMAGES ARE FORESEEABLE. TO THE
 * FULLEST EXTENT ALLOWED BY LAW, MICROCHIPS TOTAL LIABILITY ON ALL CLAIMS IN
 * ANY WAY RELATED TO THIS SOFTWARE WILL NOT EXCEED THE AMOUNT OF FEES, IF ANY,
 * THAT YOU HAVE PAID DIRECTLY TO MICROCHIP FOR THIS SOFTWARE.
 *
 * MICROCHIP PROVIDES THIS SOFTWARE CONDITIONALLY UPON YOUR ACCEPTANCE OF THESE
 * TERMS.
 */

#include "atca_const.h"

/**
 *\defgroup basic Debug (atcab_)
 * \brief Get strings from type enumerations
 @{ */

typedef struct _string_table
{
    ATCAIfaceType    value;
    const char* name;
} string_table_ele;

#define TABLE_ENTRY(x)  {x, #x}
#define TABLE_SIZE(x)   sizeof(x)/sizeof(string_table_ele)

const string_table_ele ATCAIfaceTypeNames[] = {
    TABLE_ENTRY(ATCA_I2C_IFACE),
    TABLE_ENTRY(ATCA_SWI_IFACE),
    TABLE_ENTRY(ATCA_UART_IFACE),
    TABLE_ENTRY(ATCA_SPI_IFACE),
    TABLE_ENTRY(ATCA_HID_IFACE),
};

const string_table_ele ATCADeviceTypeNames[] = {
    TABLE_ENTRY(ATSHA204A),
    TABLE_ENTRY(ATECC108A),
    TABLE_ENTRY(ATECC508A),
};

const char* atcab_get_iface_name(ATCAIfaceType iface_type)
{
    uint32_t i;
    const char * rv = "UNKNOWN";
    for (i = 0; i < TABLE_SIZE(ATCAIfaceTypeNames); i++)
    {
        if (iface_type == ATCAIfaceTypeNames[i].value)
        {
            rv = ATCAIfaceTypeNames[i].name;
            break;
        }
    }
    return rv;
}

const char* atcab_get_dev_name(ATCADeviceType dev_type)
{
    uint32_t i;
    const char * rv = "UNKNOWN";
    for (i = 0; i < TABLE_SIZE(ATCAIfaceTypeNames); i++)
    {
        if (dev_type == ATCADeviceTypeNames[i].value)
        {
            rv = ATCADeviceTypeNames[i].name;
            break;
        }
    }
    return rv;
}

/** @} */
