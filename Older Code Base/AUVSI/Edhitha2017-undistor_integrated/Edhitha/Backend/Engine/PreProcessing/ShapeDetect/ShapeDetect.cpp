/*
 * Shape.cpp
 *
 *  Created on: 24-Mar-2017
 *      Author: niran
 */

#include "ShapeDetect.h"
using namespace Edhitha2016;

namespace Edhitha2016{
    string returnShape(short int shape){
        switch(shape){
            case SQUARE: 		return "SQUARE";
                                break;
            case RECTANGLE:		return "RECTANGLE";
                                break;
            case TRAPEZOID:		return "TRAPEZOID";
                                break;
            case TRIANGLE:  	return "TRIANGLE";
                                break;
            case PENTAGON:		return "PENTAGON";
                                break;
            case HEXAGON:		return "HEXAGON";
                                break;
            case HEPTAGON: 		return "HEPTAGON";
                                break;
            case OCTAGON:		return "OCTAGON";
                                break;
            case CIRCLE:		return "CIRCLE";
                                break;
            case SEMICIRCLE:	return "SEMICIRCLE";
                                break;
            case QUARTERCIRCLE:	return "QUARTERCIRCLE";
                                break;
            case STAR:			return "STAR";
                                break;
            case CROSS:			return "CROSS";
                                break;
            default:	    return "NOT A SHAPE";
                            break;
        }
    }

    unsigned short backEndProcessing(Mat source){
        try{
            //Declaring variables
            cout<<"Inside shape detect"<<endl;

            Mat resizedSource, graySource, blurred, thresholdOutput, drawing, drawing2;
            vector<vector<Point> > contours, contoursApprox;
            vector<Vec4i> hierarchy;
            double perimeter;
            bool isCircle = false;
            bool isConvex;
            vector<Vec3f> circles;
            short int tag = 20;

            //Drawing of size source to get binary image, hence 8UC1
            drawing = Mat::zeros(source.size[0],source.size[1],CV_8UC1);
            drawing2 = Mat::zeros(source.size[0],source.size[1],CV_8UC1);

            //Changing image to grayScale
            cvtColor(source,graySource,CV_BGR2GRAY);

            //Blurring using Gaussian blur to improve accuracy of finding contours
            GaussianBlur(graySource,blurred,Size(5,5),0,0,0);

            //Thresholding the bit values
            threshold( graySource, thresholdOutput, 60, 255, THRESH_BINARY );

            //Finding the external contour from the image
            findContours(thresholdOutput,contours,hierarchy, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_SIMPLE);
            cout<<contours.size()<<endl;
            
            if(contours.size() > 0 && contourArea(contours[0]) > 500 ){
                    
                //Draw the contour to detect shapes and eliminate the alphabet inside
                drawContours( drawing2, contours, 0, (255), 2, 8, hierarchy, 0, Point() );

                //imshow("Drawing2",drawing2);
                //waitKey(0);

                //Finding if any circles are present in the image by taking the external contour
                HoughCircles( drawing2, circles, CV_HOUGH_GRADIENT, 1, 60, 200, 20, 15, 0 );
                if(circles.size()!=0){
                    //If there are any circles, change the bool value to 1
                    isCircle = true;
                    //Draw the circles
                    for( size_t i = 0; i < circles.size(); i++ )
                    {
                        Point center(cvRound(circles[i][0]), cvRound(circles[i][1]));
                        int radius = cvRound(circles[i][2]);
                        cv::circle( drawing, center, 3, Scalar(0,255,255), -1);
                        cv::circle( drawing, center, radius, Scalar(0,0,255), 1 );
                    }
                }

                cout<<"Is circle : " << isCircle << endl;

                //Declaring some more variables
                vector<vector<Point> > contours_poly( contours.size() );
                //vector<Rect> boundRect( contours.size() );
                int len;
                //String tag = "";
                //Approximating the contour
                cout<<"Approx contour"<<endl;

                perimeter = arcLength(contours[0],true);

                cout<<"Perimeter done"<<endl;
                approxPolyDP( Mat(contours[0]), contours_poly[0], perimeter * 0.04 , true );
                cout<<"Size of the shape : " << contours_poly[0].size() << endl;
                len = contours_poly[0].size();

                cout<<"Approximating done"<<endl;
                //Finding if the contour is convex or concave
                isConvex = isContourConvex(contours_poly[0]);
                cout<<"Is convex : " << isConvex <<endl;

                //Drawing the lines of the approximated contour using 'line' function on drawing matrix
                Point2f points[len];
                for(int j = 0; j < len; j++){
                    //cout<<contours_poly[i][j]<<endl;
                    points[j] = contours_poly[0][j];
                    if(j<len-1){
                        line(drawing,contours_poly[0][j],contours_poly[0][j+1],Scalar(255,255,255),1,CV_AA);
                    }
                    else{
                        line(drawing,contours_poly[0][j],contours_poly[0][0],Scalar(255,255,255),1,CV_AA);
                    }
                }

                //Declaring two matrices to hold the results of HuMoments function
                Mat ans,ans2;

                //Finding moments of the drawing and contour
                Moments m = moments(contours[0],true);
                Moments m2 = moments(drawing,true);

                //Finding HuMoments for drawing and contour
                HuMoments(m,ans);
                HuMoments(m2,ans2);

                //Output the values of the Humoments function
                /*cout<<"Starts Hu moments for contour here\n";
                  cout<<ans;
                  cout<<endl;*/

                cout<<"First Moment of contour : " << ans.at<double>(0,0)<<endl;
                //Store the first moment value of the given contour to use in the decision branch later
                double mValue = ans.at<double>(0,0);
                //double mValue2 = ans.at<double>(2,0);
                //double mValue3 = ans.at<double>(0,1);
                //cout<<"Second moment of contour : " << mValue2<<endl;
                //cout<<"Second moment of contour 2 : " << mValue3<<endl;


                /*cout<<"Starts Hu moments for drawing here\n";
                  cout<<ans2;
                  cout<<endl*/;

                //Determine the shape based on the values of isCircle, isConvex and the value of HuMoments
                if(mValue >= 0.157 && mValue <= 0.165){
                    if(isCircle){
                        tag = CIRCLE;
                    }
                }

                if(isConvex){
                    if(mValue >= 0.181 && mValue <= 0.199){
                        if(len==3)
                            tag = TRIANGLE;
                        else
                            tag = TRAPEZOID;
                    }

                    if(mValue >= 0.161 && mValue <= 0.167){
                        if(!isCircle)
                            tag = SQUARE;
                    }

                    if(mValue >= 0.170 && mValue <= 0.215){
                        if(len==4)
                            tag = RECTANGLE;
                        else
                            tag = SEMICIRCLE;
                    }
                    /*if(mValue >= 0.200 && mValue < 0.210){
                      tag = "SemiCircle";
                      }*/
                }
                else{
                    if(mValue >= 0.201 && mValue <= 0.220){
                        if(len <= 8)
                            tag = CROSS;
                        else if (len <= 10)
                            tag = STAR;
                        else
                            tag = NOTASHAPE;
                
                    }
                }

                if(tag == 20){
                    tag = NOTASHAPE;
                }
            }
            else{
                tag = NOTASHAPE;
            }

            //cout<<"Tag : " << tag << endl;
            //imshow("Source", source);
            //imshow("ApproxPoly",drawing);
            //waitKey(0);
            cout<<"Exiting shape detect"<<endl;

            return tag;
        }
        catch(...){
            cout<<"Default exception"<<endl;
            return NOTASHAPE;
        }    
    }
}
