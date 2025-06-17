---
stoplight-id: cs3amob44lhu6
---

# Advanced configurations

## API resource relationships

Before diving into advanced configurations, it's important to understand the relationship between API resources:

```
User Account
    └── Flows (multiple)
        ├── Nodes/Endpoints (multiple per flow)
        └── Edges (connections between nodes)
```

Each Flow belongs to a user account, and Nodes/Endpoints are resources that can be shared across multiple flows.

## Flow and node schemas

The API defines several schemas that are important to understand:

- `FlowDraft`: Used when creating a new flow (without ID)
- `Flow`: Used when updating an existing flow (includes ID)
- `Node`: The base type for all nodes in a flow
- `Edge`: Defines connections between nodes

Each node has a specific subtype (`NodeDataSource`, `NodeInitiateAttributes`, `NodeOutputEndpoint`) with different required properties.

## Multiple output destinations

This scenario demonstrates how to configure a flow to send data to multiple destinations simultaneously. This is useful when you need to distribute processed IoT data to different systems, for example:

- Storing data in Navixy platform for tracking and analytics.
- Sending real-time updates to an external system for immediate alerting or reporting. 

The flow processes data once and then branches it to multiple output endpoints, ensuring data consistency across all destinations.

### Prerequisites

For this example, let's presume that we have already:
- Created a flow with ID 1234 containing nodes 1, 2, and 3
- Created an MQTT output endpoint with ID 44551
- Node 1 is a data source node
- Node 2 and 3 are transformation nodes that process temperature data
- The existing flow has edges connecting node 1 to 2, and node 2 to 3

### Updating a flow with multiple output endpoints

[POST /iot/logic/flow/update](../../IoT_Logic.json/paths/~1iot~1logic~1flow~1update/post) 

The flow update operation allows you to modify the entire flow structure, including adding new output endpoints and creating the necessary connections. In this example, we're adding two output endpoint nodes that will receive the same processed data from the transformation chain. This creates a branching pattern where data goes through the processing nodes and then splits to multiple destinations simultaneously.

> You can also create a completely new flow with this configuration by using [POST /iot/logic/flow/create](../../IoT_Logic.json/paths/~1iot~1logic~1flow~1create/post)

To update an existing flow with additional output destinations, send the following request:

```bash
curl -X POST "https://api.eu.navixy.com/v2/iot/logic/flow/update" \
  -H "Authorization: NVX your_session_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "flow": {
      "id": 1234,
      "title": "Temperature Monitoring Flow",
      "description": null,
      "enabled": true,
      "default_flow": false,
      "nodes": [
        {
          "id": 1,
          "type": "data_source",
          "view": {
            "position": { "x": 50, "y": 50 }
          },
          "data": {
            "title": "Temperature Sensors",
            "source_ids": [123458]
          }
        },
        {
          "id": 2,
          "type": "initiate_attributes",
          "view": {
            "position": { "x": 150, "y": 50 }
          },
          "data": {
            "title": "Basic Calculations",
            "items": [
              {
                "name": "temp_celsius",
                "value": "(value(\"raw_temp\") - 32) * 5/9",
                "generation_time": "genTime(\"raw_temp\", 0, \"valid\")",
                "server_time": "now()"
              }
            ]
          }
        },
        {
          "id": 3,
          "type": "initiate_attributes",
          "view": {
            "position": { "x": 250, "y": 50 }
          },
          "data": {
            "title": "Advanced Calculations",
            "items": [
              {
                "name": "temp_status_numeric",
                "value": "value(\"temp_celsius\") / 10",
                "generation_time": "genTime(\"temp_celsius\", 0, \"valid\")",
                "server_time": "now()"
              }
            ]
          }
        },
        {
          "id": 4,
          "type": "output_endpoint",
          "view": {
            "position": { "x": 350, "y": 25 }
          },
          "data": {
            "title": "Send to Navixy",
            "output_endpoint_type": "output_default"
          }
        },
        {
          "id": 5,
          "type": "output_endpoint",
          "view": {
            "position": { "x": 350, "y": 75 }
          },
          "data": {
            "title": "Send to MQTT",
            "output_endpoint_type": "output_mqtt_client",
            "output_endpoint_id": 44551
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
  }'
```

You will receive thes request status in response:

```json
{
  "success": true
}
```

### Try it out

