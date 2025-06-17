---
stoplight-id: n6jl7wc7cska8
---

# Technical reference

## API environments

The Navixy IoT Logic API is available on multiple regional platforms to optimize performance and comply with data residency requirements.

### Base URLs

| Region   | Base URL                    | Data Location         |
| -------- | --------------------------- | --------------------- |
| Europe   | `https://api.eu.navixy.com` | European data centers |
| Americas | `https://api.us.navixy.com` | US-based data centers |

#### Environment selection

Choose the environment that:

1. Is geographically closest to your operations (to minimize latency)
2. Complies with your data residency requirements
3. Matches your existing Navixy platform subscription

Both environments offer identical API functionality, but may differ in:

* Response times based on your geographic location
* Data storage location (important for compliance with regulations like GDPR)
* Maintenance windows and update schedules

## Authentication

Authentication for the Navixy IoT Logic API uses API keys or user session hashes. For detailed information about authentication methods, obtaining API keys, and best practices, please refer to the [Authentication](authentication.md) documentation.

## Request formats

### HTTP methods

| Method | Usage                                  | Examples                                        |
| ------ | -------------------------------------- | ----------------------------------------------- |
| `GET`  | Retrieving information                 | Flow listing, flow details                      |
| `POST` | Creating, updating, deleting resources | Creating, updating and deleting flows and nodes |

> Some read operations use POST requests with a request body instead of GET with query parameters. Always check the endpoint documentation for the correct method.

### Content type

All requests and responses use JSON format:

```
Content-Type: application/json
```

All request bodies must be valid JSON objects. The API will return a 400 Bad Request response for malformed JSON.

### Date and time formats

All timestamps in the API use ISO 8601 format in UTC timezone:

```
YYYY-MM-DDThh:mm:ssZ
```

Example: `2025-04-08T14:30:00Z` represents April 8, 2025, at 2:30 PM UTC.

## Response structure

All API responses follow a consistent JSON format.

### Success responses

Success responses always include a `success: true` field and may include additional data:

```json
{
  "success": true,
  "value": {
    // Requested data or resource
  }
}
```

For list operations:

```json
{
  "success": true,
  "list": [
    // Array of requested items
  ]
}
```

### Error responses

Error responses include `success: false` and a `status` object with details:

```json
{
  "success": false,
  "status": {
    "code": 2,
    "description": "Invalid parameters"
  }
}
```

### Common error codes

| Code | Description         | Typical Causes                                |
| ---- | ------------------- | --------------------------------------------- |
| 1    | Database error      | Internal server issue, data format problem    |
| 2    | Invalid parameters  | Missing required fields, incorrect data types |
| 3    | Access denied       | Invalid API key or permissions                |
| 4    | Resource not found  | Incorrect ID for flow or endpoint             |
| 5    | Rate limit exceeded | Too many requests in short time period        |
| 6    | Validation error    | Flow structure issues, invalid connections    |

## Endpoint reference

> For OpenAPI reference, see [Navixy IoT Logic API](../IoT_Logic.json)

The Navixy IoT Logic API provides the following endpoints for managing flows and endpoints:

### Flow management endpoints

| Endpoint                 | Method | Description             | Key Parameters                             |
| ------------------------ | ------ | ----------------------- | ------------------------------------------ |
| `/iot/logic/flow/create` | POST   | Create a new flow       | `flow` object with title, nodes, edges     |
| `/iot/logic/flow/read`   | GET    | Read an existing flow   | `flow_id`                                  |
| `/iot/logic/flow/update` | POST   | Update an existing flow | `flow` object with id, title, nodes, edges |
| `/iot/logic/flow/delete` | POST   | Delete a flow           | `flow_id`                                  |
| `/iot/logic/flow/list`   | GET    | List all flows          | none                                       |

### Node management endpoints

| Endpoint                          | Method | Description                 | Key Parameters                                 |
| --------------------------------- | ------ | --------------------------- | ---------------------------------------------- |
| `/iot/logic/flow/endpoint/create` | POST   | Create a new endpoint       | `endpoint` object with type, title, properties |
| `/iot/logic/flow/endpoint/read`   | POST   | Read an existing endpoint   | `endpoint_id`                                  |
| `/iot/logic/flow/endpoint/update` | POST   | Update an existing endpoint | `endpoint` object with id and updated fields   |
| `/iot/logic/flow/endpoint/delete` | POST   | Delete an endpoint          | `endpoint_id`                                  |
| `/iot/logic/flow/endpoint/list`   | POST   | List all endpoints          | none                                           |

