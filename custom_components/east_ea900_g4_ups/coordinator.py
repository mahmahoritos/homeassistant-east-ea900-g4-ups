"""DataUpdateCoordinator for EAST EA900 G4 UPS."""

from __future__ import annotations

import asyncio
import logging
from datetime import timedelta
from typing import Any

from pymodbus.client import AsyncModbusTcpClient
from pymodbus.exceptions import ModbusException

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    DEFAULT_SCAN_INTERVAL,
    DISCRETE_INPUT_COUNT,
    DISCRETE_INPUT_READ_SEGMENTS,
    DOMAIN,
    INPUT_REGISTER_COUNT,
)
from .operating_mode import system_operating_mode_state

_LOGGER = logging.getLogger(__name__)


def _to_int16(unsigned: int) -> int:
    """Convert 16-bit unsigned Modbus value to signed int."""
    if unsigned & 0x8000:
        return unsigned - 0x10000
    return unsigned


def _decode_ascii_registers(registers: list[int], max_chars: int) -> str:
    """Decode ASCII from consecutive 16-bit registers (high byte, low byte)."""
    chars: list[str] = []
    for reg in registers:
        for byte in ((reg >> 8) & 0xFF, reg & 0xFF):
            if 0x20 <= byte <= 0x7E:
                chars.append(chr(byte))
    return "".join(chars).strip("\x00").strip()[:max_chars]


