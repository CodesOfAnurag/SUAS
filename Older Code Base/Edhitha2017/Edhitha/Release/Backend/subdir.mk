################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
CPP_SRCS += \
../Backend/Baelando.cpp 

OBJS += \
./Backend/Baelando.o 

CPP_DEPS += \
./Backend/Baelando.d 


# Each subdirectory must supply rules for building sources it contributes
Backend/%.o: ../Backend/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: Cross G++ Compiler'
	g++ -O3 -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


