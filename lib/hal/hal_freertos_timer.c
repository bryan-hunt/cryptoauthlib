/**
 * \file
 * \brief
 *
 * Prerequisite: add "Delay routines (service)" module to application in Atmel Studio
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

#include "FreeRTOS.h"
#include "task.h"

#include "atca_hal.h"

#if defined(WIN32)
#include "windows.h"
#define     atca_delay_ms_internal      Sleep
#elif defined(ASF_H)
#define     atca_delay_ms_internal      delay_ms
#endif

/**
 * \brief This function delays for a number of milliseconds.
 *
 *        You can override this function if you like to do
 *        something else in your system while delaying.
 *
 * \param[in] delay number of milliseconds to delay
 */
void atca_delay_ms(uint32_t delay)
{
    /* If the freeRTOS scheduler is running yield to other tasks */
    if (taskSCHEDULER_RUNNING == xTaskGetSchedulerState())
    {
        vTaskDelay(pdMS_TO_TICKS(delay));
    }
    else
    {
        atca_delay_ms_internal(delay);
    }
}

