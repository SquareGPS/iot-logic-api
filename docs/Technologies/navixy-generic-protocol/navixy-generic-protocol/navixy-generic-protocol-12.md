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
