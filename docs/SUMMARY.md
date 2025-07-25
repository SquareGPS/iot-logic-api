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
  * [Adding calculated attributes to Navixy UI](navixy-iot-guide/adding-calculated-attributes-to-navixy-ui.md)
* [Websocket access to Data Stream Analyzer](Websocket-access-for-DSA.md)

## RESOURCES

* [API reference](resources/api-reference/README.md)
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

## TECHNOLOGIES

* [Navixy Generic Protocol](Technologies/navixy-generic-protocol/navixy-generic-protocol.md)
  * [Navixy Generic Protocol 1.0](Technologies/navixy-generic-protocol/navixy-generic-protocol/navixy-generic-protocol-10.md)
    * [Transport layer](Technologies/navixy-generic-protocol/navixy-generic-protocol/navixy-generic-protocol-10/transport-layer.md)
    * [Data types and encoding standards](Technologies/navixy-generic-protocol/navixy-generic-protocol/navixy-generic-protocol-10/data-types-and-encoding-standards.md)
    * [Message structure and attributes](Technologies/navixy-generic-protocol/navixy-generic-protocol/navixy-generic-protocol-10/message-structure-and-attributes.md)
    * [Predefined event identifiers](Technologies/navixy-generic-protocol/navixy-generic-protocol/navixy-generic-protocol-10/predefined-event-identifiers.md)
  * [Navixy Generic Protocol 1.1a (on demand)](Technologies/navixy-generic-protocol/navixy-generic-protocol/navixy-generic-protocol-11a-on-demand.md)
* [Navixy IoT Logic Expression Language](Technologies/navixy-iot-logic-expression-language/navixy-iot-logic-expression-language.md)
