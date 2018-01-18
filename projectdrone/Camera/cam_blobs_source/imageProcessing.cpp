/*
 *  I-IoT: SmartCity QuadCopter: Camera ImageProcessing codefile
 *  Lastly edited on 21/12/2017 by De Laet Jan
 */
 
#include "opencv2/opencv.hpp"
#include <chrono>

//#define DBG_AMOUNT_CONTOURS
//#define DBG_CONTOUR_SIZE
//#define DBG_SHOW_GRAY
//#define DBG_SHOW_THRESHOLD

using namespace cv;
using namespace std;
using namespace chrono;

class ImageProcessing
{
    public:
        ImageProcessing(){}
        vector<Point2i> processFrame(Mat&);
        
    private:
        vector<vector<Point>>  findingBlobs(Mat&);
        vector<Point2i> sortPoints(vector<vector<Point>>);
        float euclideanDistance(Point2f&, Point2f&);
        friend bool operator==(const Point2f& p1, const Point2f& p2) //
        {
            return (p1.x == p2.x && p1.y == p2.y);
        }
};

// processing one frame: image as input, vector of 3 integer points as output
vector<Point2i> ImageProcessing::processFrame(Mat& im)
{
   return sortPoints( findingBlobs(im) );
}

// detecting blobs in image by OpenCV image processing library
vector<vector<Point>>  ImageProcessing::findingBlobs(Mat& im)
{
    Mat image;
    vector<vector<Point>> contours;
    
    cvtColor( im, image, CV_BGR2GRAY ); // conversion from BGR to grayscale
    
    #ifdef DBG_SHOW_GRAY
    imshow( "window1", image ); 
    #endif
    
    threshold( image, image, 70 ,255, THRESH_BINARY ); // threshold to convert to a binary image
    
    #ifdef DBG_SHOW_THRESHOLD
    imshow( "window2", image ); 
    #endif
    
    findContours( image, contours, CV_RETR_LIST, CV_CHAIN_APPROX_SIMPLE, Point(0, 0) ); // Searches for contours (takes the longest of the 3: ~20 ms) 
    
    #ifdef DBG_AMOUNT_CONTOURS
    cout << "Amount of Contours: " << contours.size() << endl;
    #endif
    //imwrite("test.jpg",image);  // for testing distances and new environments (remove when not testing, adds ~50 ms processing time!)
    #if defined(DBG_SHOW_GRAY) || defined(DBG_SHOW_THRESHOLD)
    waitKey(0);
    #endif

    return contours;
}

// sorting the (normally) 3 "points" vector by having the outside point (that is closest to the middle) as the first element (hardcoded solution with 3 points only)
// 1. find min and max distance between 2 points
// 2. point that belongs to both distances should be placed first, followed by the other point that belongs to the shortest distance
vector<Point2i> ImageProcessing::sortPoints(vector<vector<Point>> contours)
{
    // calculating center of every contour by making use of a bounding rectangle
    vector<Point2f> points;
    vector<float> areaSize;
    
    for(unsigned int i = 0; i < contours.size(); i++ )
    {
        float area = contourArea(contours[i]);
        if(area < 50) // filtering blobs larger than 50 pixels in area size
        {
            Rect bRect = boundingRect(contours[i]);
            points.push_back( Point2f( bRect.x + (bRect.width / 2), bRect.y + (bRect.height / 2) ) );
            areaSize.push_back(area);
        }
    }
    
    if(points.size() == 3)
    {
        typedef vector<Point2f> vdef; // vector with float points as elements
        typedef map<float, vdef> mapdef; // ordered map with float distance as key and above vector as value
        
        mapdef m; // map to automatically sort distances
        
        // all possible combinations between 3 points are added to map with calculated distance between 2 points as key and vector of 2 points as value
        m[euclideanDistance( points[0], points[1] )] = vdef { points[0], points[1] };
        m[euclideanDistance( points[1], points[2] )] = vdef { points[1], points[2] };
        m[euclideanDistance( points[0], points[2] )] = vdef { points[0], points[2] };
        
        // first element in the ordered map has the shortest distance; last element, longest distance
        vdef closest = m.begin()->second; // getting value of first element in map
        vdef furthest = m.rbegin()->second; // getting value of last element in map (reverse iteration)
        
        // sorting triplet points
        for( int i = 0; i < 2; i++ )
            for( int j = 0; j < 2; j++)
                if(closest[i] == furthest[j]) // operator overloading, see constructor
                    return { closest[i], ( i == 0 ) ? closest[1] : closest[0], (j == 0) ? furthest[1] : furthest[0] };
    }
    else if (points.size() == 2)
    { 
        #ifdef DBG_CONTOUR_SIZE
        cout << "Contour Size: " << areaSize[0] << " - " << areaSize[1] << endl;
        #endif
        if(areaSize[0] > areaSize[1])
            return { Point2i( points[0].x, points[0].y ), Point2i( points[1].x, points[1].y ),  Point2i(-1,-1) };
        else
            return { Point2i( points[1].x, points[1].y ), Point2i( points[0].x, points[0].y ),  Point2i(-1,-1) };
    }
    else if (points.size() == 1)
        return { Point2i( points[0].x, points[0].y ), Point2i(-1,-1), Point2i(-1,-1) };
    
    return { Point2i(-1,-1), Point2i(-1,-1), Point2i(-1,-1) };  //  when input vector is not of size 1, 2 or 3 (can happen when blobs slip through the size filter)
}

// calculating distance between 2 points
float ImageProcessing::euclideanDistance(Point2f& p, Point2f& q) 
{
    Point2f diff = p - q;
    return sqrt(diff.x*diff.x + diff.y*diff.y);
}