"""Config flow for EAST EA900 G4 UPS."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from pymodbus.client import AsyncModbusTcpClient
from pymodbus.exceptions import ModbusException

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_HOST, CONF_PORT

from .const import (
    CONF_SLAVE_ID,
    DEFAULT_PORT,
    DEFAULT_SLAVE_ID,
    DOMAIN,
    INPUT_REGISTER_COUNT,
)

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
        vol.Required(CONF_PORT, default=DEFAULT_PORT): vol.All(
            vol.Coerce(int), vol.Range(min=1, max=65535)
        ),
        vol.Required(CONF_SLAVE_ID, default=DEFAULT_SLAVE_ID): vol.All(
            vol.Coerce(int), vol.Range(min=1, max=247)
        ),
    }
)


class EastEA900G4UPSConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for EAST EA900 G4 UPS."""

    VERSION = 1

    async def _test_connection(
        self, host: str, port: int, slave_id: int
    ) -> bool:
        """Verify Modbus TCP access by reading input registers."""
        client = AsyncModbusTcpClient(host=host, port=port, timeout=10)
        try:
            if not await client.connect():
                return False
            result = await client.read_input_registers(
                0,
                count=min(8, INPUT_REGISTER_COUNT),
                device_id=slave_id,
            )
            return not result.isError()
        except ModbusException as err:
            _LOGGER.error("Modbus error during connection test: %s", err)
            return False
        except Exception as err:
            _LOGGER.error("Error during connection test: %s", err)
            return False
        finally:
            client.close()

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            host = user_input[CONF_HOST]
            port = user_input[CONF_PORT]
            slave_id = user_input[CONF_SLAVE_ID]

            if await self._test_connection(host, port, slave_id):
                unique_id = f"{host}_{slave_id}"
                await self.async_set_unique_id(unique_id)
                self._abort_if_unique_id_configured()

                title = f"EAST EA900 G4 ({host})"
                return self.async_create_entry(title=title, data=user_input)

            errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )
