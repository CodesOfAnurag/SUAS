mkdir Backend/Engine/Inotifier
mkdir Backend/Engine/MetaData
mkdir Backend/Engine/PreProcessing/ColourFilter
mkdir Backend/Engine/PreProcessing/OCR
mkdir Backend/Engine/PreProcessing/ShapeDetect

g++ -std=c++0x -I/usr/local/include/boost -I/usr/local/include/opencv -O3 -Wall -c -fmessage-length=0 -o Backend/Engine/PreProcessing/AnomalyDetect.o ../Backend/Engine/PreProcessing/AnomalyDetect.cpp 
g++ -std=c++0x -I/usr/local/include/boost -I/usr/local/include/opencv -O3 -Wall -c -fmessage-length=0 -o Backend/Engine/MetaData/metadata.o ../Backend/Engine/MetaData/metadata.cpp 
g++ -std=c++0x -I/usr/local/include/boost -I/usr/local/include/opencv -O3 -Wall -c -fmessage-length=0 -o Temp.o ../Temp.cpp 
g++ -std=c++0x -I/usr/local/include/boost -I/usr/local/include/opencv -O3 -Wall -c -fmessage-length=0 -o Backend/Engine/Bae.o ../Backend/Engine/Bae.cpp 
g++ -std=c++0x -I/usr/local/include/boost -I/usr/local/include/opencv -O3 -Wall -c -fmessage-length=0 -o Backend/Engine/Inotifier/Watch.o ../Backend/Engine/Inotifier/Watch.cpp 
g++ -std=c++0x -I/usr/local/include/boost -I/usr/local/include/opencv -O3 -Wall -c -fmessage-length=0 -o Backend/Engine/PreProcessing/ColourFilter/ColorDetect.o ../Backend/Engine/PreProcessing/ColourFilter/ColorDetect.cpp 
g++ -std=c++0x -I/usr/local/include/boost -I/usr/local/include/opencv -O3 -Wall -c -fmessage-length=0 -o Backend/Engine/PreProcessing/ShapeDetect/ShapeDetect.o ../Backend/Engine/PreProcessing/ShapeDetect/ShapeDetect.cpp 
g++ -std=c++0x -I/usr/local/include/boost -I/usr/local/include/opencv -O3 -Wall -c -fmessage-length=0 -o Backend/Baelando.o ../Backend/Baelando.cpp 
gcc -I/usr/local/include/boost -O3 -Wall -c -fmessage-length=0 -o Backend/Engine/MetaData/gpsData.o ../Backend/Engine/MetaData/gpsData.c 
g++ -std=c++0x -I/usr/local/include/boost -I/usr/local/include/opencv -O3 -Wall -c -fmessage-length=0 -o Main.o ../Main.cpp 
g++ -std=c++0x -I/usr/local/include/boost -I/usr/local/include/opencv -O3 -Wall -c -fmessage-length=0 -o Backend/Engine/PreProcessing/OCR/TesseractOCR.o ../Backend/Engine/PreProcessing/OCR/TesseractOCR.cpp 
g++ -L/usr/local/lib -o Edhitha Backend/Baelando.o Backend/Engine/Bae.o Backend/Engine/Inotifier/Watch.o Backend/Engine/MetaData/gpsData.o Backend/Engine/MetaData/metadata.o Backend/Engine/PreProcessing/AnomalyDetect.o Backend/Engine/PreProcessing/ColourFilter/ColorDetect.o Backend/Engine/PreProcessing/OCR/TesseractOCR.o Backend/Engine/PreProcessing/ShapeDetect/ShapeDetect.o Main.o Temp.o -lpthread -lGeographic -lexif -llept -ltbb -ltesseract -lboost_thread -lboost_system -lboost_filesystem -lopencv_core -lopencv_features2d -lopencv_imgproc -lopencv_imgcodecs -lopencv_highgui 

