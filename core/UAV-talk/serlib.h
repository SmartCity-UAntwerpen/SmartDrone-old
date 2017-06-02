#ifndef SERLIB
#define SERLIB

#include "datatypes.h"

#define SERLIB_DEBUG

int SerlibInitPort(int *fd,char *PortName, uint32 Baudrate);
            //Initialize serial port
            //Parameters:
            //Portname: serial port name ex '/dev/ttyO1'
            //Baudrate: baud rate
            //Return values:
            //0: success
            //1: error

void SerlibClosePort(int *fd);
void SerlibWriteBlock(int *fd, uint8 *Data, uint32 Length);
void SerlibReadBlock(int *fd, uint8 *Data, uint32 Length);
uint8 SerlibReadByte(int *fd);
void SerlibFlush(int *fd);

#endif
