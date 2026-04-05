"""Constants for EAST EA900 G4 UPS (Modbus)."""
from __future__ import annotations

from typing import Final

DOMAIN: Final = "east_ea900_g4_ups"

DEFAULT_PORT: Final = 502
DEFAULT_SLAVE_ID: Final = 1
DEFAULT_SCAN_INTERVAL: Final = 10

# Modbus: discrete inputs (FC 0x02), addresses 0..95 per manufacturer doc
DISCRETE_INPUT_COUNT: Final = 96

# Input registers (FC 0x04), addresses 0..71
INPUT_REGISTER_COUNT: Final = 72

# Command holding registers (FC 0x06), per EA900 G4 Modbus protocol
REG_CLEAR_FAULT: Final = 0x8000
REG_CLEAR_HISTORY_LOG: Final = 0x8001
REG_BUZZER_SILENCE: Final = 0x8002
REG_MANUAL_SWITCH_BYPASS: Final = 0x8003
REG_MANUAL_SWITCH_INVERTER: Final = 0x8004
REG_CLEAR_BATTERY_DATA: Final = 0x8005
REG_BATTERY_TEST: Final = 0x8006
REG_STOP_BATTERY_TEST: Final = 0x8007

CMD_ACTIVATE: Final = 1
BATTERY_TEST_DISCHARGE_20S: Final = 1
BATTERY_TEST_MAINTENANCE: Final = 2

PLATFORMS: Final = ["sensor", "binary_sensor", "button"]

CONF_SLAVE_ID: Final = "slave_id"
