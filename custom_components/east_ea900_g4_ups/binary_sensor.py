"""Binary sensor platform for EAST EA900 G4 UPS (Modbus discrete inputs)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

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
from .discrete_bits import DISCRETE_BIT_SPECS

_DC: dict[str, BinarySensorDeviceClass] = {
    "problem": BinarySensorDeviceClass.PROBLEM,
    "heat": BinarySensorDeviceClass.HEAT,
    "battery": BinarySensorDeviceClass.BATTERY,
    "safety": BinarySensorDeviceClass.SAFETY,
    "running": BinarySensorDeviceClass.RUNNING,
    "connectivity": BinarySensorDeviceClass.CONNECTIVITY,
}


@dataclass(frozen=True, kw_only=True)
class EastUPSBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Describes EAST UPS binary sensor mapped to a discrete input bit."""

    bit_index: int


def _build_descriptions() -> tuple[EastUPSBinarySensorEntityDescription, ...]:
    """Create one entity description per discrete input bit (0–95)."""
    out: list[EastUPSBinarySensorEntityDescription] = []
    for bit, tkey, enabled_default, dc_hint in DISCRETE_BIT_SPECS:
        kwargs: dict[str, Any] = {
            "key": tkey,
            "translation_key": tkey,
            "bit_index": bit,
            "entity_registry_enabled_default": enabled_default,
        }
        if dc_hint is not None:
            kwargs["device_class"] = _DC[dc_hint]
        out.append(EastUPSBinarySensorEntityDescription(**kwargs))
    return tuple(out)


BINARY_SENSOR_DESCRIPTIONS: tuple[EastUPSBinarySensorEntityDescription, ...] = (
    _build_descriptions()
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
