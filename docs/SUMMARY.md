# Table of contents

* [Navixy IoT Logic API](README.md)
* [Authentication](authentication.md)
* [Technical reference](Technical-details.md)
* [Flow object structure](flow-schema-structure/README.md)
  * [JSON-schema template](flow-schema-structure/general-json-schema-example.md)
* [Guides](navixy-iot-guide/README.md)
  * [Sending device data to an external system](navixy-iot-guide/scenario1.md)
  * [Managing your flows and endpoints](navixy-iot-guide/scenario2.md)
  * [Advanced configurations](navixy-iot-guide/advanced-configurations.md)
* [Websocket access to Data Stream Analyzer](Websocket-access-for-DSA.md)

## RESOURCES

* ```yaml
  type: builtin:openapi
  props:
    models: true
  dependencies:
    spec:
      ref:
        kind: openapi
        spec: iot-logic
  ```