```EUserver json http
{
  "method": "post",
  "url": "https://api.eu.navixy.com/v2/iot/logic/flow/update",
  "headers": {
    "Authorization": "NVX your_hash_here"
  },
  "body": {
    "flow": {
      "id": 1234,
      "title": "Temperature Monitoring Flow1",
      "description": null,
      "enabled": true,
      "default_flow": false,
      "nodes": [
        {
          "id": 1,
          "type": "data_source",
          "view": {
            "position": { "x": 50, "y": 50 }
          },
          "data": {
            "title": "Temperature Sensors",
            "source_ids": [123458]
          }
        },
        {
          "id": 2,
          "type": "initiate_attributes",
          "view": {
            "position": { "x": 150, "y": 50 }
          },
          "data": {
            "title": "Basic Calculations",
            "items": [
              {
                "name": "temp_celsius",
                "value": "(value(\"raw_temp\") - 32) * 5/9",
                "generation_time": "genTime(\"raw_temp\", 0, \"valid\")",
                "server_time": "now()"
              }
            ]
          }
        },
        {
          "id": 3,
          "type": "initiate_attributes",
          "view": {
            "position": { "x": 250, "y": 50 }
          },
          "data": {
            "title": "Advanced Calculations",
            "items": [
              {
                "name": "temp_status_numeric",
                "value": "value(\"temp_celsius\") / 10",
                "generation_time": "genTime(\"temp_celsius\", 0, \"valid\")",
                "server_time": "now()"
              }
            ]
          }
        },
        {
          "id": 4,
          "type": "output_endpoint",
          "view": {
            "position": { "x": 350, "y": 25 }
          },
          "data": {
            "title": "Send to Navixy",
            "output_endpoint_type": "output_default"
          }
        },
        {
          "id": 5,
          "type": "output_endpoint",
          "view": {
            "position": { "x": 350, "y": 75 }
          },
          "data": {
            "title": "Send to MQTT",
            "output_endpoint_type": "output_mqtt_client",
            "output_endpoint_id": 44551
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
}
```

```USserver json http
{
  "method": "post",
  "url": "https://api.us.navixy.com/v2/iot/logic/flow/update",
  "headers": {
    "Authorization": "NVX your_hash_here"
  },
  "body": {
    "flow": {
      "id": 1234,
      "title": "Temperature Monitoring Flow1",
      "description": null,
      "enabled": true,
      "default_flow": false,
      "nodes": [
        {
          "id": 1,
          "type": "data_source",
          "view": {
            "position": { "x": 50, "y": 50 }
          },
          "data": {
            "title": "Temperature Sensors",
            "source_ids": [123458]
          }
        },
        {
          "id": 2,
          "type": "initiate_attributes",
          "view": {
            "position": { "x": 150, "y": 50 }
          },
          "data": {
            "title": "Basic Calculations",
            "items": [
              {
                "name": "temp_celsius",
                "value": "(value(\"raw_temp\") - 32) * 5/9",
                "generation_time": "genTime(\"raw_temp\", 0, \"valid\")",
                "server_time": "now()"
              }
            ]
          }
        },
        {
          "id": 3,
          "type": "initiate_attributes",
          "view": {
            "position": { "x": 250, "y": 50 }
          },
          "data": {
            "title": "Advanced Calculations",
            "items": [
              {
                "name": "temp_status_numeric",
                "value": "value(\"temp_celsius\") / 10",
                "generation_time": "genTime(\"temp_celsius\", 0, \"valid\")",
                "server_time": "now()"
              }
            ]
          }
        },
        {
          "id": 4,
          "type": "output_endpoint",
          "view": {
            "position": { "x": 350, "y": 25 }
          },
          "data": {
            "title": "Send to Navixy",
            "output_endpoint_type": "output_default"
          }
        },
        {
          "id": 5,
          "type": "output_endpoint",
          "view": {
            "position": { "x": 350, "y": 75 }
          },
          "data": {
            "title": "Send to MQTT",
            "output_endpoint_type": "output_mqtt_client",
            "output_endpoint_id": 44551
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
}
```

#### Verifying the flow configuration

You can then validate the configuration of the updated flow using the `read` endpoint: [POST /iot/logic/flow/read](../../IoT_Logic.json/paths/~1iot~1logic~1flow~1read/post)

<!-- theme: success -->
> **Congratulations!**<br>
> You have successfully configured a flow to send processed data to multiple destinations simultaneously. This setup allows your IoT data to be processed once and then distributed to both Navixy platform and an external system.

## Complex data transformations

This scenario demonstrates how to create a flow with multiple data transformation steps for more advanced processing needs. Complex transformations are essential when working with sophisticated IoT applications that require multi-stage data processing, sequential computation paths, and the combination of multiple sensor inputs into derived metrics. This pattern shows how to build processing pipelines that can handle chained data streams, perform sequential calculations on different attributes, and then combine the results for comprehensive analysis.

