# Nodes

## Data Source node (`data_source`)

This node specifies which devices will send data to your flow. It's the entry point of all data flows.

{% openapi-schemas spec="iot-logic" schemas="NodeDataSource" grouped="true" %}
[OpenAPI iot-logic](https://raw.githubusercontent.com/SquareGPS/iot-logic-api/refs/heads/main/docs/resources/api-reference/IoT_Logic.json)
{% endopenapi-schemas %}

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

### Usage notes

* The `data_source` node type is required in every flow
* Multiple devices can be specified in the `sources` array
* Each device is identified by its numeric ID in the Navixy system
* A flow can have multiple data source nodes for different device groups

## Initiate Attribute node (`initiate_attribute`)

This node transforms raw data into meaningful information. It allows for creating new attributes or modifying existing ones through expressions.

{% openapi-schemas spec="iot-logic" schemas="NodeInitiateAttributes" grouped="true" %}
[OpenAPI iot-logic](https://raw.githubusercontent.com/SquareGPS/iot-logic-api/refs/heads/main/docs/resources/api-reference/IoT_Logic.json)
{% endopenapi-schemas %}

#### Initiate Attribute node structure

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

### Expression language

For calculations IoT Logic API uses [Navixy IoT Logic Expression Language](../technologies/navixy-iot-logic-expression-language/).\
Here's a guick reference:

| Feature                | Operators/Examples                  | Description                    |
| ---------------------- | ----------------------------------- | ------------------------------ |
| Mathematical operators | `+`, `-`, `*`, `/`, `%`             | Basic arithmetic operations    |
| Functions              | `now()`, `sqrt()`, `pow()`, `abs()` | Built-in functions             |
| Attribute references   | `speed`, `fuel_level`, `analog_1`   | Reference to device attributes |

{% hint style="info" %}
To find more examples of formulas, see [Calculation examples](https://app.gitbook.com/s/446mKak1zDrGv70ahuYZ/guide/account/iot-logic/flow-management/initiate-attribute-node/calculation-examples) in our User docs.
{% endhint %}

**Expression examples**

| Scenario               | Expression                                                | Description                       |
| ---------------------- | --------------------------------------------------------- | --------------------------------- |
| Temperature conversion | `(temperature_f - 32) * 5/9`                              | Convert Fahrenheit to Celsius     |
| Distance calculation   | `sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2))`                 | Calculate distance between points |
| Time-based condition   | `hour(time) >= 22 \|\| hour(time) <= 6 ? 'night' : 'day'` | Determine day/night status        |

### Core functions

**`value(parameter, index, validation_flag)`**

* `parameter` (string): Device parameter or calculated attribute name
* `index` (integer, 0-12, optional): Historical depth (0 = newest). Default: 0
* `validation_flag` (string, optional): "valid" excludes nulls, "all" includes nulls. Default: "valid"

#### Historical data access (`index` )

IoT Logic maintains up to 12 historical values per parameter:

* Index 0: Current value
* Index 1-11: Previous values
* Index 12: Oldest available value

{% hint style="info" %}
Short syntax is also supported for attribute names in formulas. When referencing only the latest valid value of an attribute, you can omit the full `value()` function syntax and quotation marks. For example, the temperature conversion formula can be written as `temperature*1.8 + 32` instead of `value('temperature', 0, 'valid')*1.8 + 32`.
{% endhint %}

### Usage notes

* Multiple attributes can be defined within a single node
* Expressions execute in real-time as device data arrives
* Historical values are stored in memory for high-performance access
* Use validation flags strategically: "valid" for accurate calculations, "all" when null values are meaningful
* Calculated attributes become available in Data Stream Analyzer and can create custom sensors in Navixy Tracking module when connected to Default Output Endpoint

## Logic node (`logic`)

This node creates conditional branching points that route incoming data down different paths based on logical expressions. It evaluates conditions against real-time data and creates boolean attributes for monitoring and decision-making.

{% openapi-schemas spec="iot-logic" schemas="NodeLogic" grouped="true" %}
[OpenAPI iot-logic](https://raw.githubusercontent.com/SquareGPS/iot-logic-api/refs/heads/main/docs/resources/api-reference/IoT_Logic.json)
{% endopenapi-schemas %}

#### Logic node structure

```json
{
  "id": 2,
  "type": "logic",
  "data": {
    "title": "Temperature Alert Check",
    "name": "high_temperature_alert",
    "condition": "value('temperature', 0, 'valid') > 75"
  },
  "view": {
    "position": { "x": 150, "y": 50 }
  }
}
```

#### Key properties

<table><thead><tr><th width="158.9090576171875">Property</th><th width="103.3636474609375">Type</th><th width="108.5455322265625">Required</th><th>Description</th></tr></thead><tbody><tr><td><code>id</code></td><td>integer</td><td>Yes</td><td>Unique identifier within the flow</td></tr><tr><td><code>type</code></td><td>string</td><td>Yes</td><td>Must be "logic"</td></tr><tr><td><code>data.title</code></td><td>string</td><td>Yes</td><td>Human-readable name for the node</td></tr><tr><td><code>data.name</code></td><td>string</td><td>Yes</td><td>Name for the boolean attribute created by this node</td></tr><tr><td><code>data.condition</code></td><td>string</td><td>Yes</td><td>Logical expression using Navixy IoT Logic Expression Language</td></tr></tbody></table>

#### Output connections

The Logic node supports two output connection types:

**THEN connection (`then_edge`)**

* Activates when the expression evaluates to `true`
* At least one THEN connection is required

**ELSE connection (`else_edge`)**

* Activates when the expression evaluates to `false`, `null`, or encounters errors
* Optional connection

### Expression language

For logical conditions IoT Logic API uses [Navixy IoT Logic Expression Language](../technologies/navixy-iot-logic-expression-language/).

Here's a quick reference:

| Operator category    | Operators                         | Description                       |
| -------------------- | --------------------------------- | --------------------------------- |
| Comparison operators | `==`, `!=`, `<`, `<=`, `>`, `>=`  | Basic comparison operations       |
| Logical operators    | `&&`, `\|\|`, `!`                 | Logical operations (and, or, not) |
| Pattern matching     | `=~`, `!~`                        | Pattern matching operations       |
| String operators     | `=^`, `!^`, `=$`, `!$`            | String comparison operations      |
| Attribute references | `speed`, `fuel_level`, `analog_1` | Reference to device attributes    |

#### Expression examples

| Expression                                                                   | Description                               |
| ---------------------------------------------------------------------------- | ----------------------------------------- |
| `value('temperature', 0, 'valid') > 75`                                      | Temperature monitoring                    |
| `value('speed', 0, 'valid') > 60 && value('current_hour', 0, 'valid') >= 18` | Complex conditions with logical operators |
| `value('lock_state', 0, 'valid') =~ ['locked', 'unlocked']`                  | Pattern matching with arrays              |

### Usage notes

* The Logic node creates a boolean attribute using the `data.name` value
* This attribute appears in Data Stream Analyzer and can be referenced by subsequent nodes
* When expressions cannot be evaluated, the result is treated as `false` and data flows through the ELSE path
* Multiple Logic nodes can be chained together for complex decision trees

## Action node (`action`)

This node executes automated commands when triggered by incoming data. It transforms data flows into device control actions, enabling automated responses to conditions detected in earlier nodes.

{% openapi-schemas spec="iot-logic" schemas="NodeAction" grouped="true" %}
[OpenAPI iot-logic](https://raw.githubusercontent.com/SquareGPS/iot-logic-api/refs/heads/main/docs/resources/api-reference/IoT_Logic.json)
{% endopenapi-schemas %}

#### Action node structure

```json
{
  "id": 4,
  "type": "action",
  "title": "Your Title Here",
  "data": {
    "actions": [
      {
        "number": 1,
        "value": true
      },
      {
        "command": "custom_command_here",
        "reliable": true
      }
    ]
  },
  "view": {
    "position": { "x": 400, "y": 100 }
  }
}
```

#### Key properties

| Property       | Type    | Required | Description                                |
| -------------- | ------- | -------- | ------------------------------------------ |
| `id`           | integer | Yes      | Unique identifier within the flow          |
| `type`         | string  | Yes      | Must be "action"                           |
| `title`        | string  | Yes      | Human-readable name for the node           |
| `data.actions` | array   | Yes      | Array of action definitions (max 10 items) |

### Action types

The Action node supports two types of automated responses:

#### Set Output action

Controls device outputs by switching them on or off.

```json
{
  "number": 1,
  "value": true
}
```

**Properties:**

* `number` (integer, required): Output number (1-8) as shown in device UI
* `value` (boolean, required): The state to set (true = on, false = off)

#### Send Command action

Transmits custom GPRS commands directly to devices.

```json
{
  "command": "engine_block",
  "reliable": true
}
```

**Properties:**

* `command` (string, required): Custom command string (1-512 characters)
* `reliable` (boolean, optional, default: true): Whether to retry if device is offline

### Usage notes

* Action nodes function as **terminal nodes** - they do not pass data to downstream nodes
* Actions execute **sequentially** in the order they appear in the `actions` array
* Commands are sent only to **devices that provided the triggering data**
* Each node can contain **up to 10 actions** of mixed types
* When connected to Logic nodes, actions execute only for devices where the condition evaluated to `true`
* Device compatibility varies - ensure your devices support the specific outputs or commands being configured

#### Action execution behavior

**Device targeting**

* Actions are sent only to devices that provided data in the current trigger event
* This ensures commands reach only the specific devices involved in the condition
* Prevents unnecessary commands to unaffected devices in the fleet

**Sequential processing**

* Multiple actions within a node execute in configured order (top to bottom)
* Each action completes transmission before the next action begins
* Total execution time is typically within seconds of receiving the trigger

**Device validation**

* Individual devices process received commands according to their capabilities
* Supported commands execute immediately upon receipt
* Unsupported commands are received but ignored by the device
* Device safety mechanisms may prevent inappropriate commands (e.g., engine shutdown while moving)

#### Connection patterns

**With Logic nodes (recommended)**

When connected to Logic nodes, actions execute only for devices where the logical condition evaluated to true, providing precise conditional automation.

**Direct connections**

When connected directly to other node types (Data Source, Initiate Attribute), actions execute for all devices in the data stream each time data is received.

### Device compatibility

Action execution depends on individual device capabilities:

* Ensure your devices support the specific outputs or commands you're configuring
* Consult manufacturer documentation for supported command lists
* Test actions in a controlled environment before deploying to production flows
* For device compatibility information, refer to [Navixy integrated devices](https://www.navixy.com/devices/)

## Output endpoint node (`output_endpoint`)

This node defines where your data will be sent. It's the termination point for data flow paths.

{% openapi-schemas spec="iot-logic" schemas="NodeOutputEndpoint" grouped="true" %}
[OpenAPI iot-logic](https://raw.githubusercontent.com/SquareGPS/iot-logic-api/refs/heads/main/docs/resources/api-reference/IoT_Logic.json)
{% endopenapi-schemas %}

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

### Output endpoint types

| Type                 | Description                       | Use Case                              |
| -------------------- | --------------------------------- | ------------------------------------- |
| `output_navixy`      | Default output to Navixy platform | Sending processed data back to Navixy |
| `output_mqtt_client` | External MQTT broker connection   | Integrating with third-party systems  |

<details>

<summary>MQTT endpoint properties</summary>

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

**MQTT QoS levels**

| Level     | Description                                      | Use Case                                                           |
| --------- | ------------------------------------------------ | ------------------------------------------------------------------ |
| **QoS 0** | "At most once" delivery (fire and forget)        | High-volume, non-critical data where occasional loss is acceptable |
| **QoS 1** | "At least once" delivery (acknowledged delivery) | Important messages that must be delivered, can handle duplicates   |
| **QoS 2** | Not currently supported by the API               | -                                                                  |

**MQTT protocol versions**

| Version        | Description                          | Features                                                          |
| -------------- | ------------------------------------ | ----------------------------------------------------------------- |
| **MQTT 3.1.1** | Widely supported version             | Basic pub/sub functionality, broad broker compatibility           |
| **MQTT 5.0**   | Newer version with enhanced features | Message expiry, topic aliases, shared subscriptions, reason codes |

</details>

### Usage notes

* Every flow must have at least one output endpoint node to be functional
* The `output_navixy` type doesn't require a referenced endpoint (built-in)
* The `output_mqtt_client` type requires an `output_endpoint_id` referencing a previously created endpoint
* Multiple output nodes can be used to send the same data to different destinations
* Output nodes are "terminal" - they don't connect to any downstream nodes
