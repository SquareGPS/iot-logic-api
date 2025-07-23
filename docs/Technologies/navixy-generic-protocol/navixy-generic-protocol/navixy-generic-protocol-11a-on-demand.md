# Navixy Generic Protocol 1.1a (on demand)

> [!INFO]
> This version of the protocol is not yet openly available, if you are interested in this particular version, please [contact our sales team](https://www.navixy.com/contact/).

Version 1.1a is the next step in developing the Navixy Generic Protocol (NGP). It introduces advanced data structures and enhanced custom attribute support, offering greater flexibility and efficiency in handling diverse telematics data. This version maintains backward compatibility with [1.0](navixy-generic-protocol-10.md) to ensure easy upgrade.

## Key change - Enhanced custom attributes

Version [1.0](navixy-generic-protocol-10.md) allows the creation of [simple custom attributes](https://squaregps.atlassian.net/wiki/spaces/NAV1/pages/3107553713/Message+structure+and+attributes#Custom-attributes) in `name:value` format. Version 1.1a enhances this functionality by introducing a more sophisticated structure for such attributes with additional metadata and organization options. The enhancement enables more detailed and contextualized sensor data integration, making the protocol highly adaptable to user-specific needs. It offers:

- New structured array format for complex data
- Ability to provide more detailed attribute information
- Support of additional metadata like units and identifiers
- [Dual implementation support](https://squaregps.atlassian.net/wiki/spaces/NAV/pages/edit-v2/3107553767#Dual-implementation-support) of simple and enhanced custom attributes in the same message

### Attribute structure

The new enhanced custom attributes include the following fields:

|     |     |     |     |     |
| --- | --- | --- | --- | --- |
| **Attribute** | **Type** | **Object** | **Required for object** | **Description** |
| custom\_attributes | Array \[Object\] | Root | No  | All custom parameters should be put into the custom\_attributes array of JSON objects. |
| └─ type | String | custom\_attributes | Yes | Parameter that indicates the attribute’s name. |
| └─ id | Integer | custom\_attributes | No  | Identifier that shows the attribute order number. |
| └─ value | Mixed | custom\_attributes | Yes | Value of the extended attribute that can have any data type. |
| └─ units | String | custom\_attributes | No  | If necessary units of measurement can be specified in this parameter. |

### Dual implementation support

A unique feature of version 1.1a is the ability to use both simple and enhanced custom attributes simultaneously in the same message, which allows for:

- **Backward compatibility with existing implementations**  
All version [1.0](navixy-generic-protocol-10.md) custom attributes continue to work without modifications, while new parameters can be added to them. This ensures the uninterrupted operation of existing systems.
- **Gradual migration to enhanced attributes**  
Systems can transition to the new format one attribute at a time, allowing teams to test and validate enhanced attributes in production without requiring a complete system update.
- **Mixed usage based on specific needs**  
Users can select the most appropriate format for each data point - simple attributes for basic data like status flags, and enhanced attributes for complex measurements requiring additional context like units.

## Example message structure

Below is an example showing both simple and enhanced custom attributes in the same message:

```
{
    "message_time": "2024-09-02T12:23:45Z",
    "device_id": "857378374927457",
    "version": "1.1a",
    "location": {
        "latitude": 34.15929687705282,
        "longitude": -118.4614133834839
    },
    /* Simple Custom Attribute (Version 1.0) */
    "custom_fuel": 86,
    /* Enhanced Custom Attributes (Version 1.1a) */
    "custom_attributes": [{
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
    }]
}
```