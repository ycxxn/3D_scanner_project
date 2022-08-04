#include <stdio.h>
#include "opencv2/opencv.hpp"

using namespace std;
using namespace cv;

int main(int argc, char** argv )
{
	VideoCapture cap(2);

	if (!cap.isOpened())
	{
		cout << "Cannot open camera\n";
	}

	Mat frame;
	Mat gray;

	while (1)
	{
		//cap >> frame;
		bool ret = cap.read(frame);
		cout << frame.size() << "\n";
		imshow("frame", frame);

		waitKey(1);
	}


	return 0;
}