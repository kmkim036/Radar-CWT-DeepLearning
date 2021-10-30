/**
 * @file global_ccu4.h
 * @date 2016-02-10
 *
 * NOTE:
 * This file is generated by DAVE. Any manual modification done to this file will be lost when the code is regenerated.
 *
 * @cond
 ***********************************************************************************************************************
 * GLOBAL_CCU4 v4.1.12 - Configures the global properties of CCU4x peripheral instance.
 *
 * Copyright (C) 2016-2019 Infineon Technologies AG
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification,are permitted provided that the
 * following conditions are met:
 *
 *   Redistributions of source code must retain the above copyright notice, this list of conditions and the  following
 *   disclaimer.
 *
 *   Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
 *   following disclaimer in the documentation and/or other materials provided with the distribution.
 *
 *   Neither the name of the copyright holders nor the names of its contributors may be used to endorse or promote
 *   products derived from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
 * INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE  FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
 * SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 * WHETHER IN CONTRACT, STRICT LIABILITY,OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT  OF THE
 * USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 * To improve the quality of the software, users are encouraged to share modifications, enhancements or bug fixes
 * with Infineon Technologies AG (dave@infineon.com).
 ***********************************************************************************************************************
 *
 * Change History
 * --------------
 *
 * 2015-02-16:
 *     - Initial version<br>
 *
 * 2015-05-08:
 *     - New parameter "syncstart_trigger_msk" is added in APP handle to start the specific kernel/s<br>
 *     - File guard updated according to the guidelines<br>
 *
 * 2015-05-22:
 *     - API names changed
 *         a. GLOBAL_CCU4_SyncStart_TriggerLow() --> GLOBAL_CCU4_SyncStartTriggerLow()<br>
 *         b. GLOBAL_CCU4_SyncStart_TriggerHigh() --> GLOBAL_CCU4_SyncStartTriggerHigh()<br>
 *
 * 2015-06-20:
 *     - Guidelines update
 * 2015-07-31:
 *     - xmc_scu.h file is included
 *
 * 2016-01-06:
 *     - Added a check for XMC4 devices, to verify that CCU clock is enabled or not in CLOCK_XMC4 APP.
 *     - Removed #error statement.
 * @endcond
 *
 */
#ifndef GLOBAL_CCU4_H
#define GLOBAL_CCU4_H

/***********************************************************************************************************************
 * HEADER FILES
 **********************************************************************************************************************/
#include <xmc_ccu4.h>
#include <xmc_scu.h>
#include <DAVE_Common.h>
#include "global_ccu4_conf.h"

/**********************************************************************************************************************
 * MACROS
 **********************************************************************************************************************/
#if (!((XMC_LIB_MAJOR_VERSION == 2U) && \
       (XMC_LIB_MINOR_VERSION >= 0U) && \
       (XMC_LIB_PATCH_VERSION >= 0U)))
#error "GLOBAL_CCU4 requires XMC Peripheral Library v2.0.0 or higher"
#endif

/**********************************************************************************************************************
 * ENUMS
 **********************************************************************************************************************/
/**
 * @ingroup GLOBAL_CCU4_enumerations
 * @{
 */
/**
 * @brief Return status of the GLOBAL_CCU4 APP
 */
typedef enum GLOBAL_CCU4_STATUS
{
  GLOBAL_CCU4_STATUS_SUCCESS = 0U, /**< Status success */
  GLOBAL_CCU4_STATUS_FAILURE /**< Status failure */
} GLOBAL_CCU4_STATUS_t;
/**
* @}
*/
/***********************************************************************************************************************
* DATA STRUCTURES
***********************************************************************************************************************/

/**
 * @ingroup GLOBAL_CCU4_datastructures
 * @{
 */

/**
 * This saves the context of the GLOBAL_CCU4 APP.
 */
typedef struct GLOBAL_CCU4
{
  const uint32_t module_frequency; /**< fccu frequency */
  const XMC_SCU_CCU_TRIGGER_t syncstart_trigger_msk; /**< Mask to start the timers synchronously */
  XMC_CCU4_MODULE_t* const module_ptr;   /**< reference to module handle */
  XMC_CCU4_SLICE_MCMS_ACTION_t const mcs_action; /**< Shadow transfer of selected values in multi-channel mode */
  bool  is_initialized; /**< Indicates initialized state of particular instance of the APP */
} GLOBAL_CCU4_t;

/**
 * @}
 */
