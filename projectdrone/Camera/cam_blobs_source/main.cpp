/*
 *  I-IoT: SmartCity QuadCopter: Main C++ codefile
 *  Lastly edited on 21/12/2017 by De Laet Jan
 */

#include "imageProcessing.cpp"
#include "communication.cpp"

//#define DBG_TIME_PER_FRAME

int main( int argc, char** argv )
{
    int resolution_width = 640;
    int resolution_height = 480;
    
    // gets reset when system is rebooted
    system ("sudo v4l2-ctl --set-ctrl=auto_exposure=1"); // sets auto_exposure to Manual Mode
    system ("sudo v4l2-ctl --set-ctrl=exposure_time_absolute=50"); // sets the absolute exposure time to 1 (= 100 µs) (10000 = 1s)
    
    VideoCapture cap(0); // open the default camera
    if(!cap.isOpened())  // check if we succeeded
        return -1;
    
    Mat frame;
    
    //cap.set(CV_CAP_PROP_CONVERT_RGB, 0); // VIDEOIO ERROR V4L: Property not supported by device
    cap.set(CV_CAP_PROP_FRAME_WIDTH,resolution_width); // capture width
    cap.set(CV_CAP_PROP_FRAME_HEIGHT,resolution_height); // capture height
    cap.set(CV_CAP_PROP_FPS,60);
 
    ImageProcessing imageProcessing; // Creating ImageProcessing object
    vector<Point2i> points;
    
    #ifdef DBG_TIME_PER_FRAME
    auto now = duration_cast<milliseconds>( steady_clock::now().time_since_epoch() ).count();
    #endif

    //unsigned int amount = 1000;
    while(1) //for(unsigned int i=0; i < amount; i++)
    {
        #ifdef DBG_TIME_PER_FRAME
        //if(i == 1) // getting the first frame takes ~700 ms
        //   now = duration_cast<milliseconds>( steady_clock::now().time_since_epoch() ).count();
        #endif
        
        cap >> frame; // get a new frame from camera (most  time consuming code, varies depends on chosen resolution)
        points = imageProcessing.processFrame(frame);
        
        stringstream ss;
        for( unsigned int j = 0; j < points.size(); j++ )
            ss << points[j].x << " " << points[j].y << ";";
        cout << ss.str().c_str() << endl;  // sending values through pipe
        cout.flush();
    }
    
    #ifdef DBG_TIME_PER_FRAME
    //auto duration = duration_cast<milliseconds>( steady_clock::now().time_since_epoch() ).count() - now;
    //cout << "Duration per frame: " << duration/amount << "ms" << endl;
    #endif
    
    return 0;
}
