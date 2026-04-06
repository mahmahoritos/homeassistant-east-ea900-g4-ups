"""Sensor platform for EAST EA900 G4 UPS."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import EastEA900G4UPSCoordinator
from .operating_mode import SYSTEM_OPERATING_MODE_OPTIONS


@dataclass(frozen=True, kw_only=True)
class EastUPSSensorEntityDescription(SensorEntityDescription):
    """Describes EAST UPS sensor entity."""

    value_key: str
    raw_value_key: str | None = None


SENSOR_DESCRIPTIONS: tuple[EastUPSSensorEntityDescription, ...] = (
    EastUPSSensorEntityDescription(
        key="bypass_voltage_a",
        translation_key="bypass_voltage_a",
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="bypass_voltage_a",
        entity_registry_enabled_default=False,
    ),
    EastUPSSensorEntityDescription(
        key="bypass_current_a",
        translation_key="bypass_current_a",
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="bypass_current_a",
        entity_registry_enabled_default=False,
    ),
    EastUPSSensorEntityDescription(
        key="bypass_frequency",
        translation_key="bypass_frequency",
        device_class=SensorDeviceClass.FREQUENCY,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="bypass_frequency",
        entity_registry_enabled_default=False,
    ),
    EastUPSSensorEntityDescription(
        key="bypass_power_factor",
        translation_key="bypass_power_factor",
        device_class=SensorDeviceClass.POWER_FACTOR,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="bypass_power_factor",
        entity_registry_enabled_default=False,
    ),
    EastUPSSensorEntityDescription(
        key="input_voltage_a",
        translation_key="input_voltage_a",
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="input_voltage_a",
    ),
    EastUPSSensorEntityDescription(
        key="input_voltage_b",
        translation_key="input_voltage_b",
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="input_voltage_b",
        entity_registry_enabled_default=False,
    ),
    EastUPSSensorEntityDescription(
        key="input_voltage_c",
        translation_key="input_voltage_c",
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="input_voltage_c",
        entity_registry_enabled_default=False,
    ),
    EastUPSSensorEntityDescription(
        key="input_current_a",
        translation_key="input_current_a",
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="input_current_a",
        entity_registry_enabled_default=False,
    ),
    EastUPSSensorEntityDescription(
        key="input_current_b",
        translation_key="input_current_b",
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="input_current_b",
        entity_registry_enabled_default=False,
    ),
    EastUPSSensorEntityDescription(
        key="input_current_c",
        translation_key="input_current_c",
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="input_current_c",
        entity_registry_enabled_default=False,
    ),
    EastUPSSensorEntityDescription(
        key="input_frequency",
        translation_key="input_frequency",
        device_class=SensorDeviceClass.FREQUENCY,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="input_frequency",
    ),
    EastUPSSensorEntityDescription(
        key="input_power_factor",
        translation_key="input_power_factor",
        device_class=SensorDeviceClass.POWER_FACTOR,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="input_power_factor",
        entity_registry_enabled_default=False,
    ),
    EastUPSSensorEntityDescription(
        key="output_voltage_a",
        translation_key="output_voltage_a",
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="output_voltage_a",
    ),
    EastUPSSensorEntityDescription(
        key="output_current_a",
        translation_key="output_current_a",
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="output_current_a",
    ),
    EastUPSSensorEntityDescription(
        key="output_frequency",
        translation_key="output_frequency",
        device_class=SensorDeviceClass.FREQUENCY,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="output_frequency",
    ),
    EastUPSSensorEntityDescription(
        key="output_power_factor",
        translation_key="output_power_factor",
        device_class=SensorDeviceClass.POWER_FACTOR,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="output_power_factor",
        entity_registry_enabled_default=False,
    ),
    EastUPSSensorEntityDescription(
        key="output_apparent_power",
        translation_key="output_apparent_power",
        device_class=SensorDeviceClass.APPARENT_POWER,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=0,
        value_key="output_apparent_power",
    ),
    EastUPSSensorEntityDescription(
        key="output_active_power",
        translation_key="output_active_power",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=0,
        value_key="output_active_power",
    ),
    EastUPSSensorEntityDescription(
        key="output_reactive_power",
        translation_key="output_reactive_power",
        device_class=SensorDeviceClass.REACTIVE_POWER,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=0,
        value_key="output_reactive_power",
        entity_registry_enabled_default=False,
    ),
    EastUPSSensorEntityDescription(
        key="output_load_percent",
        translation_key="output_load_percent",
        state_class=SensorStateClass.MEASUREMENT,
        value_key="output_load_percent",
        icon="mdi:gauge",
    ),
    EastUPSSensorEntityDescription(
        key="battery_voltage",
        translation_key="battery_voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="battery_voltage",
    ),
    EastUPSSensorEntityDescription(
        key="battery_current",
        translation_key="battery_current",
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="battery_current",
    ),
    EastUPSSensorEntityDescription(
        key="battery_temperature",
        translation_key="battery_temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="battery_temperature",
        entity_registry_enabled_default=False,
    ),
    EastUPSSensorEntityDescription(
        key="battery_runtime_remaining",
        translation_key="battery_runtime_remaining",
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="battery_runtime_remaining",
        icon="mdi:timer-outline",
    ),
    EastUPSSensorEntityDescription(
        key="battery_capacity",
        translation_key="battery_capacity",
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="battery_capacity",
    ),
    EastUPSSensorEntityDescription(
        key="inverter_current",
        translation_key="inverter_current",
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="inverter_current",
        entity_registry_enabled_default=False,
    ),
    EastUPSSensorEntityDescription(
        key="rectifier_temperature",
        translation_key="rectifier_temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="rectifier_temperature",
        entity_registry_enabled_default=False,
    ),
    EastUPSSensorEntityDescription(
        key="inverter_temperature",
        translation_key="inverter_temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="inverter_temperature",
    ),
    EastUPSSensorEntityDescription(
        key="status_word",
        translation_key="status_word",
        state_class=SensorStateClass.MEASUREMENT,
        value_key="status_word",
        entity_registry_enabled_default=False,
    ),
    EastUPSSensorEntityDescription(
        key="system_operating_mode",
        translation_key="system_operating_mode",
        device_class=SensorDeviceClass.ENUM,
        options=list(SYSTEM_OPERATING_MODE_OPTIONS),
        value_key="system_operating_mode_state",
        raw_value_key="system_operating_mode",
        icon="mdi:state-machine",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up EAST UPS sensors from a config entry."""
    coordinator: EastEA900G4UPSCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        EastUPSSensor(coordinator, description)
        for description in SENSOR_DESCRIPTIONS
    )


class EastUPSSensor(CoordinatorEntity[EastEA900G4UPSCoordinator], SensorEntity):
    """Representation of an EAST UPS sensor."""

    entity_description: EastUPSSensorEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: EastEA900G4UPSCoordinator,
        description: EastUPSSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        uid = f"{coordinator.host}_{coordinator.slave_id}"
        self._attr_unique_id = f"{uid}_{description.key}"
        self._attr_device_info = coordinator.device_info

    @property
    def native_value(self) -> Any:
        """Return the state of the sensor."""
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get(self.entity_description.value_key)

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Expose raw Modbus code for operating mode (and extended codes)."""
        rvk = self.entity_description.raw_value_key
        if not rvk or self.coordinator.data is None:
            return None
        raw = self.coordinator.data.get(rvk)
        if raw is None:
            return None
        return {"code": int(raw)}
