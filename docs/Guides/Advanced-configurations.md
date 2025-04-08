---
stoplight-id: cs3amob44lhu6
---

# Advanced configurations

## API Resource Relationships

Before diving into advanced configurations, it's important to understand the relationship between API resources:

```
User Account
  └── Flows (multiple)
       ├── Nodes (multiple per flow)
       └── Edges (connections between nodes)
  └── Endpoints (shared across flows)
```

Each flow belongs to a user account, and endpoints are resources that can be shared across multiple flows.

## Flow and Node Schemas

The API defines several schemas that are important to understand:

- `FlowDraft`: Used when creating a new flow (without ID)
- `Flow`: Used when updating an existing flow (includes ID)
- `Node`: The base type for all nodes in a flow
- `Edge`: Defines connections between nodes

Each node has a specific subtype (`NodeDataSource`, `NodeInitiateAttributes`, `NodeOutputEndpoint`) with different required properties.

## Multiple Output Destinations

You can send data to multiple destinations by adding more output nodes:

```http
POST /iot/logic/flow/update
```

Request body (showing only new node and edges):
```json
{
  "flow": {
    "id": 1234,
    /* existing flow properties */
    "nodes": [
      /* existing nodes 1, 2, 3 */
      {
        "id": 4,
        "type": "output_endpoint",
        "title": "Send to Navixy",
        "enabled": true,
        "data": {
          "output_endpoint_type": "output_navixy"
        },
        "view": {
          "position": { "x": 350, "y": 150 }
        }
      }
    ],
    "edges": [
      {"from": 1, "to": 2},
      {"from": 2, "to": 3},
      {"from": 2, "to": 4}
    ]
  }
}
```

This setup will now send the processed data to both your external MQTT system and Navixy simultaneously.

## Complex Data Transformations

For more advanced data processing, you can create multiple transformation nodes in sequence:

```http
POST /iot/logic/flow/update
```

Request body (showing node chain):
```json
{
  "flow": {
    "id": 1234,
    /* existing flow properties */
    "nodes": [
      /* data source node */
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
      /* output nodes */
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

This creates a pipeline of transformations where each node can use attributes created by previous nodes.
