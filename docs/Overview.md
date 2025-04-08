---
stoplight-id: ie3rt9xv91kie
---

# Navixy IoT Logic API

*BETA Version*

<!-- theme: warning -->
> *BETA Version!* <br>
>Now the easrly access of IoT Logic's API is implemented, which means possible changes in the near future. Feel free to try the functionality, however, you may need to introduce changes in your applications reflecting the API functionality updates. Stay tuned! 

## Introduction

The Navixy IoT Logic API provides a powerful way to manage data flows from your IoT devices. This API allows you to:

- Create custom data processing pipelines
- Transform raw device data into meaningful business metrics
- Route processed data to external systems 
- Configure and manage data endpoints
- Build complex IoT data workflows through a flexible node system

This guide will help you navigate the various API endpoints and create your own IoT data flows, starting with the most common use case - sending your device data to an external system.

## API Overview

The Navixy IoT Logic API is organized around **Flows** - data processing pipelines.

Each flow consists of:
- **Nodes** - Processing elements (data sources, transformations, outputs)
- **Transitions** (**Edges**) - Connections between nodes that define the data path

### API Response Structure

All API responses follow a consistent pattern:

* Success responses include a `success: true` field
* Error responses include `success: false` and a `status` object with:
  * `code`: Numeric error code
  * `description`: Human-readable error description

### Flow Architecture

Flows in Navixy IoT Logic follow a directed graph architecture:

* Every flow must have at least one data source node (input)
* Every flow must have at least one output endpoint node (termination point)
* Each node has a unique ID within its flow (not globally unique)
* Edges define directional data flow between nodes
* Nodes can have multiple incoming and outgoing connections
* Circular references are not supported

## Getting Started

### Authentication

All API requests require an API key in the header:

```
Authorization: NVX your_api_key_here
```

The API key must be prefixed with "NVX " (note the space after NVX). This is a custom Bearer format used by Navixy.

According to the API specification:

```
"securitySchemes": {
  "api_key": {
    "description": "Enter an API key with the \"NVX: \" prefix, e.g. \"NVX 123456abcdefg\"",
    "example": "NVX 123456abcdefg",
    "type": "apiKey",
    "name": "Authorization",
    "in": "header",
    "bearerFormat": "NVX "
  }
}
```

### Base URLs

Two regional servers are available:
- Europe: `https://api.eu.navixy.com/`
- Americas: `https://api.us.navixy.com/`

### HTTP Methods

The API uses specific HTTP methods for different operations:
- `GET`: For retrieving information (flow list, flow details)
- `POST`: For creating, updating, and deleting resources

### Content Type

All requests and responses use JSON format:
```
Content-Type: application/json
```
