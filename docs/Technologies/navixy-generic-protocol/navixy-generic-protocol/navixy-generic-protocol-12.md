---
description: >-
  Navixy Generic Protocol version 1.2 adds source_type and precision to the
  location object, enabling explicit identification of positioning source and
  accuracy reporting.
---

# Navixy Generic Protocol 1.2

Version 1.2 is backward compatible with [1.0](navixy-generic-protocol-10.md). It extends the `location` object with two new fields that allow devices to explicitly declare the positioning source and report location accuracy.

## Changes from 1.0

### New location fields

| **Attribute**   | **Type** | **Object** | **Required** | **Description**                                                                                                              |
| --------------- | -------- | ---------- | ------------ | ---------------------------------------------------------------------------------------------------------------------------- |
| └─ source\_type | String   | location   | No           | Positioning source. Possible values: `GNSS` (satellite), `LBS` (cell tower-based), `ATLAS` (third-party positioning service). |
| └─ precision    | Integer  | location   | No           | Location accuracy in meters. Most relevant for LBS positioning, where accuracy can vary significantly.                       |

`source_type` lets the platform handle the position correctly depending on its origin. When omitted, the platform treats the location as GNSS by default. `precision` is optional but recommended for LBS and ATLAS positions, where the platform can use it to determine whether the accuracy is sufficient for a given use case.

{% details "Full attribute reference for version 1.2" %}

