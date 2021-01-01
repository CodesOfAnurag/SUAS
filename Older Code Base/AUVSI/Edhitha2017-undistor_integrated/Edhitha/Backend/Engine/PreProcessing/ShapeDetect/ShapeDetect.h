/*
 * Shape.h
 *
 *  Created on: 24-Mar-2017
 *      Author: niran
 */

#ifndef BACKEND_ENGINE_PREPROCESSING_SHAPEDETECT_H_
#define BACKEND_ENGINE_PREPROCESSING_SHAPEDETECT_H_

#include<iostream>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>

using namespace std;
using namespace cv;

namespace Edhitha2016{

	enum ValidShapes {SQUARE, RECTANGLE, TRAPEZOID, TRIANGLE, PENTAGON, HEXAGON, HEPTAGON, OCTAGON, CIRCLE, SEMICIRCLE, QUARTERCIRCLE, STAR, CROSS, NOTASHAPE}; 
	
	string returnShape(short int shape);
	unsigned short backEndProcessing(Mat source);
}

#endif /* SHAPE_H_ */
