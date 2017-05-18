/**
 ******************************************************************************
 * @addtogroup UAVObjects LibrePilot UAVObjects
 * @{
 * @addtogroup StabilizationSettingsBank1 StabilizationSettingsBank1
 * @brief Currently selected PID bank
 *
 * Autogenerated files and functions for StabilizationSettingsBank1 Object
 *
 * @{
 *
 * @file       stabilizationsettingsbank1.h
 *
 * @author     The LibrePilot Project, https://www.librepilot.org, (C) 2017.
 *             The OpenPilot Team, http://www.openpilot.org Copyright (C) 2010-2013.
 *
 * @brief      Arduino Header of the StabilizationSettingsBank1 object. This file has been
 *             automatically generated by the UAVObjectGenerator.
 *
 * @note       Object definition file: stabilizationsettingsbank1.xml.
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

#ifndef STABILIZATIONSETTINGSBANK1_H
#define STABILIZATIONSETTINGSBANK1_H
#include <stdbool.h>
/* Object constants */
#define STABILIZATIONSETTINGSBANK1_OBJID 0xCAC270DC
#define STABILIZATIONSETTINGSBANK1_ISSINGLEINST 1
#define STABILIZATIONSETTINGSBANK1_ISSETTINGS 1
#define STABILIZATIONSETTINGSBANK1_ISPRIORITY 0
#define STABILIZATIONSETTINGSBANK1_NUMBYTES sizeof(StabilizationSettingsBank1Data)

/* Field RollRatePID information */

// Array element names for field RollRatePID
typedef enum {
    STABILIZATIONSETTINGSBANK1_ROLLRATEPID_KP=0,
    STABILIZATIONSETTINGSBANK1_ROLLRATEPID_KI=1,
    STABILIZATIONSETTINGSBANK1_ROLLRATEPID_KD=2,
    STABILIZATIONSETTINGSBANK1_ROLLRATEPID_ILIMIT=3
} StabilizationSettingsBank1RollRatePIDElem;

// Number of elements for field RollRatePID
#define STABILIZATIONSETTINGSBANK1_ROLLRATEPID_NUMELEM 4

/* Field PitchRatePID information */

// Array element names for field PitchRatePID
typedef enum {
    STABILIZATIONSETTINGSBANK1_PITCHRATEPID_KP=0,
    STABILIZATIONSETTINGSBANK1_PITCHRATEPID_KI=1,
    STABILIZATIONSETTINGSBANK1_PITCHRATEPID_KD=2,
    STABILIZATIONSETTINGSBANK1_PITCHRATEPID_ILIMIT=3
} StabilizationSettingsBank1PitchRatePIDElem;

// Number of elements for field PitchRatePID
#define STABILIZATIONSETTINGSBANK1_PITCHRATEPID_NUMELEM 4

/* Field YawRatePID information */

// Array element names for field YawRatePID
typedef enum {
    STABILIZATIONSETTINGSBANK1_YAWRATEPID_KP=0,
    STABILIZATIONSETTINGSBANK1_YAWRATEPID_KI=1,
    STABILIZATIONSETTINGSBANK1_YAWRATEPID_KD=2,
    STABILIZATIONSETTINGSBANK1_YAWRATEPID_ILIMIT=3
} StabilizationSettingsBank1YawRatePIDElem;

// Number of elements for field YawRatePID
#define STABILIZATIONSETTINGSBANK1_YAWRATEPID_NUMELEM 4

/* Field RollPI information */

// Array element names for field RollPI
typedef enum {
    STABILIZATIONSETTINGSBANK1_ROLLPI_KP=0,
    STABILIZATIONSETTINGSBANK1_ROLLPI_KI=1,
    STABILIZATIONSETTINGSBANK1_ROLLPI_ILIMIT=2
} StabilizationSettingsBank1RollPIElem;

// Number of elements for field RollPI
#define STABILIZATIONSETTINGSBANK1_ROLLPI_NUMELEM 3

/* Field PitchPI information */

// Array element names for field PitchPI
typedef enum {
    STABILIZATIONSETTINGSBANK1_PITCHPI_KP=0,
    STABILIZATIONSETTINGSBANK1_PITCHPI_KI=1,
    STABILIZATIONSETTINGSBANK1_PITCHPI_ILIMIT=2
} StabilizationSettingsBank1PitchPIElem;

// Number of elements for field PitchPI
#define STABILIZATIONSETTINGSBANK1_PITCHPI_NUMELEM 3

/* Field YawPI information */

// Array element names for field YawPI
typedef enum {
    STABILIZATIONSETTINGSBANK1_YAWPI_KP=0,
    STABILIZATIONSETTINGSBANK1_YAWPI_KI=1,
    STABILIZATIONSETTINGSBANK1_YAWPI_ILIMIT=2
} StabilizationSettingsBank1YawPIElem;

