
/*
 * AnomalyDetect.cpp
 *
 *  Created on: 15 Aug 2015
 *      Author: arjun
 */
#define CUDA
#ifdef CUDA
#include "AnomalyDetect.h"

namespace Edhitha2016{

int minArea;
int maxArea;

vector<vector<Point> > contours;

Mat __saliencyFrame;

Target currentTarget;

short targetCount;
unsigned int clamp(unsigned int number, unsigned int low, unsigned int high){
	if(number<low){
		return low;
	}
	else if(number>high){
		return high;
	}
	else
		return number;
}
AnomalyDetect::AnomalyDetect(){
	lowerBinaryThreshold=0;

	lowerAreaThreshold=0,upperAreaThreshold=0;
	isRectanglesBound=false;
}
AnomalyDetect::AnomalyDetect(Size dimension,int type,bool isRectanglesBound,
		double lowerAreaThreshold, double upperAreaThreshold, int lowerBinaryThreshold){


	this->__frame = Mat(dimension,type);

	this->lowerAreaThreshold = lowerAreaThreshold;
	this->upperAreaThreshold = upperAreaThreshold;

	this->lowerBinaryThreshold = lowerBinaryThreshold;

	minArea = (int)(lowerAreaThreshold*dimension.height*dimension.width);
	maxArea = (int)(upperAreaThreshold*dimension.height*dimension.width);

	this->isRectanglesBound =isRectanglesBound;

	__saliencyFrame = Mat(dimension,CV_8UC3);

	targetCount=0;

}
inline std::string intTostring(int number){

	std::stringstream ss;
	ss << number;
	return ss.str();
}

AnomalyDetect::~AnomalyDetect(){

	__frame.release();
	__saliencyFrame.release();

	printf("Destroyed CUDA\n");

}

Rect AnomalyDetect::enlargeROI(Mat frm, Rect boundingBox, int padding)
{
	 Rect returnRect = Rect(boundingBox.x - padding, boundingBox.y - padding, boundingBox.width + (padding * 2), boundingBox.height + (padding * 2));
	    if (returnRect.x < 0)returnRect.x = 0;
	    if (returnRect.y < 0)returnRect.y = 0;
	    if (returnRect.x+returnRect.width >= frm.cols)returnRect.width = frm.cols-returnRect.x;
	    if (returnRect.y+returnRect.height >= frm.rows)returnRect.height = frm.rows-returnRect.y;
	    return returnRect;
}
int e=1;
void AnomalyDetect::detectTarget() {
	Mat dst, grey;
	cv::cvtColor(__frame, dst, CV_BGR2HSV);
	Scalar avg_color = mean(dst);

	Mat newimg(dst.rows,dst.cols, CV_8UC3, avg_color);
      	Mat final;

      	cv::subtract(dst, newimg, final);
      	cv::cvtColor(final, final, CV_HSV2BGR);
      	cv::cvtColor(final, final, CV_BGR2GRAY);

      	vector<vector<Point> > contours;
      	vector<Rect> bboxes;
      	Ptr<MSER> mser = MSER::create(4,400,9000, 0.1, 0.2, 200, 1.01, 0.002, 5);
      	mser->detectRegions(final, contours, bboxes);
      	Mat crop2, crop, mask;
      	for(unsigned int i=0;i<bboxes.size();i++)
      			  {
      			   bboxes[i]=enlargeROI(__frame,bboxes[i],30);
      			   if(i>0)
      			   {
      				   if((abs(bboxes[i].width-bboxes[i-1].width)<10)&&(abs(bboxes[i].height-bboxes[i-1].height)<10))
      				   continue;

      			   }
      		__frame(bboxes[i]).clone().copyTo(crop2);
		Point center = (bboxes[i].br()+bboxes[i].tl())*0.5;
		//cout<<"xp = " <<center.x;
		//cout<<"yp = " <<center.y;
		currentTarget.localTargetPosition = center;
      		Mat img1,test;
      		//cv::medianBlur(crop2,crop,5);
                crop2.copyTo(crop);
      		cv::cvtColor(crop,test, CV_BGR2HSV);
      		std::vector<cv::Mat> channels;
      		cv::split(test, channels);
      		channels[2].copyTo(img1);
      		medianBlur(img1,img1,7);
      		Canny(img1, img1, 10, 150,3,true);
      		dilate(img1,img1, Mat(), Point(-1,-1));
      	        erode(img1,img1,Mat(),Point(-1,-1));
      		vector<Vec4i> lines;
      		Mat img2;
      		img1.copyTo(img2);
      		vector<vector<Point> >contours1;
      		findContours(img1,contours1,lines, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_NONE,Point(0,0));
      		Mat mask = Mat::zeros(img1.rows, img1.cols, CV_8UC1);
      		vector<double> areas(contours1.size());
      		for (unsigned int i = 0; i < contours1.size(); i++)
      			areas[i] = contourArea(Mat(contours1[i]));
      		double max;
      		Point maxPosition;
      		cv::minMaxLoc(Mat(areas), 0, &max, 0, &maxPosition);

      		drawContours(mask, contours1, maxPosition.y, Scalar(1), CV_FILLED);
      		Mat crop1(crop.rows, crop.cols, CV_8UC3,Scalar(0));
      		crop.copyTo(crop1, mask);
      		cv::normalize(mask.clone(), mask, 0.0, 255.0, CV_MINMAX, CV_8UC1);
                int k= countNonZero(mask);
                if(k<100)
      			continue;
                double minVal;
      		double maxVal;
      		minMaxLoc(crop1, &minVal, &maxVal);
      		if(maxVal==0)
      			continue;
		crop1.copyTo(currentTarget.targetImage);
		target.push(currentTarget);
                imwrite(format("/home/manohar/crops/newimg%d.jpg",e),crop1);
                e++;
	                    }
	colourFilterAndOCR();
}
void AnomalyDetect::colourFilterAndOCR(){
	Mat shapeImage,alphabetImage,alphabetImageMask,shapeImageMask,tempAlphabetImage;

	Mat alphabetMorphologyElement=getStructuringElement(MORPH_OPEN,Size(3,3));
	unsigned int limit=target.size();
	for(unsigned int i = 0 ; i < limit ; i++){
		shapeImage=Mat::zeros(target.front().targetImage.size(),CV_8UC3);
		alphabetImage=Mat::zeros(target.front().targetImage.size(),CV_8UC3);
		tempAlphabetImage=Mat::zeros(target.front().targetImage.size(),CV_8UC3);

		short colourConfig = colorDetect(target.front().targetImage,shapeImage,alphabetImage);//Where BrE meets MuE.
		char alphabet;
		float confidence,orientation;
		//10/june blr to dulles, 28/june to san diego; 20/july san fran to blr
		//10/june blr to dulles, 23/June NY to LA || 24/June Dulles to LA, 29/June LA to BLR
		bool weirdColour = colourConfig%12 == NAC || colourConfig/12 == NAC || colourConfig%12 == ABS_BLACK
				|| colourConfig/12 == ABS_BLACK;
		bool equalColour = colourConfig/12==colourConfig%12;//false; //Debatable

		if(!( weirdColour || equalColour )){

			inRange(shapeImage, Scalar(1, 1, 1), Scalar(255, 255, 255), shapeImageMask);

			inRange(alphabetImage, Scalar(1, 1, 1), Scalar(255, 255, 255), alphabetImageMask);
			morphologyEx(alphabetImageMask,alphabetImageMask,MORPH_OPEN,alphabetMorphologyElement);

			int alphabetArea = cv::countNonZero(alphabetImageMask);
			int shapeArea = cv::countNonZero(shapeImageMask)+alphabetArea;

			vector<Vec4i> hierarchy;
			vector<vector<Point> > alphabetContour;

			findContours(alphabetImageMask, alphabetContour, hierarchy, CV_RETR_EXTERNAL , CV_CHAIN_APPROX_SIMPLE);

			Moments shapeMoment = moments(shapeImageMask,1);
			Moments alphabetMoment = moments(alphabetImageMask,1);

			Vec3f shapeCentre,alphabetCentre;

			shapeCentre = Vec3f(shapeMoment.m10/shapeMoment.m00,shapeMoment.m01/shapeMoment.m00);
			alphabetCentre = Vec3f(alphabetMoment.m10/alphabetMoment.m00,alphabetMoment.m01/alphabetMoment.m00);

			float ratio = ((float)alphabetArea/shapeArea);//Problematic
			if(!(ratio>=0.05 &&ratio<=0.30)){
				goto erase;
			}
			if((alphabetArea<1 || shapeArea<1) || (alphabetArea==shapeArea) ||cv::norm(shapeCentre,alphabetCentre) > 10.0){
				erase:target.pop();
				continue;
			}

			alphabetImage.copyTo(tempAlphabetImage,alphabetImageMask);
			tempAlphabetImage.copyTo(alphabetImage);

			tesseractOCR.getCharacterAndOrientation(alphabetImage,alphabet,orientation,confidence);
			cout<<"Alphabet:"<<alphabet<<endl;
			cout<<"Alphabet Confidence:"<<confidence<<endl;
  
			if(confidence<70){
				target.pop();
				continue;
			}
			target.front().shapeCode = backEndProcessing(target.front().targetImage);

			RotatedRect alphabetBoundingBox = minAreaRect(alphabetContour[0]);

			//No such thing as too much information.
			target.front().alphabetHeight = alphabetBoundingBox.size.height;
			target.front().alphabetWidth = alphabetBoundingBox.size.width;

			//				if()
			cout<<"Shape:"<<returnShape(target.front().shapeCode)<<endl;

            if(target.front().shapeCode == NOTASHAPE){
                target.pop();
                continue;
            }

			cout<<"Shape Area:"<<shapeArea<<endl;
			cout<<"Alphabet Area:"<<alphabetArea<<endl;
			target.front().ratio =(100.0*((float)alphabetArea/shapeArea));
		}
		else{
			target.pop();
			continue;
		}
		target.front().targetColourConfig=colourConfig;
		target.front().targetAlphabet=alphabet;
		cout<<"Alphabet:"<<target.front().targetAlphabet<<endl;
		cout<<"Orientation in metadata:"<<target.front().targetOrientation<<endl;

		localisation();
		
		target.front().targetConfidence=confidence;
		target.push(target.front());
		target.pop();
	}
}

void AnomalyDetect::localisation(){

	cout<<setprecision(11)<<"Longitude in metadata:"<<target.front().longitude<<endl;
	cout<<setprecision(11)<<"Latitude in metadata:"<<target.front().latitude<<endl;
	cout<<setprecision(11)<<"altitude in metadata:"<<target.front().altitude<<endl;

	float x = target.front().localTargetPosition.y;//  #second value in pixel location // x and y exchanged coz assumed image in 3rd quadrant
	float y = target.front().localTargetPosition.y;//  #first value in pixel location
	float alt = 120;//target.front().altitude;
	cout<<"Altitude for loc"<<alt<<endl;

	int ortag = 0;

	double orientation = target.front().targetOrientation;
	double target_orientation;

	double d;
	if(target.front().rotation == 'L')
		{	
			orientation = orientation + 90;
			ortag = 1;
		}
	else if(target.front().rotation == 'T')
		{
			orientation = orientation - 90;	
			ortag = 0;		
		}
	else
		ortag = 0;


	if(ortag == 1)
	{//	cout<<"potrait"<<endl;
		double imgHeight = (2 * alt * tan(21.8*3.1415/180))/6000;
		double imgWidth  = (2 * alt * tan(14.95*3.1415/180))/4000;
		double xo=2000;
		double yo=-3000;

		double x1 = x * imgWidth;
		double y1 = y * imgHeight * -1;

		xo = xo * imgWidth;
		yo = yo * imgHeight;
		
		d = sqrt(((y1-yo)*(y1-yo))+((x1-xo)*(x1-xo)));
	 //     cout<<"distance of target from centre  : "<<d<<endl;

		double angle = abs((yo-y1)/(xo-x1));
		double target_angle = abs(atan(angle)*3.14/180);
	//	cout<<"target_angle"<<target_angle<<endl;

		if(y<3000 and x>2000)
		{	//cout<<"1st quadrant"<<endl;
			target_orientation  = orientation + target_angle;
		}  
		else if(y<3000 and x<2000)
		{	
			//cout<<"2nd quadrant"<<endl;
			target_orientation  = orientation - ( 90 - target_angle );
		}
		else if(y>3000 and x<2000)
		{
			//cout<<"3rd quadrant"<<endl;
			target_orientation  = orientation - ( 90 + target_angle );  
		}
		else
		{
			//cout<<"4th quadrant"<<endl;
			target_orientation  = orientation + 90 + target_angle;
		}
	}
	if(ortag == 0)
	{
		//cout<<"Landscape"<<endl;
		double imgHeight = (2 * alt * tan(14.95*3.1415/180))/4000;
		double imgWidth  = (2 * alt * tan(21.8*3.1415/180))/6000;
		double xo=3000;
		double yo=-2000;

		double x1 = x * imgWidth;
		double y1 = y * -1  * imgHeight;

		xo = xo * imgWidth;
		yo = yo * imgHeight; 

		d = sqrt(((y1-yo)*(y1-yo))+((x1-xo)*(x1-xo)));
	        cout<<"distance of target from centre  : "<<d<<endl;

		double angle = abs((yo-y1)/(xo-x1));	
		double target_angle = abs(atan(angle)*3.14/180);
		cout<<"target_angle" << target_angle <<endl;

		if(y<2000 and x>3000)
		{
			//cout<<"1st quadrant"<<endl;
			target_orientation  = orientation + target_angle;
		}  
		else if(y<2000 and x<3000)
		{
			//cout<<"2nd quadrant"<<endl;
			target_orientation  = orientation - ( 90 - target_angle );
		}
		else if(y>2000 and x<3000)
		{
			//cout<<"3rd quadrant"<<endl;
			target_orientation  = orientation - ( 90 + target_angle );  
		}
		else
		{
			//cout<<"4th quadrant"<<endl;	
			target_orientation  = orientation + 90 + target_angle;
		}
	}
	if(target_orientation > 360)
		target_orientation = target_orientation -360;

	if(target_orientation < 0)
		target_orientation = target_orientation + 360;

	cout<<"target_orientation with respect to centre : "<<target_orientation<<endl;
	double latitude,longitude;

	const GeodesicExact& geodesicExact = GeodesicExact::WGS84();

	geodesicExact.Direct(target.front().latitude,target.front().longitude,target_orientation,d,latitude,longitude);

	target.front().latitude = latitude;
	target.front().longitude = longitude;
	cout<<setprecision(11)<<"Target Longitude:"<<longitude<<endl;
	cout<<setprecision(11)<<"Target Latitude:"<<latitude<<endl;
	 
}


Mat AnomalyDetect::getFrame(){
	return __frame;
}
void AnomalyDetect::setFrame(Mat* frame){

	frame->copyTo(this->__frame);
}
void AnomalyDetect::setFrame(string address){

	cout<<endl<<"Address:"<<address<<endl;

	do{
		this->__frame = imread(address);
	}while(__frame.empty());

	currentTarget.fileAddress=address;
	entryPoint(address.c_str(),&currentTarget.latitude,&currentTarget.longitude, &currentTarget.targetOrientation,&currentTarget.altitude,currentTarget.rotation);
	
	while(!target.empty())
		target.pop();
}
queue<Target>& AnomalyDetect::getTargets(){
	return target;
}
}
#endif
