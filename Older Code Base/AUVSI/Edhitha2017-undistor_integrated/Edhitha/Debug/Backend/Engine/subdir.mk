################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
CPP_SRCS += \
../Backend/Engine/Bae.cpp 

OBJS += \
./Backend/Engine/Bae.o 

CPP_DEPS += \
./Backend/Engine/Bae.d 


# Each subdirectory must supply rules for building sources it contributes
Backend/Engine/%.o: ../Backend/Engine/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -O0 -g3 -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


