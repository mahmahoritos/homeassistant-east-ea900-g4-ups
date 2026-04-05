"""System operating mode (input register 71) — enum state keys and lookup."""

from __future__ import annotations

from typing import Final

# Internal state strings for SensorDeviceClass.ENUM (English keys; UI via translations).
SYSTEM_OPERATING_MODE_OPTIONS: Final[tuple[str, ...]] = (
    "unknown",
    "bypass_mode",
    "online_mode",
    "battery_mode",
    "mode_0",
    "mode_1",
    "mode_2",
    "mode_5",
    "mode_7",
    "mode_8",
    "mode_9",
    "mode_10",
    "mode_extended",
)


def system_operating_mode_state(mode: int | None) -> str:
    """Map raw register value to a fixed ENUM option id.

    Known codes (field observation): 3 bypass, 4 online, 6 battery.
    Other values 0–10 use mode_<n> except 3, 4, 6 which use the known names.
    Values outside 0–10 map to mode_extended (raw code in entity attributes).
    """
    if mode is None:
        return "unknown"
    if mode == 3:
        return "bypass_mode"
    if mode == 4:
        return "online_mode"
    if mode == 6:
        return "battery_mode"
    if mode in (0, 1, 2, 5, 7, 8, 9, 10):
        return f"mode_{mode}"
    return "mode_extended"
