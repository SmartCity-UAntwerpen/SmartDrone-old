#ifndef LibrePilotSerial_h
#define LibrePilotSerial_h


#include <serlib.h>
#include <stdio.h>
#include "datatypes.h"

typedef uint8 byte;
typedef unsigned char uint8_t;
typedef unsigned short uint16_t;
typedef unsigned int uint32_t;

/**
 * \brief Connect to UAVTalk serial port
 * \param Port: serial port device
 * \param BaudRate: serial port baud rate
 * \return
 * 0:OK \n
 * 1:Error \n
*/
int LibrePilotSerialInit(char *Port, int BaudRate);


/**
 * \brief Blocking receive. Waits until specified UAVObject is received
 * \param objId: UAVObject ID to receive
 * \param ret: Returned object, store in xxxDataPacked struct
 * \return
 * 0:OK \n
 * 1:Error \n
*/
int LibrePilotSerialReceive(unsigned long objId, byte *ret);

/**
 * \brief Send request for UAVObject
 * \param objId: UAVObject ID to request
*/
void LibrePilotSerialRequest(unsigned long objId);

/**
 * \brief Send UAVObject
 * \param objId: UAVObject ID to send
 * \param data: Pointer to UAVObject data struct (xxxDataPacked struct)
 * \param length: UAVObject length
*/
void LibrePilotSerialSend(unsigned long objId, byte* data, int length);


#endif
