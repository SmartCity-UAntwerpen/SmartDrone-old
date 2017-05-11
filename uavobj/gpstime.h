/**
 ******************************************************************************
 * @addtogroup UAVObjects LibrePilot UAVObjects
 * @{
 * @addtogroup GPSTime GPSTime
 * @brief Contains the GPS time from @ref GPSModule.  Required to compute the world magnetic model correctly when setting the home location.
 *
 * Autogenerated files and functions for GPSTime Object
 *
 * @{
 *
 * @file       gpstime.h
 *
 * @author     The LibrePilot Project, https://www.librepilot.org, (C) 2017.
 *             The OpenPilot Team, http://www.openpilot.org Copyright (C) 2010-2013.
 *
 * @brief      Arduino Header of the GPSTime object. This file has been
 *             automatically generated by the UAVObjectGenerator.
 *
 * @note       Object definition file: gpstime.xml.
 *             This is an automatically generated file.
 *             DO NOT modify manually.
 *
 * @see        The GNU Public License (GPL) Version 3
 *
 *****************************************************************************/
/*
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
 * or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
 * for more details.
 *
 * You should have received a copy of the GNU General Public License along
 * with this program; if not, write to the Free Software Foundation, Inc.,
 * 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
 */

#ifndef GPSTIME_H
#define GPSTIME_H
#include <stdbool.h>
/* Object constants */
#define GPSTIME_OBJID 0x1E2F477E
#define GPSTIME_ISSINGLEINST 1
#define GPSTIME_ISSETTINGS 0
#define GPSTIME_ISPRIORITY 0
#define GPSTIME_NUMBYTES sizeof(GPSTimeData)

/* Field Year information */

/* Field Millisecond information */

/* Field Month information */

/* Field Day information */

/* Field Hour information */

/* Field Minute information */

/* Field Second information */




/*
 * Packed Object data (unaligned).
 * Should only be used where 4 byte alignment can be guaranteed
 * (eg a single instance on the heap)
 */
typedef struct {
    int16_t Year;
    int16_t Millisecond;
    int8_t Month;
    int8_t Day;
    int8_t Hour;
    int8_t Minute;
    int8_t Second;

} __attribute__((packed)) GPSTimeDataPacked;

/*
 * Packed Object data.
 * Alignment is forced to 4 bytes
 */
typedef GPSTimeDataPacked __attribute__((aligned(4))) GPSTimeData;

/*
 * Union to apply the data array to and to use as structured object data
 */
union {
    GPSTimeDataPacked data;
    byte arr[GPSTIME_NUMBYTES];
 } GPSTimeDataUnion;

#endif // GPSTIME_H

/**
 * @}
 * @}
 */