// Number of elements for field YawPI
#define STABILIZATIONSETTINGSBANK1_YAWPI_NUMELEM 3

/* Field ManualRate information */

// Array element names for field ManualRate
typedef enum {
    STABILIZATIONSETTINGSBANK1_MANUALRATE_ROLL=0,
    STABILIZATIONSETTINGSBANK1_MANUALRATE_PITCH=1,
    STABILIZATIONSETTINGSBANK1_MANUALRATE_YAW=2
} StabilizationSettingsBank1ManualRateElem;

// Number of elements for field ManualRate
#define STABILIZATIONSETTINGSBANK1_MANUALRATE_NUMELEM 3

/* Field MaximumRate information */

// Array element names for field MaximumRate
typedef enum {
    STABILIZATIONSETTINGSBANK1_MAXIMUMRATE_ROLL=0,
    STABILIZATIONSETTINGSBANK1_MAXIMUMRATE_PITCH=1,
    STABILIZATIONSETTINGSBANK1_MAXIMUMRATE_YAW=2
} StabilizationSettingsBank1MaximumRateElem;

// Number of elements for field MaximumRate
#define STABILIZATIONSETTINGSBANK1_MAXIMUMRATE_NUMELEM 3

/* Field RollMax information */

/* Field PitchMax information */

/* Field YawMax information */

/* Field StickExpo information */

// Array element names for field StickExpo
typedef enum {
    STABILIZATIONSETTINGSBANK1_STICKEXPO_ROLL=0,
    STABILIZATIONSETTINGSBANK1_STICKEXPO_PITCH=1,
    STABILIZATIONSETTINGSBANK1_STICKEXPO_YAW=2
} StabilizationSettingsBank1StickExpoElem;

// Number of elements for field StickExpo
#define STABILIZATIONSETTINGSBANK1_STICKEXPO_NUMELEM 3

/* Field AcroInsanityFactor information */

// Array element names for field AcroInsanityFactor
typedef enum {
    STABILIZATIONSETTINGSBANK1_ACROINSANITYFACTOR_ROLL=0,
    STABILIZATIONSETTINGSBANK1_ACROINSANITYFACTOR_PITCH=1,
    STABILIZATIONSETTINGSBANK1_ACROINSANITYFACTOR_YAW=2
} StabilizationSettingsBank1AcroInsanityFactorElem;

// Number of elements for field AcroInsanityFactor
#define STABILIZATIONSETTINGSBANK1_ACROINSANITYFACTOR_NUMELEM 3

/* Field EnablePiroComp information */

// Enumeration options for field EnablePiroComp
typedef enum __attribute__ ((__packed__)) {
    STABILIZATIONSETTINGSBANK1_ENABLEPIROCOMP_FALSE=0,
    STABILIZATIONSETTINGSBANK1_ENABLEPIROCOMP_TRUE=1
} StabilizationSettingsBank1EnablePiroCompOptions;

/* Field FpvCamTiltCompensation information */

/* Field EnableThrustPIDScaling information */

// Enumeration options for field EnableThrustPIDScaling
typedef enum __attribute__ ((__packed__)) {
    STABILIZATIONSETTINGSBANK1_ENABLETHRUSTPIDSCALING_FALSE=0,
    STABILIZATIONSETTINGSBANK1_ENABLETHRUSTPIDSCALING_TRUE=1
} StabilizationSettingsBank1EnableThrustPIDScalingOptions;

/* Field ThrustPIDScaleCurve information */

// Array element names for field ThrustPIDScaleCurve
typedef enum {
    STABILIZATIONSETTINGSBANK1_THRUSTPIDSCALECURVE_0=0,
    STABILIZATIONSETTINGSBANK1_THRUSTPIDSCALECURVE_25=1,
    STABILIZATIONSETTINGSBANK1_THRUSTPIDSCALECURVE_50=2,
    STABILIZATIONSETTINGSBANK1_THRUSTPIDSCALECURVE_75=3,
    STABILIZATIONSETTINGSBANK1_THRUSTPIDSCALECURVE_100=4
} StabilizationSettingsBank1ThrustPIDScaleCurveElem;

// Number of elements for field ThrustPIDScaleCurve
#define STABILIZATIONSETTINGSBANK1_THRUSTPIDSCALECURVE_NUMELEM 5

/* Field ThrustPIDScaleSource information */

