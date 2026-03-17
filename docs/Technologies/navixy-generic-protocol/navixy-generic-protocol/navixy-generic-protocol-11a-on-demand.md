---
hidden: true
noIndex: true
---

# Navixy Generic Protocol 1.1a (on demand)

For current integration, use [Navixy Generic Protocol 1.0](navixy-generic-protocol-10.md).

Version 1.1a introduced advanced data structures and enhanced custom attribute support. It maintains backward compatibility with [1.0](navixy-generic-protocol-10.md).

## Key change: Enhanced custom attributes

Version [1.0](navixy-generic-protocol-10.md) allows simple custom attributes in `name:value` format. Version 1.1a enhanced this with a structured array format including additional metadata.

### Attribute structure

| **Attribute**      | **Type**        | **Object**         | **Required** | **Description**                             |
| ------------------ | --------------- | ------------------ | ------------ | ------------------------------------------- |
| custom\_attributes | Array \[Object] | Root               | No           | Array of enhanced custom attribute objects. |
| └─ type            | String          | custom\_attributes | Yes          | Attribute name.                             |
| └─ id              | Integer         | custom\_attributes | No           | Attribute order number.                     |
| └─ value           | Mixed           | custom\_attributes | Yes          | Attribute value. Any JSON type.             |
| └─ units           | String          | custom\_attributes | No           | Unit of measurement, e.g. `rpm`, `percent`. |

{% details "Full attribute reference for version 1.1a" %}

