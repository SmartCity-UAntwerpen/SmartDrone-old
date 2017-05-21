/**
 ******************************************************************************
 * @addtogroup UAVObjects LibrePilot UAVObjects
 * @{
 * @addtogroup PathStatus PathStatus
 * @brief Status of the current path mode  Can come from any @ref PathFollower module
 *
 * Autogenerated files and functions for PathStatus Object
 *
 * @{
 *
 * @file       pathstatus.h
 *
 * @author     The LibrePilot Project, https://www.librepilot.org, (C) 2017.
 *             The OpenPilot Team, http://www.openpilot.org Copyright (C) 2010-2013.
 *
 * @brief      Arduino Header of the PathStatus object. This file has been
 *             automatically generated by the UAVObjectGenerator.
 *
 * @note       Object definition file: pathstatus.xml.
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

#ifndef PATHSTATUS_H
#define PATHSTATUS_H
#include <stdbool.h>
/* Object constants */
#define PATHSTATUS_OBJID 0x65C06EB0
#define PATHSTATUS_ISSINGLEINST 1
#define PATHSTATUS_ISSETTINGS 0
#define PATHSTATUS_ISPRIORITY 0
#define PATHSTATUS_NUMBYTES sizeof(PathStatusData)

/* Field fractional_progress information */

/* Field error information */

/* Field path_direction_north information */

/* Field path_direction_east information */

/* Field path_direction_down information */

/* Field correction_direction_north information */

/* Field correction_direction_east information */

/* Field correction_direction_down information */

/* Field path_time information */

/* Field UID information */

/* Field Status information */

// Enumeration options for field Status
typedef enum __attribute__ ((__packed__)) {
    PATHSTATUS_STATUS_INPROGRESS=0,
    PATHSTATUS_STATUS_COMPLETED=1,
    PATHSTATUS_STATUS_WARNING=2,
    PATHSTATUS_STATUS_CRITICAL=3
} PathStatusStatusOptions;




/*
 * Packed Object data (unaligned).
 * Should only be used where 4 byte alignment can be guaranteed
 * (eg a single instance on the heap)
 */
typedef struct {
    float fractional_progress;
    float error;
    float path_direction_north;
    float path_direction_east;
    float path_direction_down;
    float correction_direction_north;
    float correction_direction_east;
    float correction_direction_down;
    float path_time;
    int16_t UID;
    PathStatusStatusOptions Status;

} __attribute__((packed)) PathStatusDataPacked;

/*
 * Packed Object data.
 * Alignment is forced to 4 bytes
 */
typedef PathStatusDataPacked __attribute__((aligned(4))) PathStatusData;

/*
 * Union to apply the data array to and to use as structured object data
 */
union {
    PathStatusDataPacked data;
    byte arr[PATHSTATUS_NUMBYTES];
 } PathStatusDataUnion;

#endif // PATHSTATUS_H

/**
 * @}
 * @}
 */