class EastEA900G4UPSCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator for EAST EA900 G4 UPS via Modbus TCP gateway."""

    def __init__(
        self,
        hass: HomeAssistant,
        host: str,
        port: int,
        slave_id: int,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )
        self.host = host
        self.port = port
        self.slave_id = slave_id
        self._client: AsyncModbusTcpClient | None = None
        self._lock = asyncio.Lock()

        self.software_version: str = ""

    async def _ensure_connected(self) -> AsyncModbusTcpClient:
        """Ensure we have a connected client."""
        if self._client is None or not self._client.connected:
            self._client = AsyncModbusTcpClient(
                host=self.host,
                port=self.port,
                timeout=10,
            )
            connected = await self._client.connect()
            if not connected:
                raise UpdateFailed(f"Failed to connect to {self.host}:{self.port}")
        return self._client

    async def async_close(self) -> None:
        """Close the Modbus connection."""
        if self._client is not None:
            self._client.close()
            self._client = None

    def _none_if_invalid(self, raw: int) -> int | None:
        """Treat 0xFFFF as unavailable."""
        return None if raw == 0xFFFF else raw

    def _scaled_int16(self, raw: int, divisor: float) -> float | None:
        """Scale signed int16; None if unavailable."""
        if raw == 0xFFFF:
            return None
        return _to_int16(raw) / divisor

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from the UPS."""
        async with self._lock:
            try:
                client = await self._ensure_connected()
                data: dict[str, Any] = {}

                bits = [False] * DISCRETE_INPUT_COUNT
                for start, count in DISCRETE_INPUT_READ_SEGMENTS:
                    di_result = await client.read_discrete_inputs(
                        start,
                        count=count,
                        device_id=self.slave_id,
                    )
                    if di_result.isError():
                        raise UpdateFailed(
                            f"Failed to read discrete inputs at {start} (alarms)"
                        )
                    raw_bits = di_result.bits
                    if len(raw_bits) < count:
                        raise UpdateFailed("Discrete input response too short")
                    for i in range(count):
                        bits[start + i] = bool(raw_bits[i])
                data["discrete_inputs"] = bits

                ir_result = await client.read_input_registers(
                    0,
                    count=INPUT_REGISTER_COUNT,
                    device_id=self.slave_id,
                )
                if ir_result.isError():
                    raise UpdateFailed("Failed to read input registers (telemetry)")

                reg = ir_result.registers

                if len(reg) >= INPUT_REGISTER_COUNT:
                    ver = _decode_ascii_registers(reg[67:70], 12)
                    if ver:
                        self.software_version = ver

                # Telemetry (addresses per manufacturer table, 0-based)
                data["bypass_voltage_a"] = self._scaled_int16(reg[0], 10.0)
                data["bypass_current_a"] = self._scaled_int16(reg[3], 10.0)
                data["bypass_frequency"] = self._scaled_int16(reg[6], 10.0)
                data["bypass_power_factor"] = self._scaled_int16(reg[9], 100.0)

                data["input_voltage_a"] = self._scaled_int16(reg[12], 10.0)
                data["input_voltage_b"] = self._scaled_int16(reg[13], 10.0)
                data["input_voltage_c"] = self._scaled_int16(reg[14], 10.0)
                data["input_current_a"] = self._scaled_int16(reg[15], 10.0)
                data["input_current_b"] = self._scaled_int16(reg[16], 10.0)
                data["input_current_c"] = self._scaled_int16(reg[17], 10.0)
                data["input_frequency"] = self._scaled_int16(reg[18], 10.0)
                data["input_power_factor"] = self._scaled_int16(reg[21], 100.0)

                data["output_voltage_a"] = self._scaled_int16(reg[24], 10.0)
                data["output_current_a"] = self._scaled_int16(reg[27], 10.0)
                data["output_frequency"] = self._scaled_int16(reg[30], 10.0)
                data["output_power_factor"] = self._scaled_int16(reg[33], 100.0)

                # Apparent power: register × 0.1 kVA (per protocol table).
                s_kva = self._none_if_invalid(reg[36])
                data["output_apparent_power"] = (
                    None if s_kva is None else _to_int16(s_kva) * 0.1
                )

                # Active power: register × 0.1 kW.
                p_kw = self._none_if_invalid(reg[39])
                data["output_active_power"] = (
                    None if p_kw is None else _to_int16(p_kw) * 0.1
                )

                # Reactive power: register × 0.1 kvar.
                q_kvar = self._none_if_invalid(reg[42])
                data["output_reactive_power"] = (
                    None if q_kvar is None else _to_int16(q_kvar) * 0.1
                )

                data["output_load_percent"] = self._scaled_int16(reg[45], 10.0)

                data["battery_voltage"] = self._scaled_int16(reg[49], 10.0)
                data["battery_current"] = self._scaled_int16(reg[51], 10.0)
                data["battery_temperature"] = self._scaled_int16(reg[53], 10.0)

                rt = self._none_if_invalid(reg[54])
                data["battery_runtime_remaining"] = (
                    None if rt is None else float(_to_int16(rt))
                )

                data["battery_capacity"] = self._scaled_int16(reg[55], 10.0)
                data["inverter_current"] = self._scaled_int16(reg[56], 10.0)
                data["rectifier_temperature"] = self._scaled_int16(reg[57], 10.0)
                data["inverter_temperature"] = self._scaled_int16(reg[58], 10.0)

                sw = self._none_if_invalid(reg[70])
                data["status_word"] = None if sw is None else sw

                om = self._none_if_invalid(reg[71])
                om_int = None if om is None else int(om)
                data["system_operating_mode"] = om_int
                data["system_operating_mode_state"] = system_operating_mode_state(om_int)

                return data

            except ModbusException as err:
                self._client = None
                raise UpdateFailed(f"Modbus error: {err}") from err
            except Exception as err:
                self._client = None
                raise UpdateFailed(f"Error communicating with UPS: {err}") from err

    async def async_write_register(self, address: int, value: int) -> bool:
        """Write a single holding register."""
        async with self._lock:
            try:
                client = await self._ensure_connected()
                result = await client.write_register(
                    address, value, device_id=self.slave_id
                )
                if result.isError():
                    _LOGGER.error(
                        "Failed to write register 0x%04X: %s", address, result
                    )
                    return False
                return True
            except ModbusException as err:
                _LOGGER.error("Modbus error writing register: %s", err)
                return False

    @property
    def device_info(self) -> dict[str, Any]:
        """Return device info for the UPS."""
        uid = f"{self.host}_{self.slave_id}"
        return {
            "identifiers": {(DOMAIN, uid)},
            "name": "EAST EA900 G4 UPS",
            "manufacturer": "EAST",
            "model": "EA900 G4",
            "sw_version": self.software_version or None,
        }
