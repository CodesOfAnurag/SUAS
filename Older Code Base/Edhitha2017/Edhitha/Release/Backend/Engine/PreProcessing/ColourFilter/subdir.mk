################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
CPP_SRCS += \
../Backend/Engine/PreProcessing/ColourFilter/ColorDetect.cpp 

OBJS += \
./Backend/Engine/PreProcessing/ColourFilter/ColorDetect.o 

CPP_DEPS += \
./Backend/Engine/PreProcessing/ColourFilter/ColorDetect.d 


# Each subdirectory must supply rules for building sources it contributes
Backend/Engine/PreProcessing/ColourFilter/%.o: ../Backend/Engine/PreProcessing/ColourFilter/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: Cross G++ Compiler'
	g++ -O3 -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


