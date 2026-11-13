# Coverage matrix

FULL zde znamená bohaté použitelné pokrytí vymezeného tématu, nikoli kopii všech stránek manuálu nebo HW přijetí. Přesný strojový přehled: [coverage.json](coverage.json).

| Oblast | Stav | Rozsah a mezera |
|---|---|---|
| A — Hardware/model selection | PARTIAL | Model families, FOV examples/conditional limits; not every dimension/accessory pinout reproduced |
| B — Navigator workflow and programs | FULL | Detailed setup/program/storage workflow within cited manual versions; runtime unverified |
| C — Vision tool families | FULL | Major supported tool classes and concrete decision/parameter checks; not every UI parameter page |
| C2 — All per-tool advanced UI parameters | PARTIAL | Exact uncommon parameter requires source/corpus retrieval |
| D — Logic/validity/trigger/buffering | FULL | Total/Logic and physical 2-image Buffer distinction, source-scoped |
| E — Documented command inventory | FULL | 43 IV4 + 46 IV4-H rows; every formal syntax and detail reference |
| E2 — Wire parameters and anomalies | PARTIAL | Own parameter summaries for all 46 variants; unresolved source CSR/ITR/MC/BR conflicts remain explicit |
| F — PLC integration workflows | FULL | Siemens/OMRON/Rockwell/Beckhoff distinctions, EIP/PN/ECAT and handshake |
| F2 — GSDML module identity/type navigation | FULL | 3 XML versions, 33 module entries; selected field examples |
| F3 — Complete active PLC IO map | REFERENCED_ONLY | Original descriptor/local evidence + chosen PLC project required; no universal offsets |
| G — Network services and images | FULL | OPC UA/MQTT/FTP-SFTP/BR roles, security, framing and freshness |
| G2 — Every OPC UA/MQTT schema field | PARTIAL | Important fields/methods and source conflicts; full schema needs exact manual/device Browse |
| H — Troubleshooting | FULL | Symptom/minimal-test branches, protocol vs device errors |
| I — Practical application design | FULL | Sourced tools + GENERAL validation procedures; no claimed physical accuracy |
| I2 — Barcode/QR reader | UNVERIFIED | No supported decoder established; AI OCR is not barcode proof |
| J — GPixel methods/capabilities/experiments | FULL | Explicit INFERRED design, not implementation |
| WEB — Official current supplement | FULL | 13 source URLs checked; exact release and catalog dates kept separate |
| ACCESS — Restricted/dynamic downloads | PARTIAL | Serial-number markers and parsed-view limits; no bypass/download of binaries |
| HW — Runtime/HW interoperability | UNVERIFIED | No IV4 camera/PLC operation performed |

## Mapování proti kapitolám manuálů


### IV4_UserManual_WW_GB_AS_167146.pdf / iv4_82ffe8b0fedc105a

