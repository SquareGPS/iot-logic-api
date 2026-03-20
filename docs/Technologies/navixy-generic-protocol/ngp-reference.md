---
description: >-
  Complete NGP reference: transport connection parameters, data types, message
  structure and attributes, and predefined event identifiers.
---

# NGP reference

This page is the complete reference for Navixy Generic Protocol. It covers transport connection parameters for HTTP/HTTPS and MQTT, data type definitions, the full message attribute table with availability tags, and predefined event identifiers.

{% hint style="info" %}
Fields with no availability tag work in all versions. Fields with restricted availability are marked:

- `1.2+` — requires `"version": "1.2"` in the message
- `on demand` — requires a separate arrangement with Navixy; not available for standard integrations
{% endhint %}

## Transport layer

NGP supports both **HTTP/HTTPS** and **MQTT** as transport options. Choose based on your device capabilities and infrastructure requirements.

### HTTP/HTTPS

NGP supports **HTTP/HTTPS versions 1.1 and 2.0**. This is the simplest option for devices that already support HTTP.

**Request format:**

| Parameter     | Value              |
| ------------- | ------------------ |
| Method        | `POST`             |
| Content-Type  | `application/json` |
| Body encoding | UTF-8              |
| Body          | Single JSON object |

**Regional endpoints:**

| Region | Endpoint                             |
| ------ | ------------------------------------ |
| EU     | `http://tracker.navixy.com:47642`    |
| US     | `http://tracker.us.navixy.com:47642` |

**Response codes:**

| Code  | Meaning                                                                           |
| ----- | --------------------------------------------------------------------------------- |
| `200` | Message received successfully.                                                    |
| `400` | Invalid request. Malformed JSON or field values are outside allowed ranges.       |
| `403` | Unknown device identifier. Verify that `device_id` is registered on the platform. |
| `500` | Unexpected server error. Contact the platform's technical support.                |

**Example: sending a message via curl:**

```bash
curl --location 'tracker.navixy.com:47642' \
--header 'Content-Type: application/json' \
--data '{
    "message_time": "2024-10-10T06:00:11Z",
    "device_id": "1112312212",
    "location": {
        "latitude": 34.15929687705282,
        "longitude": -118.4614133834839,
        "satellites": 3
    },
    "battery_level": 68
}'
```

### MQTT

NGP uses MQTT as a lightweight, reliable transport over TCP.

**Supported MQTT versions:** 5.0 and 3.1.1

**Quality of Service levels:**

| QoS | Behaviour                                                            |
| --- | -------------------------------------------------------------------- |
| 0   | At most once. Suitable where occasional message loss is acceptable.  |
| 1   | At least once. Use when reliable delivery is required.               |

All message bodies must be UTF-8 encoded JSON containing a single JSON object per message. Responses to messages are not supported. The platform strictly validates incoming messages and silently discards those with invalid JSON or out-of-range attribute values.

**Connection parameters:**

