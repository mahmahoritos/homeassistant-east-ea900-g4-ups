"""Binary sensor platform for EAST EA900 G4 UPS (Modbus discrete inputs)."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import EastEA900G4UPSCoordinator


@dataclass(frozen=True, kw_only=True)
class EastUPSBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Describes EAST UPS binary sensor mapped to a discrete input bit."""

    bit_index: int


# Bit indices per EA900 G4 Modbus protocol (remote signalling table, FC 0x02).
BINARY_SENSOR_DESCRIPTIONS: tuple[EastUPSBinarySensorEntityDescription, ...] = (
    EastUPSBinarySensorEntityDescription(
        key="bus_high_voltage",
        translation_key="bus_high_voltage",
        device_class=BinarySensorDeviceClass.PROBLEM,
        bit_index=0,
        entity_registry_enabled_default=False,
    ),
    EastUPSBinarySensorEntityDescription(
        key="overtemperature",
        translation_key="overtemperature",
        device_class=BinarySensorDeviceClass.HEAT,
        bit_index=8,
    ),
    EastUPSBinarySensorEntityDescription(
        key="output_short_circuit",
        translation_key="output_short_circuit",
        device_class=BinarySensorDeviceClass.PROBLEM,
        bit_index=9,
    ),
    EastUPSBinarySensorEntityDescription(
        key="overload_fault",
        translation_key="overload_fault",
        device_class=BinarySensorDeviceClass.PROBLEM,
        bit_index=10,
        icon="mdi:flash-alert",
    ),
    EastUPSBinarySensorEntityDescription(
        key="fan_failed",
        translation_key="fan_failed",
        device_class=BinarySensorDeviceClass.PROBLEM,
        bit_index=29,
        icon="mdi:fan-alert",
    ),
    EastUPSBinarySensorEntityDescription(
        key="epo",
        translation_key="epo",
        device_class=BinarySensorDeviceClass.SAFETY,
        bit_index=30,
        icon="mdi:stop-circle",
    ),
    EastUPSBinarySensorEntityDescription(
        key="battery_disconnected",
        translation_key="battery_disconnected",
        device_class=BinarySensorDeviceClass.PROBLEM,
        bit_index=52,
        icon="mdi:battery-off",
    ),
    EastUPSBinarySensorEntityDescription(
        key="input_overcurrent",
        translation_key="input_overcurrent",
        device_class=BinarySensorDeviceClass.PROBLEM,
        bit_index=53,
        entity_registry_enabled_default=False,
    ),
    EastUPSBinarySensorEntityDescription(
        key="high_battery_voltage",
        translation_key="high_battery_voltage",
        device_class=BinarySensorDeviceClass.PROBLEM,
        bit_index=54,
        entity_registry_enabled_default=False,
    ),
    EastUPSBinarySensorEntityDescription(
        key="charger_failure",
        translation_key="charger_failure",
        device_class=BinarySensorDeviceClass.PROBLEM,
        bit_index=56,
        icon="mdi:battery-charging-wireless-alert",
    ),
    EastUPSBinarySensorEntityDescription(
        key="low_battery_voltage_fault",
        translation_key="low_battery_voltage_fault",
        device_class=BinarySensorDeviceClass.BATTERY,
        bit_index=59,
    ),
    EastUPSBinarySensorEntityDescription(
        key="bypass_fault",
        translation_key="bypass_fault",
        device_class=BinarySensorDeviceClass.PROBLEM,
        bit_index=65,
        icon="mdi:swap-horizontal",
    ),
    EastUPSBinarySensorEntityDescription(
        key="mains_high_voltage",
        translation_key="mains_high_voltage",
        device_class=BinarySensorDeviceClass.PROBLEM,
        bit_index=66,
        entity_registry_enabled_default=False,
    ),
    EastUPSBinarySensorEntityDescription(
        key="mains_frequency_abnormal",
        translation_key="mains_frequency_abnormal",
        device_class=BinarySensorDeviceClass.PROBLEM,
        bit_index=67,
        entity_registry_enabled_default=False,
    ),
    EastUPSBinarySensorEntityDescription(
        key="battery_end_of_discharge",
        translation_key="battery_end_of_discharge",
        device_class=BinarySensorDeviceClass.BATTERY,
        bit_index=70,
        icon="mdi:battery-alert",
    ),
    EastUPSBinarySensorEntityDescription(
        key="battery_test_success",
        translation_key="battery_test_success",
        bit_index=71,
        icon="mdi:check-circle",
        entity_registry_enabled_default=False,
    ),
    EastUPSBinarySensorEntityDescription(
        key="battery_test_failed",
        translation_key="battery_test_failed",
        device_class=BinarySensorDeviceClass.PROBLEM,
        bit_index=73,
        icon="mdi:close-circle",
    ),
    EastUPSBinarySensorEntityDescription(
        key="mains_abnormality",
        translation_key="mains_abnormality",
        device_class=BinarySensorDeviceClass.PROBLEM,
        bit_index=82,
        icon="mdi:transmission-tower-off",
    ),
    EastUPSBinarySensorEntityDescription(
        key="bypass_abnormality",
        translation_key="bypass_abnormality",
        device_class=BinarySensorDeviceClass.PROBLEM,
        bit_index=83,
        entity_registry_enabled_default=False,
    ),
    EastUPSBinarySensorEntityDescription(
        key="overload_alarm",
        translation_key="overload_alarm",
        device_class=BinarySensorDeviceClass.PROBLEM,
        bit_index=51,
        icon="mdi:flash-alert-outline",
    ),
    EastUPSBinarySensorEntityDescription(
        key="inverter_abnormality",
        translation_key="inverter_abnormality",
        device_class=BinarySensorDeviceClass.PROBLEM,
        bit_index=24,
        entity_registry_enabled_default=False,
    ),
    EastUPSBinarySensorEntityDescription(
        key="maintain_bypass_enabled",
        translation_key="maintain_bypass_enabled",
        device_class=BinarySensorDeviceClass.RUNNING,
        bit_index=89,
        entity_registry_enabled_default=False,
    ),
    EastUPSBinarySensorEntityDescription(
        key="test_mode",
        translation_key="test_mode",
        device_class=BinarySensorDeviceClass.RUNNING,
        bit_index=94,
        icon="mdi:test-tube",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up EAST UPS binary sensors from a config entry."""
    coordinator: EastEA900G4UPSCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        EastUPSBinarySensor(coordinator, description)
        for description in BINARY_SENSOR_DESCRIPTIONS
    )


class EastUPSBinarySensor(
    CoordinatorEntity[EastEA900G4UPSCoordinator], BinarySensorEntity
):
    """Representation of an EAST UPS binary sensor."""

    entity_description: EastUPSBinarySensorEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: EastEA900G4UPSCoordinator,
        description: EastUPSBinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        uid = f"{coordinator.host}_{coordinator.slave_id}"
        self._attr_unique_id = f"{uid}_{description.key}"
        self._attr_device_info = coordinator.device_info

    @property
    def is_on(self) -> bool | None:
        """Return true if the condition is active (per protocol: 1 = occur)."""
        if self.coordinator.data is None:
            return None
        bits: list[bool] | None = self.coordinator.data.get("discrete_inputs")
        if bits is None:
            return None
        idx = self.entity_description.bit_index
        if idx < 0 or idx >= len(bits):
            return None
        return bits[idx]