// Enumeration options for field ThrustPIDScaleSource
typedef enum __attribute__ ((__packed__)) {
    STABILIZATIONSETTINGSBANK1_THRUSTPIDSCALESOURCE_MANUALCONTROLTHROTTLE=0,
    STABILIZATIONSETTINGSBANK1_THRUSTPIDSCALESOURCE_STABILIZATIONDESIREDTHRUST=1,
    STABILIZATIONSETTINGSBANK1_THRUSTPIDSCALESOURCE_ACTUATORDESIREDTHRUST=2
} StabilizationSettingsBank1ThrustPIDScaleSourceOptions;

/* Field ThrustPIDScaleTarget information */

// Enumeration options for field ThrustPIDScaleTarget
typedef enum __attribute__ ((__packed__)) {
    STABILIZATIONSETTINGSBANK1_THRUSTPIDSCALETARGET_PID=0,
    STABILIZATIONSETTINGSBANK1_THRUSTPIDSCALETARGET_PI=1,
    STABILIZATIONSETTINGSBANK1_THRUSTPIDSCALETARGET_PD=2,
    STABILIZATIONSETTINGSBANK1_THRUSTPIDSCALETARGET_ID=3,
    STABILIZATIONSETTINGSBANK1_THRUSTPIDSCALETARGET_P=4,
    STABILIZATIONSETTINGSBANK1_THRUSTPIDSCALETARGET_I=5,
    STABILIZATIONSETTINGSBANK1_THRUSTPIDSCALETARGET_D=6
} StabilizationSettingsBank1ThrustPIDScaleTargetOptions;

/* Field ThrustPIDScaleAxes information */

// Enumeration options for field ThrustPIDScaleAxes
typedef enum __attribute__ ((__packed__)) {
    STABILIZATIONSETTINGSBANK1_THRUSTPIDSCALEAXES_ROLLPITCHYAW=0,
    STABILIZATIONSETTINGSBANK1_THRUSTPIDSCALEAXES_ROLLPITCH=1,
    STABILIZATIONSETTINGSBANK1_THRUSTPIDSCALEAXES_ROLLYAW=2,
    STABILIZATIONSETTINGSBANK1_THRUSTPIDSCALEAXES_ROLL=3,
    STABILIZATIONSETTINGSBANK1_THRUSTPIDSCALEAXES_PITCHYAW=4,
    STABILIZATIONSETTINGSBANK1_THRUSTPIDSCALEAXES_PITCH=5,
    STABILIZATIONSETTINGSBANK1_THRUSTPIDSCALEAXES_YAW=6
} StabilizationSettingsBank1ThrustPIDScaleAxesOptions;



typedef struct __attribute__ ((__packed__)) {
    float Kp;
    float Ki;
    float Kd;
    float ILimit;
}  StabilizationSettingsBank1RollRatePIDData ;
typedef struct __attribute__ ((__packed__)) {
    float array[4];
}  StabilizationSettingsBank1RollRatePIDDataArray ;
#define StabilizationSettingsBank1RollRatePIDToArray( var ) UAVObjectFieldToArray( StabilizationSettingsBank1RollRatePIDData, var )

typedef struct __attribute__ ((__packed__)) {
    float Kp;
    float Ki;
    float Kd;
    float ILimit;
}  StabilizationSettingsBank1PitchRatePIDData ;
typedef struct __attribute__ ((__packed__)) {
    float array[4];
}  StabilizationSettingsBank1PitchRatePIDDataArray ;
#define StabilizationSettingsBank1PitchRatePIDToArray( var ) UAVObjectFieldToArray( StabilizationSettingsBank1PitchRatePIDData, var )

typedef struct __attribute__ ((__packed__)) {
    float Kp;
    float Ki;
    float Kd;
    float ILimit;
}  StabilizationSettingsBank1YawRatePIDData ;
typedef struct __attribute__ ((__packed__)) {
    float array[4];
}  StabilizationSettingsBank1YawRatePIDDataArray ;
#define StabilizationSettingsBank1YawRatePIDToArray( var ) UAVObjectFieldToArray( StabilizationSettingsBank1YawRatePIDData, var )

typedef struct __attribute__ ((__packed__)) {
    float Kp;
    float Ki;
    float ILimit;
}  StabilizationSettingsBank1RollPIData ;
typedef struct __attribute__ ((__packed__)) {
    float array[3];
}  StabilizationSettingsBank1RollPIDataArray ;
#define StabilizationSettingsBank1RollPIToArray( var ) UAVObjectFieldToArray( StabilizationSettingsBank1RollPIData, var )

typedef struct __attribute__ ((__packed__)) {
    float Kp;
    float Ki;
    float ILimit;
}  StabilizationSettingsBank1PitchPIData ;
typedef struct __attribute__ ((__packed__)) {
    float array[3];
}  StabilizationSettingsBank1PitchPIDataArray ;
#define StabilizationSettingsBank1PitchPIToArray( var ) UAVObjectFieldToArray( StabilizationSettingsBank1PitchPIData, var )