| Parameter | Value                                                                   |
| --------- | ----------------------------------------------------------------------- |
| Host (EU) | `mqtt.eu.navixy.com`                                                    |
| Host (US) | `mqtt.us.navixy.com`                                                    |
| Port      | `1883` (plain TCP) / `8883` (TLS)                                       |
| Username  | `ngp_device`                                                            |
| Password  | Device password configured in the Navixy platform                       |
| Topic     | `ngp/{device_id}` (replace `{device_id}` with your device's identifier) |

**Example: sending a message via Mosquitto client:**

```bash
mosquitto_pub \
  -h mqtt.eu.navixy.com \
  -p 1883 \
  -u ngp_device \
  -P <your_device_password> \
  -t "ngp/1112312212" \
  -m '{
    "message_time": "2024-10-10T06:00:11Z",
    "device_id": "1112312212",
    "location": {
        "latitude": 34.15929687705282,
        "longitude": -118.4614133834839,
        "satellites": 3
    },
    "battery_level": 68
}'
```

## Data types and encoding standards

### Data types

| **Type**  | **JSON** | **Description**                                    | **Examples**                                               | **Limitations**                                        |
| --------- | -------- | -------------------------------------------------- | ---------------------------------------------------------- | ------------------------------------------------------ |
| Integer   | Number   | Whole numeric values, no decimals                  | Bitmasks, counters, impulse counts, passenger counts, RPM  | Signed or unsigned, 1–8 bytes                          |
| Float     | Number   | Numeric values with decimal precision              | Coordinates, speed, altitude, mileage, voltage             | IEEE 754 signed float, up to 8 bytes                   |
| String    | String   | UTF-8 encoded text                                 | Driver name, registration plate, driver ID                 | Up to 10 KB                                            |
| Boolean   | Boolean  | `true` or `false`                                  | Ignition state, door state, presence of movement           | `true` or `false` only                                 |
| Timestamp | String   | ISO 8601 date-time in UTC                          | Message time, GNSS fix time                                | Must be valid ISO 8601 UTC                             |
| Blob      | String   | Binary data, Base64-encoded                        | Photos, raw sensor data, BLE payloads, audio               | Up to 1 MB encoded                                     |
| Mixed     | Any      | Value of any JSON type                             | Custom attributes where type varies by attribute           | Follows the type constraints of the specific attribute |
| Array     | Array    | Ordered list of objects of the same structure      | `mobile_cells`, `wifi_points`                              | No size limit                                          |
| Object    | Object   | Named set of attributes grouped under a single key | `location`, individual mobile cell, individual Wi-Fi point | No size limit                                          |

### Timestamps

All timestamps must use **ISO 8601 UTC** format.

```
"message_time": "2024-09-02T23:59:59Z"
```

The trailing `Z` indicates UTC. Timezone offsets are not supported. Always convert to UTC before sending.

### Binary data

For raw payloads such as sensor data, tachograph logs, images, or audio, binary content must be **Base64-encoded** and sent as a string value.

```json
{
  "my_sensor_data": "SGVsbG8gd29ybGQh",
  "tachograph_log": "U29tZSB0YWNoZW9nIGxvZw==",
  "photo": "/9j/4AAQSkZJRgABAQEAYABgAAD...",
  "audio": "UklGRjIAAABXRUJQVlA4WAoAAAAQAAAA..."
}
```

{% hint style="warning" %}
NGP is not optimized for large binary payloads. The 1 MB limit per encoded blob applies per attribute. Avoid sending multiple large blobs in a single message.
{% endhint %}

## Message structure and attributes

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

### Attributes

The table below lists all pre-defined attributes, organized by category. In addition to these, the protocol allows custom attributes. See [Custom attributes](#custom-attributes).

<table><thead><tr><th width="158">Attribute</th><th width="111">Type</th><th width="105">Object</th><th width="110">Required</th><th>Description</th><th>Availability</th></tr></thead><tbody><tr><td><strong>Basic attributes</strong></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>message_time</td><td>Timestamp</td><td>Root</td><td>Yes</td><td>Date and time the message was sent by the device (ISO 8601 UTC).</td><td></td></tr><tr><td>device_id</td><td>String</td><td>Root</td><td>Yes</td><td>Unique device identifier. Maximum 64 characters.</td><td></td></tr><tr><td>version</td><td>String</td><td>Root</td><td>No</td><td>NGP version of this message. Defaults to <code>1.0</code> if omitted.</td><td></td></tr><tr><td><strong>Location</strong></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>location</td><td>Object</td><td>Root</td><td>No</td><td>Device position. May be determined by GNSS (satellite), LBS (cell towers), or a third-party positioning service.</td><td></td></tr><tr><td>└─ latitude</td><td>Float</td><td>location</td><td>No</td><td>Latitude in decimal degrees (−90.0 to 90.0).</td><td></td></tr><tr><td>└─ longitude</td><td>Float</td><td>location</td><td>No</td><td>Longitude in decimal degrees (−180.0 to 180.0).</td><td></td></tr><tr><td>└─ altitude</td><td>Float</td><td>location</td><td>No</td><td>Altitude above sea level in meters (−1000 to 10000).</td><td></td></tr><tr><td>└─ gnss_time</td><td>Timestamp</td><td>location</td><td>No</td><td>Time when the position fix was acquired by the device.</td><td></td></tr><tr><td>└─ fix_type</td><td>String</td><td>location</td><td>No</td><td>Position fix type. Possible values: <code>HAS_FIX</code> (default), <code>NO_FIX</code>, <code>LAST_KNOWN_POSITION</code>, <code>FIX_2D</code>, <code>FIX_3D</code>.</td><td></td></tr><tr><td>└─ satellites</td><td>Integer</td><td>location</td><td>No</td><td>Number of GNSS satellites used for the fix (0–64).</td><td></td></tr><tr><td>└─ hdop</td><td>Float</td><td>location</td><td>No</td><td>Horizontal dilution of precision. Lower is more accurate.</td><td></td></tr><tr><td>└─ vdop</td><td>Float</td><td>location</td><td>No</td><td>Vertical dilution of precision. Lower is more accurate.</td><td></td></tr><tr><td>└─ pdop</td><td>Float</td><td>location</td><td>No</td><td>3D position dilution of precision, combining horizontal and vertical.</td><td></td></tr><tr><td>└─ speed</td><td>Float</td><td>location</td><td>No</td><td>Device speed in km/h (positive values only).</td><td></td></tr><tr><td>└─ heading</td><td>Integer</td><td>location</td><td>No</td><td>Direction of movement in degrees, clockwise from north (1–360).</td><td></td></tr><tr><td>└─ source_type</td><td>String</td><td>location</td><td>No</td><td>Positioning source. Possible values: <code>GNSS</code> (satellite), <code>LBS</code> (cell tower-based), <code>ATLAS</code> (third-party positioning service). Defaults to <code>GNSS</code> when omitted.</td><td><code>1.2+</code></td></tr><tr><td>└─ precision</td><td>Integer</td><td>location</td><td>No</td><td>Location accuracy in meters. Recommended for LBS and ATLAS positions.</td><td><code>1.2+</code></td></tr><tr><td><strong>Event information</strong></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>event_id</td><td>Integer</td><td>Root</td><td>No</td><td>Platform event identifier. See <a href="#predefined-event-identifiers">Predefined event identifiers</a> for standard values. Custom events start at 10,000.</td><td></td></tr><tr><td><strong>Mobile cells</strong></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>mobile_cells</td><td>Array [Object]</td><td>Root</td><td>No</td><td>List of visible cell towers. Used to provide data for network-based positioning (LBS) when GNSS is unavailable.</td><td></td></tr><tr><td>└─ mcc</td><td>Integer</td><td>mobile_cells</td><td>Yes</td><td>Mobile Country Code. Identifies the country of the mobile network.</td><td></td></tr><tr><td>└─ mnc</td><td>Integer</td><td>mobile_cells</td><td>Yes</td><td>Mobile Network Code. Identifies the mobile operator within the country.</td><td></td></tr><tr><td>└─ lac</td><td>Integer</td><td>mobile_cells</td><td>Yes</td><td>Location Area Code. Identifies the area within the mobile network.</td><td></td></tr><tr><td>└─ cell_id</td><td>Integer</td><td>mobile_cells</td><td>Yes</td><td>Unique identifier of the cell tower.</td><td></td></tr><tr><td>└─ rssi</td><td>Integer</td><td>mobile_cells</td><td>No</td><td>Signal strength from the cell tower in dBm (negative values).</td><td></td></tr><tr><td>└─ type</td><td>String</td><td>mobile_cells</td><td>No</td><td>Radio access technology. Possible values: <code>GSM</code> (default), <code>CDMA</code>, <code>WCDMA</code>, <code>LTE</code>, <code>NR</code>.</td><td></td></tr><tr><td><strong>Wi-Fi points</strong></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>wifi_points</td><td>Array [Object]</td><td>Root</td><td>No</td><td>List of visible Wi-Fi access points. Used alongside <code>mobile_cells</code> to improve network-based positioning accuracy.</td><td></td></tr><tr><td>└─ mac</td><td>String</td><td>wifi_points</td><td>Yes</td><td>MAC address of the access point. Colon-delimited bytes, e.g. <code>12:33:FF:45:04:33</code>.</td><td></td></tr><tr><td>└─ rssi</td><td>Integer</td><td>wifi_points</td><td>Yes</td><td>Signal strength in dBm (negative values).</td><td></td></tr><tr><td>└─ age</td><td>Integer</td><td>wifi_points</td><td>No</td><td>Milliseconds since this access point was last detected.</td><td></td></tr><tr><td>└─ channel</td><td>Integer</td><td>wifi_points</td><td>No</td><td>Radio channel number used by the access point.</td><td></td></tr><tr><td><strong>Device motion and status</strong></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>is_moving</td><td>Boolean</td><td>Root</td><td>No</td><td><code>true</code> if the device is currently moving, <code>false</code> if stationary.</td><td></td></tr><tr><td>hardware_mileage</td><td>Float</td><td>Root</td><td>No</td><td>Cumulative mileage counted by the device hardware, in kilometers.</td><td></td></tr><tr><td>battery_voltage</td><td>Float</td><td>Root</td><td>No</td><td>Built-in battery voltage in volts.</td><td></td></tr><tr><td>battery_level</td><td>Integer</td><td>Root</td><td>No</td><td>Built-in battery charge level as a percentage (0–100).</td><td></td></tr><tr><td>board_voltage</td><td>Float</td><td>Root</td><td>No</td><td>External power supply voltage in volts.</td><td></td></tr><tr><td><strong>Input/Output status</strong></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>input_status</td><td>Integer</td><td>Root</td><td>No</td><td>State of discrete inputs as a bitmask. Bit 0 = input 1, bit 1 = input 2, and so on. A set bit means the input is active.</td><td></td></tr><tr><td>output_status</td><td>Integer</td><td>Root</td><td>No</td><td>State of outputs as a bitmask. Bit 0 = output 1, bit 1 = output 2, and so on. A set bit means the output is active.</td><td></td></tr><tr><td><strong>Sensor data</strong></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>analog_n</td><td>Float</td><td>Root</td><td>No</td><td>Analog input voltage in volts. <code>n</code> is the sensor index from 1 to 16, e.g. <code>analog_1</code>, <code>analog_2</code>.</td><td></td></tr><tr><td>temperature_internal</td><td>Float</td><td>Root</td><td>No</td><td>Temperature from the built-in hardware sensor, in degrees Celsius.</td><td></td></tr><tr><td>temperature_n</td><td>Float</td><td>Root</td><td>No</td><td>External temperature sensor reading in degrees Celsius. <code>n</code> is the sensor index from 1 to 16, e.g. <code>temperature_1</code>, <code>temperature_2</code>.</td><td></td></tr><tr><td>humidity_internal</td><td>Float</td><td>Root</td><td>No</td><td>Relative humidity from the built-in hardware sensor, as a percentage.</td><td></td></tr><tr><td>humidity_n</td><td>Float</td><td>Root</td><td>No</td><td>External relative humidity sensor reading as a percentage. <code>n</code> is the sensor index from 1 to 16, e.g. <code>humidity_1</code>.</td><td></td></tr><tr><td>fuel_level_n</td><td>Float</td><td>Root</td><td>No</td><td>Fuel level from a fuel sensor, in liters or as a percentage. <code>n</code> is the sensor index from 1 to 16, e.g. <code>fuel_level_1</code>.</td><td></td></tr><tr><td>fuel_temperature_n</td><td>Float</td><td>Root</td><td>No</td><td>Fuel temperature from a fuel sensor, in degrees Celsius. <code>n</code> is the sensor index from 1 to 16, e.g. <code>fuel_temperature_1</code>.</td><td></td></tr><tr><td>impulse_counter_n</td><td>Integer</td><td>Root</td><td>No</td><td>Impulse counter reading. <code>n</code> is the counter index from 1 to 16, e.g. <code>impulse_counter_1</code>.</td><td></td></tr><tr><td><strong>Identification data</strong></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>hardware_key</td><td>String</td><td>Root</td><td>No</td><td>Driver or asset identifier, typically read via RFID, iButton, or similar method.</td><td></td></tr><tr><td>vin</td><td>String</td><td>Root</td><td>No</td><td>Vehicle Identification Number (VIN).</td><td></td></tr><tr><td><strong>Custom data</strong></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>custom_*</td><td>Mixed</td><td>Root</td><td>No</td><td>Any additional device-specific attribute. See <a href="#custom-attributes">Custom attributes</a>.</td><td></td></tr><tr><td>custom_attributes</td><td>Array [Object]</td><td>Root</td><td>No</td><td>Structured custom attribute array with metadata. Requires <code>"version": "1.1a"</code> and a separate arrangement with Navixy.</td><td><code>on demand</code></td></tr><tr><td>└─ type</td><td>String</td><td>custom_attributes</td><td>Yes</td><td>Attribute name.</td><td><code>on demand</code></td></tr><tr><td>└─ id</td><td>Integer</td><td>custom_attributes</td><td>No</td><td>Attribute order number.</td><td><code>on demand</code></td></tr><tr><td>└─ value</td><td>Mixed</td><td>custom_attributes</td><td>Yes</td><td>Attribute value. Any JSON type.</td><td><code>on demand</code></td></tr><tr><td>└─ units</td><td>String</td><td>custom_attributes</td><td>No</td><td>Unit of measurement, e.g. <code>rpm</code>, <code>percent</code>.</td><td><code>on demand</code></td></tr></tbody></table>

### Location source and accuracy

`source_type` identifies where the position coordinates came from. When omitted, the platform treats the location as GNSS by default. Declaring the source explicitly lets the platform apply the correct processing logic — for example, skipping satellite-count validation for LBS positions.

`precision` reports the estimated accuracy of the resolved coordinates in meters. It is optional but recommended for LBS and ATLAS positions, where accuracy can vary significantly. The platform can use this value to determine whether the accuracy is sufficient for a given use case.

Both fields require `"version": "1.2"` in the message.

{% code title="Example: LBS-based position report" %}
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
{% endcode %}

The `precision` value of `800` indicates the resolved coordinates are accurate within approximately 800 meters.

### Message example

A complete telemetry message from a GPS device with GNSS positioning:

```json
{
    "message_time": "2024-09-02T10:03:43Z",
    "device_id": "857378374927457",
    "version": "1.2",
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

### Custom attributes

The protocol allows you to extend messages with device-specific or application-specific data that has no pre-defined attribute. Custom attributes are added directly to the root of the message object.

Any field name not listed in the attributes table above is treated as a custom attribute and passed through to the platform unchanged. Common use cases include hardware-specific telemetry fields such as `avl_io_1`, `flex_id`, or `engine_rpm`. This format requires no version declaration and covers most integration needs.

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

#### Structured custom attributes

For integrations that need typed metadata alongside sensor values, NGP supports an alternative format: the `custom_attributes` array. Each entry carries a `type` (attribute name), `value`, and optional `id` (ordering) and `units` fields. This is useful when units of measurement, attribute ordering, or typed metadata are required by the receiving system.

For most integrations, the simple `custom_*` format above is sufficient and preferable. Use `custom_attributes` only when the structured metadata is a specific requirement of your integration.

Both formats can coexist in the same message. `custom_attributes` requires `"version": "1.1a"` and a separate arrangement with Navixy — it is not available for standard integrations.

{% code title="Example: simple and structured custom attributes in the same message" %}
```json
{
    "message_time": "2024-09-02T12:23:45Z",
    "device_id": "857378374927457",
    "version": "1.1a",
    "location": {
        "latitude": 34.15929687705282,
        "longitude": -118.4614133834839
    },
    "custom_fuel": 86,
    "custom_attributes": [
        {
            "type": "engine_rpm",
            "id": 1,
            "value": 2100,
            "units": "rpm"
        },
        {
            "type": "vehicle_load",
            "id": 2,
            "value": 75,
            "units": "percent"
        }
    ]
}
```
{% endcode %}

## Predefined event identifiers

NGP includes pre-defined event identifiers (`event_id`) for the most common device events. Use these standard IDs wherever possible. For device-specific events not covered here, use custom IDs starting from **10,000**.

### Power

Range: 1–100.

| **Event ID** | **Description**                             |
| ------------ | ------------------------------------------- |
| 1            | Low battery                                 |
| 2            | Power lost or external power cut            |
| 3            | Power On button pressed                     |
| 4            | Power recovered or external power connected |
| 5            | OBD unplugged from the car's connector      |
| 6            | OBD plugged in                              |
| 7            | Device backup battery low                   |
| 8            | Device wakes up from sleep mode             |
| 9            | Sleep mode start                            |
| 10           | Timer wakeup                                |
| 11           | Motion wakeup                               |
| 12           | External power wakeup                       |
| 13           | Power Off button pressed                    |
| 14           | Device power off                            |
| 15           | Device power on                             |

### Security

Range: 101–200.

| **Event ID** | **Description**                                                      |
| ------------ | -------------------------------------------------------------------- |
| 101          | Unauthorized movement event determined by the device (tow detection) |
| 102          | Unauthorized movement end                                            |
| 103          | Device detached from the tracked object                              |
| 104          | Car alarm                                                            |
| 105          | Device case closed                                                   |
| 106          | Device case opened                                                   |
| 107          | Unplug from the tracked object                                       |
| 108          | Device attached to the tracked object                                |
| 109          | Door alarm                                                           |
| 110          | Device lock closed                                                   |
| 111          | Device lock opened                                                   |
| 112          | Vibration end                                                        |
| 113          | Vibration start                                                      |
| 114          | Strap bolt inserted                                                  |
| 115          | Strap bolt cut                                                       |
| 116          | GPS jamming detected                                                 |
| 117          | GSM signal jamming alarm                                             |
| 118          | Bracelet opened                                                      |
| 119          | Bracelet closed                                                      |
| 120          | G-sensor alert                                                       |
| 121          | GPS jamming end                                                      |

### Safety

Range: 201–300.

| **Event ID** | **Description**                                          |
| ------------ | -------------------------------------------------------- |
| 201          | Emergency contact number called                          |
| 202          | SOS button pressed                                       |
| 203          | Cruise control switched on                               |
| 204          | Cruise control switched off                              |
| 205          | DMS: driver not identified                               |
| 206          | DMS: driver identified                                   |
| 207          | ADAS: frequent lane change                               |
| 208          | DMS: device cannot detect human face                     |
| 209          | Seat belt unbuckled                                      |
| 210          | DMS: driver is drinking                                  |
| 211          | DMS: driver eyes closed                                  |
| 212          | DMS: new driver detection reported                       |
| 213          | DMS: driver enters cabin                                 |
| 214          | DMS: driver absence start                                |
| 215          | DMS: driver stopped smoking (driver distraction)         |
| 216          | DMS: driver started smoking (driver distraction)         |
| 217          | DMS: driver finished using phone (driver distraction)    |
| 218          | DMS: driver started using phone (driver distraction)     |
| 219          | DMS: yawning detected (fatigue driving)                  |
| 220          | DMS: driver stopped distraction                          |
| 221          | DMS: driver started distraction                          |
| 222          | DMS: driver stopped drowsiness (fatigue driving)         |
| 223          | DMS: driver started drowsiness (fatigue driving)         |
| 224          | Overspeeding                                             |
| 225          | Unexpected movement start                                |
| 226          | Unexpected movement end                                  |
| 227          | ADAS: pedestrian in danger zone                          |
| 228          | ADAS: traffic sign recognition                           |
| 229          | ADAS: pedestrian collision warning                       |
| 230          | Fatigue driving                                          |
| 231          | ADAS: headway warning                                    |
| 232          | ADAS: right lane departure                               |
| 233          | ADAS: left lane departure                                |
| 234          | ADAS: lane departure                                     |
| 235          | ADAS: forward collision warning                          |
| 236          | Harsh driving: quick lane change                         |
| 237          | Harsh driving: acceleration and turn                     |
| 238          | Harsh driving: braking and turn                          |
| 239          | Harsh driving: turn                                      |
| 240          | Harsh driving: acceleration                              |
| 241          | Harsh driving: braking                                   |
| 242          | Crash alarm                                              |
| 243          | Harsh driving                                            |
| 244          | Call button pressed                                      |
| 245          | Driver distraction: texting while driving                |
| 246          | Driver distraction: not watching the road ("lizard eye") |
| 247          | Lane drift detected                                      |
| 248          | Traffic STOP sign violation                              |
| 249          | Speed limit exceeded                                     |
| 250          | Traffic light violation                                  |
| 251          | Tailgating: unsafe following distance                    |

### Vehicle efficiency

Range: 301–400.

| **Event ID** | **Description**    |
| ------------ | ------------------ |
| 301          | Idle end           |
| 302          | Idle start         |
| 303          | Check engine light |

### Track information

Range: 401–500.

| **Event ID** | **Description**                     |
| ------------ | ----------------------------------- |
| 401          | Track point (no specific event)     |
| 402          | GSM LBS point report                |
| 403          | Track point by time interval        |
| 404          | Track point by distance             |
| 405          | Track point by heading angle change |
| 406          | Movement start                      |
| 407          | Movement end                        |
| 408          | Non-track message                   |
| 409          | Tracker entered auto geofence       |
| 410          | Tracker exited auto geofence        |

### Inputs

Range: 501–550.

| **Event ID** | **Description**       |
| ------------ | --------------------- |
| 501          | Input 1 state changed |
| 502          | Input 2 state changed |
| 503          | Input 3 state changed |
| 504          | Input 4 state changed |
| 505          | Input 5 state changed |
| 506          | Input 6 state changed |
| 507          | Input 7 state changed |
| 508          | Input 8 state changed |

### Outputs

Range: 551–600.

| **Event ID** | **Description**        |
| ------------ | ---------------------- |
| 551          | Output 1 state changed |
| 552          | Output 2 state changed |
| 553          | Output 3 state changed |
| 554          | Output 4 state changed |
| 555          | Output 5 state changed |
| 556          | Output 6 state changed |
| 557          | Output 7 state changed |
| 558          | Output 8 state changed |

### Peripherals and other

Range: 601–700.

| **Event ID** | **Description**                |
| ------------ | ------------------------------ |
| 601          | Antenna disconnected           |
| 602          | Accessory disconnected         |
| 603          | Accessory connected            |
| 604          | Ignition off                   |
| 605          | Ignition on                    |
| 606          | Light sensor determined dark   |
| 607          | Light sensor determined bright |
| 608          | GPS signal recovered           |
| 609          | GPS signal lost                |

### Custom event identifiers

For device-specific or application-specific events not covered by the ranges above, use identifiers starting from **10,000**. Values below 10,000 are reserved for future NGP standard events.