| **Attribute**                | **Type**          | **Object**         | **Required** | **Description**                                                                                                                                                   |
| ---------------------------- | ----------------- | ------------------ | ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Basic attributes**         |                   |                    |              |                                                                                                                                                                   |
| message\_time                | Timestamp         | Root               | Yes          | Date and time the message was sent by the device (ISO 8601 UTC).                                                                                                  |
| device\_id                   | String            | Root               | Yes          | Unique device identifier. Maximum 64 characters.                                                                                                                  |
| version                      | String            | Root               | No           | NGP version of this message. Use `1.1a` to enable enhanced custom attributes.                                                                                     |
| **Location**                 |                   |                    |              |                                                                                                                                                                   |
| location                     | Object            | Root               | No           | Device position. May be determined by GNSS (satellite), LBS (cell towers), or a third-party positioning service.                                                  |
| └─ latitude                  | Float             | location           | No           | Latitude in decimal degrees (−90.0 to 90.0).                                                                                                                      |
| └─ longitude                 | Float             | location           | No           | Longitude in decimal degrees (−180.0 to 180.0).                                                                                                                   |
| └─ altitude                  | Float             | location           | No           | Altitude above sea level in meters (−1000 to 10000).                                                                                                              |
| └─ gnss\_time                | Timestamp         | location           | No           | Time when the position fix was acquired by the device.                                                                                                            |
| └─ fix\_type                 | String            | location           | No           | Position fix type. Possible values: `HAS_FIX` (default), `NO_FIX`, `LAST_KNOWN_POSITION`, `FIX_2D`, `FIX_3D`.                                                    |
| └─ satellites                | Integer           | location           | No           | Number of GNSS satellites used for the fix (0–64).                                                                                                                |
| └─ hdop                      | Float             | location           | No           | Horizontal dilution of precision. Lower is more accurate.                                                                                                         |
| └─ vdop                      | Float             | location           | No           | Vertical dilution of precision. Lower is more accurate.                                                                                                           |
| └─ pdop                      | Float             | location           | No           | 3D position dilution of precision, combining horizontal and vertical.                                                                                             |
| └─ speed                     | Float             | location           | No           | Device speed in km/h (positive values only).                                                                                                                      |
| └─ heading                   | Integer           | location           | No           | Direction of movement in degrees, clockwise from north (1–360).                                                                                                   |
| **Event information**        |                   |                    |              |                                                                                                                                                                   |
| event\_id                    | Integer           | Root               | No           | Platform event identifier. See [Predefined event identifiers](navixy-generic-protocol-10/predefined-event-identifiers.md) for standard values. Custom events start at 10,000. |
| **Mobile cells**             |                   |                    |              |                                                                                                                                                                   |
| mobile\_cells                | Array \[Object]   | Root               | No           | List of visible cell towers. Used to provide data for network-based positioning (LBS) when GNSS is unavailable.                                                   |
| └─ mcc                       | Integer           | mobile\_cells      | Yes          | Mobile Country Code. Identifies the country of the mobile network.                                                                                                |
| └─ mnc                       | Integer           | mobile\_cells      | Yes          | Mobile Network Code. Identifies the mobile operator within the country.                                                                                           |
| └─ lac                       | Integer           | mobile\_cells      | Yes          | Location Area Code. Identifies the area within the mobile network.                                                                                                |
| └─ cell\_id                  | Integer           | mobile\_cells      | Yes          | Unique identifier of the cell tower.                                                                                                                              |
| └─ rssi                      | Integer           | mobile\_cells      | No           | Signal strength from the cell tower in dBm (negative values).                                                                                                     |
| └─ type                      | String            | mobile\_cells      | No           | Radio access technology. Possible values: `GSM` (default), `CDMA`, `WCDMA`, `LTE`, `NR`.                                                                         |
| **Wi-Fi points**             |                   |                    |              |                                                                                                                                                                   |
| wifi\_points                 | Array \[Object]   | Root               | No           | List of visible Wi-Fi access points. Used alongside `mobile_cells` to improve network-based positioning accuracy.                                                 |
| └─ mac                       | String            | wifi\_points       | Yes          | MAC address of the access point. Colon-delimited bytes, e.g. `12:33:FF:45:04:33`.                                                                                |
| └─ rssi                      | Integer           | wifi\_points       | Yes          | Signal strength in dBm (negative values).                                                                                                                         |
| └─ age                       | Integer           | wifi\_points       | No           | Milliseconds since this access point was last detected.                                                                                                           |
| └─ channel                   | Integer           | wifi\_points       | No           | Radio channel number used by the access point.                                                                                                                    |
| **Device motion and status** |                   |                    |              |                                                                                                                                                                   |
| is\_moving                   | Boolean           | Root               | No           | `true` if the device is currently moving, `false` if stationary.                                                                                                  |
| hardware\_mileage            | Float             | Root               | No           | Cumulative mileage counted by the device hardware, in kilometers.                                                                                                 |
| battery\_voltage             | Float             | Root               | No           | Built-in battery voltage in volts.                                                                                                                                |
| battery\_level               | Integer           | Root               | No           | Built-in battery charge level as a percentage (0–100).                                                                                                            |
| board\_voltage               | Float             | Root               | No           | External power supply voltage in volts.                                                                                                                           |
| **Input/Output status**      |                   |                    |              |                                                                                                                                                                   |
| input\_status                | Integer           | Root               | No           | State of discrete inputs as a bitmask. Bit 0 = input 1, bit 1 = input 2, and so on. A set bit means the input is active.                                         |
| output\_status               | Integer           | Root               | No           | State of outputs as a bitmask. Bit 0 = output 1, bit 1 = output 2, and so on. A set bit means the output is active.                                              |
| **Sensor data**              |                   |                    |              |                                                                                                                                                                   |
| analog\_n                    | Float             | Root               | No           | Analog input voltage in volts. `n` is the sensor index from 1 to 16, e.g. `analog_1`.                                                                            |
| temperature\_internal        | Float             | Root               | No           | Temperature from the built-in hardware sensor, in degrees Celsius.                                                                                               |
| temperature\_n               | Float             | Root               | No           | External temperature sensor reading in degrees Celsius. `n` is the sensor index from 1 to 16.                                                                    |
| humidity\_internal           | Float             | Root               | No           | Relative humidity from the built-in hardware sensor, as a percentage.                                                                                            |
| humidity\_n                  | Float             | Root               | No           | External relative humidity sensor reading as a percentage. `n` is the sensor index from 1 to 16.                                                                 |
| fuel\_level\_n               | Float             | Root               | No           | Fuel level from a fuel sensor, in liters or as a percentage. `n` is the sensor index from 1 to 16.                                                               |
| fuel\_temperature\_n         | Float             | Root               | No           | Fuel temperature from a fuel sensor, in degrees Celsius. `n` is the sensor index from 1 to 16.                                                                   |
| impulse\_counter\_n          | Integer           | Root               | No           | Impulse counter reading. `n` is the counter index from 1 to 16.                                                                                                  |
| **Identification data**      |                   |                    |              |                                                                                                                                                                   |
| hardware\_key                | String            | Root               | No           | Driver or asset identifier, typically read via RFID, iButton, or similar method.                                                                                 |
| vin                          | String            | Root               | No           | Vehicle Identification Number (VIN).                                                                                                                              |
| **Custom data**              |                   |                    |              |                                                                                                                                                                   |
| custom\_\*                   | Mixed             | Root               | No           | Simple custom attribute in `name:value` format, inherited from version 1.0.                                                                                       |
| custom\_attributes           | Array \[Object]   | Root               | No           | **New in 1.1a.** Structured custom attribute array with metadata.                                                                                                 |
| └─ type                      | String            | custom\_attributes | Yes          | Attribute name.                                                                                                                                                   |
| └─ id                        | Integer           | custom\_attributes | No           | Attribute order number.                                                                                                                                           |
| └─ value                     | Mixed             | custom\_attributes | Yes          | Attribute value. Any JSON type.                                                                                                                                   |
| └─ units                     | String            | custom\_attributes | No           | Unit of measurement, e.g. `rpm`, `percent`.                                                                                                                       |

{% enddetails %}

### Dual implementation support

Version 1.1a supports both simple (1.0-style) and enhanced custom attributes in the same message:

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
