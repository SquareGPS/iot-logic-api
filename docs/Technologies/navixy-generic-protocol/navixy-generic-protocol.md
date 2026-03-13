---
description: >-
  Navixy Generic Protocol (NGP) — an open, JSON-based telematics protocol for
  transmitting device data to the Navixy platform and compatible systems.
---

# Navixy Generic Protocol

The Navixy Generic Protocol (NGP) is an open protocol freely available for manufacturers of GPS trackers and IoT devices. It defines a compact, JSON-based message format for transmitting telematics data — location, sensor readings, events, and custom attributes — over HTTP/HTTPS or MQTT.

## Protocol purpose

NGP is designed to be the single, standardized data format between devices and the Navixy platform. Its straightforward message structure makes it easy to implement on new hardware and extend with device-specific fields, while the platform handles decoding, validation, and routing.

Typical senders include: GPS trackers, IoT sensors, telematics terminals, and gateways that aggregate data from multiple sub-devices.

![NGP-purpose.jpg](<../../.gitbook/assets/NGP-purpose (1).jpg>)

## Protocol versions

| **Date**   | **Version**                                                              | **Status**  | **Description**                                                                                                        |
| ---------- | ------------------------------------------------------------------------ | ----------- | ---------------------------------------------------------------------------------------------------------------------- |
| 2024-09-03 | [**Version 1.0**](navixy-generic-protocol/navixy-generic-protocol-10.md) | **Current** | Base version with general availability. Standard data structures with foundational telematics and sensor data support. |

## Section content

* [Navixy Generic Protocol 1.0](navixy-generic-protocol/navixy-generic-protocol-10.md)
  * [Transport layer](navixy-generic-protocol/navixy-generic-protocol-10/transport-layer.md) — HTTP/HTTPS and MQTT connection parameters, endpoints, and code examples
  * [Data types and encoding standards](navixy-generic-protocol/navixy-generic-protocol-10/data-types-and-encoding-standards.md) — JSON type mapping, timestamps, and binary encoding
  * [Message structure and attributes](navixy-generic-protocol/navixy-generic-protocol-10/message-structure-and-attributes.md) — full attribute reference with location, sensors, I/O, and custom fields
  * [Predefined event identifiers](navixy-generic-protocol/navixy-generic-protocol-10/predefined-event-identifiers.md) — standard `event_id` values for common device events
* [NGP Mapper skill](navixy-generic-protocol/ngp-mapper-skill.md) — AI-assisted field mapping from any device format to NGP

## Implementing NGP

If you are adapting an existing device or data source to send NGP messages, the [NGP Mapper skill](navixy-generic-protocol/ngp-mapper-skill.md) can accelerate the process. Provide a sample message from your source system and the skill produces a complete field mapping table, a ready-to-send example NGP message, and transport setup — without having to work through the reference manually.
