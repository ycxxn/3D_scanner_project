#include <stdio.h>
#include "opencv2/opencv.hpp"
#include "simple-serial-port/SimpleSerial.h"

using namespace std;
using namespace cv;

void project_1()
{
	// 1. open webcam 
	VideoCapture cap(1);
	if (!cap.isOpened())
	{
		cout << "Cannot open camera\n";
	}

	// 2. open serial
	char com_port[] = "\\\\.\\COM5";
	DWORD COM_BAUD_RATE = CBR_115200;
	SimpleSerial Serial(com_port, COM_BAUD_RATE);
	if (Serial.connected_) {
		cout << "Serial Connected\n";
	}

	// 3. 宣告相關變數
	Mat frame1, frame2, frame_a, frame_b, frame, gray, hsv, mask;
	string read_in;
	char* to_send;
	bool is_sent;
	int delay_t = 1;

	// 4. 設定影像range
	Scalar scalarL = Scalar(156, 43, 46);
	Scalar scalarH = Scalar(180, 255, 255);

	while (1)
	{
		//bool ret = cap.read(frame);
		read_in = "on\n";
		to_send = &read_in[0];
		is_sent = Serial.WriteSerialPort(to_send);
		_sleep(delay_t);
		cap >> frame1;

		read_in = "off\n";
		to_send = &read_in[0];
		is_sent = Serial.WriteSerialPort(to_send);
		_sleep(delay_t);
		cap >> frame2;

		subtract(frame1, frame2, frame_a);
		subtract(frame2, frame1, frame_b);
		add(frame_a, frame_b, frame);

		cvtColor(frame, gray, CV_BGR2GRAY);
		cvtColor(frame, hsv, CV_BGR2HSV);

		threshold(gray, mask, 30, 255, CV_THRESH_BINARY);

		//inRange(hsv, scalarL, scalarH, mask);

		//Mat element = getStructuringElement(MORPH_RECT, Size(3, 3));
		//morphologyEx(mask, mask, MORPH_OPEN, element);

		//閉操作 (連接一些連通域)
		//morphologyEx(mask, mask, MORPH_CLOSE, element);

		imshow("frame1", frame1);
		imshow("frame2", frame2);
		imshow("frame", frame);
		imshow("gray", gray);
		//imshow("hsv", hsv);
		imshow("mask", mask);
		waitKey(1);

	}
}

void project_2()
{
	// 1. open webcam 
	VideoCapture cap(1);
	if (!cap.isOpened())
	{
		cout << "Cannot open camera\n";
	}

	// 2. open serial
	char com_port[] = "\\\\.\\COM3";
	DWORD COM_BAUD_RATE = CBR_115200;
	SimpleSerial Serial(com_port, COM_BAUD_RATE);
	if (Serial.connected_) {
		cout << "Serial Connected\n";
	}


	string read_in;
	char* to_send;
	bool is_sent;
	int delay_t = 10;

	Mat frame,gray, mask;
	while (1)
	{
		read_in = "on\n";
		to_send = &read_in[0];
		is_sent = Serial.WriteSerialPort(to_send);
		/*_sleep(delay_t);*/

		cap >> frame;

		cvtColor(frame, gray, COLOR_BGR2GRAY);

		threshold(gray, mask, 100, 255, CV_THRESH_BINARY);

		Mat element = getStructuringElement(MORPH_RECT, Size(5, 5));
		morphologyEx(mask, mask, MORPH_OPEN, element);
		morphologyEx(mask, mask, MORPH_CLOSE, element);

		Mat edge;
		Canny(mask, edge, 100, 200, 3, false);


		imshow("frame", frame);
		imshow("gray", gray);
		imshow("mask", mask);
		imshow("edge", edge);

		waitKey(1);
	}
}


int main(int argc, char** argv )
{
	project_1();
	//project_2();

	return 0;
}