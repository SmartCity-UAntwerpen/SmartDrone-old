/**
 ******************************************************************************
 * @addtogroup UAVObjects LibrePilot UAVObjects
 * @{
 * @addtogroup EKFStateVariance EKFStateVariance
 * @brief Extended Kalman Filter state covariance
 *
 * Autogenerated files and functions for EKFStateVariance Object
 *
 * @{
 *
 * @file       ekfstatevariance.h
 *
 * @author     The LibrePilot Project, https://www.librepilot.org, (C) 2017.
 *             The OpenPilot Team, http://www.openpilot.org Copyright (C) 2010-2013.
 *
 * @brief      Arduino Header of the EKFStateVariance object. This file has been
 *             automatically generated by the UAVObjectGenerator.
 *
 * @note       Object definition file: ekfstatevariance.xml.
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

#ifndef EKFSTATEVARIANCE_H
#define EKFSTATEVARIANCE_H
#include <stdbool.h>
/* Object constants */
#define EKFSTATEVARIANCE_OBJID 0x1EB385E4
#define EKFSTATEVARIANCE_ISSINGLEINST 1
#define EKFSTATEVARIANCE_ISSETTINGS 0
#define EKFSTATEVARIANCE_ISPRIORITY 0
#define EKFSTATEVARIANCE_NUMBYTES sizeof(EKFStateVarianceData)

/* Field P information */

// Array element names for field P
typedef enum {
    EKFSTATEVARIANCE_P_POSITIONNORTH=0,
    EKFSTATEVARIANCE_P_POSITIONEAST=1,
    EKFSTATEVARIANCE_P_POSITIONDOWN=2,
    EKFSTATEVARIANCE_P_VELOCITYNORTH=3,
    EKFSTATEVARIANCE_P_VELOCITYEAST=4,
    EKFSTATEVARIANCE_P_VELOCITYDOWN=5,
    EKFSTATEVARIANCE_P_ATTITUDEQ1=6,
    EKFSTATEVARIANCE_P_ATTITUDEQ2=7,
    EKFSTATEVARIANCE_P_ATTITUDEQ3=8,
    EKFSTATEVARIANCE_P_ATTITUDEQ4=9,
    EKFSTATEVARIANCE_P_GYRODRIFTX=10,
    EKFSTATEVARIANCE_P_GYRODRIFTY=11,
    EKFSTATEVARIANCE_P_GYRODRIFTZ=12
} EKFStateVariancePElem;

// Number of elements for field P
#define EKFSTATEVARIANCE_P_NUMELEM 13



typedef struct __attribute__ ((__packed__)) {
    float PositionNorth;
    float PositionEast;
    float PositionDown;
    float VelocityNorth;
    float VelocityEast;
    float VelocityDown;
    float AttitudeQ1;
    float AttitudeQ2;
    float AttitudeQ3;
    float AttitudeQ4;
    float GyroDriftX;
    float GyroDriftY;
    float GyroDriftZ;
}  EKFStateVariancePData ;
typedef struct __attribute__ ((__packed__)) {
    float array[13];
}  EKFStateVariancePDataArray ;
#define EKFStateVariancePToArray( var ) UAVObjectFieldToArray( EKFStateVariancePData, var )


/*
 * Packed Object data (unaligned).
 * Should only be used where 4 byte alignment can be guaranteed
 * (eg a single instance on the heap)
 */
typedef struct {
    EKFStateVariancePData P;

} __attribute__((packed)) EKFStateVarianceDataPacked;

/*
 * Packed Object data.
 * Alignment is forced to 4 bytes
 */
typedef EKFStateVarianceDataPacked __attribute__((aligned(4))) EKFStateVarianceData;

/*
 * Union to apply the data array to and to use as structured object data
 */
union {
    EKFStateVarianceDataPacked data;
    byte arr[EKFSTATEVARIANCE_NUMBYTES];
 } EKFStateVarianceDataUnion;

#endif // EKFSTATEVARIANCE_H

/**
 * @}
 * @}
 */
