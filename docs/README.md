---
stoplight-id: ie3rt9xv91kie
---

# Navixy IoT Logic API

> _BETA Version!_\
> Now the early access of IoT Logic's API is implemented, which means possible changes in the near future. Feel free to try the functionality, however, you may need to introduce changes in your applications reflecting the API functionality updates. Stay tuned!

## Introduction

**Navixy IoT Logic** is a no-code/low-code tool that enables seamless IoT data processing and integration. Its API provides programmatic access to create, manage, and optimize data flows between IoT devices and destination systems without requiring extensive development resources.

### Purpose and core capabilities

**Navixy IoT Logic** functions as a data flow manager that:

* Receives information from devices connected to the platform
* Decodes and converts data in real-time
* Sends processed data to other platforms and services
* Enables building complex flows with nodes responsible for specific data processing tasks
* Standardizes telematics data through the [Navixy Generic Protocol](https://docs.navixy.com/iot-logic/ngp)

The **IoT Logic API** allows developers and system integrators to programmatically implement these capabilities, making it effective for organizations that need to:

* Work efficiently with decoded device data
* Apply flexible data transformation to match specific business needs
* Monitor and troubleshoot data streams
* Create consistent data flows across multiple devices and protocols

### Key concepts

**Navixy IoT Logic** operates based on two fundamental components that work together to process device data:

#### Flow

A **Flow** is the foundation for all data logic in the product. It defines how data moves through stages of reception, enrichment, and transmission. Each flow consists of connected nodes that determine what happens to the data at each processing stage.

Key characteristics of flows:

* Flows can be enabled or disabled to control data processing
* Every flow requires at least one data source and one output endpoint
* Each device can only be assigned to one flow at a time
* Flows process data in real-time as it arrives from devices

#### Nodes

**Nodes** are the functional elements of a **flow**, with each node handling a specific stage of the data lifecycle. There are three primary types of nodes:

* **Data Source node**: Receives data from M2M devices and serves as the entry point for all device data
* **Initiate Attribute node**: Processes and enriches incoming data, including creating new calculated attributes trough mathematical operations in [Navixy IoT Logic Expression Language](https://docs.navixy.com/iot-logic/navixy-iot-logic-expression-language)
* **Output Endpoint node**: Transmits data to target systems using the [Navixy Generic Protocol](https://docs.navixy.com/iot-logic/ngp). This node can be configured to use different endpoint types:
  * **Default endpoint**: Pre-configured destination for sending data to the Navixy platform
  * **MQTT endpoint**: Configurable connection for sending data to third-party systems and services

Nodes are connected through transitions (`edges`) that define the path data follows through the flow.

### Data flow architecture

The following screenshot from IoT Logic UI illustrates the basic architecture of a flow in IoT Logic:

![Flow-example.png](../assets/images/Flow-example.png)

This represents a simple linear flow where:

1. The **Data Source** node collects telemetry from selected devices
2. The **Initiate Attribute** node processes and enriches this data
3. The **Default Output Endpoint** node delivers the transformed data to its destination - Navixy platform

More complex architectures can be created by:

* Adding multiple data source nodes to process different device types
* Chaining multiple attribute nodes for multi-stage data processing
* Including several output endpoints to deliver data to multiple destinations outside Navixy simultaneously

## Quick start for IoT Logic API

To ensure a clear picture of the basic IoT Logic API capabilities, let's create your first flow.

The following example demonstrates how to create a complete flow with three nodes that sends data to Navixy. This flow will:

1. Collect data from specified devices
2. Calculate temperature in Fahrenheit from Celsius readings
3. Send the enriched data to the Navixy platform

### Step 1: Authentication

First, authenticate to obtain a session token. To do it, send a POST request to the user authentication endpoint `{baseURL}/v2/user/auth` providing your account's login and password as parameters:

```bash
curl -X POST "https://your.server.com/v2/user/auth" \
  -H "Content-Type: application/json" \
  -d '{
    "login": "your_email_or_username",
    "password": "your_password"
  }'
```

Response (example):

```jsonresponse
{
  "success": true,
  "hash": "22eac1c27af4be7b9d04da2ce1af111b"
}
```

Copy the `hash` value from the response.

> For more details on how to authenticate your requests, see [Authentication](authentication.md).

### Step 2: Create a complete flow with nodes and connections

Create a flow with all nodes and connections in a single request:

```bash
curl -X POST "https://your.server.com/iot/logic/flow/create" \
  -H "Content-Type: application/json" \
  -H "Authorization: NVX hash_value" \
  -d '{
    "flow": {                                   
      "title": "Basic Temperature Monitoring",
      "enabled": true,                          
      "nodes": [                                
        {
          "id": 1,                              
          "type": "data_source",
          "enabled": true,
          "data": {                             
            "title": "Fleet Vehicles",
            "sources": [394892, 394893, 394894] 
          },
          "view": {                             
            "position": {
              "x": 50,
              "y": 100
            }
          }
        },
        {                                       
          "id": 2,              
          "type": "initiate_attributes",
          "data": {
            "title": "Temperature Conversion",
            "items": [
              {
                "name": "temperature_f",
                "value": "value(\"temperature\")*1.8 + 32",
                "generation_time": "genTime(\"temperature\", 0, \"valid\")",
                "server_time": "now()"
              }
            ]
          },
          "view": {                           
            "position": {
              "x": 300,
              "y": 100
            }
          }
        },
        {
          "id": 3,                            
          "type": "output_endpoint",
          "enabled": true,
          "data": {
            "title": "Navixy Platform",
            "output_endpoint_type": "output_navixy"
          },
          "view": {                           
            "position": {
              "x": 550,
              "y": 100
            }
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
  }'
```

Response (example):

```json
{
  "success": true,
  "id": 123
}
```

### Parameters explained

* **Flow entity**: The main container defining a complete data processing pipeline
  * `title`: Names your flow for easier identification
  * `enabled`: When true, flow begins processing data immediately after creation
* **Nodes**: Functional components that each handle a specific step in data processing
  * **Node 1 (data\_source)**:
    * Entry point collecting data from devices (IDs: 394892, 394893, 394894)
    * Unique ID within the flow for connection references
    * Position coordinates control UI display location
  * **Node 2 (initiate\_attributes)**:
    * Transforms data with custom calculations
    * Creates new `temperature_f` attribute using formula
    * Uses timestamps for data validity tracking
  * **Node 3 (output\_endpoint)**:
    * Destination for processed data
    * Type `output_navixy` sends to Navixy platform
    * Final step in the processing pipeline
* **Edges**: Define connections between nodes
  * Reference nodes by their IDs to create the processing sequence
  * Create a clear path for data to follow from source to destination

{% hint style="success" %}
This single request creates a complete flow that:

* Collects data from three specific devices (IDs: 394892, 394893, 394894)
* Converts temperature values from Celsius to Fahrenheit
* Transmits all data, including the new calculated attribute, to the Navixy platform

The success response includes the ID of the newly created flow, which you can use for future operations like updating the flow or adding additional nodes.

You can expand this example by adding more devices, creating additional calculated attributes, or configuring MQTT endpoints to send data to external systems.
{% endhint %}
