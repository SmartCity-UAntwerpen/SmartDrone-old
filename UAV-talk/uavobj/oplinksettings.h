/**
 ******************************************************************************
 * @addtogroup UAVObjects LibrePilot UAVObjects
 * @{
 * @addtogroup OPLinkSettings OPLinkSettings
 * @brief OPLink configurations options.
 *
 * Autogenerated files and functions for OPLinkSettings Object
 *
 * @{
 *
 * @file       oplinksettings.h
 *
 * @author     The LibrePilot Project, https://www.librepilot.org, (C) 2017.
 *             The OpenPilot Team, http://www.openpilot.org Copyright (C) 2010-2013.
 *
 * @brief      Arduino Header of the OPLinkSettings object. This file has been
 *             automatically generated by the UAVObjectGenerator.
 *
 * @note       Object definition file: oplinksettings.xml.
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

#ifndef OPLINKSETTINGS_H
#define OPLINKSETTINGS_H
#include <stdbool.h>
/* Object constants */
#define OPLINKSETTINGS_OBJID 0xCB2A32C
#define OPLINKSETTINGS_ISSINGLEINST 1
#define OPLINKSETTINGS_ISSETTINGS 1
#define OPLINKSETTINGS_ISPRIORITY 0
#define OPLINKSETTINGS_NUMBYTES sizeof(OPLinkSettingsData)

/* Field CoordID information */

/* Field CustomDeviceID information */

/* Field SerialBaudrate information */

/* Field RFFrequency information */

/* Field FailsafeDelay information */

/* Field BeaconFrequency information */

/* Field Protocol information */

// Enumeration options for field Protocol
typedef enum __attribute__ ((__packed__)) {
    OPLINKSETTINGS_PROTOCOL_DISABLED=0,
    OPLINKSETTINGS_PROTOCOL_OPLINKRECEIVER=1,
    OPLINKSETTINGS_PROTOCOL_OPLINKCOORDINATOR=2,
    OPLINKSETTINGS_PROTOCOL_OPENLRS=3
} OPLinkSettingsProtocolOptions;

/* Field LinkType information */

// Enumeration options for field LinkType
typedef enum __attribute__ ((__packed__)) {
    OPLINKSETTINGS_LINKTYPE_DATA=0,
    OPLINKSETTINGS_LINKTYPE_CONTROL=1,
    OPLINKSETTINGS_LINKTYPE_DATAANDCONTROL=2
} OPLinkSettingsLinkTypeOptions;

/* Field MainPort information */

// Enumeration options for field MainPort
typedef enum __attribute__ ((__packed__)) {
    OPLINKSETTINGS_MAINPORT_DISABLED=0,
    OPLINKSETTINGS_MAINPORT_TELEMETRY=1,
    OPLINKSETTINGS_MAINPORT_SERIAL=2,
    OPLINKSETTINGS_MAINPORT_COMBRIDGE=3,
    OPLINKSETTINGS_MAINPORT_PPM=4,
    OPLINKSETTINGS_MAINPORT_PWM=5
} OPLinkSettingsMainPortOptions;

/* Field FlexiPort information */

// Enumeration options for field FlexiPort
typedef enum __attribute__ ((__packed__)) {
    OPLINKSETTINGS_FLEXIPORT_DISABLED=0,
    OPLINKSETTINGS_FLEXIPORT_TELEMETRY=1,
    OPLINKSETTINGS_FLEXIPORT_SERIAL=2,
    OPLINKSETTINGS_FLEXIPORT_COMBRIDGE=3,
    OPLINKSETTINGS_FLEXIPORT_PPM=4,
    OPLINKSETTINGS_FLEXIPORT_PWM=5
} OPLinkSettingsFlexiPortOptions;

/* Field VCPPort information */

// Enumeration options for field VCPPort
typedef enum __attribute__ ((__packed__)) {
    OPLINKSETTINGS_VCPPORT_DISABLED=0,
    OPLINKSETTINGS_VCPPORT_SERIAL=1,
    OPLINKSETTINGS_VCPPORT_COMBRIDGE=2
} OPLinkSettingsVCPPortOptions;

/* Field ComSpeed information */

// Enumeration options for field ComSpeed
typedef enum __attribute__ ((__packed__)) {
    OPLINKSETTINGS_COMSPEED_4800=0,
    OPLINKSETTINGS_COMSPEED_9600=1,
    OPLINKSETTINGS_COMSPEED_19200=2,
    OPLINKSETTINGS_COMSPEED_38400=3,
    OPLINKSETTINGS_COMSPEED_57600=4,
    OPLINKSETTINGS_COMSPEED_115200=5
} OPLinkSettingsComSpeedOptions;

