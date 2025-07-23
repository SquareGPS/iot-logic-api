# Data types and encoding standards

## Data types

| **Type** | **JSON** | **Description** | **Examples** | **Limitations** |
| --- | --- | --- | --- | --- |
| Integer | Number | Integer numeric values | Bit masks, counters, impulses, passengers and RPM | From 1 to 8 byte signed or unsigned integer number |
| Float | Number | Numeric floating-point values | Coordinates, telemetry, speed, altitude, mileage | Up to 8 byte signed float number (IEEE 754) |
| String | String | UTF-8 encoded text string | Driver's name, registration number, driver ID | Up to 10KB escaped text |
| Boolean | Boolean | Values true or false | CAN attributes states: ignition state, doors state, presence of movement, etc. | True or false |
| Timestamp | String | Date and time value in ISO 8601 UTC format | Date and time when the coordinate was received by the device | ISO 8601 related restrictions |
| Blob | String | Binary data in Base-64 format | Photo, raw data from sensors, BLE data, Voice | Up to 1 MB encoded binary data |
| Array | Array | A list of objects with identical types | Mobile cells, Wi-fi points | No limitations |
| Object | Object | Structures that consist of several attributes | Location data, Mobile cell, Wi-fi point | No limitations |

## Timestamps and data encoding

All timestamps must adhere to the **ISO 8601** format.

Example:

- `"message_time": "2024-09-02T23:59:59Z"`

For raw data such as sensor readings, tachograph logs, images, or audio, binary transmission is supported. When transmitting binary data, it must be **Base64-encoded**.

Examples:

- `"my_sensor_data": "SGVsbG8gd29ybGQh"`
- `"tachograph_log": "U29tZSB0YWNoZW9nIGxvZw=="`
- `"photo": "/9j/4AAQSkZJRgABAQEAYABgAAD..."`
- `"audio": "UklGRjIAAABXRUJQVlA4WAoAAAAQAAAA..."`

By adhering to these standards, the protocol ensures universal understanding of timestamps and reliable transmission of binary data. Keep in mind, the protocol is not optimized for large binary payloads within messages.

Continue reading to learn about [Message structure and attributes](message-structure-and-attributes.md) in Navixy Generic Protocol.