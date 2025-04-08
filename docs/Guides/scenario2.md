---
stoplight-id: 14s9rqt7rrkvq
---

# Managing your flows and endpoints

## Viewing Your Flows

To see all your existing flows:

```http
GET /iot/logic/flow/list
```

Response:
```json
{
  "success": true,
  "list": [
    {
      "id": 1234,
      "title": "Fleet Data to External System"
    }
  ]
}
```

## Viewing Flow Details

To see the details of a specific flow:

```http
GET /iot/logic/flow/read
```

Request body:
```json
{
  "flow_id": 1234
}
```

The response will include all nodes, edges, and settings for the flow.

## Updating a Flow

Let's add another processing rule to calculate engine temperature in Celsius:

```http
POST /iot/logic/flow/update
```

Request body (showing only the relevant changes):
```json
{
  "flow": {
    "id": 1234,
    "title": "Fleet Data to External System",
    "enabled": true,
    "nodes": [
      {
        "id": 1,
        "type": "data_source",
        "title": "Fleet Vehicles",
        "enabled": true,
        "data": {
          "sources": [12345, 12346, 12347]
        },
        "view": {
          "position": { "x": 50, "y": 50 }
        }
      },
      {
        "id": 2,
        "type": "initiate_attributes",
        "title": "Calculate Business Metrics",
        "data": {
          "items": [
            {
              "name": "fuel_efficiency",
              "value": "distance_traveled / fuel_consumed",
              "generation_time": "now()",
              "server_time": "now()"
            },
            {
              "name": "idle_time_percent",
              "value": "(idle_time / (idle_time + moving_time)) * 100",
              "generation_time": "now()",
              "server_time": "now()"
            },
            {
              "name": "vehicle_status",
              "value": "speed > 0 ? 'moving' : (engine_on ? 'idle' : 'stopped')",
              "generation_time": "now()",
              "server_time": "now()"
            },
            {
              "name": "engine_temp_celsius",
              "value": "(engine_temp_f - 32) * 5/9",
              "generation_time": "now()",
              "server_time": "now()"
            }
          ]
        },
        "view": {
          "position": { "x": 200, "y": 50 }
        }
      },
      {
        "id": 3,
        "type": "output_endpoint",
        "title": "Send to External System",
        "enabled": true,
        "data": {
          "output_endpoint_type": "output_mqtt_client",
          "output_endpoint_id": 45678
        },
        "view": {
          "position": { "x": 350, "y": 50 }
        }
      }
    ],
    "edges": [
      {
        "from": 1,
        "to": 2
      },
      {
        "from": 2,
        "to": 3
      }
    ]
  }
}
```

## Managing Endpoints

### Listing Your Endpoints

```http
POST /iot/logic/flow/endpoint/list
```

Response:
```json
{
  "success": true,
  "list": [
    {
      "id": 45678,
      "title": "External MQTT System",
      "type": "output_mqtt_client",
      "status": "active",
      "properties": {
        /* endpoint properties */
      }
    }
  ]
}
```

### Updating an Endpoint

To update an endpoint's connection details:

```http
POST /iot/logic/flow/endpoint/update
```

Request body:
```json
{
  "endpoint": {
    "id": 45678,
    "title": "External MQTT System (Updated)",
    "type": "output_mqtt_client",
    "status": "active",
    "properties": {
      "protocol": "NGP",
      "domain": "new-mqtt.mycompany.com",
      "port": 8883,
      "client_id": "navixy-integration",
      "qos": 1,
      "topics": ["fleet/vehicles/data/v2"],
      "version": "5.0",
      "use_ssl": true,
      "mqtt_auth": true,
      "user_name": "mqtt_username",
      "user_password": "updated_password"
    }
  }
}
```
