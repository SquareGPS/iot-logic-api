# Message structure and attributes

Messages are processed sequentially and follow a straightforward **JSON** structure. Each message includes two **mandatory** attributes: `device_id` and `message_time`.

Minimum possible message:

```
{
   "message_time": "...",
   "device_id": "..."
}
```

This example demonstrates the basic structure of a message with only the mandatory attributes. You can then add optional attributes as needed based on the specific protocol and device type. Continue reading to learn more about attributes supported by the protocol.

### Attributes

The Navixy Generic Protocol offers a set of pre-defined attributes that devices can include in their messages. These attributes cover a wide range of functionalities, forming the core vocabulary of the protocol for transmitting data such as basic telemetry and advanced sensor readings. Below, you will find detailed specifications for each of the pre-defined attributes, organized by functional categories.

In addition to the pre-defined attributes, the protocol allows defining custom attributes to handle specific cases. See [Custom attributes](message-structure-and-attributes.md#custom-attributes) for details on how to define and transmit such attributes.

| **Attribute**                | **Type**        | **Object**    | **Required for object** | **Description**                                                                                                                                                                                                 |
| ---------------------------- | --------------- | ------------- | ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Basic attributes**         |                 |               |                         |                                                                                                                                                                                                                 |
| message\_time                | Timestamp       | Root          | Yes                     | Date and time the message was sent by a device.                                                                                                                                                                 |
| device\_id                   | String          | Root          | Yes                     | A unique device identifier. Max size 64 characters.                                                                                                                                                             |
| version                      | String          | Root          | No                      | Version of this protocol (JSON structure). If the version attribute is not specified, v1.0 will be used by default.                                                                                             |
| **Location information**     |                 |               |                         |                                                                                                                                                                                                                 |
| location                     | Object          | Root          | No                      | Contains details about the device's GPS location.                                                                                                                                                               |
| └─ gnss\_time                | String          | location      | No                      | Time when coordinates were registered by the device.                                                                                                                                                            |
| └─ latitude                  | Float           | location      | No                      | Latitude in degrees (-90.0 to 90.0).                                                                                                                                                                            |
| └─ longitude                 | Float           | location      | No                      | Longitude in degrees (-180.0 to 180.0).                                                                                                                                                                         |
| └─ altitude                  | Float           | location      | No                      | Altitude above sea level in meters (-1000 to 10000).                                                                                                                                                            |
| └─ fix\_type                 | String          | location      | No                      | <p>Location fixation type.<br><br>Possible values are:<br><br>- HAS_FIX<br>- NO_FIX<br>- LAST_KNOWN_POSITION<br>- FIX_2D<br>- FIX_3D<br><br>Default is HAS_FIX.</p>                                             |
| └─ satellites                | Integer         | location      | No                      | Number of satellites involved in positioning (0 to 64).                                                                                                                                                         |
| └─ hdop                      | Float           | location      | No                      | Horizontal dilution of precision, a measure of GPS accuracy.                                                                                                                                                    |
| └─ vdop                      | Float           | location      | No                      | Vertical dilution of precision, a measure of altitude accuracy in GPS.                                                                                                                                          |
| └─ pdop                      | Float           | location      | No                      | 3D position dilution of precision, combining horizontal and vertical accuracy.                                                                                                                                  |
| └─ speed                     | Float           | location      | No                      | Device's speed in km/h (positive value).                                                                                                                                                                        |
| └─ heading                   | Integer         | location      | No                      | Heading in degrees, azimuth, direction of movement (1 to 360).                                                                                                                                                  |
| **Event information**        |                 |               |                         |                                                                                                                                                                                                                 |
| event\_id                    | Integer         | Root          | No                      | Platform event identifier. For a full list of possible values, see [Appendix 1](https://docs.navixy.com/iot-logic/navixy-generic-protocol-v-1-0#NavixyGenericProtocol1.0-Appendix1.Predefinedeventidentifiers). |
| **Mobile cells**             |                 |               |                         |                                                                                                                                                                                                                 |
| mobile\_cells                | Array \[Object] | Root          | No                      | List of visible cell towers.                                                                                                                                                                                    |
| └─ mcc                       | Integer         | mobile\_cells | Yes                     | Mobile Country Code that identifies the country of the mobile network.                                                                                                                                          |
| └─ mnc                       | Integer         | mobile\_cells | Yes                     | Mobile Network Code that identifies the specific mobile operator in the country.                                                                                                                                |
| └─ lac                       | Integer         | mobile\_cells | Yes                     | Location Area Code, which helps identify the area in the mobile network.                                                                                                                                        |
| └─ cell\_id                  | Integer         | mobile\_cells | Yes                     | Unique identifier of the mobile cell tower.                                                                                                                                                                     |
| └─ rssi                      | Integer         | mobile\_cells | No                      | Signal strength from the mobile tower, measured in dBm (negative values).                                                                                                                                       |
| └─ type                      | String          | mobile\_cells | No                      | The mobile radio type. Supported values are `GSM`, `CDMA`, `WCDMA`, `LTE` and `NR`. Default is `GSM`.                                                                                                           |
| **Wi-Fi points**             |                 |               |                         |                                                                                                                                                                                                                 |
| wifi\_points                 | Array \[Object] | Root          | No                      | List of visible Wi-Fi access points.                                                                                                                                                                            |
| └─ mac                       | String          | wifi\_points  | Yes                     | MAC address (hardware identifier) of the Wi-Fi access point. Each byte is delimited with a colon (e.g., 12:33:FF:45:04:33).                                                                                     |
| └─ rssi                      | Integer         | wifi\_points  | Yes                     | Signal strength from the Wi-Fi access point, measured in dBm (negative values).                                                                                                                                 |
| └─ age                       | Integer         | wifi\_points  | No                      | Time in milliseconds since this Wi-Fi access point was last discovered.                                                                                                                                         |
| └─ channel                   | Integer         | wifi\_points  | No                      | Radio channel number used by the Wi-Fi access point.                                                                                                                                                            |
| **Device motion and status** |                 |               |                         |                                                                                                                                                                                                                 |
| is\_moving                   | Boolean         | Root          | No                      | Indicates whether the device is currently moving (True or False).                                                                                                                                               |
| hardware\_mileage            | Float           | Root          | No                      | Mileage counted by the device's hardware in kilometers.                                                                                                                                                         |
| battery\_voltage             | Float           | Root          | No                      | Built-in battery voltage in volts.                                                                                                                                                                              |
| battery\_level               | Integer         | Root          | No                      | Current built-in battery level as a percentage (0 to 100).                                                                                                                                                      |
| board\_voltage               | Float           | Root          | No                      | Voltage supplied by the external power source in volts.                                                                                                                                                         |
| **Input/Output status**      |                 |               |                         |                                                                                                                                                                                                                 |
| input\_status                | Integer         | Root          | No                      | Current status of the device's discrete inputs, represented as a bitmask.                                                                                                                                       |
| output\_status               | Integer         | Root          | No                      | Current status of the device's outputs, represented as a bitmask.                                                                                                                                               |
| **Sensor data**              |                 |               |                         |                                                                                                                                                                                                                 |
| analog\_n                    | Float           | Root          | No                      | <p>Analog input voltage (volts).<br><br>Where n stands for the ordinal number of the attribute and n = 1..16.</p>                                                                                               |
| temperature\_internal        | Float           | Root          | No                      | Temperature from the built-in hardware sensor (degrees Celsius).                                                                                                                                                |
| temperature\_n               | Float           | Root          | No                      | <p>External temperature sensor (degrees Celsius).<br><br>Where n stands for the ordinal number of the attribute and n = 1..16.</p>                                                                              |
| humidity\_internal           | Float           | Root          | No                      | Relative humidity from the built-in hardware sensor (percentage).                                                                                                                                               |
| humidity\_n                  | Float           | Root          | No                      | <p>External relative humidity sensor (percentage).<br><br>Where n stands for the ordinal number of the attribute and n = 1..16.</p>                                                                             |
| fuel\_level\_n               | Float           | Root          | No                      | <p>Fuel level from fuel sensor (liters or percentage). <br><br>Where n stands for the ordinal number of the attribute and n = 1..16.</p>                                                                        |
| fuel\_temperature\_n         | Float           | Root          | No                      | <p>Fuel temperature from fuel sensor (degrees Celsius).<br><br>Where n stands for the ordinal number of the attribute and n = 1..16.</p>                                                                        |
| impulse\_counter\_n          | Integer         | Root          | No                      | <p>Impulse counter sensor. <br><br>Where n stands for the ordinal number of the attribute and n = 1..16.</p>                                                                                                    |
| **Identification data**      |                 |               |                         |                                                                                                                                                                                                                 |
| hardware\_key                | String          | Root          | No                      | Driver ID, typically read via RFID, iButton, or other identification methods.                                                                                                                                   |
| vin                          | String          | Root          | No                      | Vehicle Identification Number (VIN).                                                                                                                                                                            |
| **Custom data**              |                 |               |                         |                                                                                                                                                                                                                 |
| custom\_attribute            | Mixed           | Root          | No                      | Any additional custom data described below.                                                                                                                                                                     |

### Custom attributes

The table's final section refers to custom data. You can also expand the protocol by adding your own custom data, which will be passed through unchanged, for example, hardware-specific attributes like `avl_io_n` or `flex_id`.

The following example shows a message containing a custom data attribute. Custom attributes, like the `custom_attribute` in the example, are added directly to the root of the message structure.

```
{
 "message_time": "2024-09-02T12:23:45Z",
    "device_id": "857378374927457",
    "version": "1.0",
    "location": {
        ...
    },
    "custom_attribute": 123.44
}
```

## Message example

A typical GPS device telemetry message will follow this format:

```
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
        "heading": 77
    },
    "event_id": 2,
    "mobile_cells": [{
            "mcc": 250,
            "mnc": 0,
            "lac": 32445,
            "cell_id": 343455,
            "rssi": -54,
            "type": "LTE"
        }
    ],
    "wifi_points": [{
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
    "input_status": 23424,
    "output_status": 23424,
    "hardware_key": "12FFABC54234",
    "temperature_internal": 12.3,
    "temperature_2": -13.7,
    "custom_attribute": 123.44
}
```

Continue reading to learn about [Predefined event identifiers](predefined-event-identifiers.md) in Navixy Generic Protocol.
