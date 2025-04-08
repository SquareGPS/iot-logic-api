---
stoplight-id: v3pj5ugo604ke
---

# Sending device data to an external MQTT system

Let's create a complete workflow to send your device data to an external MQTT broker.

## Step 1: Create an MQTT Endpoint

First, we need to define where the data will be sent:

```http
POST /iot/logic/flow/endpoint/create
```

Request body:
```json
{
  "endpoint": {
    "title": "External MQTT System",
    "type": "output_mqtt_client",
    "status": "active",
    "properties": {
      "protocol": "NGP",
      "domain": "mqtt.mycompany.com",
      "port": 1883,
      "client_id": "navixy-integration",
      "qos": 1,
      "topics": ["fleet/vehicles/data"],
      "version": "5.0",
      "use_ssl": true,
      "mqtt_auth": true,
      "user_name": "mqtt_username",
      "user_password": "mqtt_password"
    }
  }
}
```

The response will include the endpoint ID that we'll need later:
```json
{
  "success": true,
  "id": 45678
}
```

## Step 2: Create a Flow with Data Processing

Now we'll create a flow that:
1. Takes data from your devices
2. Processes it to calculate useful metrics
3. Sends it to your MQTT system

```http
POST /iot/logic/flow/create
```

Request body:
```json
{
  "flow": {
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

The response will include the flow ID:
```json
{
  "success": true,
  "id": 1234
}
```

## Congratulations! 

You've now set up a complete flow that:
- Collects data from multiple vehicles
- Calculates business-relevant metrics like fuel efficiency
- Determines vehicle operational status
- Sends all this processed data to your external MQTT system