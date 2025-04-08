---
stoplight-id: cs3amob44lhu6
---

# Advanced configurations

## API resource relationships

Before diving into advanced configurations, it's important to understand the relationship between API resources:

```
User Account
  └── Flows (multiple)
       ├── Nodes (multiple per flow)
       └── Edges (connections between nodes)
  └── Endpoints (shared across flows)
```

Each flow belongs to a user account, and endpoints are resources that can be shared across multiple flows.

## Flow and node schemas

The API defines several schemas that are important to understand:

- `FlowDraft`: Used when creating a new flow (without ID)
- `Flow`: Used when updating an existing flow (includes ID)
- `Node`: The base type for all nodes in a flow
- `Edge`: Defines connections between nodes

Each node has a specific subtype (`NodeDataSource`, `NodeInitiateAttributes`, `NodeOutputEndpoint`) with different required properties.

## Multiple output destinations

This scenario demonstrates how to configure a flow to send data to multiple destinations simultaneously.

### Prerequisites

For this example, let's presume that we have already:
- Created a flow with ID 1234 containing nodes 1, 2, and 3
- Created an MQTT output endpoint with ID 44551
- Node 1 is a data source node
- Node 2 and 3 are transformation nodes that process temperature data
- The existing flow has edges connecting node 1 to 2, and node 2 to 3

### Updating a flow with multiple output endpoints

We'll update the existing flow to send the processed data to both Navixy and our MQTT endpoint:

#### [POST /iot/logic/flow/update](IoT_Logic.json/paths/~1iot~1logic~1flow~1update/post) 

Request body:
```json
{
  "flow": {
    "id": 1234,
    "title": "Temperature Monitoring Flow",
    "enabled": true,
    "nodes": [
      {
        "id": 1,
        "type": "data_source",
        "title": "Temperature Sensors",
        "enabled": true,
        "data": {
          "sources": [123458]
        },
        "view": {
          "position": { "x": 50, "y": 50 }
        }
      },
      {
        "id": 2,
        "type": "initiate_attributes",
        "title": "Basic Calculations",
        "data": {
          "items": [
            {
              "name": "temp_celsius",
              "value": "(raw_temp - 32) * 5/9",
              "generation_time": "now()",
              "server_time": "now()"
            }
          ]
        },
        "view": {
          "position": { "x": 150, "y": 50 }
        }
      },
      {
        "id": 3,
        "type": "initiate_attributes",
        "title": "Advanced Calculations",
        "data": {
          "items": [
            {
              "name": "temp_status",
              "value": "temp_celsius > 90 ? 'critical' : (temp_celsius > 70 ? 'warning' : 'normal')",
              "generation_time": "now()",
              "server_time": "now()"
            }
          ]
        },
        "view": {
          "position": { "x": 250, "y": 50 }
        }
      },
      {
        "id": 4,
        "type": "output_endpoint",
        "title": "Send to Navixy",
        "enabled": true,
        "data": {
          "output_endpoint_type": "output_navixy"
        },
        "view": {
          "position": { "x": 350, "y": 25 }
        }
      },
      {
        "id": 5,
        "type": "output_endpoint",
        "title": "Send to MQTT",
        "enabled": true,
        "data": {
          "output_endpoint_type": "output_mqtt_client",
          "output_endpoint_id": 44551
        },
        "view": {
          "position": { "x": 350, "y": 75 }
        }
      }
    ],
    "edges": [
      {"from": 1, "to": 2},
      {"from": 2, "to": 3},
      {"from": 3, "to": 4},
      {"from": 3, "to": 5}
    ]
  }
}
```

Response:
```json
{
  "success": true
}
```

### Verifying the flow configuration

#### [GET /iot/logic/flow/read](IoT_Logic.json/paths/~1iot~1logic~1flow~1read/get)

Request body:
```json
{
  "flow_id": 1234
}
```

Response:
```json
{
  "success": true,
  "value": {
    "id": 1234,
    "title": "Temperature Monitoring Flow",
    "enabled": true,
    "nodes": [
      /* Node details as in the update request */
    ],
    "edges": [
      {"from": 1, "to": 2},
      {"from": 2, "to": 3},
      {"from": 3, "to": 4},
      {"from": 3, "to": 5}
    ]
  }
}
```
<!-- theme: success -->
> **Congratulations!**<br>
> You have successfully configured a flow to send processed data to multiple destinations simultaneously. This setup allows your IoT data to be processed once and then distributed to both Navixy's internal system and an external MQTT broker.



