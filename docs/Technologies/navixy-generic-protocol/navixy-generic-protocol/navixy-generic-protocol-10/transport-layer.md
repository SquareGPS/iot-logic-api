# Transport layer

The Navixy Generic Protocol supports both MQTT and HTTP/HTTPS as transport layers, ensuring flexibility and scalability for various devices and systems.

### HTTP/HTTPS

Navixy Generic Protocol supports **HTTP/HTTPS version 1.1 and 2.0** as a transport method. This is a common, well-known, and user-friendly option for developers and technicians. Below are the HTTP/HTTPS parameters and headers used for Navixy Generic Protocol:

* Method: POST
* Body: UTF-8 encoded JSON text
* Content-Type: application/json

Moreover, Navixy Generic Protocol supports response codes for HTTP that telematics platform can send in reply to the HTTP request:

`200` OK - message received successfully.

`400` BAD\_REQUEST - invalid request body, e.g. broken JSON of incorrect format.

`403` FORBIDDEN - unknown device identifier. Please check the device identifier that is specified in the data packet.

`500` INTERNAL\_SERVER\_ERROR - unexpected server error. Something went wrong on the server. Please contact the technical support team of the recipient’s side.

&#x20;For your convenience below you can find the **CURL example** of possible HTTP request:

```
curl --location 'tracker.navixy.com:47642' \
--header 'Content-Type: application/json' \
--data '{
    "message_time": "2024-10-10T06:00:11Z",
    "device_id": "1112312212",
    "location": {
        "latitude": 34.15929687705282,
        "longitude": -118.4614133834839
    },
    "battery_level": 68
}'
```

### MQTT

The Navixy Generic Protocol uses [MQTT](https://www.navixy.com/blog/mqtt-gps-devices/), a proven, lightweight, and scalable messaging protocol, to ensure reliable data delivery over TCP.

The protocol supports **MQTT 5.0** and **MQTT 3.1.1**, offering flexibility and compatibility with various devices and systems. To guarantee message delivery, two Quality of Service (QoS) levels are available:

* **QoS 0:** Messages are delivered at most once, suitable for applications where occasional message loss is acceptable.
* **QoS 1:** Messages are delivered at least once, ensuring reliable delivery.

All message bodies must be encoded as **UTF-8 JSON** text, containing a single JSON object per message. Responses to messages are not currently supported. To maintain data integrity, Navixy strictly validates incoming messages, discarding those with invalid JSON or attributes that exceed defined value ranges.

As a reference, you can use **example of sending a message via Mosquitto client**:

```
mosquitto_pub -h mqtt.eu.navixy.com -p 1883 -u ngp_device -P secretword -t "ngp/1112312212" -m "{
```

Continue reading to learn about [Data types and encoding standards](data-types-and-encoding-standards.md) in Navixy Generic Protocol.
