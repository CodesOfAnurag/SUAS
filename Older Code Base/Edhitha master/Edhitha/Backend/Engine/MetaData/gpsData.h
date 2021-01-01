#ifdef __GPSDATA_H
extern "C"{
#endif
#define GPSDATA_H_

	#include <stdio.h>
	#include <stdlib.h>
	#include <string.h>
	#include <libexif/exif-data.h>
	#include <dirent.h>

	
	void entryPoint(const char* address, long double* latitude, long double* longitude, long double* imageDirection, long double* altitude);

	#ifdef __GPS_DATA_H
}
#endif
