---
description: >-
  Use the NGP Mapper Claude skill to generate a ready-to-implement field
  mapping from any device or telematics platform format to Navixy Generic
  Protocol.
hidden: true
---

# NGP Mapper skill

The NGP Mapper is a Claude skill that takes your device's or system's data format as input and produces a complete, actionable mapping to Navixy Generic Protocol (NGP). Instead of working through the reference manually, you describe your source data and get back a specification ready to hand to your developer.

## Who it is for

**System integrators** who have an existing telematics platform, fleet application, or data pipeline and want to forward data to Navixy. The skill maps your platform's output fields to NGP so you can build a converter service that bridges the two systems.

**Device manufacturers and firmware developers** who want their hardware to send data to Navixy natively. The skill maps your device's proprietary fields to the corresponding NGP attributes, including the transforms needed when units or formats differ.

In both cases the conversion happens on your side — Navixy receives standard NGP messages as if the device were natively supported.

## What the skill produces

For each source protocol you describe, the skill outputs a self-contained mapping specification:

**Field mapping table** — every source field alongside its NGP equivalent, the transform required (unit conversion, enum remapping, bitmask extraction, timestamp normalisation), and notes on optionality.

**Example NGP message** — a complete, copy-pasteable JSON object built from your actual sample values with all transforms applied.

**Transport setup** — exact connection parameters for HTTP or MQTT based on your target Navixy region, including endpoint URLs, authentication, topic format, and response codes.

**Handling notes** — callouts for source fields with no NGP equivalent (promoted to `custom_*` attributes or dropped), fields that need to be synthesised (such as `device_id` or `message_time`), and any platform rules that could cause silent message discard.

## How to use it

{% stepper %}
{% step %}
## Install the skill

Download `ngp-mapper.skill` from this repository and install it in Claude desktop (Settings → Skills → Install from file). The skill loads automatically when you describe a protocol mapping task.
{% endstep %}

{% step %}
## Describe your source protocol

Start a conversation with Claude and paste a sample message from your device or system. Include any context that isn't obvious from field names — units, whether a field is a Unix epoch or formatted string, what a flag value of `1` means, and so on.

The more concrete the input, the more precise the output. A raw sample message with real values produces a better mapping than a field list alone.

{% hint style="info" %}
You don't need to describe every field upfront. The skill will ask about anything ambiguous as it works through the mapping.
{% endhint %}
{% endstep %}

{% step %}
## Tell the skill your transport preference and region

HTTP is simpler to start with; MQTT suits devices that need persistent connections or low overhead. The EU region uses `tracker.navixy.com` and `mqtt.eu.navixy.com`; the US region uses `tracker.us.navixy.com` and `mqtt.us.navixy.com`.
{% endstep %}

{% step %}
## Review and implement

The skill produces the mapping document in the conversation. Review the field table and the example message, then pass the specification to whoever is implementing the converter — your middleware developer, firmware team, or yourself.
{% endstep %}
{% endstepper %}

## Example input and output

**What you provide:**

```json
{
  "imei": "352656100901234",
  "utc": "2024-09-02 10:03:43",
  "lat": 56.348579,
  "lon": 60.12344,
  "spd": 43,
  "sat": 8,
  "ign": 1,
  "bat": 4.12,
  "adt1": -13.7
}
```

Plus: `ign` is ignition state (1=on/0=off), `adt1` is an external temperature sensor, HTTP transport, EU region.

**What you get back** (excerpt):

| Source field | NGP field | Transform | Notes |
|---|---|---|---|
| `imei` | `device_id` | none | Max 64 chars |
| `utc` | `message_time` | Add `T`, append `Z` | `"2024-09-02 10:03:43"` → `"2024-09-02T10:03:43Z"` |
| `lat` | `location.latitude` | none | Already decimal degrees |
| `spd` | `location.speed` | none | Already km/h |
| `ign` | `input_status` | bit 0: `ign=1` → `input_status=1` | Bitmask; bit 0 = input 1 |
| `adt1` | `temperature_2` | none | External sensor; `temperature_internal` is reserved for built-in |

…plus a ready-to-send JSON example and HTTP transport parameters.

## LBS-only devices

If your device has no GPS and reports cell tower data only, the skill handles this as a separate positioning path. It maps your cell fields (`mcc`, `mnc`, `lac`, `cell_id`, signal strength) to the `mobile_cells` array, sets `location.source_type: "LBS"`, and explains how Navixy resolves cell tower identifiers to approximate coordinates. A satellite count is not required for LBS-based messages.

See [Message structure and attributes](message-structure-and-attributes.md) for the full `mobile_cells` schema and the `source_type` / `precision` fields.
