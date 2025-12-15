# Navixy Generic Protocol

This document outlines the Navixy Generic Protocol, covering its fundamental data structures, format, and transport layer.

The Navixy Generic Protocol is freely available and can be adopted by manufacturers of GPS and IoT devices as the primary protocol for transmitting data between their hardware and telematics platforms.

## Protocol purpose

The primary function of this protocol is to facilitate the efficient transmission of telematics data, particularly location information, between clients and servers. Its straightforward and adaptable message structure allows for easy expansion with various data types.

Additionally, this protocol can be employed to send data from a wide range of devices, including IoT devices, GPS trackers, terminals, and gateways that aggregate messages from other devices.

![NGP-purpose.jpg](../../.gitbook/assets/NGP-purpose.jpg)

## Protocol versions

| **Date**   | **Version**                                                                                          | **Description**                                                                                                                                                                                                                                       |
| ---------- | ---------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2024-09-03 | [**Version 1.0**](navixy-generic-protocol/navixy-generic-protocol-10.md)                             | Base version with general availability. Standard data structures with foundational telematics and sensor data support.                                                                                                                                |
| 2024-10-25 | [**Version 1.1a**](navixy-generic-protocol/navixy-generic-protocol-11a-on-demand.md) **(on demand)** | Early release for advanced data structures and enhanced custom attributes support. Enhanced custom attributes, available exclusively in version 1.1a, open up new possibilities for users to integrate diverse sensor data and custom configurations. |

## Section content

* [Navixy Generic Protocol 1.0](navixy-generic-protocol/navixy-generic-protocol-10.md)
  * [Transport layer](navixy-generic-protocol/navixy-generic-protocol-10/transport-layer.md)
  * [Data types and encoding standards](navixy-generic-protocol/navixy-generic-protocol-10/data-types-and-encoding-standards.md)
  * [Message structure and attributes](navixy-generic-protocol/navixy-generic-protocol-10/message-structure-and-attributes.md)
  * [Predefined event identifiers](navixy-generic-protocol/navixy-generic-protocol-10/predefined-event-identifiers.md)
* [Navixy Generic Protocol 1.1a (on demand)](navixy-generic-protocol/navixy-generic-protocol-11a-on-demand.md)