- PDF p.2 — Introduction: PARTIAL, reference source-map.md; úplný detail přes source lookup.
- PDF p.3 — Safety Information: PARTIAL, reference source-map.md; úplný detail přes source lookup.
- PDF p.4 — Important Instructions: PARTIAL, reference source-map.md; úplný detail přes source lookup.
- PDF p.6 — Safety Precautions on LED Product: PARTIAL, reference source-map.md; úplný detail přes source lookup.
- PDF p.7 — Precautions on Regulations and Standards: PARTIAL, reference source-map.md; úplný detail přes source lookup.
- PDF p.10 — Version of the IV4 Series: PARTIAL, reference source-map.md; úplný detail přes source lookup.
- PDF p.11 — Contents: PARTIAL, reference source-map.md; úplný detail přes source lookup.
- PDF p.19 — Chapter 1 Getting Started: PARTIAL, reference hardware.md; úplný detail přes source lookup.
- PDF p.37 — Chapter 2 Installation and Connection: PARTIAL, reference hardware.md; úplný detail přes source lookup.
- PDF p.69 — Chapter 3 Basic Operation: PARTIAL, reference navigator.md; úplný detail přes source lookup.
- PDF p.87 — Chapter 4 Sensor Setup: PARTIAL, reference vision-tools.md; úplný detail přes source lookup.
- PDF p.179 — Chapter 5 Running: PARTIAL, reference evaluation-logic.md; úplný detail přes source lookup.
- PDF p.197 — Chapter 6 Adjusting: PARTIAL, reference navigator.md; úplný detail přes source lookup.
- PDF p.223 — Chapter 7 Various Functions: PARTIAL, reference navigator.md; úplný detail přes source lookup.
- PDF p.261 — Chapter 8 Saving Settings and Images, SD Card: PARTIAL, reference navigator.md; úplný detail přes source lookup.
- PDF p.281 — Chapter 9 Connecting to a Network: PARTIAL, reference tcp-contract.md; úplný detail přes source lookup.
- PDF p.447 — Chapter 10 Simulator (PC Only): PARTIAL, reference navigator.md; úplný detail přes source lookup.
- PDF p.459 — Chapter 11 Controlling with the Input/Output Line: PARTIAL, reference evaluation-logic.md; úplný detail přes source lookup.
- PDF p.481 — Chapter 12 Specifications: PARTIAL, reference hardware.md; úplný detail přes source lookup.
- PDF p.519 — Appendices: PARTIAL, reference troubleshooting.md; úplný detail přes source lookup.

### IV4_UserManual_WW_GB_AS_170071.pdf / iv4_f2b18663143f7e12

- PDF p.2 — Introduction: PARTIAL, reference source-map.md; úplný detail přes source lookup.
- PDF p.3 — Safety Information: PARTIAL, reference source-map.md; úplný detail přes source lookup.
- PDF p.4 — Important Instructions: PARTIAL, reference source-map.md; úplný detail přes source lookup.
- PDF p.6 — Safety Precautions on LED Product: PARTIAL, reference source-map.md; úplný detail přes source lookup.
- PDF p.7 — Precautions on Regulations and Standards: PARTIAL, reference source-map.md; úplný detail přes source lookup.
- PDF p.10 — Version of IV4-H: PARTIAL, reference source-map.md; úplný detail přes source lookup.
- PDF p.11 — Contents: PARTIAL, reference source-map.md; úplný detail přes source lookup.
- PDF p.21 — Chapter 1 Getting Started: PARTIAL, reference hardware.md; úplný detail přes source lookup.
- PDF p.39 — Chapter 2 Installation and Connection: PARTIAL, reference hardware.md; úplný detail přes source lookup.
- PDF p.71 — Chapter 3 Basic Operation: PARTIAL, reference navigator.md; úplný detail přes source lookup.
- PDF p.89 — Chapter 4 Sensor Setup: PARTIAL, reference vision-tools.md; úplný detail přes source lookup.
- PDF p.205 — Chapter 5 Running: PARTIAL, reference evaluation-logic.md; úplný detail přes source lookup.
- PDF p.229 — Chapter 6 Adjusting: PARTIAL, reference navigator.md; úplný detail přes source lookup.
- PDF p.255 — Chapter 7 Various Functions: PARTIAL, reference navigator.md; úplný detail přes source lookup.
- PDF p.293 — Chapter 8 Saving Settings and Images, SD Card: PARTIAL, reference navigator.md; úplný detail přes source lookup.
- PDF p.313 — Chapter 9 Connecting to a Network: PARTIAL, reference tcp-contract.md; úplný detail přes source lookup.
- PDF p.529 — Chapter 10 Simulator (PC Only): PARTIAL, reference navigator.md; úplný detail přes source lookup.
- PDF p.541 — Chapter 11 Controlling with the Input/Output Line: PARTIAL, reference evaluation-logic.md; úplný detail přes source lookup.
- PDF p.563 — Chapter 12 Specifications: PARTIAL, reference hardware.md; úplný detail přes source lookup.
- PDF p.601 — Appendices: PARTIAL, reference troubleshooting.md; úplný detail přes source lookup.
