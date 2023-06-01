################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../drivers/fsl_adc16.c \
../drivers/fsl_clock.c \
../drivers/fsl_common.c \
../drivers/fsl_common_arm.c \
../drivers/fsl_dspi.c \
../drivers/fsl_gpio.c \
../drivers/fsl_i2c.c \
../drivers/fsl_rtc.c \
../drivers/fsl_smc.c \
../drivers/fsl_uart.c 

OBJS += \
./drivers/fsl_adc16.o \
./drivers/fsl_clock.o \
./drivers/fsl_common.o \
./drivers/fsl_common_arm.o \
./drivers/fsl_dspi.o \
./drivers/fsl_gpio.o \
./drivers/fsl_i2c.o \
./drivers/fsl_rtc.o \
./drivers/fsl_smc.o \
./drivers/fsl_uart.o 

C_DEPS += \
./drivers/fsl_adc16.d \
./drivers/fsl_clock.d \
./drivers/fsl_common.d \
./drivers/fsl_common_arm.d \
./drivers/fsl_dspi.d \
./drivers/fsl_gpio.d \
./drivers/fsl_i2c.d \
./drivers/fsl_rtc.d \
./drivers/fsl_smc.d \
./drivers/fsl_uart.d 


# Each subdirectory must supply rules for building sources it contributes
drivers/%.o: ../drivers/%.c drivers/subdir.mk
	@echo 'Building file: $<'
	@echo 'Invoking: MCU C Compiler'
	arm-none-eabi-gcc -D__REDLIB__ -DCPU_MK22FN512VLH12 -DCPU_MK22FN512VLH12_cm4 -DSDK_OS_BAREMETAL -DSERIAL_PORT_TYPE_UART=1 -DSDK_DEBUGCONSOLE=0 -DCR_INTEGER_PRINTF -DPRINTF_FLOAT_ENABLE=0 -D__MCUXPRESSO -D__USE_CMSIS -DDEBUG -I"C:\Users\FrosterOTG\OneDrive - Hochschule Luzern\Module\TA.BA_PAIND+E1.F23\Software_Code\tinyK22\PAIND_Backscattering_Modulator\board" -I"C:\Users\FrosterOTG\OneDrive - Hochschule Luzern\Module\TA.BA_PAIND+E1.F23\Software_Code\tinyK22\PAIND_Backscattering_Modulator\source" -I"C:\Users\FrosterOTG\OneDrive - Hochschule Luzern\Module\TA.BA_PAIND+E1.F23\Software_Code\tinyK22\PAIND_Backscattering_Modulator\drivers" -I"C:\Users\FrosterOTG\OneDrive - Hochschule Luzern\Module\TA.BA_PAIND+E1.F23\Software_Code\tinyK22\PAIND_Backscattering_Modulator\component\serial_manager" -I"C:\Users\FrosterOTG\OneDrive - Hochschule Luzern\Module\TA.BA_PAIND+E1.F23\Software_Code\tinyK22\PAIND_Backscattering_Modulator\utilities" -I"C:\Users\FrosterOTG\OneDrive - Hochschule Luzern\Module\TA.BA_PAIND+E1.F23\Software_Code\tinyK22\PAIND_Backscattering_Modulator\component\uart" -I"C:\Users\FrosterOTG\OneDrive - Hochschule Luzern\Module\TA.BA_PAIND+E1.F23\Software_Code\tinyK22\PAIND_Backscattering_Modulator\component\lists" -I"C:\Users\FrosterOTG\OneDrive - Hochschule Luzern\Module\TA.BA_PAIND+E1.F23\Software_Code\tinyK22\PAIND_Backscattering_Modulator\CMSIS" -I"C:\Users\FrosterOTG\OneDrive - Hochschule Luzern\Module\TA.BA_PAIND+E1.F23\Software_Code\tinyK22\PAIND_Backscattering_Modulator\device" -O0 -fno-common -g3 -Wall -c -ffunction-sections -fdata-sections -ffreestanding -fno-builtin -fmerge-constants -fmacro-prefix-map="$(<D)/"= -mcpu=cortex-m4 -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -D__REDLIB__ -fstack-usage -specs=redlib.specs -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.o)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