## Flow architecture

Flows in Navixy IoT Logic follow a directed graph architecture with specific requirements and constraints.

### Basic requirements

| Requirement          | Description                                                     |
| -------------------- | --------------------------------------------------------------- |
| Input nodes          | Every flow must have at least one data source node              |
| Output nodes         | Every flow must have at least one output endpoint node          |
| Node IDs             | Each node has a unique ID within its flow (not globally unique) |
| Connections          | Edges define directional data flow between nodes                |
| Multiple connections | Nodes can have multiple incoming and outgoing connections       |
| No cycles            | Circular references are not supported                           |

### Flow validation

When creating or updating flows, the API performs several validation checks:

1. Node IDs must be unique within a flow
2. Each edge must reference valid node IDs
3. The flow must be acyclic (no circular references)
4. All nodes must be reachable from data sources
5. All required fields must be present for each node type

### Flow states

| State            | Description   | Effect                               |
| ---------------- | ------------- | ------------------------------------ |
| `enabled: true`  | Active flow   | The flow processes data in real-time |
| `enabled: false` | Inactive flow | Data is not processed by this flow   |

Individual nodes can also be enabled or disabled, allowing for partial flow activation.

### Node positioning

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

## Endpoint management

### Endpoint status options

| Status     | Description          | Use Case                                          |
| ---------- | -------------------- | ------------------------------------------------- |
| `active`   | Fully operational    | Normal operation, actively sending/receiving data |
| `suspend`  | Temporarily paused   | Maintenance periods, temporary disconnection      |
| `disabled` | Permanently disabled | Decommissioned endpoints, security concerns       |

### Rate limiting

To ensure system stability for all customers, the platform limits API requests to 50 requests per second per user and per IP address (for applications serving multiple users). These limits are applied based on user session hash and API keys.

> When a rate limit is exceeded, the API returns a 429 Too Many Requests status code with a specific error message

To avoid rate limiting issues:

1. Implement exponential backoff for retries
2. Batch operations where possible
3. Cache frequently accessed data
4. Distribute non-urgent requests over time

## Node reference

### 1. Data source node (`data_source`)

This node specifies which devices will send data to your flow. It's the entry point of all data flows.

#### Data source node structure

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

#### Key properties

| Property       | Type    | Required | Description                              |
| -------------- | ------- | -------- | ---------------------------------------- |
| `id`           | integer | Yes      | Unique identifier within the flow        |
| `type`         | string  | Yes      | Must be `"data_source"`                  |
| `title`        | string  | Yes      | Human-readable name for the node         |
| `enabled`      | boolean | Yes      | Whether this node processes data         |
| `data.sources` | array   | Yes      | Array of device IDs to collect data from |

#### Usage notes

* The `data_source` node type is required in every flow
* Multiple devices can be specified in the `sources` array
* Each device is identified by its numeric ID in the Navixy system
* A flow can have multiple data source nodes for different device groups

### 2. Data processing node (`initiate_attribute`)

This node transforms raw data into meaningful information. It allows for creating new attributes or modifying existing ones through expressions.

#### Data processing node structure

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

#### Key properties

| Property                       | Type    | Required | Description                        |
| ------------------------------ | ------- | -------- | ---------------------------------- |
| `id`                           | integer | Yes      | Unique identifier within the flow  |
| `type`                         | string  | Yes      | Must be `"initiate_attributes"`    |
| `title`                        | string  | Yes      | Human-readable name for the node   |
| `data.items`                   | array   | Yes      | Array of attribute definitions     |
| `data.items[].name`            | string  | Yes      | The attribute identifier           |
| `data.items[].value`           | string  | Yes      | Mathematical or logical expression |
| `data.items[].generation_time` | string  | Yes      | When the data was generated        |
| `data.items[].server_time`     | string  | Yes      | When the server received the data  |

#### Expression language

