# Managing your flows and endpoints

## Prerequisites

For this example, let's presume that we have already:

1. Created an MQTT output endpoint with ID 45678 using `/iot/logic/flow/endpoint/create`
2. Created a flow with ID 1234 using `/iot/logic/flow/create` with the following components:
   - A data source node (ID: 1) that captures data from devices 12345, 12346, and 12347
   - An attribute calculation node (ID: 2) for basic metrics
   - An output endpoint node (ID: 3) that sends data to the MQTT endpoint

## Viewing your flows

To see all your existing flows, send the request:

### [GET /iot/logic/flow/list](IoT_Logic.json/paths/~1iot~1logic~1flow~1list/get)

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

## Viewing flow details

To see the details of a specific flow, send the request:

### [GET /iot/logic/flow/read](IoT_Logic.json/paths/~1iot~1logic~1flow~1read/get)

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

## Updating a flow

Let's add another processing rule to calculate engine temperature in Celsius:

### [POST /iot/logic/flow/update](IoT_Logic.json/paths/~1iot~1logic~1flow~1update/post)

Request body:
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

Response:
```json
{
  "success": true
}
```

<!-- theme: success -->
> **Congratulations!**<br>
> You've now successfully enhanced your data flow by:
> - Adding an engine temperature conversion calculation (Fahrenheit to Celsius)
> - Maintaining your existing business metrics calculations
> - Updating your flow while preserving the connection to your fleet vehicles and MQTT endpoint