/* Field MaxRFPower information */

// Enumeration options for field MaxRFPower
typedef enum __attribute__ ((__packed__)) {
    OPLINKSETTINGS_MAXRFPOWER_0=0,
    OPLINKSETTINGS_MAXRFPOWER_125=1,
    OPLINKSETTINGS_MAXRFPOWER_16=2,
    OPLINKSETTINGS_MAXRFPOWER_316=3,
    OPLINKSETTINGS_MAXRFPOWER_63=4,
    OPLINKSETTINGS_MAXRFPOWER_126=5,
    OPLINKSETTINGS_MAXRFPOWER_25=6,
    OPLINKSETTINGS_MAXRFPOWER_50=7,
    OPLINKSETTINGS_MAXRFPOWER_100=8
} OPLinkSettingsMaxRFPowerOptions;

/* Field RFBand information */

// Enumeration options for field RFBand
typedef enum __attribute__ ((__packed__)) {
    OPLINKSETTINGS_RFBAND_433MHZ=0,
    OPLINKSETTINGS_RFBAND_868MHZ=1,
    OPLINKSETTINGS_RFBAND_915MHZ=2
} OPLinkSettingsRFBandOptions;

/* Field MinChannel information */

/* Field MaxChannel information */

/* Field RFXtalCap information */

/* Field Version information */

/* Field RSSIType information */

// Enumeration options for field RSSIType
typedef enum __attribute__ ((__packed__)) {
    OPLINKSETTINGS_RSSITYPE_COMBINED=0,
    OPLINKSETTINGS_RSSITYPE_RSSI=1,
    OPLINKSETTINGS_RSSITYPE_LINKQUALITY=2
} OPLinkSettingsRSSITypeOptions;

/* Field RadioAuxStream information */

// Enumeration options for field RadioAuxStream
typedef enum __attribute__ ((__packed__)) {
    OPLINKSETTINGS_RADIOAUXSTREAM_COMBRIDGE=0,
    OPLINKSETTINGS_RADIOAUXSTREAM_DISABLED=1
} OPLinkSettingsRadioAuxStreamOptions;

/* Field RFPower information */

/* Field RFChannelSpacing information */

/* Field HopChannel information */

// Number of elements for field HopChannel
#define OPLINKSETTINGS_HOPCHANNEL_NUMELEM 24

/* Field ModemParams information */

/* Field Flags information */

/* Field BeaconDelay information */

/* Field BeaconPeriod information */




/*
 * Packed Object data (unaligned).
 * Should only be used where 4 byte alignment can be guaranteed
 * (eg a single instance on the heap)
 */
typedef struct {
    uint32_t CoordID;
    uint32_t CustomDeviceID;
    uint32_t SerialBaudrate;
    uint32_t RFFrequency;
    uint32_t FailsafeDelay;
    uint32_t BeaconFrequency;
    OPLinkSettingsProtocolOptions Protocol;
    OPLinkSettingsLinkTypeOptions LinkType;
    OPLinkSettingsMainPortOptions MainPort;
    OPLinkSettingsFlexiPortOptions FlexiPort;
    OPLinkSettingsVCPPortOptions VCPPort;
    OPLinkSettingsComSpeedOptions ComSpeed;
    OPLinkSettingsMaxRFPowerOptions MaxRFPower;
    OPLinkSettingsRFBandOptions RFBand;
    uint8_t MinChannel;
    uint8_t MaxChannel;
    uint8_t RFXtalCap;
    uint8_t Version;
    OPLinkSettingsRSSITypeOptions RSSIType;
    OPLinkSettingsRadioAuxStreamOptions RadioAuxStream;
    uint8_t RFPower;
    uint8_t RFChannelSpacing;
    uint8_t HopChannel[24];
    uint8_t ModemParams;
    uint8_t Flags;
    uint8_t BeaconDelay;
    uint8_t BeaconPeriod;

} __attribute__((packed)) OPLinkSettingsDataPacked;

/*
 * Packed Object data.
 * Alignment is forced to 4 bytes
 */
typedef OPLinkSettingsDataPacked __attribute__((aligned(4))) OPLinkSettingsData;

/*
 * Union to apply the data array to and to use as structured object data
 */
union {
    OPLinkSettingsDataPacked data;
    byte arr[OPLINKSETTINGS_NUMBYTES];
 } OPLinkSettingsDataUnion;

#endif // OPLINKSETTINGS_H

/**
 * @}
 * @}
 */
