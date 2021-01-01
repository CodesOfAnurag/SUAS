#include "gpsData.h"
//Remove spaces on the right of the string

void main()
{
    const char* address; long double* latitude; long double* longitude; long double* imageDirection;long double* altitude;
    ExifData *ed;
    ed = exif_data_new_from_file();
    char directionChar[100];
    ExifEntry *entry = exif_content_get_entry(ed->ifd[EXIF_IFD_EXIF],EXIF_TAG_USER_COMMENT);
    exif_entry_get_value(entry, directionChar, 100);
    char lat[100],lon[100],alt[100],head[100];
    char s[4]="    ";
    char *token;
    token = strtok(directionChar, s);
    long double lat1,lon1,alt1,head1;
    int i=1;
    while( token != NULL ) 
     {
      
      if(i==1)
      strcpy(lat,token);
      if(i==2)
      strcpy(lon,token);
      if(i==3)
      strcpy(alt,token);
      if(i==4)
      strcpy(head,token);
      i++;
      token = strtok(NULL, s);
     }
lat1=atof(lat);
lon1=atof(lon);
alt1=atof(alt);
head1=atof(head);
*latitude=lat1;
*longitude=lon1;
*imageDirection=head1;
*altitude=alt1;

    //EUCLIDEAN DISTANCE
    //  cv::Point a(0, 0);
    //  cv::Point b(2248, 0);
    //  double res = cv::norm(a-b);//Euclidian distance

     //Free the EXIF data
    //exif_data_unref(ed);
}
