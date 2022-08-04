#include <iostream>
#include <windows.h>
#include "simple-serial-port/SimpleSerial.h"

void seiral_init()
{

}
int main()
{
	char com_port[] = "\\\\.\\COM3";
	DWORD COM_BAUD_RATE = CBR_115200;
	SimpleSerial Serial(com_port, COM_BAUD_RATE);
	
	if (Serial.connected_) {
		cout << "Serial Connected\n";
	}

	string read_in;
	char* to_send;
	bool is_sent;
	while(1)
	{
		read_in = "on\n";
		to_send = &read_in[0];
		is_sent = Serial.WriteSerialPort(to_send);
		_sleep(500);

		read_in = "off\n";
		to_send = &read_in[0];
		is_sent = Serial.WriteSerialPort(to_send);
		_sleep(500);
	}
}