## Complex data transformations

This scenario demonstrates how to create a flow with multiple data transformation steps for more advanced processing needs.

### Prerequisites

For this example, let's presume that we have already:
- Created a flow with ID 5678
- Added a data source node with ID 1 that reads from sensor ID 98765

### Adding multiple transformation nodes

#### [POST /iot/logic/flow/update](IoT_Logic.json/paths/~1iot~1logic~1flow~1update/post)

Request body:
```json
{
  "flow": {
    "id": 5678,
    "title": "Sensor Data Processing Flow",
    "enabled": true,
    "nodes": [
      {
        "id": 1,
        "type": "data_source",
        "title": "Environmental Sensors",
        "enabled": true,
        "data": {
          "sources": [98765]
        },
        "view": {
          "position": { "x": 50, "y": 50 }
        }
      },
      {
        "id": 2,
        "type": "initiate_attributes",
        "title": "Temperature Processing",
        "data": {
          "items": [
            {
              "name": "temp_celsius",
              "value": "(analog_1 - 32) * 5/9",
              "generation_time": "now()",
              "server_time": "now()"
            }
          ]
        },
        "view": {
          "position": { "x": 150, "y": 25 }
        }
      },
      {
        "id": 3,
        "type": "initiate_attributes",
        "title": "Humidity Processing",
        "data": {
          "items": [
            {
              "name": "humidity_adjusted",
              "value": "analog_2 * 1.05",
              "generation_time": "now()",
              "server_time": "now()"
            }
          ]
        },
        "view": {
          "position": { "x": 150, "y": 75 }
        }
      },
      {
        "id": 4,
        "type": "initiate_attributes",
        "title": "Combined Analysis",
        "data": {
          "items": [
            {
              "name": "heat_index",
              "value": "temp_celsius + (0.05 * humidity_adjusted)",
              "generation_time": "now()",
              "server_time": "now()"
            },
            {
              "name": "comfort_level",
              "value": "heat_index < 25 ? 'comfortable' : (heat_index < 35 ? 'warm' : 'hot')",
              "generation_time": "now()",
              "server_time": "now()"
            }
          ]
        },
        "view": {
          "position": { "x": 250, "y": 50 }
        }
      },
      {
        "id": 5,
        "type": "output_endpoint",
        "title": "Send to Navixy",
        "enabled": true,
        "data": {
          "output_endpoint_type": "output_navixy"
        },
        "view": {
          "position": { "x": 350, "y": 50 }
        }
      }
    ],
    "edges": [
      {"from": 1, "to": 2},
      {"from": 1, "to": 3},
      {"from": 2, "to": 4},
      {"from": 3, "to": 4},
      {"from": 4, "to": 5}
    ]
  }
}
```

Response:
```json
{
  "success": true
}
```

### Verifying the flow configuration

#### [GET /iot/logic/flow/read](IoT_Logic.json/paths/~1iot~1logic~1flow~1read/get)

Request body:
```json
{
  "flow_id": 5678
}
```

Response:
```json
{
  "success": true,
  "value": {
    "id": 5678,
    "title": "Sensor Data Processing Flow",
    "enabled": true,
    "nodes": [
      /* Node details as in the update request */
    ],
    "edges": [
      {"from": 1, "to": 2},
      {"from": 1, "to": 3},
      {"from": 2, "to": 4},
      {"from": 3, "to": 4},
      {"from": 4, "to": 5}
    ]
  }
}
```

<!-- theme: success -->
> **Congratulations!**<br>
> You have successfully built a complex data transformation chain that processes multiple sensor inputs through a series of calculations. This flow demonstrates advanced patterns including:
> 
> 1. Parallel processing of different sensor attributes (temperature and humidity)
> 2. Combining processed data from multiple paths into a unified analysis
> 3. Creating derived values using conditional expressions
> 
> This type of multi-step transformation is powerful for implementing complex business logic and data processing requirements within your IoT system.