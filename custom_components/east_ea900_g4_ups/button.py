"""Button platform for EAST EA900 G4 UPS (Modbus holding commands)."""

from __future__ import annotations

from dataclasses import dataclass
import logging

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    BATTERY_TEST_DISCHARGE_20S,
    BATTERY_TEST_MAINTENANCE,
    CMD_ACTIVATE,
    REG_BATTERY_TEST,
    REG_BUZZER_SILENCE,
    REG_CLEAR_FAULT,
    REG_MANUAL_SWITCH_BYPASS,
    REG_MANUAL_SWITCH_INVERTER,
    REG_STOP_BATTERY_TEST,
)
from .const import DOMAIN
from .coordinator import EastEA900G4UPSCoordinator

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, kw_only=True)
class EastUPSButtonEntityDescription(ButtonEntityDescription):
    """Describes EAST UPS button entity."""

    register_address: int
    register_value: int


BUTTON_DESCRIPTIONS: tuple[EastUPSButtonEntityDescription, ...] = (
    EastUPSButtonEntityDescription(
        key="clear_fault",
        translation_key="clear_fault",
        icon="mdi:bell-cancel",
        register_address=REG_CLEAR_FAULT,
        register_value=CMD_ACTIVATE,
    ),
    EastUPSButtonEntityDescription(
        key="buzzer_silence",
        translation_key="buzzer_silence",
        icon="mdi:volume-off",
        register_address=REG_BUZZER_SILENCE,
        register_value=CMD_ACTIVATE,
    ),
    EastUPSButtonEntityDescription(
        key="manual_switch_bypass",
        translation_key="manual_switch_bypass",
        icon="mdi:swap-horizontal",
        register_address=REG_MANUAL_SWITCH_BYPASS,
        register_value=CMD_ACTIVATE,
        entity_registry_enabled_default=False,
    ),
    EastUPSButtonEntityDescription(
        key="manual_switch_inverter",
        translation_key="manual_switch_inverter",
        icon="mdi:current-ac",
        register_address=REG_MANUAL_SWITCH_INVERTER,
        register_value=CMD_ACTIVATE,
        entity_registry_enabled_default=False,
    ),
    EastUPSButtonEntityDescription(
        key="battery_test_20s",
        translation_key="battery_test_20s",
        icon="mdi:battery-sync",
        register_address=REG_BATTERY_TEST,
        register_value=BATTERY_TEST_DISCHARGE_20S,
    ),
    EastUPSButtonEntityDescription(
        key="battery_maintenance",
        translation_key="battery_maintenance",
        icon="mdi:battery-heart-variant",
        register_address=REG_BATTERY_TEST,
        register_value=BATTERY_TEST_MAINTENANCE,
        entity_registry_enabled_default=False,
    ),
    EastUPSButtonEntityDescription(
        key="stop_battery_test",
        translation_key="stop_battery_test",
        icon="mdi:battery-remove",
        register_address=REG_STOP_BATTERY_TEST,
        register_value=CMD_ACTIVATE,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up EAST UPS buttons from a config entry."""
    coordinator: EastEA900G4UPSCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        EastUPSButton(coordinator, description)
        for description in BUTTON_DESCRIPTIONS
    )


class EastUPSButton(CoordinatorEntity[EastEA900G4UPSCoordinator], ButtonEntity):
    """Representation of an EAST UPS button."""

    entity_description: EastUPSButtonEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: EastEA900G4UPSCoordinator,
        description: EastUPSButtonEntityDescription,
    ) -> None:
        """Initialize the button."""
        super().__init__(coordinator)
        self.entity_description = description
        uid = f"{coordinator.host}_{coordinator.slave_id}"
        self._attr_unique_id = f"{uid}_{description.key}"
        self._attr_device_info = coordinator.device_info

    async def async_press(self) -> None:
        """Write the command register."""
        ok = await self.coordinator.async_write_register(
            self.entity_description.register_address,
            self.entity_description.register_value,
        )
        if ok:
            _LOGGER.info("Sent command %s to UPS", self.entity_description.key)
            await self.coordinator.async_request_refresh()
        else:
            _LOGGER.error("Failed to send command %s", self.entity_description.key)
