# Expression syntax reference

This reference documents the complete syntax of the Navixy IoT Logic Expression Language, including literals, operators, functions, and data types. For conceptual information about how expressions work within IoT Logic, see the [Expression language overview](./).

## Basic syntax elements

The expression language uses JEXL (Java Expression Language) as its foundation, with IoT-specific enhancements for device data processing.

### Literals

| Literal Type            | Syntax                                                | Example                                 |
| ----------------------- | ----------------------------------------------------- | --------------------------------------- |
| Integer                 | Digits 0-9                                            | `42`                                    |
| Float                   | Digits with decimal point, optional `f` or `F` suffix | `3.14`, `42.0f`                         |
| Long                    | Digits with `l` or `L` suffix                         | `42L`                                   |
| Double                  | Digits with decimal point and `d` or `D` suffix       | `42.0d`                                 |
| Hexadecimal             | `0x` or `0X` prefix, then hex digits                  | `0xFF`, `0x1A2B`                        |
| Octal                   | `0` prefix, then octal digits                         | `010`                                   |
| Scientific notation     | Standard scientific notation with `e` or `E`          | `1.5e-10`                               |
| String (double quotes)  | Text enclosed in double quotes                        | `"Hello world"`                         |
| String (single quotes)  | Text enclosed in single quotes                        | `'Hello world'`                         |
| String escape sequences | Backslash escape character                            | `"Line 1\nLine 2"`, `"Quote: \"text\""` |
| Boolean                 | Keywords `true` or `false`                            | `true`, `false`                         |
| Null                    | Keyword `null`                                        | `null`                                  |

#### Identifiers and attribute names

Attribute names must exactly match names from device telemetry. To make sure you use correct names, you can:

* Use the [Autofill attribute names](https://app.gitbook.com/s/446mKak1zDrGv70ahuYZ/guide/account/iot-logic/flow-management/initiate-attribute-node/managing-attributes#autofill-attribute-names) option
* Lookup attribute names in [Data Stream Analyzer](https://app.gitbook.com/s/446mKak1zDrGv70ahuYZ/guide/account/iot-logic/data-stream-analyzer)&#x20;

## Attribute access

### Short syntax

**Purpose:** Access current attribute values (most readable form)

**Syntax:** `attribute_name`

**Defaults:**

* Index: `0` (current value)
* Validation: `'all'` (includes null values)

**Example:** `temperature * 1.8 + 32`

### Full syntax

**Purpose:** Access historical values or explicit validation mode

**Function:** `value(attribute_name, index, validation)`

**Parameters:**

| Parameter        | Type    | Range/Values         | Description                                                                        |
| ---------------- | ------- | -------------------- | ---------------------------------------------------------------------------------- |
| `attribute_name` | String  | Any valid attribute  | Exact name from device telemetry                                                   |
| `index`          | Integer | 0-12                 | Historical position: 0=current, 1=previous, 12=12 readings ago                     |
| `validation`     | String  | `'all'` or `'valid'` | `'all'`=includes nulls (exact index), `'valid'`=excludes nulls (Nth valid reading) |

**Return value:** Attribute value at specified position, or `null` if unavailable

**Examples:**

| Expression                                     | Description                                                                  |
| ---------------------------------------------- | ---------------------------------------------------------------------------- |
| `temperature`                                  | Current value with short syntax (equals to `value('temperature', 0, 'all')`) |
| `value('temperature', 1, 'all')`               | Previous reading                                                             |
| `value('speed', 5, 'valid')`                   | 5th valid reading back                                                       |
| `temperature - value('temperature', 1, 'all')` | Temperature change                                                           |

## Operators

### Arithmetic operators

| Operator | Operation           | Example             |
| -------- | ------------------- | ------------------- |
| `+`      | Addition            | `temperature + 10`  |
| `-`      | Subtraction         | `fuel_level - 5`    |
| `*`      | Multiplication      | `temperature * 1.8` |
| `/`      | Division            | `distance / time`   |
| `%`      | Modulus (remainder) | `value % 100`       |

### Comparison operators

| Operator | Comparison            | Example            |
| -------- | --------------------- | ------------------ |
| `==`     | Equal                 | `speed == 80`      |
| `!=`     | Not equal             | `status != 0`      |
| `<`      | Less than             | `temperature < 0`  |
| `<=`     | Less than or equal    | `fuel_level <= 10` |
| `>`      | Greater than          | `speed > 80`       |
| `>=`     | Greater than or equal | `voltage >= 12.0`  |

### Logical operators

| Operator | Alternative | Operation   | Example                      |
| -------- | ----------- | ----------- | ---------------------------- |
| `&&`     | `and`       | Logical AND | `speed > 80 && engine_on`    |
| `\|\|`   | `or`        | Logical OR  | `temp < 0 \|\| pressure_low` |
| `!`      | `not`       | Logical NOT | `!door_closed`               |

### Pattern matching operators

<table><thead><tr><th width="138.54547119140625">Operator</th><th>Description</th></tr></thead><tbody><tr><td><code>=~</code></td><td>Checks if the value of the left operand is in the set of the right operand. For strings, checks for regex pattern match</td></tr><tr><td><code>!~</code></td><td>Checks if the value of the left operand is not in the set of the right operand. For strings, checks for regex pattern mismatch</td></tr><tr><td><code>=^</code></td><td>Checks that the left string operand starts with the right string operand</td></tr><tr><td><code>!^</code></td><td>Checks that the left string operand doesn't start with the right string operand</td></tr><tr><td><code>=$</code></td><td>Checks that the left string operand ends with the right string operand</td></tr><tr><td><code>!$</code></td><td>Checks that the left string operand doesn't end with the right string operand</td></tr></tbody></table>

#### Ternary conditional

**Syntax:** `condition ? value_if_true : value_if_false`

**Example:** `speed > 80 ? "Speeding" : "Normal"`

### Operator precedence

Operators are evaluated in order from highest to lowest precedence:

| Precedence  | Operators                            | Description                       |
| ----------- | ------------------------------------ | --------------------------------- |
| 1 (highest) | `( )`                                | Parentheses                       |
| 2           | `!`, `not`, `-` (unary), `+` (unary) | Unary operators                   |
| 3           | `*`, `/`, `%`                        | Multiplication, division, modulus |
| 4           | `+`, `-`                             | Addition, subtraction             |
| 5           | `<`, `<=`, `>`, `>=`                 | Comparison                        |
| 6           | `==`, `!=`                           | Equality                          |
| 7           | `&&`, `and`                          | Logical AND                       |
| 8           | `\|\|`, `or`                         | Logical OR                        |
| 9 (lowest)  | `? :`                                | Ternary conditional               |

{% hint style="info" %}
Use parentheses to override precedence or clarify complex expressions.
{% endhint %}

## Core functions

### Time and data access functions

| Function                                     | Parameters                                                                                                                                                              | Description                                                                           |
| -------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| `value(attribute_name, index, validation)`   | <p><code>attribute_name</code> (String)</p><p><code>index</code> (Integer, 0-12)</p><p><code>validation</code> (String: <code>'all'</code> or <code>'valid'</code>)</p> | Attribute value at specified historical position                                      |
| `genTime(attribute_name, index, validation)` | <p><code>attribute_name</code> (String</p><p><code>index</code> (Integer, 0-12)</p><p><code>validation</code> (String: <code>'all'</code> or <code>'valid'</code>)</p>  | Device-side generation timestamp (milliseconds) for attribute value. Default: `now()` |
| `srvTime(attribute_name, index, validation)` | <p><code>attribute_name</code> (String</p><p><code>index</code> (Integer, 0-12</p><p><code>validation</code> (String: <code>'all'</code> or <code>'valid'</code>)</p>   | Server-side reception timestamp (milliseconds) for attribute value. Default: `now()`  |

**Usage examples:**

<table><thead><tr><th width="268.54541015625">Use case</th><th>Expression</th></tr></thead><tbody><tr><td>Default timestamp (current time)</td><td><code>"server_time": "now()"</code> or <code>"generation_time": "now()"</code></td></tr><tr><td>Data age</td><td><code>now() - genTime('temperature', 0, 'all')</code></td></tr><tr><td>Transmission delay</td><td><code>srvTime('temperature', 0, 'all') - genTime('temperature', 0, 'all')</code></td></tr><tr><td>Time offset</td><td><code>genTime('temperature', 0, 'valid') + 120000</code></td></tr></tbody></table>

{% hint style="info" %}
For calculated attributes in IoT Logic flows, if `genTime` and `srvTime` are not explicitly specified, both default to `now()` (current timestamp).
{% endhint %}

### Bit-level operations

The `util:` namespace provides specialized functions for binary data processing, data format conversions, and string operations.

#### Bit-level functions

<table><thead><tr><th>Function</th><th>Parameters</th><th width="85.181884765625">Type</th><th>Description</th></tr></thead><tbody><tr><td><code>util:signed(n, bytesAmount)</code></td><td><p><code>n</code> (Number): unsigned number</p><p><code>bytesAmount</code> (int): bytes (1, 2, 4, 8)</p></td><td>Long</td><td>Convert unsigned to signed number</td></tr><tr><td><code>util:checkBit(n, bitIndex)</code></td><td><p><code>n</code> (Number): number to check</p><p><code>bitIndex</code> (int): bit position (0=LSB)</p></td><td>Boolean</td><td>Check if bit is set (true) or not (false)</td></tr><tr><td><code>util:bit(n, bitIndex)</code></td><td><p><code>n</code> (Number): number to check</p><p><code>bitIndex</code> (int): bit position (0=LSB)</p></td><td>Integer</td><td>Get bit value (1 or 0)</td></tr><tr><td><code>util:bits(n, firstBit, lastBitInclusive)</code></td><td><p><code>n</code> (Number): source number</p><p><code>firstBit</code> (int): start position</p><p><code>lastBitInclusive</code> (int): end position</p></td><td>Long</td><td>Extract bit range; reverse if last &#x3C; first</td></tr><tr><td><code>util:bytes(n, firstByte, lastByteInclusive)</code></td><td><p><code>n</code> (Number): source number</p><p><code>firstByte</code> (int): start position</p><p><code>lastByteInclusive</code> (int): end position</p></td><td>Long</td><td>Extract byte range; byte swap if last &#x3C; first</td></tr></tbody></table>

**Examples:**

<table><thead><tr><th width="270.81817626953125">Expression</th><th width="109">Result</th><th>Use Case</th></tr></thead><tbody><tr><td><code>util:signed(65535, 2)</code></td><td><code>-1</code></td><td>Convert 0xFFFF to signed 16-bit</td></tr><tr><td><code>util:checkBit(4, 2)</code></td><td><code>true</code></td><td>Check status flag bit</td></tr><tr><td><code>util:bits(1321678, 0, 3)</code></td><td><code>14</code></td><td>Extract 4-bit sensor value</td></tr><tr><td><code>util:bytes(sensor_data, 1, 0)</code></td><td>Swapped</td><td>Little-endian byte swap</td></tr></tbody></table>

#### HEX string operations

Binary data is processed as HEX strings (uppercase) for readability and protocol compatibility.

<table><thead><tr><th>Function</th><th>Parameters</th><th width="92.45452880859375">Type</th><th>Description</th></tr></thead><tbody><tr><td><code>util:hex(n)</code></td><td><code>n</code> (Number): value to convert</td><td>String</td><td>Convert to HEX string; 16 chars for negative/float, variable for positive int; <code>null</code> if invalid</td></tr><tr><td><code>util:hex(n, bytesAmount)</code></td><td><code>n</code> (Number): value to convert<code>bytesAmount</code> (int): byte length</td><td>String</td><td>Convert to fixed-length HEX (bytesAmount * 2 chars); pad/truncate as needed; <code>null</code> if invalid</td></tr><tr><td><code>util:hexToLong(s)</code></td><td><code>s</code> (String): HEX string</td><td>Long</td><td>Convert HEX string to Long; <code>null</code> if invalid</td></tr><tr><td><code>util:hexToLong(s, firstByte, lastByteInclusive)</code></td><td><p><code>s</code> (String): HEX string</p><p><code>firstByte</code> (int): start byte (0=left)</p><p><code>lastByteInclusive</code> (int): end byte</p></td><td>Long</td><td>Extract bytes from HEX string to Long; reverse if last &#x3C; first; <code>null</code> if invalid</td></tr></tbody></table>

**Examples:**

| Expression                       | Result           | Use Case                   |
| -------------------------------- | ---------------- | -------------------------- |
| `util:hex(127)`                  | `"7F"`           | Variable length conversion |
| `util:hex(127, 6)`               | `"00000000007F"` | Fixed-width formatting     |
| `util:hexToLong("FF")`           | `255`            | Parse HEX value            |
| `util:hexToLong("AABBCC", 1, 0)` | Reversed bytes   | Little-endian parsing      |

### Data format conversions

<table><thead><tr><th>Function</th><th>Parameters</th><th width="100.6363525390625">Type</th><th>Description</th></tr></thead><tbody><tr><td><code>util:fromBcd(o)</code></td><td><code>o</code> (Object): BCD number</td><td>Long</td><td>Convert BCD to decimal; <code>null</code> if invalid BCD</td></tr><tr><td><code>util:toBcd(o)</code></td><td><code>o</code> (Object): decimal (0 to 9999999999999999)</td><td>Long</td><td>Convert decimal to BCD; <code>null</code> if out of range</td></tr><tr><td><code>util:toFloat(o)</code></td><td><code>o</code> (Object): Long (IEEE 754 bits) or Double</td><td>Float</td><td>Convert to Float; interpret Long as IEEE 754 bits; <code>null</code> if invalid</td></tr><tr><td><code>util:toDouble(o)</code></td><td><code>o</code> (Object): Long (IEEE 754 bits) or Double</td><td>Double</td><td>Convert to Double; interpret Long as IEEE 754 bits; <code>null</code> if invalid</td></tr></tbody></table>

**Examples:**

| Expression                 | Result          | Use Case                |
| -------------------------- | --------------- | ----------------------- |
| `util:fromBcd(0x1234)`     | `1234`          | Decode BCD device ID    |
| `util:toBcd(1234)`         | `0x1234` (4660) | Encode for BCD protocol |
| `util:toFloat(1065353216)` | `1.0`           | Decode IEEE 754 float   |

### String padding functions

<table><thead><tr><th>Function</th><th>Parameters</th><th width="78.81817626953125">Type</th><th>Description</th></tr></thead><tbody><tr><td><code>util:leftPad(o, length)</code></td><td><code>o</code> (Object): value&#x3C;br><code>length</code> (int): target length</td><td>String</td><td>Pad left with "0" to length; <code>null</code> if input null</td></tr><tr><td><code>util:leftPad(o, length, padStr)</code></td><td><code>o</code> (Object): value&#x3C;br><code>length</code> (int): target length&#x3C;br><code>padStr</code> (String): padding</td><td>String</td><td>Pad left with custom string; <code>null</code> if input null</td></tr><tr><td><code>util:rightPad(o, length)</code></td><td><code>o</code> (Object): value&#x3C;br><code>length</code> (int): target length</td><td>String</td><td>Pad right with "0" to length; <code>null</code> if input null</td></tr><tr><td><code>util:rightPad(o, length, padStr)</code></td><td><code>o</code> (Object): value&#x3C;br><code>length</code> (int): target length&#x3C;br><code>padStr</code> (String): padding</td><td>String</td><td>Pad right with custom string; <code>null</code> if input null</td></tr></tbody></table>

**Examples:**

| Expression                | Result    |
| ------------------------- | --------- |
| `util:leftPad(123, 5)`    | `"00123"` |
| `util:leftPad(7, 3, "*")` | `"**7"`   |
| `util:rightPad(123, 5)`   | `"12300"` |

## Data types and type handling

### Supported data types

| Data Type  | Description                             | Examples             |
| ---------- | --------------------------------------- | -------------------- |
| Integer    | Whole numbers                           | `42`, `-100`, `0xFF` |
| Long       | Large integers with `L` suffix          | `42L`, `9999999999L` |
| Float      | Floating-point with optional `f` suffix | `3.14`, `42.0f`      |
| Double     | Double-precision floating-point         | `3.14`, `42.0d`      |
| String     | Text enclosed in quotes                 | `"text"`, `'text'`   |
| Boolean    | True or false values                    | `true`, `false`      |
| HEX String | Uppercase hexadecimal representation    | `"FF"`, `"1A2B"`     |
| Null       | Absence of value                        | `null`               |

### Null propagation

**Rule:** Null values propagate through expressions without errors. When any operand is null, the expression typically evaluates to null.

| Expression         | Result  | Notes                  |
| ------------------ | ------- | ---------------------- |
| `null + 5`         | `null`  | Arithmetic with null   |
| `temperature + 10` | `null`  | If temperature is null |
| `null == null`     | `true`  | Null equality          |
| `null != 5`        | `true`  | Null comparison        |
| `null > 0`         | `false` | Null in comparison     |

{% hint style="info" %}
In **Logic** nodes expressions evaluating to null are treated as `false` and route through ELSE path.
{% endhint %}

#### Error conditions resulting in null

| Condition               | Expression example                 | Result                         |
| ----------------------- | ---------------------------------- | ------------------------------ |
| Invalid function input  | `util:hexToLong("invalid")`        | `null`                         |
| Invalid BCD             | `util:fromBcd(0x99A0)`             | `null`                         |
| Missing historical data | `value('temperature', 5, 'valid')` | `null` (if < 5 valid readings) |
| Type mismatch           | `"text" + 123`                     | `null`                         |

{% hint style="danger" %}
Mismatched attribute names prevent calculation execution (no null returned; calculation skipped).
{% endhint %}

## Expression patterns

<table><thead><tr><th width="159">Pattern Type</th><th>Expression</th><th>Use Case</th></tr></thead><tbody><tr><td><strong>Unit conversion</strong></td><td><code>temperature * 1.8 + 32</code></td><td>Celsius to Fahrenheit</td></tr><tr><td></td><td><code>distance / 1.609</code></td><td>Kilometers to miles</td></tr><tr><td></td><td><code>volume * 0.264172</code></td><td>Liters to gallons</td></tr><tr><td><strong>Change detection</strong></td><td><code>temperature - value('temperature', 1, 'all')</code></td><td>Temperature change</td></tr><tr><td></td><td><code>value('fuel_level', 1, 'valid') - fuel_level</code></td><td>Fuel consumption</td></tr><tr><td></td><td><code>speed - value('speed', 1, 'valid')</code></td><td>Speed change</td></tr><tr><td><strong>Binary parsing</strong></td><td><code>util:signed(util:hexToLong(hex_data, 0, 1), 2) / 10.0</code></td><td>Signed temp from HEX</td></tr><tr><td></td><td><code>util:checkBit(status_flags, 0)</code></td><td>Check status flag</td></tr><tr><td></td><td><code>util:bits(status_word, 4, 7)</code></td><td>Extract sensor value</td></tr><tr><td><strong>Time calculations</strong></td><td><code>now() - genTime('temperature', 0, 'all')</code></td><td>Data age</td></tr><tr><td></td><td><code>srvTime('temp', 0, 'all') - genTime('temp', 0, 'all')</code></td><td>Transmission delay</td></tr><tr><td></td><td><code>genTime('temperature', 0, 'valid') + 120000</code></td><td>Time offset (2 min)</td></tr></tbody></table>

## Quick reference tables

#### Core functions summary

<table><thead><tr><th>Function</th><th width="99.90911865234375">Type</th><th>Primary Use</th></tr></thead><tbody><tr><td><code>value(attr, idx, val)</code></td><td>Any</td><td>Historical attribute value</td></tr><tr><td><code>genTime(attr, idx, val)</code></td><td>Long</td><td>Device generation time (default: <code>now()</code>)</td></tr><tr><td><code>srvTime(attr, idx, val)</code></td><td>Long</td><td>Server reception time (default: <code>now()</code>)</td></tr></tbody></table>

#### Bit operations summary

<table><thead><tr><th>Function</th><th width="99.90911865234375">Type</th><th>Primary Use</th></tr></thead><tbody><tr><td><code>util:signed(n, bytes)</code></td><td>Long</td><td>Convert unsigned to signed</td></tr><tr><td><code>util:checkBit(n, bit)</code></td><td>Boolean</td><td>Check if bit is set</td></tr><tr><td><code>util:bit(n, bit)</code></td><td>Integer</td><td>Get bit value (0/1)</td></tr><tr><td><code>util:bits(n, first, last)</code></td><td>Long</td><td>Extract bit range</td></tr><tr><td><code>util:bytes(n, first, last)</code></td><td>Long</td><td>Extract byte range</td></tr></tbody></table>

#### HEX operations summary

<table><thead><tr><th>Function</th><th width="99.90911865234375">Type</th><th>Primary Use</th></tr></thead><tbody><tr><td><code>util:hex(n)</code></td><td>String</td><td>Number to variable-length HEX</td></tr><tr><td><code>util:hex(n, bytes)</code></td><td>String</td><td>Number to fixed-length HEX</td></tr><tr><td><code>util:hexToLong(s)</code></td><td>Long</td><td>HEX string to number</td></tr><tr><td><code>util:hexToLong(s, first, last)</code></td><td>Long</td><td>Extract bytes from HEX string</td></tr></tbody></table>

#### Data conversion summary

<table><thead><tr><th>Function</th><th width="99.90911865234375">Type</th><th>Primary Use</th></tr></thead><tbody><tr><td><code>util:fromBcd(o)</code></td><td>Long</td><td>BCD to decimal</td></tr><tr><td><code>util:toBcd(o)</code></td><td>Long</td><td>Decimal to BCD</td></tr><tr><td><code>util:toFloat(o)</code></td><td>Float</td><td>IEEE 754 bits to float</td></tr><tr><td><code>util:toDouble(o)</code></td><td>Double</td><td>IEEE 754 bits to double</td></tr></tbody></table>

#### String operations summary

<table><thead><tr><th>Function</th><th width="99.9090576171875">Type</th><th>Primary Use</th></tr></thead><tbody><tr><td><code>util:leftPad(o, len)</code></td><td>String</td><td>Pad left with "0"</td></tr><tr><td><code>util:leftPad(o, len, pad)</code></td><td>String</td><td>Pad left with custom string</td></tr><tr><td><code>util:rightPad(o, len)</code></td><td>String</td><td>Pad right with "0"</td></tr><tr><td><code>util:rightPad(o, len, pad)</code></td><td>String</td><td>Pad right with custom string</td></tr></tbody></table>