typedef struct __attribute__ ((__packed__)) {
    float Kp;
    float Ki;
    float ILimit;
}  StabilizationSettingsBank1YawPIData ;
typedef struct __attribute__ ((__packed__)) {
    float array[3];
}  StabilizationSettingsBank1YawPIDataArray ;
#define StabilizationSettingsBank1YawPIToArray( var ) UAVObjectFieldToArray( StabilizationSettingsBank1YawPIData, var )

typedef struct __attribute__ ((__packed__)) {
    uint16_t Roll;
    uint16_t Pitch;
    uint16_t Yaw;
}  StabilizationSettingsBank1ManualRateData ;
typedef struct __attribute__ ((__packed__)) {
    uint16_t array[3];
}  StabilizationSettingsBank1ManualRateDataArray ;
#define StabilizationSettingsBank1ManualRateToArray( var ) UAVObjectFieldToArray( StabilizationSettingsBank1ManualRateData, var )

typedef struct __attribute__ ((__packed__)) {
    uint16_t Roll;
    uint16_t Pitch;
    uint16_t Yaw;
}  StabilizationSettingsBank1MaximumRateData ;
typedef struct __attribute__ ((__packed__)) {
    uint16_t array[3];
}  StabilizationSettingsBank1MaximumRateDataArray ;
#define StabilizationSettingsBank1MaximumRateToArray( var ) UAVObjectFieldToArray( StabilizationSettingsBank1MaximumRateData, var )

typedef struct __attribute__ ((__packed__)) {
    int8_t Roll;
    int8_t Pitch;
    int8_t Yaw;
}  StabilizationSettingsBank1StickExpoData ;
typedef struct __attribute__ ((__packed__)) {
    int8_t array[3];
}  StabilizationSettingsBank1StickExpoDataArray ;
#define StabilizationSettingsBank1StickExpoToArray( var ) UAVObjectFieldToArray( StabilizationSettingsBank1StickExpoData, var )

typedef struct __attribute__ ((__packed__)) {
    uint8_t Roll;
    uint8_t Pitch;
    uint8_t Yaw;
}  StabilizationSettingsBank1AcroInsanityFactorData ;
typedef struct __attribute__ ((__packed__)) {
    uint8_t array[3];
}  StabilizationSettingsBank1AcroInsanityFactorDataArray ;
#define StabilizationSettingsBank1AcroInsanityFactorToArray( var ) UAVObjectFieldToArray( StabilizationSettingsBank1AcroInsanityFactorData, var )


/*
 * Packed Object data (unaligned).
 * Should only be used where 4 byte alignment can be guaranteed
 * (eg a single instance on the heap)
 */
typedef struct {
    StabilizationSettingsBank1RollRatePIDData RollRatePID;
    StabilizationSettingsBank1PitchRatePIDData PitchRatePID;
    StabilizationSettingsBank1YawRatePIDData YawRatePID;
    StabilizationSettingsBank1RollPIData RollPI;
    StabilizationSettingsBank1PitchPIData PitchPI;
    StabilizationSettingsBank1YawPIData YawPI;
    StabilizationSettingsBank1ManualRateData ManualRate;
    StabilizationSettingsBank1MaximumRateData MaximumRate;
    uint8_t RollMax;
    uint8_t PitchMax;
    uint8_t YawMax;
    StabilizationSettingsBank1StickExpoData StickExpo;
    StabilizationSettingsBank1AcroInsanityFactorData AcroInsanityFactor;
    StabilizationSettingsBank1EnablePiroCompOptions EnablePiroComp;
    uint8_t FpvCamTiltCompensation;
    StabilizationSettingsBank1EnableThrustPIDScalingOptions EnableThrustPIDScaling;
    int8_t ThrustPIDScaleCurve[5];
    StabilizationSettingsBank1ThrustPIDScaleSourceOptions ThrustPIDScaleSource;
    StabilizationSettingsBank1ThrustPIDScaleTargetOptions ThrustPIDScaleTarget;
    StabilizationSettingsBank1ThrustPIDScaleAxesOptions ThrustPIDScaleAxes;

} __attribute__((packed)) StabilizationSettingsBank1DataPacked;

/*
 * Packed Object data.
 * Alignment is forced to 4 bytes
 */
typedef StabilizationSettingsBank1DataPacked __attribute__((aligned(4))) StabilizationSettingsBank1Data;

/*
 * Union to apply the data array to and to use as structured object data
 */
union {
    StabilizationSettingsBank1DataPacked data;
    byte arr[STABILIZATIONSETTINGSBANK1_NUMBYTES];
 } StabilizationSettingsBank1DataUnion;

#endif // STABILIZATIONSETTINGSBANK1_H

/**
 * @}
 * @}
 */