For calculations IoT Logic API uses [Navixy IoT Logic Expression Language](https://docs.navixy.com/iot-logic/navixy-iot-logic-expression-language).\
Here's a guick reference:

| Feature                | Operators/Examples                  | Description                    |
| ---------------------- | ----------------------------------- | ------------------------------ |
| Mathematical operators | `+`, `-`, `*`, `/`, `%`             | Basic arithmetic operations    |
| Functions              | `now()`, `sqrt()`, `pow()`, `abs()` | Built-in functions             |
| Attribute references   | `speed`, `fuel_level`, `analog_1`   | Reference to device attributes |

**Expression examples**

| Scenario               | Expression                                                | Description                       |
| ---------------------- | --------------------------------------------------------- | --------------------------------- |
| Temperature conversion | `(temperature_f - 32) * 5/9`                              | Convert Fahrenheit to Celsius     |
| Distance calculation   | `sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2))`                 | Calculate distance between points |
| Time-based condition   | `hour(time) >= 22 \|\| hour(time) <= 6 ? 'night' : 'day'` | Determine day/night status        |

### 3. Output endpoint node (`output_endpoint`)

This node defines where your data will be sent. It's the termination point for data flow paths.

#### Output types

The output endpoint node supports different destination types:

**Default output for sending data to Navixy**

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

**MQTT output for sending data to to external systems**

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

#### Key properties

| Property                    | Type    | Required      | Description                                                              |
| --------------------------- | ------- | ------------- | ------------------------------------------------------------------------ |
| `id`                        | integer | Yes           | Unique identifier within the flow                                        |
| `type`                      | string  | Yes           | Must be `"output_endpoint"`                                              |
| `title`                     | string  | Yes           | Human-readable name for the node                                         |
| `enabled`                   | boolean | Yes           | Whether this node processes data                                         |
| `data.output_endpoint_type` | string  | Yes           | Type of output destination (`"output_navixy"` or `"output_mqtt_client"`) |
| `data.output_endpoint_id`   | integer | For MQTT only | Reference to a previously created endpoint                               |

#### Usage notes

* Every flow must have at least one output endpoint node to be functional
* The `output_navixy` type doesn't require a referenced endpoint (built-in)
* The `output_mqtt_client` type requires an `output_endpoint_id` referencing a previously created endpoint
* Multiple output nodes can be used to send the same data to different destinations
* Output nodes are "terminal" - they don't connect to any downstream nodes

## Endpoint reference

### Endpoint types

| Type                 | Description                        | Use Case                              |
| -------------------- | ---------------------------------- | ------------------------------------- |
| `input_navixy`       | Default input from Navixy platform | Receiving data from Navixy devices    |
| `output_navixy`      | Default output to Navixy platform  | Sending processed data back to Navixy |
| `output_mqtt_client` | External MQTT broker connection    | Integrating with third-party systems  |

### MQTT endpoint properties

| Property        | Type             | Required                  | Description                 | Example                           |
| --------------- | ---------------- | ------------------------- | --------------------------- | --------------------------------- |
| `protocol`      | string           | Yes                       | Protocol of messages        | `"NGP"` (Navixy Generic Protocol) |
| `domain`        | string           | Yes                       | MQTT broker domain/IP       | `"mqtt.example.com"`              |
| `port`          | integer          | Yes                       | MQTT port                   | `1883`                            |
| `client_id`     | string           | Yes                       | Client identifier           | `"navixy-client-1"`               |
| `qos`           | integer          | Yes                       | Quality of Service (0 or 1) | `1`                               |
| `topics`        | array of strings | Yes                       | Topic names                 | `["iot/data"]`                    |
| `version`       | string           | Yes                       | MQTT version                | `"5.0"` or `"3.1.1"`              |
| `use_ssl`       | boolean          | Yes                       | Whether to use SSL          | `true`                            |
| `mqtt_auth`     | boolean          | Yes                       | Whether auth is required    | `true`                            |
| `user_name`     | string           | Only if `mqtt_auth: true` | MQTT username               | `"mqtt_user"`                     |
| `user_password` | string           | Only if `mqtt_auth: true` | MQTT password               | `"mqtt_password"`                 |

#### MQTT QoS levels

| Level     | Description                                      | Use Case                                                           |
| --------- | ------------------------------------------------ | ------------------------------------------------------------------ |
| **QoS 0** | "At most once" delivery (fire and forget)        | High-volume, non-critical data where occasional loss is acceptable |
| **QoS 1** | "At least once" delivery (acknowledged delivery) | Important messages that must be delivered, can handle duplicates   |
| **QoS 2** | Not currently supported by the API               | -                                                                  |

#### MQTT protocol versions

| Version        | Description                          | Features                                                          |
| -------------- | ------------------------------------ | ----------------------------------------------------------------- |
| **MQTT 3.1.1** | Widely supported version             | Basic pub/sub functionality, broad broker compatibility           |
| **MQTT 5.0**   | Newer version with enhanced features | Message expiry, topic aliases, shared subscriptions, reason codes |

## Best practices

#### Flow design

1. **Plan your flow design** before implementation
   * Sketch your flow structure including all nodes and connections
   * Identify device sources and required data transformations
   * Determine appropriate output endpoints
2. **Create endpoints first** before referencing them in flows
   * MQTT endpoints must exist before they can be referenced
   * Test endpoint connectivity independently before adding to flows
3. **Use descriptive titles** for both flows and nodes
   * Clear naming helps with maintenance and troubleshooting
   * Include purpose or function in the title
4. **Test incrementally** by adding one component at a time
   * Start with a minimal viable flow and expand
   * Test each node's functionality before adding complexity
5. **Monitor data flow** after implementation
   * Verify data is flowing as expected
   * Check for proper attribute transformation

#### Data processing

6. **Keep expressions simple** where possible
   * Complex expressions are harder to debug and maintain
   * Consider using multiple nodes for complex transformations
7. **Use consistent naming conventions** for attributes
   * Follow a pattern like `category_attribute_unit`
   * For example: `engine_temperature_celsius`
8. **Document complex expressions** with clear comments
   * Keep documentation for non-obvious calculations
   * Include business logic explanations
9. **Consider data volume** when creating flows
   * High-frequency data may impact performance
   * Multiple outputs multiply processing requirements

#### Security

10. **Secure your MQTT connections** with SSL when possible
    * Enable `use_ssl: true` for production environments
    * Use secure ports (typically 8883 for MQTT over SSL)
11. **Rotate credentials** periodically for MQTT endpoints
    * Update credentials every 90 days or after personnel changes
    * Use strong, unique passwords for each endpoint
12. **Use unique client IDs** for each MQTT endpoint
    * Avoid connection conflicts by using distinctive IDs
    * Consider including account ID and purpose in the client ID
13. **Restrict topic access** on your MQTT broker
    * Limit permissions to only necessary topics
    * Use topic structures that enable precise access control

#### Maintenance

14. **Back up your flow configurations**
    * Store JSON responses from successful flow creation
    * Document flow purposes and interconnections
15. **Version your flows** with sequential titles
    * Include version numbers in flow titles
    * Maintain a changelog of modifications
16. **Regularly review active flows**
    * Audit flows to ensure they're still needed
    * Remove or disable unused flows to reduce overhead
17. **Keep a library of common patterns**
    * Reuse successful flow patterns across applications
    * Standardize approaches to similar problems

#### Data security considerations

When working with the Navixy IoT Logic API:

1. **API Keys**: Protect your API keys as they provide full access to your account
2. **MQTT Credentials**: Use strong passwords for MQTT authentication
3. **SSL**: Enable SSL (`use_ssl: true`) for MQTT connections whenever possible
4. **Data Privacy**: Be mindful of what device data you transmit to external systems
5. **Endpoint Security**: Regularly audit your endpoints and disable unused ones

## Troubleshooting

| Issue                            | Possible Solution                                        |
| -------------------------------- | -------------------------------------------------------- |
| Flow not processing data         | Check that both flow and all nodes have `enabled: true`  |
| MQTT connection failing          | Verify credentials, domain, port, and SSL settings       |
| Data transformations not working | Test expressions in isolation to identify issues         |
| Missing data in output           | Ensure all required attributes are being processed       |
| API errors                       | Double-check JSON syntax and required fields             |
| Flow validation errors           | Ensure node IDs are unique and edges connect valid nodes |
| Unexpected data format           | Verify the calculation expressions in processing nodes   |
| Missing fields in response       | Check if you have all required permissions               |

### Error handling

Common error codes and their solutions:

| Error Code | Description         | Solution                                     |
| ---------- | ------------------- | -------------------------------------------- |
| 1          | Database error      | Check your data format and try again         |
| 2          | Invalid parameters  | Ensure all required fields are provided      |
| 3          | Access denied       | Check your API key and permissions           |
| 4          | Resource not found  | Verify IDs for flows and endpoints           |
| 5          | Rate limit exceeded | Reduce request frequency                     |
| 6          | Validation error    | Check flow structure for circular references |

#### Error troubleshooting guide

When encountering API errors:

1. **Check request format**
   * Verify JSON syntax is correct
   * Ensure all required fields are included
2. **Validate authentication**
   * Confirm API key format includes "NVX " prefix
   * Check that your key has required permissions
3. **Review error response details**
   * The `description` field often provides specific guidance
   * Note the exact error code for documentation reference
4. **Test with minimal examples**
   * Reduce request complexity to isolate issues
   * Start with known working examples
5. **Implement proper error handling**
   * Design applications to handle API errors gracefully
   * Include retry logic with exponential backoff for rate limiting
