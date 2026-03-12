---
description: Complete reference for NGP message attributes — location, events, cell towers, Wi-Fi, sensors, I/O, and custom fields.
---

# Message structure and attributes

NGP messages are JSON objects transmitted one per request. Each message must contain two **mandatory** attributes: `device_id` and `message_time`.

{% hint style="warning" %}
`message_time` must not be earlier than the timestamp of the most recently received message for this device. Messages with an out-of-order timestamp will be discarded by the platform.
{% endhint %}

### Minimum valid message

```json
{
    "message_time": "2026-02-05T06:00:11Z",
    "device_id": "1112312212"
}
```

### Minimum message to be stored by the platform

The platform requires a valid location with at least 3 satellites before saving a data point. The `device_id` must already be registered on the platform.

```json
{
    "message_time": "2026-02-05T06:00:11Z",
    "device_id": "1112312212",
    "location": {
        "latitude": 34.15929687705282,
        "longitude": -118.4614133834839,
        "satellites": 3
    }
}
```

## Attributes

The table below lists all pre-defined attributes, organized by category. In addition to these, the protocol allows custom attributes — see [Custom attributes](#custom-attributes).

| **Attribute**                | **Type**        | **Object**     | **Required** | **Description**                                                                                                                                                           |
| ---------------------------- | --------------- | -------------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Basic attributes**         |                 |                |              |                                                                                                                                                                           |
| message\_time                | Timestamp       | Root           | Yes          | Date and time the message was sent by the device (ISO 8601 UTC).                                                                                                          |
| device\_id                   | String          | Root           | Yes          | Unique device identifier. Maximum 64 characters.                                                                                                                          |
| version                      | String          | Root           | No           | NGP version of this message. Defaults to `1.0` if omitted.                                                                                                                |
| **Location**                 |                 |                |              |                                                                                                                                                                           |
| location                     | Object          | Root           | No           | Device position. May be determined by GNSS (satellite), LBS (cell towers), or a third-party positioning service. Use `source_type` to indicate the positioning method.    |
| └─ latitude                  | Float           | location       | No           | Latitude in decimal degrees (−90.0 to 90.0).                                                                                                                              |
| └─ longitude                 | Float           | location       | No           | Longitude in decimal degrees (−180.0 to 180.0).                                                                                                                           |
| └─ altitude                  | Float           | location       | No           | Altitude above sea level in meters (−1000 to 10000).                                                                                                                      |
| └─ gnss\_time                | Timestamp       | location       | No           | Time when the position fix was acquired by the device.                                                                                                                    |
| └─ fix\_type                 | String          | location       | No           | Position fix type. Possible values: `HAS_FIX` (default), `NO_FIX`, `LAST_KNOWN_POSITION`, `FIX_2D`, `FIX_3D`.                                                            |
| └─ satellites                | Integer         | location       | No           | Number of GNSS satellites used for the fix (0–64).                                                                                                                        |
| └─ hdop                      | Float           | location       | No           | Horizontal dilution of precision — lower is more accurate.                                                                                                                |
| └─ vdop                      | Float           | location       | No           | Vertical dilution of precision — lower is more accurate.                                                                                                                  |
| └─ pdop                      | Float           | location       | No           | 3D position dilution of precision, combining horizontal and vertical.                                                                                                     |
| └─ speed                     | Float           | location       | No           | Device speed in km/h (positive values only).                                                                                                                              |
| └─ heading                   | Integer         | location       | No           | Direction of movement in degrees, clockwise from north (1–360).                                                                                                           |
| └─ source\_type              | String          | location       | No           | Positioning source. Possible values: `GNSS` (satellite), `LBS` (cell tower–based), `ATLAS` (third-party positioning service).                                             |
| └─ precision                 | Integer         | location       | No           | Location accuracy in meters. Most relevant for non-GNSS positioning methods such as LBS, where accuracy can vary significantly.                                            |
| **Event information**        |                 |                |              |                                                                                                                                                                           |
| event\_id                    | Integer         | Root           | No           | Platform event identifier. See [Predefined event identifiers](predefined-event-identifiers.md) for standard values. Custom events start at 10,000.                        |
| **Mobile cells**             |                 |                |              |                                                                                                                                                                           |
| mobile\_cells                | Array [Object]  | Root           | No           | List of visible cell towers. Used to provide data for network-based positioning (LBS) when GNSS is unavailable.                                                           |
| └─ mcc                       | Integer         | mobile\_cells  | Yes          | Mobile Country Code — identifies the country of the mobile network.                                                                                                       |
| └─ mnc                       | Integer         | mobile\_cells  | Yes          | Mobile Network Code — identifies the mobile operator within the country.                                                                                                  |
| └─ lac                       | Integer         | mobile\_cells  | Yes          | Location Area Code — identifies the area within the mobile network.                                                                                                       |
| └─ cell\_id                  | Integer         | mobile\_cells  | Yes          | Unique identifier of the cell tower.                                                                                                                                      |
| └─ rssi                      | Integer         | mobile\_cells  | No           | Signal strength from the cell tower in dBm (negative values).                                                                                                            |
| └─ type                      | String          | mobile\_cells  | No           | Radio access technology. Possible values: `GSM` (default), `CDMA`, `WCDMA`, `LTE`, `NR`.                                                                                 |
| **Wi-Fi points**             |                 |                |              |                                                                                                                                                                           |
| wifi\_points                 | Array [Object]  | Root           | No           | List of visible Wi-Fi access points. Used alongside `mobile_cells` to improve network-based positioning accuracy.                                                         |
| └─ mac                       | String          | wifi\_points   | Yes          | MAC address of the access point. Colon-delimited bytes, e.g. `12:33:FF:45:04:33`.                                                                                        |
| └─ rssi                      | Integer         | wifi\_points   | Yes          | Signal strength in dBm (negative values).                                                                                                                                 |
| └─ age                       | Integer         | wifi\_points   | No           | Milliseconds since this access point was last detected.                                                                                                                   |
| └─ channel                   | Integer         | wifi\_points   | No           | Radio channel number used by the access point.                                                                                                                            |
| **Device motion and status** |                 |                |              |                                                                                                                                                                           |
| is\_moving                   | Boolean         | Root           | No           | `true` if the device is currently moving, `false` if stationary.                                                                                                          |
| hardware\_mileage            | Float           | Root           | No           | Cumulative mileage counted by the device hardware, in kilometers.                                                                                                         |
| battery\_voltage             | Float           | Root           | No           | Built-in battery voltage in volts.                                                                                                                                        |
| battery\_level               | Integer         | Root           | No           | Built-in battery charge level as a percentage (0–100).                                                                                                                    |
| board\_voltage               | Float           | Root           | No           | External power supply voltage in volts.                                                                                                                                   |
| **Input/Output status**      |                 |                |              |                                                                                                                                                                           |
| input\_status                | Integer         | Root           | No           | State of discrete inputs as a bitmask. Bit 0 = input 1, bit 1 = input 2, and so on. A set bit means the input is active.                                                  |
| output\_status               | Integer         | Root           | No           | State of outputs as a bitmask. Bit 0 = output 1, bit 1 = output 2, and so on. A set bit means the output is active.                                                       |
| **Sensor data**              |                 |                |              |                                                                                                                                                                           |
| analog\_n                    | Float           | Root           | No           | Analog input voltage in volts. `n` is the sensor index from 1 to 16, e.g. `analog_1`, `analog_2`.                                                                        |
| temperature\_internal        | Float           | Root           | No           | Temperature from the built-in hardware sensor, in degrees Celsius.                                                                                                        |
| temperature\_n               | Float           | Root           | No           | External temperature sensor reading in degrees Celsius. `n` is the sensor index from 1 to 16, e.g. `temperature_1`, `temperature_2`.                                      |
| humidity\_internal           | Float           | Root           | No           | Relative humidity from the built-in hardware sensor, as a percentage.                                                                                                     |
| humidity\_n                  | Float           | Root           | No           | External relative humidity sensor reading as a percentage. `n` is the sensor index from 1 to 16, e.g. `humidity_1`.                                                       |
| fuel\_level\_n               | Float           | Root           | No           | Fuel level from a fuel sensor, in liters or as a percentage. `n` is the sensor index from 1 to 16, e.g. `fuel_level_1`.                                                   |
| fuel\_temperature\_n         | Float           | Root           | No           | Fuel temperature from a fuel sensor, in degrees Celsius. `n` is the sensor index from 1 to 16, e.g. `fuel_temperature_1`.                                                 |
| impulse\_counter\_n          | Integer         | Root           | No           | Impulse counter reading. `n` is the counter index from 1 to 16, e.g. `impulse_counter_1`.                                                                                 |
| **Identification data**      |                 |                |              |                                                                                                                                                                           |
| hardware\_key                | String          | Root           | No           | Driver or asset identifier, typically read via RFID, iButton, or similar method.                                                                                          |
| vin                          | String          | Root           | No           | Vehicle Identification Number (VIN).                                                                                                                                      |
| **Custom data**              |                 |                |              |                                                                                                                                                                           |
| custom\_*                    | Mixed           | Root           | No           | Any additional device-specific attribute. See [Custom attributes](#custom-attributes).                                                                                    |

## Custom attributes

The protocol allows you to extend messages with device-specific or application-specific data that has no pre-defined attribute. Custom attributes are added directly to the root of the message object.

Any field name not listed in the attributes table above is treated as a custom attribute and passed through to the platform unchanged. Common use cases include hardware-specific telemetry fields such as `avl_io_1`, `flex_id`, or `engine_rpm`.

```json
{
    "message_time": "2024-09-02T12:23:45Z",
    "device_id": "857378374927457",
    "version": "1.0",
    "location": {
        "latitude": 34.15929687705282,
        "longitude": -118.4614133834839
    },
    "custom_fuel": 86
}
```

## Message example

A complete telemetry message from a GPS tracker with GNSS positioning:

```json
{
    "message_time": "2024-09-02T10:03:43Z",
    "device_id": "857378374927457",
    "version": "1.0",
    "location": {
        "gnss_time": "2024-09-02T10:03:41Z",
        "fix_type": "HAS_FIX",
        "latitude": 56.348579,
        "longitude": 60.12344,
        "altitude": 271,
        "satellites": 8,
        "hdop": 0.41,
        "pdop": 2.0,
        "speed": 43,
        "heading": 77,
        "source_type": "GNSS"
    },
    "event_id": 406,
    "mobile_cells": [
        {
            "mcc": 250,
            "mnc": 0,
            "lac": 32445,
            "cell_id": 343455,
            "rssi": -54,
            "type": "LTE"
        }
    ],
    "wifi_points": [
        {
            "mac": "12:33:FF:45:04:33",
            "rssi": -54,
            "age": 4002,
            "channel": 11
        }
    ],
    "is_moving": true,
    "hardware_mileage": 7382.3,
    "battery_voltage": 4.12,
    "battery_level": 93,
    "board_voltage": 13.9,
    "input_status": 1,
    "output_status": 0,
    "hardware_key": "12FFABC54234",
    "temperature_internal": 12.3,
    "temperature_2": -13.7,
    "custom_fuel": 86
}
```

**Example — LBS-based position report** (no GNSS fix available):

```json
{
    "message_time": "2024-09-02T10:05:12Z",
    "device_id": "857378374927457",
    "version": "1.0",
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

Continue reading to learn about [Predefined event identifiers](predefined-event-identifiers.md) in Navixy Generic Protocol.
