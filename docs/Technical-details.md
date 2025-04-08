---
stoplight-id: n6jl7wc7cska8
---

# Technical Details

## Flow Structure Validation

When creating or updating flows, the API performs several validation checks:

1. Node IDs must be unique within a flow
2. Each edge must reference valid node IDs
3. The flow must be acyclic (no circular references)
4. All nodes must be reachable from data sources
5. All required fields must be present for each node type

## Node Positioning

The `view` property in nodes is used for visual representation in UI tools:

```json
"view": {
  "position": {
    "x": 150,
    "y": 50
  }
}
```

While optional for API functionality, including this data helps maintain visual layout when editing flows later.

## Flow States

Flows can be in one of two states:
- `enabled: true` - The flow is active and processing data
- `enabled: false` - The flow is inactive (data is not processed)

Individual nodes can also be enabled or disabled, allowing for partial flow activation.

## Endpoint Status Options

Endpoints can have one of three status values:
- `active` - The endpoint is operational
- `suspend` - The endpoint is temporarily paused
- `disabled` - The endpoint is disabled and cannot be used

## Reference: Node Types

### 1. Data Source Node (`data_source`)

This node specifies which devices will send data to your flow. It's the entry point of all data flows.

```json
{
  "id": 1,
  "type": "data_source",
  "title": "Your Title Here",
  "enabled": true,
  "data": {
    "sources": [12345, 67890]  // Device IDs
  },
  "view": {
    "position": { "x": 50, "y": 50 }
  }
}
```

#### Key Points:
- The `data_source` node type is required in every flow
- Multiple devices can be specified in the `sources` array
- Each device is identified by its numeric ID in the Navixy system
- The `enabled` flag controls whether this node processes data
- A flow can have multiple data source nodes for different device groups

### 2. Data Processing Node (`initiate_attributes`)

This node transforms raw data into meaningful information. It allows for creating new attributes or modifying existing ones through expressions.

```json
{
  "id": 2,
  "type": "initiate_attributes",
  "title": "Your Title Here",
  "data": {
    "items": [
      {
        "name": "attribute_name",
        "value": "expression",
        "generation_time": "now()",
        "server_time": "now()"
      }
    ]
  },
  "view": {
    "position": { "x": 150, "y": 50 }
  }
}
```

#### Attribute Fields:

| Field | Description | Example |
|-------|-------------|---------|
| `name` | The attribute identifier | `"fuel_level"` |
| `value` | Mathematical or logical expression | `"analog_1 * 0.1"` |
| `generation_time` | When the data was generated | `"now()"` |
| `server_time` | When the server received the data | `"now()"` |

#### Expression Language:

The expression language supports:
- Mathematical operators: `+`, `-`, `*`, `/`, `%`
- Comparison operators: `>`, `<`, `>=`, `<=`, `==`, `!=`
- Logical operators: `&&`, `||`, `!`
- Conditional expressions: `condition ? true_value : false_value`
- Functions: `now()`, `sqrt()`, `pow()`, `abs()`
- References to device attributes: `speed`, `fuel_level`, `analog_1`, etc.

#### Expression Examples:

| Scenario | Expression |
|----------|------------|
| Temperature conversion | `(temperature_f - 32) * 5/9` |
| Speed alert | `speed > 80 ? 'speeding' : 'normal'` |
| Battery status | `battery_voltage < 11.5 ? 'low' : 'normal'` |
| Distance calculation | `sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2))` |
| Time-based condition | `hour(time) >= 22 || hour(time) <= 6 ? 'night' : 'day'` |

### 3. Output Endpoint Node (`output_endpoint`)

This node defines where your data will be sent. It's the termination point for data flow paths.

#### Navixy Output:

```json
{
  "id": 3,
  "type": "output_endpoint",
  "title": "Your Title Here",
  "enabled": true,
  "data": {
    "output_endpoint_type": "output_navixy"
  },
  "view": {
    "position": { "x": 250, "y": 50 }
  }
}
```

#### MQTT Output:

```json
{
  "id": 4,
  "type": "output_endpoint",
  "title": "Your Title Here",
  "enabled": true,
  "data": {
    "output_endpoint_type": "output_mqtt_client",
    "output_endpoint_id": 45678
  },
  "view": {
    "position": { "x": 250, "y": 150 }
  }
}
```

#### Key Points:
- Every flow must have at least one output endpoint node
- The `output_navixy` type doesn't require a referenced endpoint (built-in)
- The `output_mqtt_client` type requires an `output_endpoint_id` referencing a previously created endpoint
- Multiple output nodes can be used to send the same data to different destinations
- Output nodes are "terminal" - they don't connect to any downstream nodes