### Prerequisites

For this example, let's presume that we have already:
- Created a flow with ID 5678
- Added a data source node with ID 1 that reads from sensor ID 98765

### Adding multiple transformation nodes

[POST /iot/logic/flow/update](../../IoT_Logic.json/paths/~1iot~1logic~1flow~1update/post)

This example updates a flow with sequential branches that process temperature and humidity data in series before combining them into advanced analytics. The flow demonstrates several important patterns: sequential processing of different sensor attributes, chained transformation steps, and the accumulation of multiple data transformations into unified analysis nodes. This approach is particularly useful for environmental monitoring, industrial sensors, or any scenario where multiple related measurements need to be processed through different algorithms in a specific order before being combined.

> You can also create a completely new flow with this configuration by using [POST /iot/logic/flow/create](../../IoT_Logic.json/paths/~1iot~1logic~1flow~1create/post)

To update an existing flow with additional output destinations, send the following request:

```bash
curl -X POST "https://api.eu.navixy.com/v2/iot/logic/flow/update" \
  -H "Authorization: NVX your_session_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "flow": {
      "id": 5678,
      "title": "Sensor Data Processing Flow",
      "description": null,
      "enabled": true,
      "default_flow": false,
      "nodes": [
        {
          "id": 1,
          "type": "data_source",
          "view": {
            "position": { "x": 50, "y": 50 }
          },
          "data": {
            "title": "Environmental Sensors",
            "source_ids": [98765]
          }
        },
        {
          "id": 2,
          "type": "initiate_attributes",
          "view": {
            "position": { "x": 150, "y": 25 }
          },
          "data": {
            "title": "Temperature Processing",
            "items": [
              {
                "name": "temp_celsius",
                "value": "(value(\"analog_1\") - 32) * 5/9",
                "generation_time": "genTime(\"analog_1\", 0, \"valid\")",
                "server_time": "now()"
              }
            ]
          }
        },
        {
          "id": 3,
          "type": "initiate_attributes",
          "view": {
            "position": { "x": 150, "y": 75 }
          },
          "data": {
            "title": "Humidity Processing",
            "items": [
              {
                "name": "humidity_adjusted",
                "value": "value(\"analog_2\") * 1.05",
                "generation_time": "genTime(\"analog_2\", 0, \"valid\")",
                "server_time": "now()"
              }
            ]
          }
        },
        {
          "id": 4,
          "type": "initiate_attributes",
          "view": {
            "position": { "x": 250, "y": 50 }
          },
          "data": {
            "title": "Combined Analysis",
            "items": [
              {
                "name": "heat_index",
                "value": "value(\"temp_celsius\") + (0.05 * value(\"humidity_adjusted\"))",
                "generation_time": "genTime(\"temp_celsius\", 0, \"valid\")",
                "server_time": "now()"
              },
              {
                "name": "comfort_score",
                "value": "value(\"heat_index\") / 10",
                "generation_time": "genTime(\"heat_index\", 0, \"valid\")",
                "server_time": "now()"
              }
            ]
          }
        },
        {
          "id": 5,
          "type": "output_endpoint",
          "view": {
            "position": { "x": 350, "y": 50 }
          },
          "data": {
            "title": "Send to Navixy",
            "output_endpoint_type": "output_default"
          }
        }
      ],
      "edges": [
        {"from": 1, "to": 2},
        {"from": 2, "to": 3},
        {"from": 3, "to": 4},
        {"from": 4, "to": 5}
      ]
    }
  }'
```

You will receive thes request status in response:

```json
{
  "success": true
}
```

### Try it out

