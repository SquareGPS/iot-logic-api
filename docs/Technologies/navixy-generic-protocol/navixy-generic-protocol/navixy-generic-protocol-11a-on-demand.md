---
hidden: true
---

# Navixy Generic Protocol 1.1a (on demand)

{% hint style="danger" %}
This version is deprecated and no longer actively developed. The documentation is retained for reference only.

For current integration, use [Navixy Generic Protocol 1.0](navixy-generic-protocol-10.md).
{% endhint %}

Version 1.1a introduced advanced data structures and enhanced custom attribute support. It maintains backward compatibility with [1.0](navixy-generic-protocol-10.md).

## Key change — Enhanced custom attributes

Version [1.0](navixy-generic-protocol-10.md) allows simple custom attributes in `name:value` format. Version 1.1a enhanced this with a structured array format including additional metadata.

### Attribute structure

| **Attribute**      | **Type**        | **Object**          | **Required** | **Description**                                                        |
| ------------------ | --------------- | ------------------- | ------------ | ---------------------------------------------------------------------- |
| custom\_attributes | Array [Object]  | Root                | No           | Array of enhanced custom attribute objects.                            |
| └─ type            | String          | custom\_attributes  | Yes          | Attribute name.                                                        |
| └─ id              | Integer         | custom\_attributes  | No           | Attribute order number.                                                |
| └─ value           | Mixed           | custom\_attributes  | Yes          | Attribute value — any JSON type.                                       |
| └─ units           | String          | custom\_attributes  | No           | Unit of measurement, e.g. `rpm`, `percent`.                            |

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
