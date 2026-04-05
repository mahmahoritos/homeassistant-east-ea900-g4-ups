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

- **Sensors**: input/output electrical values, battery, temperatures, software version fields (when available), status word, operating mode code
- **Binary sensors**: selected alarm bits from the discrete-input table (enable more in the entity registry if needed)
- **Buttons**: clear fault, buzzer silence, battery test (20 s), stop battery test, optional manual bypass/inverter and maintenance discharge (disabled by default)

**Note:** Numeric **system operating mode** values are device-specific; extend automations using numeric thresholds or map values after observing your unit.

## Credits

Derived in structure from [homeassistant-ever-powerline-ups](https://github.com/corapoid/homeassistant-ever-powerline-ups) (Ever UPS), adapted for EAST EA900 G4 register maps.

## License

MIT — see [LICENSE](LICENSE).