```EUserver json http
{
  "method": "post",
  "url": "https://api.eu.navixy.com/v2/iot/logic/flow/update",
  "headers": {
    "Authorization": "NVX your_hash_here"
  },
  "body": {
    "flow": {
      "id": 5678,
      "title": "Sensor Data Processing Flow",
      "description": null,
      "enabled": true,
      "default_flow": false,
      "nodes": [
        {
          "id": 1,
          "type": "data_source",
          "view": {
            "position": { "x": 50, "y": 50 }
          },
          "data": {
            "title": "Environmental Sensors",
            "source_ids": [98765]
          }
        },
        {
          "id": 2,
          "type": "initiate_attributes",
          "view": {
            "position": { "x": 150, "y": 25 }
          },
          "data": {
            "title": "Temperature Processing",
            "items": [
              {
                "name": "temp_celsius",
                "value": "(value(\"analog_1\") - 32) * 5/9",
                "generation_time": "now()",
                "server_time": "now()"
              }
            ]
          }
        },
        {
          "id": 3,
          "type": "initiate_attributes",
          "view": {
            "position": { "x": 150, "y": 75 }
          },
          "data": {
            "title": "Humidity Processing",
            "items": [
              {
                "name": "humidity_adjusted",
                "value": "value(\"analog_2\") * 1.05",
                "generation_time": "now()",
                "server_time": "now()"
              }
            ]
          }
        },
        {
          "id": 4,
          "type": "initiate_attributes",
          "view": {
            "position": { "x": 250, "y": 50 }
          },
          "data": {
            "title": "Combined Analysis",
            "items": [
              {
                "name": "heat_index",
                "value": "value(\"temp_celsius\") + (0.05 * value(\"humidity_adjusted\"))",
                "generation_time": "now()",
                "server_time": "now()"
              }
            ]
          }
        },
        {
          "id": 5,
          "type": "output_endpoint",
          "view": {
            "position": { "x": 350, "y": 50 }
          },
          "data": {
            "title": "Send to Navixy",
            "output_endpoint_type": "output_default"
          }
        }
      ],
      "edges": [
        {"from": 1, "to": 2},
        {"from": 2, "to": 3},
        {"from": 3, "to": 4},
        {"from": 4, "to": 5}
      ]
    }
  }
}
```

```USserver json http
{
  "method": "post",
  "url": "https://api.us.navixy.com/v2/iot/logic/flow/update",
  "headers": {
    "Authorization": "NVX your_hash_here"
  },
  "body": {
    "flow": {
      "id": 5678,
      "title": "Sensor Data Processing Flow",
      "description": null,
      "enabled": true,
      "default_flow": false,
      "nodes": [
        {
          "id": 1,
          "type": "data_source",
          "view": {
            "position": { "x": 50, "y": 50 }
          },
          "data": {
            "title": "Environmental Sensors",
            "source_ids": [98765]
          }
        },
        {
          "id": 2,
          "type": "initiate_attributes",
          "view": {
            "position": { "x": 150, "y": 25 }
          },
          "data": {
            "title": "Temperature Processing",
            "items": [
              {
                "name": "temp_celsius",
                "value": "(value(\"analog_1\") - 32) * 5/9",
                "generation_time": "now()",
                "server_time": "now()"
              }
            ]
          }
        },
        {
          "id": 3,
          "type": "initiate_attributes",
          "view": {
            "position": { "x": 150, "y": 75 }
          },
          "data": {
            "title": "Humidity Processing",
            "items": [
              {
                "name": "humidity_adjusted",
                "value": "value(\"analog_2\") * 1.05",
                "generation_time": "now()",
                "server_time": "now()"
              }
            ]
          }
        },
        {
          "id": 4,
          "type": "initiate_attributes",
          "view": {
            "position": { "x": 250, "y": 50 }
          },
          "data": {
            "title": "Combined Analysis",
            "items": [
              {
                "name": "heat_index",
                "value": "value(\"temp_celsius\") + (0.05 * value(\"humidity_adjusted\"))",
                "generation_time": "now()",
                "server_time": "now()"
              }
            ]
          }
        },
        {
          "id": 5,
          "type": "output_endpoint",
          "view": {
            "position": { "x": 350, "y": 50 }
          },
          "data": {
            "title": "Send to Navixy",
            "output_endpoint_type": "output_default"
          }
        }
      ],
      "edges": [
        {"from": 1, "to": 2},
        {"from": 2, "to": 3},
        {"from": 3, "to": 4},
        {"from": 4, "to": 5}
      ]
    }
  }
}
```

#### Verifying the flow configuration

You can then validate the configuration of the updated flow using the `read` endpoint: [POST /iot/logic/flow/read](../../IoT_Logic.json/paths/~1iot~1logic~1flow~1read/post)

<!-- theme: success -->
> **Congratulations!**<br>
> You have successfully built a complex data transformation chain that processes multiple sensor inputs through a series of calculations. This flow demonstrates advanced patterns including:
> 
> 1. Sequential processing of different sensor attributes (temperature and humidity)
> 2. Chaining processed data through multiple transformation steps into a unified analysis
> 3. Creating derived values that reference previously calculated attributes from earlier nodes
> 
> This type of multi-step transformation is powerful for implementing complex business logic and data processing requirements within your IoT system, allowing each processing stage to build upon the results of previous calculations.