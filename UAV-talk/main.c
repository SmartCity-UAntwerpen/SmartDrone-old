#include "datatypes.h"
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include "serlib.h"
#include "LibrePilotSerial.h"

#include "uavobj/airspeedsettings.h"
#include "uavobj/barosensor.h"

int main(void)
{
printf ("LibrePilotSerialInit() init\r\n");
    int res;
    AirspeedSettingsData AirspeedSettings;
    BaroSensorData Baro;

    res=LibrePilotSerialInit("/dev/ttyACM0",57600);
    if (res!=0)
    {
        printf ("LibrePilotSerialInit() error\r\n");
        exit (-1);
    }
while(1)
{
        LibrePilotSerialRequest(BAROSENSOR_OBJID);
        LibrePilotSerialReceive(BAROSENSOR_OBJID,(uint16 *) &Baro);
        printf ("Barometer:%f\r\n",Baro.Pressure);
        //AirspeedSettings.SamplePeriod++;
        //LibrePilotSerialSend(AIRSPEEDSETTINGS_OBJID,(uint8 *)&AirspeedSettings,AIRSPEEDSETTINGS_NUMBYTES);

        usleep(100E3);

}
    while(1)
    {


        LibrePilotSerialRequest(AIRSPEEDSETTINGS_OBJID);
        LibrePilotSerialReceive(AIRSPEEDSETTINGS_OBJID,(uint8 *) &AirspeedSettings);
        printf ("Sample period:%d\r\n",AirspeedSettings.SamplePeriod);
        AirspeedSettings.SamplePeriod++;
        LibrePilotSerialSend(AIRSPEEDSETTINGS_OBJID,(uint8 *)&AirspeedSettings,AIRSPEEDSETTINGS_NUMBYTES);

        usleep(100E3);
	}
	return 0;
}



