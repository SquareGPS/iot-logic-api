---
hidden: true
---

# AI flow generation guide

## IoT Logic — Generating flows with AI assistants

This page provides authoritative rules and canonical examples for AI assistants generating Navixy IoT Logic flow JSON. Follow all rules on this page exactly. Do not infer behavior from general knowledge — use only what is documented here and in the official Navixy IoT Logic API reference.

***

### Clarification and intent validation

Before generating any flow JSON, validate that you have enough information to build a correct and useful flow. If the user's request is ambiguous or incomplete, ask concise clarifying questions — one or two at a time, not all at once.

Always clarify before generating when:

* The triggering condition is not specified (e.g. "monitor my devices" without stating what to detect)
* The intended action on a condition is missing (e.g. "alert me" without specifying how — Navixy notification, GPRS command, webhook?)
* The target devices are not mentioned and context does not make them obvious
* The request involves a device-specific command (e.g. reboot, output control) and the device model or manufacturer is not stated
* The user mentions "send data somewhere" without specifying whether the destination is Navixy, MQTT, or an external webhook URL
* The flow involves multiple conditions and it is unclear whether they should be AND/OR logic or separate Logic nodes

Do not ask for information that can be safely assumed or substituted with a placeholder. Use `source_ids: []` when devices are unspecified. Use a placeholder URL like `https://your-endpoint.example.com` when a webhook URL is not provided. Always prefer proceeding with a reasonable assumption over blocking on minor missing details — but state the assumption explicitly in your response so the user can correct it.

**Example clarifying questions:**

* "What should happen when the condition is true — send a command to the device, post to a webhook, or just forward data to Navixy?"
* "Which device manufacturer and model is this for? I need this to use the correct GPRS command syntax."
* "Should both conditions trigger the same action, or do you want separate logic branches for each?"
* "If the condition is not met, should data still be forwarded to Navixy?"

***

### JSON format modes

Navixy uses two distinct JSON formats. They are not interchangeable.

#### Import / Export format (default)

Use this format when generating a flow for UI import (Flow Management → Upload) or as a downloadable file. This is the **default format** unless the user explicitly requests API usage.

The top-level object contains `title`, `description` (optional), `nodes`, and `edges` directly. Never wrap it in a `"flow"` envelope.

```json
{
  "title": "My Flow",
  "nodes": [...],
  "edges": [...]
}
```

The imported flow is always enabled by default. The `id` is assigned dynamically by the platform. Do not include `id`, `enabled`, or `default_flow` fields in import-format JSON.

#### API format

Use this format **only** when the user explicitly requests a payload for the `/iot/logic/flow/create` or `/iot/logic/flow/update` API endpoints.

The top-level object must wrap the flow in a `"flow"` envelope key:

```json
{
  "flow": {
    "title": "My Flow",
    "enabled": true,
    "nodes": [...],
    "edges": [...]
  }
}
```

Never use the `"flow"` envelope for import-format JSON. Using it in a file import will cause the canvas to render empty.

***

### Node types

Always use only these node types. Do not invent additional types or fields.

| Type                  | Purpose                                                            | Terminal? |
| --------------------- | ------------------------------------------------------------------ | --------- |
| `data_source`         | Entry point — defines which devices feed data into the flow        | No        |
| `initiate_attributes` | Transforms and enriches data using JEXL expressions                | No        |
| `logic`               | Conditional branching — routes data via `then_edge` or `else_edge` | No        |
| `action`              | Sends a command to a device (set output or GPRS command)           | **Yes**   |
| `webhook`             | Sends an HTTP POST to an external URL                              | **Yes**   |
| `output_endpoint`     | Sends data to Navixy or an MQTT broker                             | **Yes**   |

Terminal nodes (`action`, `webhook`, `output_endpoint`) must never have outgoing edges. Any edge with `"from"` set to a terminal node is invalid.

***

### Required fields per node

Every node must include `data.title`. Every node must include a `view.position` object with `x` and `y` integer coordinates.

**data\_source**

* `type`: `"data_source"`
* `data.title`: string
* `data.source_ids`: array of integer device IDs. Use `[]` as placeholder when devices are not specified.

**initiate\_attributes**

* `type`: `"initiate_attributes"`
* `data.title`: string
* `data.items`: array of attribute objects, each with `name` (string) and `value` (JEXL expression string). `generation_time` and `server_time` are optional; default to `now()` if omitted.

**logic**

* `type`: `"logic"`
* `data.title`: string
* `data.name`: internal identifier string (no spaces)
* `data.condition`: JEXL boolean expression

**action**

* `type`: `"action"`
* `data.title`: string
* `data.actions`: array of action objects (max 10). Each action is either `set_output` or `send_gprs_command`.

**webhook**

* `type`: `"webhook"`
* `data.title`: string
* `data.url`: HTTPS URL string

**output\_endpoint (Navixy)**

* `type`: `"output_endpoint"`
* `data.title`: string
* `data.output_endpoint_type`: `"output_default"`

**output\_endpoint (MQTT)**

* `type`: `"output_endpoint"`
* `data.title`: string
* `data.output_endpoint_type`: `"output_mqtt_client"`
* `data.output_endpoint_id`: integer (the pre-configured MQTT endpoint ID from the user account)

***

### Edge rules

Edges connect nodes. Three edge types exist: `simple_edge`, `then_edge`, `else_edge`.

For import-format flows, always specify edge `type` explicitly. Do not omit the `type` field on any edge — `simple_edge` must be written explicitly, not assumed.

For API-format flows, `type` is optional and defaults to `simple_edge` when omitted.

