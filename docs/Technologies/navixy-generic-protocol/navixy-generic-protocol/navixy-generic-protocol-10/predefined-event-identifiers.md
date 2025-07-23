# Predefined event identifiers

Navixy Generic Protocol includes pre-defined event identifiers (`event_id`) for the most common cases and alerts. Use these standard IDs whenever possible, reserving custom IDs (starting from 10,000) for unmatched events.

### Power

The range for power alerts is 1 – 100.

| **Event id** | **Description** |
| --- | --- |
| 1   | Low battery |
| 2   | Power lost or external power cut |
| 3   | Power On button pressed |
| 4   | Power recovered or external power connected |
| 5   | OBD Unplug from the car’s connector |
| 6   | OBD Plug in |
| 7   | Device’s backup battery low |
| 8   | Device wakes up from a sleep mode |
| 9   | Sleep mode start |
| 10  | Timer wakeup |
| 11  | Motion wakeup |
| 12  | External power wakeup |
| 13  | Power Off button pressed |
| 14  | Device power Off |
| 15  | Device power On |

### Security

The range for security alerts is 101 – 200.

| **Identifier** | **Description** |
| --- | --- |
| 101 | Unauthorized movement event determined by the device (tow detection) |
| 102 | Unauthorized movement end |
| 103 | Device detached from the tracked object |
| 104 | Car alarm |
| 105 | Device’s case closed |
| 106 | Device’s case opened |
| 107 | Unplug from the tracked object |
| 108 | Attach device to the tracked object |
| 109 | Door alarm |
| 110 | Device’s lock closed |
| 111 | Device’s lock opened |
| 112 | Vibration end |
| 113 | Vibration start |
| 114 | Strap bolt Inserted |
| 115 | Strap bolt cut |
| 116 | GPS jamming |
| 117 | GSM signal jamming alarm |
| 118 | Bracelet open |
| 119 | Bracelet closed |
| 120 | G sensor alert |

### Safety

The range for safety alerts is 201 – 300.

| **Identifier** | **Description** |
| --- | --- |
| 201 | Emergency contact number called |
| 202 | SOS button pressed event |
| 203 | Cruise control switched on |
| 204 | Cruise control switched off |
| 205 | DMS. Driver not identified |
| 206 | DMS. Driver identified |
| 207 | ADAS. Frequent lane change |
| 208 | DMS. Device can't detect human face |
| 209 | Seat belt unbuckled |
| 210 | DMS. Driver is drinking |
| 211 | DMS. Driver eyes are closed |
| 212 | DMS. Report new driver detection |
| 213 | DMS. Driver enters cabin |
| 214 | DMS. Start driver absence |
| 215 | DMS. Driver stopped smoking (Driver distraction) |
| 216 | DMS. Driver started smoking (Driver distraction) |
| 217 | DMS. Driver finished using the phone (Driver distraction) |
| 218 | DMS. Driver started using the phone (Driver distraction) |
| 219 | DMS. Yawning detected (Fatigue driving) |
| 220 | DMS. Driver stopped distraction (Driver distraction) |
| 221 | DMS. Driver started distraction (Driver distraction) |
| 222 | DMS. Driver stop drowsiness (Fatigue driving) |
| 223 | DMS. Driver start drowsiness (Fatigue driving) |
| 224 | Over speeding |
| 225 | Unexpected movement start |
| 226 | Unexpected movement end |
| 227 | ADAS. Peds in danger zone |
| 228 | ADAS. Traffic sign recognition |
| 229 | ADAS. Peds collision warning |
| 230 | Fatigue driving |
| 231 | ADAS. Headway warning |
| 232 | ADAS. Right lane departure |
| 233 | ADAS. Left lane departure |
| 234 | ADAS. Lane departure |
| 235 | ADAS. Forward collision warning |
| 236 | Harsh driving quick lane change |
| 237 | Harsh driving acceleration and turn |
| 238 | Harsh driving braking and turn |
| 239 | Harsh driving turn |
| 240 | Harsh driving acceleration |
| 241 | Harsh driving braking |
| 242 | Crash alarm |
| 243 | Harsh driving |
| 244 | Call button pressed |

### Vehicle efficiency

The range for vehicle efficiency alerts is 301 – 400.

| **Identifier** | **Description** |
| --- | --- |
| 301 | Idle end |
| 302 | Idle start |
| 303 | Check engine light |

### Track information

The range for track information alerts is 401 – 500.

| **Identifier** | **Description** |
| --- | --- |
| 401 | Track. No specific event, just a track point |
| 402 | GSM LBS point report |
| 403 | Track point by time |
| 404 | Track point by distance |
| 405 | Track point by angle |
| 406 | Track movement start |
| 407 | Track movement end |
| 408 | Non-track message |
| 409 | Tracker entered auto geofence |
| 410 | Tracker exited auto geofence |

### Inputs

The range for inputs is 501 – 550.

| **Identifier** | **Description** |
| --- | --- |
| 501 | Input 1 state changed |
| 502 | Input 2 state changed |
| 503 | Input 3 state changed |
| 504 | Input 4 state changed |
| 505 | Input 5 state changed |
| 506 | Input 6 state changed |
| 507 | Input 7 state changed |
| 508 | Input 8 state changed |

### Outputs

The range for outputs is 551 – 600.

| **Identifier** | **Description** |
| --- | --- |
| 551 | Output 1 state changed |
| 552 | Output 2 state changed |
| 553 | Output 3 state changed |
| 554 | Output 4 state changed |
| 555 | Output 5 state changed |
| 556 | Output 6 state changed |
| 557 | Output 7 state changed |
| 558 | Output 8 state changed |

### Peripherals and other

The range for inputs and outputs alerts is 601 – 700.

| **Identifier** | **Description** |
| --- | --- |

| **Identifier** | **Description** |
| --- | --- |
| 601 | Antenna disconnected |
| 602 | Accessory disconnected |
| 603 | Accessory connected |
| 604 | Ignition Off |
| 605 | Ignition On |
| 606 | Light sensor determined dark |
| 607 | Light Sensor determined bright |
| 608 | GPS signal recovered |
| 609 | GPS signal lost |