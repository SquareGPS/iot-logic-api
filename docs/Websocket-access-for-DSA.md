---
stoplight-id: 09sx1g2wm5gw3
---

# Websocket access to Data Stream Analyzer

## Overview

The WebSocket functionality provides real-time, event-driven access to device data. It enables you to subscribe to various event types—such as location updates, device state changes, and telemetry streams—without the need for continuous polling.

WebSocket communication is ideal for applications that require immediate data delivery, such as monitoring dashboards, alert systems, or integrations that rely on timely IoT events.

For more details, see [WebSocket in Navixy API](https://developers.navixy.com/docs/navixy-api/2c02b575c8af8-web-socket-api)
This guide covers connection setup, authentication, event types, and message formats.

The iot_monitor event stream is designed for Data Stream Analyzer (DSA) and delivers real-time telemetry from selected devices. It provides both the latest data and short-term history, allowing you to track attribute changes over time.

This feature supports use cases like diagnostics, trend visualization, and alerting—where understanding recent attribute patterns is as important as receiving the newest values. Its structured format also helps you distinguish between missing and inactive data, improving clarity and reliability in IoT monitoring.

## Data Stream Analyzer's "iot_monitor" event subscription

<!-- theme: warning -->
> This is a DSA-focused snippet showcasing subscription parameters. For complete information, see [WebSocket Subscription](https://developers.navixy.com/docs/navixy-api/8437c2abc0274-web-socket-subscription)

This subscription type is intended for the Data Stream Analyzer tool, 
which allows viewing the attribute values of the last N messages received from a tracker.
The server stores attributes for no more than the last 12 messages, sorted in descending order by message timestamp.
For each attribute, data is stored in two queues:

* Without data gaps – only messages where the specific attribute was present (not null).
* With data gaps – if an attribute was missing in one of the last messages, a null value is recorded in the queue.

After subscribing to "iot_monitor", server will send values of attributes from the latest messages for 
all non-blocked trackers included in the subscription in a single packet.
Receiver must be able to parse data from different devices in this packet.
New data will arrive in real-time in the [event message](https://developers.navixy.com/docs/navixy-api/bdb1d20bafe28-web-socket-events), 
but no more frequently than the specified `rate_limit`.

```json
{
  "action": "subscribe",
  "hash": "6c638c52cb40729d5e6181a48f868649",
  "requests": [
    {
      "type": "iot_monitor",
      "target": {
        "type": "selected",
        "tracker_ids": [
          21080
        ]
      },
      "rate_limit": "5s"
    }
  ]
}
```

Request fields:

* `type` – required, text: _"iot_monitor"_. Event type.
* `target` – required, [target](https://developers.navixy.com/docs/navixy-api/8437c2abc0274-web-socket-subscription). Trackers to subscribe. Maximum 10 trackers.
* `rate_limit` – optional, string. A timespan for batching.


### Response

Response parameters:

* `type` – required, text: _"response"_.
* `action` – required, text: _"subscription/subscribe"_.
* `events` – required, array of [enum](https://developers.navixy.com/docs/navixy-api/d87ce89118d15-introduction#data-types), without nulls. List of the subscribed events types ("", "" or "iot_monitor").
* `data` – required, map <string, object>. Map with events subscription result. One key per subscribed event.
    * `state` – present if the "state" subscription requested, see sub response below.
    * `state_batch` – present if the "state_batch" subscription requested, see sub response below.
    * `readings_batch` – present if the "readings_batch" subscription requested, see sub response below.

Sub response:
* `success` – required, boolean.
* `value` – required, map <string, enum>, present if success. The current status of requested trackers.

Keys is a tracker IDs, values – one of the item:

* `normal` – non-blocked, normal status. [State events](https://developers.navixy.com/docs/navixy-api/bdb1d20bafe28-web-socket-events#state-event) for this
  tracker will be delivered to client.
* `blocked` – tracker blocked. [State events](https://developers.navixy.com/docs/navixy-api/bdb1d20bafe28-web-socket-events#state-event) for this tracker 
`will *not* be delivered to client. [Lifecycle events](https://developers.navixy.com/docs/navixy-api/bdb1d20bafe28-web-socket-events#lifecycle-event) will be delivered. After unblocking, 
current tracker state will be sent automatically.
* `unknown` – tracker ID missed in the database or not belong to current user.  
* `disallowed` – subscription for this tracker not allowed by the current session.

Response sample:

```json
{
  "type": "response",
  "action": "subscription/subscribe",
  "events": ["state"],
  "data": {
    "state": {
      "value": {
        "15564": "normal",
        "15565": "blocked",
        "15568": "unknown"
      },
      "success": true
    }
  }
}
```

## Data Stream Analyzer event

<!-- theme: warning -->
> This is a DSA-focused snippet showcasing only its event. For complete information, see [WebSocket Events](https://developers.navixy.com/docs/navixy-api/bdb1d20bafe28-web-socket-events)

You can receive Data Stream Analyser messages through websocket. These messages are coming from server if client [subscribed](https://developers.navixy.com/docs/navixy-api/8437c2abc0274-web-socket-subscription)
to the `iot_monitor` events of the specific tracker that is not blocked. These packets contain values 
of attributes from the latest messages sent by the selected tracker.
It occurs in the next cases:

* Immediately after subscription.
* The latest attribute values are updated. But no more frequently than the `rate_limit`.

Message fields:

* `type` – "event".
* `event` – "iot_monitor".
* `data`:
  * `iot_last_values` – list of objects:
    * `tracker_id` – tracker ID.
    * `nonnull_fields` – list of objects. Queue without data gaps – only messages where the specific attribute was present (not null).
      * `<field_name>` – name of the attribute.
        * `value` – value of attribute.
        * `msg_time` – message time.
        * `srv_time` – server time.
    * `all_fields` – list of objects. Queue with data gaps – if an attribute was missing in one of the last messages, a null value is recorded in the queue.
      * `<field_name>` – name of the attribute.
        * `value` – value of attribute.
        * `msg_time` – message time.
        * `srv_time` – server time.

Message sample:

```json
{
  "event": "iot_monitor",
  "type": "event",
  "data": {
    "iot_last_values": [
      {
        "tracker_id": 21080,
        "nonnull_fields": {
          "satellites": [
            {
              "msg_time": "2025-02-11T15:12:58Z",
              "srv_time": "2025-02-11T15:12:58Z",
              "value": 10
            },
            {
              "msg_time": "2025-02-11T15:12:52Z",
              "srv_time": "2025-02-11T15:12:53Z",
              "value": 10
            }
          ],
          "heading": [
            {
              "msg_time": "2025-02-11T15:12:58Z",
              "srv_time": "2025-02-11T15:12:58Z",
              "value": 7
            },
            {
              "msg_time": "2025-02-11T15:12:52Z",
              "srv_time": "2025-02-11T15:12:53Z",
              "value": 6
            }
          ],
          "latitude": [
            {
              "msg_time": "2025-02-11T15:12:58Z",
              "srv_time": "2025-02-11T15:12:58Z",
              "value": "5.9654133"
            },
            {
              "msg_time": "2025-02-11T15:12:52Z",
              "srv_time": "2025-02-11T15:12:53Z",
              "value": "5.9646583"
            }
          ],
          "longitude": [
            {
              "msg_time": "2025-02-11T15:12:58Z",
              "srv_time": "2025-02-11T15:12:58Z",
              "value": "6.5171267"
            },
            {
              "msg_time": "2025-02-11T15:12:52Z",
              "srv_time": "2025-02-11T15:12:53Z",
              "value": "6.5169383"
            }
          ],
          "lls_level_1": [
            {
              "msg_time": "2025-02-11T15:12:58Z",
              "srv_time": "2025-02-11T15:12:58Z",
              "value": "262.9138"
            },
            {
              "msg_time": "2025-02-11T15:12:52Z",
              "srv_time": "2025-02-11T15:12:53Z",
              "value": "262.9945"
            }
          ],
          "speed": [
            {
              "msg_time": "2025-02-11T15:12:58Z",
              "srv_time": "2025-02-11T15:12:58Z",
              "value": 43
            },
            {
              "msg_time": "2025-02-11T15:12:52Z",
              "srv_time": "2025-02-11T15:12:53Z",
              "value": 48
            }
          ]
        },
        "all_fields": {
          "satellites": [
            {
              "msg_time": "2025-02-11T15:12:58Z",
              "srv_time": "2025-02-11T15:12:58Z",
              "value": 10
            },
            {
              "msg_time": "2025-02-11T15:12:52Z",
              "srv_time": "2025-02-11T15:12:53Z",
              "value": 10
            }
          ],
          "heading": [
            {
              "msg_time": "2025-02-11T15:12:58Z",
              "srv_time": "2025-02-11T15:12:58Z",
              "value": 7
            },
            {
              "msg_time": "2025-02-11T15:12:52Z",
              "srv_time": "2025-02-11T15:12:53Z",
              "value": 6
            }
          ],
          "latitude": [
            {
              "msg_time": "2025-02-11T15:12:58Z",
              "srv_time": "2025-02-11T15:12:58Z",
              "value": "5.9654133"
            },
            {
              "msg_time": "2025-02-11T15:12:52Z",
              "srv_time": "2025-02-11T15:12:53Z",
              "value": "5.9646583"
            }
          ],
          "longitude": [
            {
              "msg_time": "2025-02-11T15:12:58Z",
              "srv_time": "2025-02-11T15:12:58Z",
              "value": "6.5171267"
            },
            {
              "msg_time": "2025-02-11T15:12:52Z",
              "srv_time": "2025-02-11T15:12:53Z",
              "value": "6.5169383"
            }
          ],
          "lls_level_1": [
            {
              "msg_time": "2025-02-11T15:12:59Z",
              "srv_time": "2025-02-11T15:12:59Z",
              "value": null
            },
            {
              "msg_time": "2025-02-11T15:12:52Z",
              "srv_time": "2025-02-11T15:12:53Z",
              "value": "262.9945"
            }
          ],
          "speed": [
            {
              "msg_time": "2025-02-11T15:12:58Z",
              "srv_time": "2025-02-11T15:12:58Z",
              "value": 43
            },
            {
              "msg_time": "2025-02-11T15:12:52Z",
              "srv_time": "2025-02-11T15:12:53Z",
              "value": 48
            }
          ]
        }
      }
    ]
  }
}
```