/***********************************************************************************************************************
* API Prototypes
***********************************************************************************************************************/
#ifdef __cplusplus
extern "C" {
#endif
/**
 * @ingroup GLOBAL_CCU4_apidoc
 * @{
 */

/**
 * @brief Get GLOBAL_CCU4 APP version
 * @return DAVE_APP_VERSION_t APP version information (major, minor and patch number)
 * <BR>
 * \par<b>Description:</b><br>
 * The function can be used to check application software compatibility with a
 * specific version of the APP.
 *
 * Example Usage:
 * @code
 * #include <DAVE.h>
 * int main(void)
 * {
 *   DAVE_STATUS_t status;
 *   DAVE_APP_VERSION_t app_version;
 *
 *   status = DAVE_Init();	// GLOBAL_CCU4_Init() is called from DAVE_Init()
 *
 *   app_version = GLOBAL_CCU4_GetAppVersion();
 *
 *   if (app_version.major != 4U)
 *   {
 *     // Probably, not the right version.
 *   }
 *
 *   while(1U)
 *   {
 *   }
 *   return 1;
 * }
 * @endcode<BR>
 */
DAVE_APP_VERSION_t GLOBAL_CCU4_GetAppVersion(void);

/**
 * @brief Initializes a GLOBAL_CCU4 with generated configuration.
 *
 * @param handle pointer to the GLOBAL_CCU4 APP handle structure.
 * @return GLOBAL_CCU4_STATUS_t\n  GLOBAL_CCU4_STATUS_SUCCESS : if initialization is successful\n
 *                                 GLOBAL_CCU4_STATUS_FAILURE : if initialization is failed\n
 * <BR>
 * \par<b>Description:</b><br>
 * <ul>
 * <li>Enable the module.</li>
 * <li>Start the prescaler.</li>
 * </ul>
 *
 * Example Usage:
 * @code
 * #include <DAVE.h>
 * int main(void)
 * {
 *  DAVE_STATUS_t init_status;
 *  init_status = DAVE_Init();	// GLOBAL_CCU4_Init(&GLOBAL_CCU4_0) will be called from DAVE_Init()
 *
 *  while(1)
 *  {
 *  }
 *  return 1;
 * }
 * @endcode<BR>
 */
GLOBAL_CCU4_STATUS_t GLOBAL_CCU4_Init(GLOBAL_CCU4_t* handle);

/**
 * @brief Start all the timers which are configured to start externally on positive edge.<br>
 * @param ccucon_msk mask for which kernels sync start has to be applied.
 * \par<b>Note:</b><br>
 * This mask has been generated in the APP handle and as a macro in global_ccu4_conf.h file.
 * 1. The variable from the APP handle is useful while starting the specific kernel/s
 * 2. GLOBAL_CCU4_CCUCON_Msk Macro from global_ccu4_conf.h file can be used to start all the selected kernels at a time.
 * @retval none
 *
 * \par<b>Description:</b><br>
 * The top level APPs have to be enabled, to start the timer externally with positive trigger edge.
 *
 * Example Usage:
 * @code
 * #include <DAVE.h>
 * int main(void)
 * {
 *   DAVE_STATUS_t status;
 *
 *   status = DAVE_Init();	// GLOBAL_CCU4_Init() is called from DAVE_Init()
 *
 *  // Below can be used to start the specific kernels, by generating two instance of APP
 *  // GLOBAL_CCU4_SyncStartTriggerHigh((uint32_t)(GLOBAL_CCU4_0.syncstart_trigger_msk | GLOBAL_CCU4_1.syncstart_trigger_msk));
 *  // Below can be used to start all the kernels simultaneously
 *   GLOBAL_CCU4_SyncStartTriggerHigh(GLOBAL_CCU4_CCUCON_Msk);
 *
 *   while(1)
 *   {
 *   }
 *
 *   return 1;
 * }
 * @endcode <BR> </p>
 */
__STATIC_INLINE void GLOBAL_CCU4_SyncStartTriggerHigh(uint32_t ccucon_msk)
{
  XMC_SCU_SetCcuTriggerHigh(ccucon_msk);
}

/**
 * @brief Start all the timers which are configured to start externally on negative edge.<br>
 * @param ccucon_msk mask for which kernels sync start has to be applied.
 * \par<b>Note:</b><br>
 * This mask has been generated in the APP handle and a macro in global_ccu4_conf.h file.
 * 1. The variable from the APP handle is useful while starting the specific kernel/s
 * 2. GLOBAL_CCU4_CCUCON_Msk Macro from global_ccu4_conf.h file can be used to start all the selected kernels at a time.
 * @retval none
 *
 * \par<b>Description:</b><br>
 * The top level APPs have to be enabled, to start the timer externally with negative trigger edge.
 *
 * Example Usage:
 * @code
 * #include <DAVE.h>
 * int main(void)
 * {
 *   DAVE_STATUS_t status;
 *
 *   status = DAVE_Init();	// GLOBAL_CCU4_Init() is called from DAVE_Init()
 *
 *  // Below can be used to start the specific kernels, by generating two instance of APP
 *  // GLOBAL_CCU4_SyncStartTriggerLow((uint32_t)(GLOBAL_CCU4_0.syncstart_trigger_msk | GLOBAL_CCU4_1.syncstart_trigger_msk));
 *  // Below can be used to start all the kernels simultaneously
 *   GLOBAL_CCU4_SyncStartTriggerLow(GLOBAL_CCU4_CCUCON_Msk);
 *
 *   while(1)
 *   {
 *   }
 *
 *   return 1;
 * }
 * @endcode <BR> </p>
 */
__STATIC_INLINE void GLOBAL_CCU4_SyncStartTriggerLow(uint32_t ccucon_msk)
{
  XMC_SCU_SetCcuTriggerLow(ccucon_msk);
}

/**
 * @}
 */


#include "global_ccu4_extern.h"

#ifdef __cplusplus
}
#endif

#endif /*CCUGLOBAL_H*/
