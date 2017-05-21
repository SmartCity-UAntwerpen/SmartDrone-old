/**
 ******************************************************************************
 * @addtogroup UAVObjects LibrePilot UAVObjects
 * @{
 * @addtogroup AltitudeFilterSettings AltitudeFilterSettings
 * @brief Settings for the @ref State Estimator module plugin altitudeFilter
 *
 * Autogenerated files and functions for AltitudeFilterSettings Object
 *
 * @{
 *
 * @file       altitudefiltersettings.h
 *
 * @author     The LibrePilot Project, https://www.librepilot.org, (C) 2017.
 *             The OpenPilot Team, http://www.openpilot.org Copyright (C) 2010-2013.
 *
 * @brief      Arduino Header of the AltitudeFilterSettings object. This file has been
 *             automatically generated by the UAVObjectGenerator.
 *
 * @note       Object definition file: altitudefiltersettings.xml.
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

#ifndef ALTITUDEFILTERSETTINGS_H
#define ALTITUDEFILTERSETTINGS_H
#include <stdbool.h>
/* Object constants */
#define ALTITUDEFILTERSETTINGS_OBJID 0xE611042C
#define ALTITUDEFILTERSETTINGS_ISSINGLEINST 1
#define ALTITUDEFILTERSETTINGS_ISSETTINGS 1
#define ALTITUDEFILTERSETTINGS_ISPRIORITY 0
#define ALTITUDEFILTERSETTINGS_NUMBYTES sizeof(AltitudeFilterSettingsData)

/* Field AccelLowPassKp information */

/* Field AccelDriftKi information */

/* Field InitializationAccelDriftKi information */

/* Field BaroKp information */




/*
 * Packed Object data (unaligned).
 * Should only be used where 4 byte alignment can be guaranteed
 * (eg a single instance on the heap)
 */
typedef struct {
    float AccelLowPassKp;
    float AccelDriftKi;
    float InitializationAccelDriftKi;
    float BaroKp;

} __attribute__((packed)) AltitudeFilterSettingsDataPacked;

/*
 * Packed Object data.
 * Alignment is forced to 4 bytes
 */
typedef AltitudeFilterSettingsDataPacked __attribute__((aligned(4))) AltitudeFilterSettingsData;

/*
 * Union to apply the data array to and to use as structured object data
 */
union {
    AltitudeFilterSettingsDataPacked data;
    byte arr[ALTITUDEFILTERSETTINGS_NUMBYTES];
 } AltitudeFilterSettingsDataUnion;

#endif // ALTITUDEFILTERSETTINGS_H

/**
 * @}
 * @}
 */
