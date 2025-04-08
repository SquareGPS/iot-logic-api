# Sending device data to an external MQTT system

Let's create a complete workflow to send your device data to an external MQTT broker.

## Step 1: Create an MQTT Output Endpoint

First, we need to define where the data will be sent:

### [POST /iot/logic/flow/endpoint/create](../../IoT_Logic.json/paths/~1iot~1logic~1flow~1endpoint~1create/post)

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

## Step 2: Create a data source endpoint

Next, we need to create a data source endpoint to connect to your devices:

### [POST /iot/logic/flow/endpoint/create](../../IoT_Logic.json/paths/~1iot~1logic~1flow~1endpoint~1create/post)

Request body:
```json
{
  "endpoint": {
    "title": "Fleet Vehicles Data Source",
    "type": "input_navixy",
    "status": "active",
    "properties": {
      "sources": [12345, 12346, 12347]
    }
  }
}
```

> Ensure the device IDs (12345, 12346, 12347 in this example) are valid and registered in your Navixy system.

The response will include the endpoint ID that we'll need later:
```json
{
  "success": true,
  "id": 56789
}
```

## Step 3: Create a complete flow

Now we'll create the complete flow that connects your data source endpoint to the MQTT endpoint:

### [POST /iot/logic/flow/create](../../IoT_Logic.json/paths/~1iot~1logic~1flow~1create/post)

Request body:
```json
{
  "flow": {
    "title": "Fleet data to external system",
    "enabled": true,
    "nodes": [
      {
        "id": 1,
        "type": "data_source",
        "title": "Fleet vehicles",
        "enabled": true,
        "data": {
          "sources": [56789]
        },
        "view": {
          "position": { "x": 50, "y": 50 }
        }
      },
      {
        "id": 2,
        "type": "output_endpoint",
        "title": "Send to external system",
        "enabled": true,
        "data": {
          "output_endpoint_type": "output_mqtt_client",
          "output_endpoint_id": 45678
        },
        "view": {
          "position": { "x": 250, "y": 50 }
        }
      }
    ],
    "edges": [
      {
        "from": 1,
        "to": 2
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
<!-- theme: success -->
> **Congratulations!**<br>
> You've now set up a complete flow that:
> - Connects to multiple vehicles in your fleet through a data source endpoint
> - Sends the device data to your external MQTT system
> - Uses your custom MQTT broker settings for secure data transfer