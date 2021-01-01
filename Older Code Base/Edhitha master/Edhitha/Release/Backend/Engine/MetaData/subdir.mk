################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Backend/Engine/MetaData/gpsData.c 

CPP_SRCS += \
../Backend/Engine/MetaData/metadata.cpp 

OBJS += \
./Backend/Engine/MetaData/gpsData.o \
./Backend/Engine/MetaData/metadata.o 

C_DEPS += \
./Backend/Engine/MetaData/gpsData.d 

CPP_DEPS += \
./Backend/Engine/MetaData/metadata.d 


# Each subdirectory must supply rules for building sources it contributes
Backend/Engine/MetaData/%.o: ../Backend/Engine/MetaData/%.c
	@echo 'Building file: $<'
	@echo 'Invoking: Cross GCC Compiler'
	gcc -O3 -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '

Backend/Engine/MetaData/%.o: ../Backend/Engine/MetaData/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: Cross G++ Compiler'
	g++ -O3 -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


