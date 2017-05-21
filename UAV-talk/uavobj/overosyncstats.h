/**
 ******************************************************************************
 * @addtogroup UAVObjects LibrePilot UAVObjects
 * @{
 * @addtogroup OveroSyncStats OveroSyncStats
 * @brief Maintains statistics on transfer rate to and from over
 *
 * Autogenerated files and functions for OveroSyncStats Object
 *
 * @{
 *
 * @file       overosyncstats.h
 *
 * @author     The LibrePilot Project, https://www.librepilot.org, (C) 2017.
 *             The OpenPilot Team, http://www.openpilot.org Copyright (C) 2010-2013.
 *
 * @brief      Arduino Header of the OveroSyncStats object. This file has been
 *             automatically generated by the UAVObjectGenerator.
 *
 * @note       Object definition file: overosyncstats.xml.
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

#ifndef OVEROSYNCSTATS_H
#define OVEROSYNCSTATS_H
#include <stdbool.h>
/* Object constants */
#define OVEROSYNCSTATS_OBJID 0xD2085FAC
#define OVEROSYNCSTATS_ISSINGLEINST 1
#define OVEROSYNCSTATS_ISSETTINGS 0
#define OVEROSYNCSTATS_ISPRIORITY 0
#define OVEROSYNCSTATS_NUMBYTES sizeof(OveroSyncStatsData)

/* Field Send information */

/* Field Received information */

/* Field FramesyncErrors information */

/* Field UnderrunErrors information */

/* Field DroppedUpdates information */

/* Field Packets information */

/* Field Connected information */

// Enumeration options for field Connected
typedef enum __attribute__ ((__packed__)) {
    OVEROSYNCSTATS_CONNECTED_FALSE=0,
    OVEROSYNCSTATS_CONNECTED_TRUE=1
} OveroSyncStatsConnectedOptions;




/*
 * Packed Object data (unaligned).
 * Should only be used where 4 byte alignment can be guaranteed
 * (eg a single instance on the heap)
 */
typedef struct {
    uint32_t Send;
    uint32_t Received;
    uint32_t FramesyncErrors;
    uint32_t UnderrunErrors;
    uint32_t DroppedUpdates;
    uint32_t Packets;
    OveroSyncStatsConnectedOptions Connected;

} __attribute__((packed)) OveroSyncStatsDataPacked;

/*
 * Packed Object data.
 * Alignment is forced to 4 bytes
 */
typedef OveroSyncStatsDataPacked __attribute__((aligned(4))) OveroSyncStatsData;

/*
 * Union to apply the data array to and to use as structured object data
 */
union {
    OveroSyncStatsDataPacked data;
    byte arr[OVEROSYNCSTATS_NUMBYTES];
 } OveroSyncStatsDataUnion;

#endif // OVEROSYNCSTATS_H

/**
 * @}
 * @}
 */