## Reference: Endpoint Types and Properties

The API supports different endpoint types, each with specific properties.

### Endpoint Types

| Type | Description | Use Case |
|------|-------------|----------|
| `input_navixy` | Default input from Navixy platform | Receiving data from Navixy devices |
| `output_navixy` | Default output to Navixy platform | Sending processed data back to Navixy |
| `output_mqtt_client` | External MQTT broker connection | Integrating with third-party systems |

### MQTT Endpoint Properties

The following properties are available when creating MQTT endpoints:

| Property | Description | Required | Example |
|----------|-------------|----------|---------|
| `protocol` | Protocol of messages | Yes | `"NGP"` (Navixy Generic Protocol) |
| `domain` | MQTT broker domain/IP | Yes | `"mqtt.example.com"` |
| `port` | MQTT port | Yes | `1883` |
| `client_id` | Client identifier | Yes | `"navixy-client-1"` |
| `qos` | Quality of Service (0 or 1) | Yes | `1` |
| `topics` | Array of topic names | Yes | `["iot/data"]` |
| `version` | MQTT version | Yes | `"5.0"` or `"3.1.1"` |
| `use_ssl` | Whether to use SSL | Yes | `true` |
| `mqtt_auth` | Whether auth is required | Yes | `true` |
| `user_name` | MQTT username | Only if `mqtt_auth: true` | `"mqtt_user"` |
| `user_password` | MQTT password | Only if `mqtt_auth: true` | `"mqtt_password"` |

### MQTT QoS Levels

The API supports MQTT QoS (Quality of Service) levels:

- **QoS 0**: "At most once" delivery (fire and forget)
- **QoS 1**: "At least once" delivery (acknowledged delivery)
- **QoS 2**: Not currently supported by the API

### MQTT Protocol Versions

Two MQTT protocol versions are supported:

- **MQTT 3.1.1**: Widely supported version
- **MQTT 5.0**: Newer version with enhanced features

## Best Practices

### Flow Design

1. **Plan your flow design** before implementation
2. **Create endpoints first** before referencing them in flows
3. **Use descriptive titles** for both flows and nodes
4. **Test incrementally** by adding one component at a time
5. **Monitor data flow** after implementation to ensure it's working correctly

### Data Processing

6. **Keep expressions simple** where possible for easier maintenance
7. **Use consistent naming conventions** for attributes
8. **Document complex expressions** with clear comments in your own documentation
9. **Consider data volume** when creating flows with multiple outputs

### Security

10. **Secure your MQTT connections** with SSL when possible
11. **Rotate credentials** periodically for MQTT endpoints
12. **Use unique client IDs** for each MQTT endpoint to avoid connection conflicts
13. **Restrict topic access** on your MQTT broker to only necessary paths

### Maintenance

14. **Back up your flow configurations** by storing the JSON responses
15. **Version your flows** with sequential titles or internal documentation
16. **Regularly review active flows** to ensure they're still needed
17. **Keep a library of common patterns** for reuse across flows

## Error Handling

The API returns specific error codes when requests fail. Common error codes include:

| Error Code | Description | Solution |
|------------|-------------|----------|
| 1 | Database error | Check your data format and try again |
| 2 | Invalid parameters | Ensure all required fields are provided |
| 3 | Access denied | Check your API key and permissions |
| 4 | Resource not found | Verify IDs for flows and endpoints |
| 5 | Rate limit exceeded | Reduce request frequency |

Error responses follow this format:
```json
{
  "success": false,
  "status": {
    "code": 2,
    "description": "Invalid parameters"
  }
}
```

## Data Security Considerations

When working with the Navixy IoT Gateway API:

1. **API Keys**: Protect your API keys as they provide full access to your account
2. **MQTT Credentials**: Use strong passwords for MQTT authentication
3. **SSL**: Enable SSL (`use_ssl: true`) for MQTT connections whenever possible
4. **Data Privacy**: Be mindful of what device data you transmit to external systems
5. **Endpoint Security**: Regularly audit your endpoints and disable unused ones

## Troubleshooting

| Issue | Possible Solution |
|-------|-------------------|
| Flow not processing data | Check that both flow and all nodes have `enabled: true` |
| MQTT connection failing | Verify credentials, domain, port, and SSL settings |
| Data transformations not working | Test expressions in isolation to identify issues |
| Missing data in output | Ensure all required attributes are being processed |
| API errors | Double-check JSON syntax and required fields |
| Flow validation errors | Ensure node IDs are unique and edges connect valid nodes |
| Unexpected data format | Verify the calculation expressions in processing nodes |
| Missing fields in response | Check if you have all required permissions |