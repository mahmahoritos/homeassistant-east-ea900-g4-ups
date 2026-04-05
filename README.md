# EAST EA900 G4 UPS (Home Assistant)

Custom integration for **EAST EA900 G4** series UPS (6–20 kVA) via **Modbus TCP** (for example, a Modbus TCP → RS232 gateway). Telemetry uses **function code 0x04** (input registers); alarms use **0x02** (discrete inputs); commands use **holding registers 0x8000–0x8007** (function **0x06**), per the manufacturer Modbus protocol.

## Requirements

- Home Assistant 2024.1 or newer
- Network access from Home Assistant to the Modbus TCP gateway
- Correct RS232 parameters on the gateway (per UPS manual, commonly 9600 8N1)

## Installation

### HACS

1. HACS → **Integrations** → **⋮** → **Custom repositories**
2. Add this repository URL, category **Integration**
3. Install **EAST EA900 G4 UPS** and restart Home Assistant

### Manual

Copy `custom_components/east_ea900_g4_ups` into your Home Assistant `config/custom_components/` directory and restart.

## Configuration

**Settings → Devices & services → Add integration → EAST EA900 G4 UPS**

- **Host / port**: your Modbus TCP gateway
- **Modbus slave ID**: unit ID configured on the gateway (often `1`)

## Entities overview

- **Sensors**: input/output electrical values, battery, temperatures, software version fields (when available), status word, **system operating mode** (ENUM + raw `code` attribute), **active / apparent / reactive power** in **kW / kVA / kvar** with **0.1** resolution per Modbus (one decimal in the UI)
- **Binary sensors**: discrete-input alarm bits **except reserved** manufacturer positions (bits 32–47 and 79); those addresses are **not** requested over Modbus (three FC 0x02 reads: 0–31, 48–78, 80–95). A subset of entities is enabled by default, the rest can be turned on in the entity registry
- **Buttons**: clear fault, buzzer silence, battery test (20 s), stop battery test, optional manual bypass/inverter and maintenance discharge (disabled by default)

### System operating mode (register 71)

| Code (attribute `code`) | English (UI)   | Русский (UI)        |
|-------------------------|----------------|---------------------|
| 3                       | Bypass mode    | Режим байпаса       |
| 4                       | Online mode    | Нормальный режим    |
| 6                       | Battery mode   | Режим работы от батарей |
| 0, 1, 2, 5, 7–10        | Mode *n*       | Режим *n*           |
| \>10                    | Mode above 10  | Режим выше 10       |
| unavailable             | Unknown        | Неизвестно          |

Automations can use the numeric attribute `code` on **System operating mode** when needed.

## Credits

Derived in structure from [homeassistant-ever-powerline-ups](https://github.com/corapoid/homeassistant-ever-powerline-ups) (Ever UPS), adapted for EAST EA900 G4 register maps.

## License

MIT — see [LICENSE](LICENSE).
