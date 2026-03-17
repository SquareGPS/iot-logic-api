---
description: >-
  Complete reference for NGP message attributes: location, events, cell towers,
  Wi-Fi, sensors, I/O, and custom fields.
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

The table below lists all pre-defined attributes, organized by category. In addition to these, the protocol allows custom attributes. See [Custom attributes](message-structure-and-attributes.md#custom-attributes).

<table><thead><tr><th width="158">Attribute</th><th width="111">Type</th><th width="105">Object</th><th width="110">Required</th><th>Description</th></tr></thead><tbody><tr><td><strong>Basic attributes</strong></td><td></td><td></td><td></td><td></td></tr><tr><td>message_time</td><td>Timestamp</td><td>Root</td><td>Yes</td><td>Date and time the message was sent by the device (ISO 8601 UTC).</td></tr><tr><td>device_id</td><td>String</td><td>Root</td><td>Yes</td><td>Unique device identifier. Maximum 64 characters.</td></tr><tr><td>version</td><td>String</td><td>Root</td><td>No</td><td>NGP version of this message. Defaults to <code>1.0</code> if omitted.</td></tr><tr><td><strong>Location</strong></td><td></td><td></td><td></td><td></td></tr><tr><td>location</td><td>Object</td><td>Root</td><td>No</td><td>Device position. May be determined by GNSS (satellite), LBS (cell towers), or a third-party positioning service.</td></tr><tr><td>└─ latitude</td><td>Float</td><td>location</td><td>No</td><td>Latitude in decimal degrees (−90.0 to 90.0).</td></tr><tr><td>└─ longitude</td><td>Float</td><td>location</td><td>No</td><td>Longitude in decimal degrees (−180.0 to 180.0).</td></tr><tr><td>└─ altitude</td><td>Float</td><td>location</td><td>No</td><td>Altitude above sea level in meters (−1000 to 10000).</td></tr><tr><td>└─ gnss_time</td><td>Timestamp</td><td>location</td><td>No</td><td>Time when the position fix was acquired by the device.</td></tr><tr><td>└─ fix_type</td><td>String</td><td>location</td><td>No</td><td>Position fix type. Possible values: <code>HAS_FIX</code> (default), <code>NO_FIX</code>, <code>LAST_KNOWN_POSITION</code>, <code>FIX_2D</code>, <code>FIX_3D</code>.</td></tr><tr><td>└─ satellites</td><td>Integer</td><td>location</td><td>No</td><td>Number of GNSS satellites used for the fix (0–64).</td></tr><tr><td>└─ hdop</td><td>Float</td><td>location</td><td>No</td><td>Horizontal dilution of precision. Lower is more accurate.</td></tr><tr><td>└─ vdop</td><td>Float</td><td>location</td><td>No</td><td>Vertical dilution of precision. Lower is more accurate.</td></tr><tr><td>└─ pdop</td><td>Float</td><td>location</td><td>No</td><td>3D position dilution of precision, combining horizontal and vertical.</td></tr><tr><td>└─ speed</td><td>Float</td><td>location</td><td>No</td><td>Device speed in km/h (positive values only).</td></tr><tr><td>└─ heading</td><td>Integer</td><td>location</td><td>No</td><td>Direction of movement in degrees, clockwise from north (1–360).</td></tr><tr><td><strong>Event information</strong></td><td></td><td></td><td></td><td></td></tr><tr><td>event_id</td><td>Integer</td><td>Root</td><td>No</td><td>Platform event identifier. See <a href="predefined-event-identifiers.md">Predefined event identifiers</a> for standard values. Custom events start at 10,000.</td></tr><tr><td><strong>Mobile cells</strong></td><td></td><td></td><td></td><td></td></tr><tr><td>mobile_cells</td><td>Array [Object]</td><td>Root</td><td>No</td><td>List of visible cell towers. Used to provide data for network-based positioning (LBS) when GNSS is unavailable.</td></tr><tr><td>└─ mcc</td><td>Integer</td><td>mobile_cells</td><td>Yes</td><td>Mobile Country Code. Identifies the country of the mobile network.</td></tr><tr><td>└─ mnc</td><td>Integer</td><td>mobile_cells</td><td>Yes</td><td>Mobile Network Code. Identifies the mobile operator within the country.</td></tr><tr><td>└─ lac</td><td>Integer</td><td>mobile_cells</td><td>Yes</td><td>Location Area Code. Identifies the area within the mobile network.</td></tr><tr><td>└─ cell_id</td><td>Integer</td><td>mobile_cells</td><td>Yes</td><td>Unique identifier of the cell tower.</td></tr><tr><td>└─ rssi</td><td>Integer</td><td>mobile_cells</td><td>No</td><td>Signal strength from the cell tower in dBm (negative values).</td></tr><tr><td>└─ type</td><td>String</td><td>mobile_cells</td><td>No</td><td>Radio access technology. Possible values: <code>GSM</code> (default), <code>CDMA</code>, <code>WCDMA</code>, <code>LTE</code>, <code>NR</code>.</td></tr><tr><td><strong>Wi-Fi points</strong></td><td></td><td></td><td></td><td></td></tr><tr><td>wifi_points</td><td>Array [Object]</td><td>Root</td><td>No</td><td>List of visible Wi-Fi access points. Used alongside <code>mobile_cells</code> to improve network-based positioning accuracy.</td></tr><tr><td>└─ mac</td><td>String</td><td>wifi_points</td><td>Yes</td><td>MAC address of the access point. Colon-delimited bytes, e.g. <code>12:33:FF:45:04:33</code>.</td></tr><tr><td>└─ rssi</td><td>Integer</td><td>wifi_points</td><td>Yes</td><td>Signal strength in dBm (negative values).</td></tr><tr><td>└─ age</td><td>Integer</td><td>wifi_points</td><td>No</td><td>Milliseconds since this access point was last detected.</td></tr><tr><td>└─ channel</td><td>Integer</td><td>wifi_points</td><td>No</td><td>Radio channel number used by the access point.</td></tr><tr><td><strong>Device motion and status</strong></td><td></td><td></td><td></td><td></td></tr><tr><td>is_moving</td><td>Boolean</td><td>Root</td><td>No</td><td><code>true</code> if the device is currently moving, <code>false</code> if stationary.</td></tr><tr><td>hardware_mileage</td><td>Float</td><td>Root</td><td>No</td><td>Cumulative mileage counted by the device hardware, in kilometers.</td></tr><tr><td>battery_voltage</td><td>Float</td><td>Root</td><td>No</td><td>Built-in battery voltage in volts.</td></tr><tr><td>battery_level</td><td>Integer</td><td>Root</td><td>No</td><td>Built-in battery charge level as a percentage (0–100).</td></tr><tr><td>board_voltage</td><td>Float</td><td>Root</td><td>No</td><td>External power supply voltage in volts.</td></tr><tr><td><strong>Input/Output status</strong></td><td></td><td></td><td></td><td></td></tr><tr><td>input_status</td><td>Integer</td><td>Root</td><td>No</td><td>State of discrete inputs as a bitmask. Bit 0 = input 1, bit 1 = input 2, and so on. A set bit means the input is active.</td></tr><tr><td>output_status</td><td>Integer</td><td>Root</td><td>No</td><td>State of outputs as a bitmask. Bit 0 = output 1, bit 1 = output 2, and so on. A set bit means the output is active.</td></tr><tr><td><strong>Sensor data</strong></td><td></td><td></td><td></td><td></td></tr><tr><td>analog_n</td><td>Float</td><td>Root</td><td>No</td><td>Analog input voltage in volts. <code>n</code> is the sensor index from 1 to 16, e.g. <code>analog_1</code>, <code>analog_2</code>.</td></tr><tr><td>temperature_internal</td><td>Float</td><td>Root</td><td>No</td><td>Temperature from the built-in hardware sensor, in degrees Celsius.</td></tr><tr><td>temperature_n</td><td>Float</td><td>Root</td><td>No</td><td>External temperature sensor reading in degrees Celsius. <code>n</code> is the sensor index from 1 to 16, e.g. <code>temperature_1</code>, <code>temperature_2</code>.</td></tr><tr><td>humidity_internal</td><td>Float</td><td>Root</td><td>No</td><td>Relative humidity from the built-in hardware sensor, as a percentage.</td></tr><tr><td>humidity_n</td><td>Float</td><td>Root</td><td>No</td><td>External relative humidity sensor reading as a percentage. <code>n</code> is the sensor index from 1 to 16, e.g. <code>humidity_1</code>.</td></tr><tr><td>fuel_level_n</td><td>Float</td><td>Root</td><td>No</td><td>Fuel level from a fuel sensor, in liters or as a percentage. <code>n</code> is the sensor index from 1 to 16, e.g. <code>fuel_level_1</code>.</td></tr><tr><td>fuel_temperature_n</td><td>Float</td><td>Root</td><td>No</td><td>Fuel temperature from a fuel sensor, in degrees Celsius. <code>n</code> is the sensor index from 1 to 16, e.g. <code>fuel_temperature_1</code>.</td></tr><tr><td>impulse_counter_n</td><td>Integer</td><td>Root</td><td>No</td><td>Impulse counter reading. <code>n</code> is the counter index from 1 to 16, e.g. <code>impulse_counter_1</code>.</td></tr><tr><td><strong>Identification data</strong></td><td></td><td></td><td></td><td></td></tr><tr><td>hardware_key</td><td>String</td><td>Root</td><td>No</td><td>Driver or asset identifier, typically read via RFID, iButton, or similar method.</td></tr><tr><td>vin</td><td>String</td><td>Root</td><td>No</td><td>Vehicle Identification Number (VIN).</td></tr><tr><td><strong>Custom data</strong></td><td></td><td></td><td></td><td></td></tr><tr><td>custom_*</td><td>Mixed</td><td>Root</td><td>No</td><td>Any additional device-specific attribute. See <a href="message-structure-and-attributes.md#custom-attributes">Custom attributes</a>.</td></tr></tbody></table>

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

**Example: LBS-based position report** (no GNSS fix available):

```json
{
    "message_time": "2024-09-02T10:05:12Z",
    "device_id": "857378374927457",
    "version": "1.0",
    "location": {
        "latitude": 56.352100,
        "longitude": 60.128900
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

{% hint style="info" %}
To explicitly identify the positioning source (GNSS, LBS, or ATLAS) and include a location accuracy value, use [version 1.2](../navixy-generic-protocol-12.md), which adds `source_type` and `precision` to the `location` object.
{% endhint %}

Continue reading to learn about [Predefined event identifiers](predefined-event-identifiers.md) in Navixy Generic Protocol.
