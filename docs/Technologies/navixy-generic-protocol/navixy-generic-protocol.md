---
description: >-
  Navixy Generic Protocol (NGP), an open, JSON-based telematics protocol for
  transmitting device data to the Navixy platform and compatible systems.
---

# Navixy Generic Protocol

The Navixy Generic Protocol (NGP) is an open protocol freely available for manufacturers of GPS trackers and IoT devices. It defines a compact, JSON-based message format for transmitting telematics data (location, sensor readings, events, and custom attributes) over HTTP/HTTPS or MQTT.

## Protocol purpose

NGP is designed to be the single, standardized data format between devices and the Navixy platform. Its straightforward message structure makes it easy to implement on new hardware and extend with device-specific fields, while the platform handles decoding, validation, and routing.

Typical senders include: GPS trackers, IoT sensors, telematics terminals, and gateways that aggregate data from multiple sub-devices.

![NGP-purpose.jpg](<../../.gitbook/assets/NGP-purpose (1).jpg>)

## Protocol versions

<table><thead><tr><th width="136">Date</th><th width="124">Version</th><th width="133">Status</th><th>Description</th></tr></thead><tbody><tr><td>2024-09-03</td><td><a href="navixy-generic-protocol/navixy-generic-protocol-10.md"><strong>Version 1.0</strong></a></td><td><strong>Stable</strong></td><td>Base version with general availability. Standard data structures with foundational telematics and sensor data support.</td></tr><tr><td>2024-10-25</td><td><a href="navixy-generic-protocol/navixy-generic-protocol-11a-on-demand.md"><strong>Version 1.1a</strong></a></td><td><strong>On demand</strong></td><td>Early release for advanced data structures and enhanced custom attributes support. Enhanced custom attributes, available exclusively in version 1.1a, open up new possibilities for users to integrate diverse sensor data and custom configurations.</td></tr><tr><td>2026-03-12</td><td><a href="navixy-generic-protocol/navixy-generic-protocol-12.md"><strong>Version 1.2</strong></a></td><td><strong>Current</strong></td><td>Adds <code>source_type</code> and <code>precision</code> to the <code>location</code> object, enabling explicit positioning source identification. Backward compatible with 1.0.</td></tr></tbody></table>

## Section content

* [Navixy Generic Protocol 1.0](navixy-generic-protocol/navixy-generic-protocol-10.md) - base version with complete reference
  * [Transport layer](navixy-generic-protocol/navixy-generic-protocol-10/transport-layer.md) - HTTP/HTTPS and MQTT connection parameters, endpoints, and code examples
  * [Data types and encoding standards](navixy-generic-protocol/navixy-generic-protocol-10/data-types-and-encoding-standards.md) - JSON type mapping, timestamps, and binary encoding
  * [Message structure and attributes](navixy-generic-protocol/navixy-generic-protocol-10/message-structure-and-attributes.md) - full attribute reference with location, sensors, I/O, and custom fields
  * [Predefined event identifiers](navixy-generic-protocol/navixy-generic-protocol-10/predefined-event-identifiers.md) - standard `event_id` values for common device events
* [Navixy Generic Protocol 1.1a (on demand)](navixy-generic-protocol/navixy-generic-protocol-11a-on-demand.md) - structured custom attribute arrays with metadata
* [Navixy Generic Protocol 1.2](navixy-generic-protocol/navixy-generic-protocol-12.md) - adds `source_type` and `precision` to the `location` object
* [NGP Mapper skill](navixy-generic-protocol/ngp-mapper-skill.md) - AI-assisted field mapping from any device format to NGP

## Implementing NGP

Mapping an existing device or data source to NGP typically means working through the field reference, identifying transforms for unit conversions and enum remappings, and handling edge cases such as LBS-only positioning or bitmask extraction. The [NGP Mapper skill](navixy-generic-protocol/ngp-mapper-skill.md) handles this process automatically.

You provide a sample message from your source system (a raw JSON export, a proprietary tracker payload, a Wialon record, or any structured format) and the skill produces a complete field mapping table with every required transform, a ready-to-send NGP JSON example built from your real values, exact transport parameters for HTTP or MQTT in your target region, and notes on fields with no direct NGP equivalent and how to handle them.

The result is a self-contained specification you can hand to a developer or use to implement the converter yourself, without having to read through the entire reference first.

{% hint style="info" %}
The NGP Mapper skill runs inside your AI assistant and requires no additional tools or accounts. [Download the skill file and see how to use it](navixy-generic-protocol/ngp-mapper-skill.md).
{% endhint %}