| **Attribute**                | **Type**        | **Object**    | **Required** | **Description**                                                                                                                                                        |
| ---------------------------- | --------------- | ------------- | ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Basic attributes**         |                 |               |              |                                                                                                                                                                        |
| message\_time                | Timestamp       | Root          | Yes          | Date and time the message was sent by the device (ISO 8601 UTC).                                                                                                       |
| device\_id                   | String          | Root          | Yes          | Unique device identifier. Maximum 64 characters.                                                                                                                       |
| version                      | String          | Root          | No           | NGP version of this message. Use `1.2` to enable `source_type` and `precision`.                                                                                        |
| **Location**                 |                 |               |              |                                                                                                                                                                        |
| location                     | Object          | Root          | No           | Device position. May be determined by GNSS (satellite), LBS (cell towers), or a third-party positioning service.                                                       |
| └─ latitude                  | Float           | location      | No           | Latitude in decimal degrees (−90.0 to 90.0).                                                                                                                           |
| └─ longitude                 | Float           | location      | No           | Longitude in decimal degrees (−180.0 to 180.0).                                                                                                                        |
| └─ altitude                  | Float           | location      | No           | Altitude above sea level in meters (−1000 to 10000).                                                                                                                   |
| └─ gnss\_time                | Timestamp       | location      | No           | Time when the position fix was acquired by the device.                                                                                                                 |
| └─ fix\_type                 | String          | location      | No           | Position fix type. Possible values: `HAS_FIX` (default), `NO_FIX`, `LAST_KNOWN_POSITION`, `FIX_2D`, `FIX_3D`.                                                          |
| └─ satellites                | Integer         | location      | No           | Number of GNSS satellites used for the fix (0–64).                                                                                                                     |
| └─ hdop                      | Float           | location      | No           | Horizontal dilution of precision. Lower is more accurate.                                                                                                              |
| └─ vdop                      | Float           | location      | No           | Vertical dilution of precision. Lower is more accurate.                                                                                                                |
| └─ pdop                      | Float           | location      | No           | 3D position dilution of precision, combining horizontal and vertical.                                                                                                  |
| └─ speed                     | Float           | location      | No           | Device speed in km/h (positive values only).                                                                                                                           |
| └─ heading                   | Integer         | location      | No           | Direction of movement in degrees, clockwise from north (1–360).                                                                                                        |
| └─ source\_type              | String          | location      | No           | **New in 1.2.** Positioning source. Possible values: `GNSS` (satellite), `LBS` (cell tower-based), `ATLAS` (third-party positioning service). Defaults to `GNSS`.      |
| └─ precision                 | Integer         | location      | No           | **New in 1.2.** Location accuracy in meters. Most relevant for LBS positioning, where accuracy can vary significantly.                                                 |
| **Event information**        |                 |               |              |                                                                                                                                                                        |
| event\_id                    | Integer         | Root          | No           | Platform event identifier. See [Predefined event identifiers](navixy-generic-protocol-10/predefined-event-identifiers.md) for standard values. Custom events start at 10,000. |
| **Mobile cells**             |                 |               |              |                                                                                                                                                                        |
| mobile\_cells                | Array \[Object] | Root          | No           | List of visible cell towers. Used to provide data for network-based positioning (LBS) when GNSS is unavailable.                                                        |
| └─ mcc                       | Integer         | mobile\_cells | Yes          | Mobile Country Code. Identifies the country of the mobile network.                                                                                                     |
| └─ mnc                       | Integer         | mobile\_cells | Yes          | Mobile Network Code. Identifies the mobile operator within the country.                                                                                                |
| └─ lac                       | Integer         | mobile\_cells | Yes          | Location Area Code. Identifies the area within the mobile network.                                                                                                     |
| └─ cell\_id                  | Integer         | mobile\_cells | Yes          | Unique identifier of the cell tower.                                                                                                                                   |
| └─ rssi                      | Integer         | mobile\_cells | No           | Signal strength from the cell tower in dBm (negative values).                                                                                                          |
| └─ type                      | String          | mobile\_cells | No           | Radio access technology. Possible values: `GSM` (default), `CDMA`, `WCDMA`, `LTE`, `NR`.                                                                               |
| **Wi-Fi points**             |                 |               |              |                                                                                                                                                                        |
| wifi\_points                 | Array \[Object] | Root          | No           | List of visible Wi-Fi access points. Used alongside `mobile_cells` to improve network-based positioning accuracy.                                                      |
| └─ mac                       | String          | wifi\_points  | Yes          | MAC address of the access point. Colon-delimited bytes, e.g. `12:33:FF:45:04:33`.                                                                                      |
| └─ rssi                      | Integer         | wifi\_points  | Yes          | Signal strength in dBm (negative values).                                                                                                                              |
| └─ age                       | Integer         | wifi\_points  | No           | Milliseconds since this access point was last detected.                                                                                                                |
| └─ channel                   | Integer         | wifi\_points  | No           | Radio channel number used by the access point.                                                                                                                         |
| **Device motion and status** |                 |               |              |                                                                                                                                                                        |
| is\_moving                   | Boolean         | Root          | No           | `true` if the device is currently moving, `false` if stationary.                                                                                                       |
| hardware\_mileage            | Float           | Root          | No           | Cumulative mileage counted by the device hardware, in kilometers.                                                                                                      |
| battery\_voltage             | Float           | Root          | No           | Built-in battery voltage in volts.                                                                                                                                     |
| battery\_level               | Integer         | Root          | No           | Built-in battery charge level as a percentage (0–100).                                                                                                                 |
| board\_voltage               | Float           | Root          | No           | External power supply voltage in volts.                                                                                                                                |
| **Input/Output status**      |                 |               |              |                                                                                                                                                                        |
| input\_status                | Integer         | Root          | No           | State of discrete inputs as a bitmask. Bit 0 = input 1, bit 1 = input 2, and so on. A set bit means the input is active.                                               |
| output\_status               | Integer         | Root          | No           | State of outputs as a bitmask. Bit 0 = output 1, bit 1 = output 2, and so on. A set bit means the output is active.                                                    |
| **Sensor data**              |                 |               |              |                                                                                                                                                                        |
| analog\_n                    | Float           | Root          | No           | Analog input voltage in volts. `n` is the sensor index from 1 to 16, e.g. `analog_1`.                                                                                  |
| temperature\_internal        | Float           | Root          | No           | Temperature from the built-in hardware sensor, in degrees Celsius.                                                                                                     |
| temperature\_n               | Float           | Root          | No           | External temperature sensor reading in degrees Celsius. `n` is the sensor index from 1 to 16.                                                                          |
| humidity\_internal           | Float           | Root          | No           | Relative humidity from the built-in hardware sensor, as a percentage.                                                                                                  |
| humidity\_n                  | Float           | Root          | No           | External relative humidity sensor reading as a percentage. `n` is the sensor index from 1 to 16.                                                                       |
| fuel\_level\_n               | Float           | Root          | No           | Fuel level from a fuel sensor, in liters or as a percentage. `n` is the sensor index from 1 to 16.                                                                     |
| fuel\_temperature\_n         | Float           | Root          | No           | Fuel temperature from a fuel sensor, in degrees Celsius. `n` is the sensor index from 1 to 16.                                                                         |
| impulse\_counter\_n          | Integer         | Root          | No           | Impulse counter reading. `n` is the counter index from 1 to 16.                                                                                                        |
| **Identification data**      |                 |               |              |                                                                                                                                                                        |
| hardware\_key                | String          | Root          | No           | Driver or asset identifier, typically read via RFID, iButton, or similar method.                                                                                       |
| vin                          | String          | Root          | No           | Vehicle Identification Number (VIN).                                                                                                                                   |
| **Custom data**              |                 |               |              |                                                                                                                                                                        |
| custom\_\*                   | Mixed           | Root          | No           | Any additional device-specific attribute. See [Custom attributes](navixy-generic-protocol-10/message-structure-and-attributes.md#custom-attributes).                   |

{% enddetails %}

### Example: LBS-based message

A position report from a device with no GNSS fix, using cell tower data to resolve an approximate location:

```json
{
    "message_time": "2024-09-02T10:05:12Z",
    "device_id": "857378374927457",
    "version": "1.2",
    "location": {
        "latitude": 56.352100,
        "longitude": 60.128900,
        "source_type": "LBS",
        "precision": 800
    },
    "event_id": 402,
    "mobile_cells": [
        {
            "mcc": 250,
            "mnc": 0,
            "lac": 32445,
            "cell_id": 343455,
            "rssi": -78,
            "type": "LTE"
        }
    ]
}
```

The `precision` value of `800` indicates the resolved coordinates are accurate within approximately 800 meters.
