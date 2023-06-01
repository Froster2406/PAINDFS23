################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../board/board.c \
../board/clock_config.c \
../board/peripherals.c \
../board/pin_mux.c 

OBJS += \
./board/board.o \
./board/clock_config.o \
./board/peripherals.o \
./board/pin_mux.o 

C_DEPS += \
./board/board.d \
./board/clock_config.d \
./board/peripherals.d \
./board/pin_mux.d 


# Each subdirectory must supply rules for building sources it contributes
board/%.o: ../board/%.c board/subdir.mk
	@echo 'Building file: $<'
	@echo 'Invoking: MCU C Compiler'
	arm-none-eabi-gcc -D__REDLIB__ -DCPU_MK22FN512VLH12 -DCPU_MK22FN512VLH12_cm4 -DSDK_OS_BAREMETAL -DSERIAL_PORT_TYPE_UART=1 -DSDK_DEBUGCONSOLE=0 -DCR_INTEGER_PRINTF -DPRINTF_FLOAT_ENABLE=0 -D__MCUXPRESSO -D__USE_CMSIS -DDEBUG -I"C:\Users\FrosterOTG\OneDrive - Hochschule Luzern\Module\TA.BA_PAIND+E1.F23\Software_Code\tinyK22\PAIND_Backscattering_Modulator\board" -I"C:\Users\FrosterOTG\OneDrive - Hochschule Luzern\Module\TA.BA_PAIND+E1.F23\Software_Code\tinyK22\PAIND_Backscattering_Modulator\source" -I"C:\Users\FrosterOTG\OneDrive - Hochschule Luzern\Module\TA.BA_PAIND+E1.F23\Software_Code\tinyK22\PAIND_Backscattering_Modulator\drivers" -I"C:\Users\FrosterOTG\OneDrive - Hochschule Luzern\Module\TA.BA_PAIND+E1.F23\Software_Code\tinyK22\PAIND_Backscattering_Modulator\component\serial_manager" -I"C:\Users\FrosterOTG\OneDrive - Hochschule Luzern\Module\TA.BA_PAIND+E1.F23\Software_Code\tinyK22\PAIND_Backscattering_Modulator\utilities" -I"C:\Users\FrosterOTG\OneDrive - Hochschule Luzern\Module\TA.BA_PAIND+E1.F23\Software_Code\tinyK22\PAIND_Backscattering_Modulator\component\uart" -I"C:\Users\FrosterOTG\OneDrive - Hochschule Luzern\Module\TA.BA_PAIND+E1.F23\Software_Code\tinyK22\PAIND_Backscattering_Modulator\component\lists" -I"C:\Users\FrosterOTG\OneDrive - Hochschule Luzern\Module\TA.BA_PAIND+E1.F23\Software_Code\tinyK22\PAIND_Backscattering_Modulator\CMSIS" -I"C:\Users\FrosterOTG\OneDrive - Hochschule Luzern\Module\TA.BA_PAIND+E1.F23\Software_Code\tinyK22\PAIND_Backscattering_Modulator\device" -O0 -fno-common -g3 -Wall -c -ffunction-sections -fdata-sections -ffreestanding -fno-builtin -fmerge-constants -fmacro-prefix-map="$(<D)/"= -mcpu=cortex-m4 -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -D__REDLIB__ -fstack-usage -specs=redlib.specs -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.o)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