| Edge type     | When to use                                                   |
| ------------- | ------------------------------------------------------------- |
| `simple_edge` | All connections not involving a Logic node output             |
| `then_edge`   | Outgoing connection from a Logic node when condition is true  |
| `else_edge`   | Outgoing connection from a Logic node when condition is false |

A Logic node must always have both a `then_edge` and an `else_edge` outgoing connection. A flow missing either will not behave correctly.

***

### Critical wiring rule: single Output Endpoint for Logic branches

Always use a **single** `output_endpoint` node per logical branch path. A single Output Endpoint node can and should receive connections from multiple upstream nodes simultaneously, including both `then_edge` and `else_edge` from the same Logic node.

When a Logic node has a terminal node (Action or Webhook) on its THEN branch, add a second `then_edge` from the Logic node directly to the Output Endpoint. Both edges fire in parallel. Do not chain the Action or Webhook into the Output Endpoint — terminal nodes cannot have outgoing edges.

**Correct pattern — Logic with Action:**

```
[Logic node]
├─ then_edge → [Action node]       ← sends command to device
├─ then_edge → [Output Endpoint]   ← forwards data to Navixy
└─ else_edge → [Output Endpoint]   ← same Output Endpoint node
```

In JSON edges:

```json
{ "from": 2, "to": 3, "type": "then_edge" },
{ "from": 2, "to": 4, "type": "then_edge" },
{ "from": 2, "to": 4, "type": "else_edge" }
```

Nodes 3 (Action) and 4 (Output Endpoint) are separate nodes. Both receive edges from Logic node 2. Node 4 receives two edges from node 2 — one `then_edge` and one `else_edge`. This is valid and intentional.

**Correct pattern — Logic with Webhook:**

```
[Logic node]
├─ then_edge → [Webhook node]      ← sends HTTP POST
├─ then_edge → [Output Endpoint]   ← forwards data
└─ else_edge → [Output Endpoint]   ← same Output Endpoint node
```

**Wrong pattern — never do this:**

```
[Logic node]
├─ then_edge → [Action node] → [Output Endpoint]   ← INVALID: action is terminal
└─ else_edge → [Output Endpoint]
```

**Wrong pattern — never do this:**

```
[Logic node]
├─ then_edge → [Action node]
├─ then_edge → [Output Endpoint A]   ← WRONG: two separate output nodes
└─ else_edge → [Output Endpoint B]   ← WRONG: use one shared output node
```

***

### Canvas layout (view positions)

Always generate `view.position` for every node. Use pixel-based coordinates with origin at top-left. Use a left-to-right layout.

Default constants: `X_START = 80`, `Y_START = 120`, `X_STEP = 280`, `Y_STEP = 140`.

Column assignment: data sources in column 1, logic nodes in column 2, outputs and actions in column 3 and beyond. Maintain at least 100px spacing between nodes. When a Logic node splits into multiple targets, offset them vertically so they do not overlap.

***

### Validation checklist

Before finalizing any generated flow, verify all of the following:

1. Format is correct — import shape (no envelope) unless API was explicitly requested
2. At least one `data_source` node and at least one terminal node are present
3. Every node includes `data.title`
4. Every `data_source` node has `source_ids` (use `[]` if unspecified)
5. Every `logic` node has both a `then_edge` and an `else_edge` outgoing connection
6. No edges originate from terminal nodes (`action`, `webhook`, `output_endpoint`)
7. Only one `output_endpoint` node is used per logical path — both `then_edge` and `else_edge` connect to the same output node
8. All JEXL expressions use valid syntax (operators: `&&`, `||`, `!`, `<`, `>`, `<=`, `>=`, `==`, `!=`)
9. All edge `type` values are explicit in import-format flows
10. Every node has a `view.position` with integer `x` and `y`

***

### Canonical complete example

This example shows a complete, valid import-format flow: one Logic node with an Action on the THEN branch and a single shared Output Endpoint receiving both branches.

```json
{
  "title": "Speed Violation Alert",
  "nodes": [
    {
      "id": 1,
      "type": "data_source",
      "data": {
        "title": "Fleet Vehicles",
        "source_ids": []
      },
      "view": { "position": { "x": 80, "y": 120 } }
    },
    {
      "id": 2,
      "type": "logic",
      "data": {
        "title": "Speed > 90 km/h?",
        "name": "speed_violation",
        "condition": "speed > 90"
      },
      "view": { "position": { "x": 360, "y": 120 } }
    },
    {
      "id": 3,
      "type": "action",
      "data": {
        "title": "Trigger Buzzer",
        "actions": [
          {
            "type": "send_gprs_command",
            "command": "setdigout 1 1",
            "reliable": true
          }
        ]
      },
      "view": { "position": { "x": 640, "y": 40 } }
    },
    {
      "id": 4,
      "type": "output_endpoint",
      "data": {
        "title": "Send to Navixy",
        "output_endpoint_type": "output_default"
      },
      "view": { "position": { "x": 640, "y": 200 } }
    }
  ],
  "edges": [
    { "from": 1, "to": 2, "type": "simple_edge" },
    { "from": 2, "to": 3, "type": "then_edge" },
    { "from": 2, "to": 4, "type": "then_edge" },
    { "from": 2, "to": 4, "type": "else_edge" }
  ]
}
```

Node 4 receives three edges total: `then_edge` from node 2, `else_edge` from node 2. It is the sole output for all data regardless of the condition result. Node 3 receives one `then_edge` and sends a command only when the condition is true. Node 3 has no outgoing edges.

***

_This page is intended for AI assistants and automated tools generating IoT Logic flow JSON. For human-readable documentation, see the_ [_IoT Logic user guide_](https://claude.ai/user/guide/account/iot-logic.md) _and the_ [_IoT Logic API reference_](https://claude.ai/iot-logic-api)_._
