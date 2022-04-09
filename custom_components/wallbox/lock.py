"""Home Assistant component for accessing the Wallbox Portal API. The lock component creates a lock entity."""
from __future__ import annotations

from typing import Any

from homeassistant.components.lock import LockEntity, LockEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import InvalidAuth, WallboxCoordinator, WallboxEntity
from .const import (
    CONF_DATA_KEY,
    CONF_LOCKED_UNLOCKED_KEY,
    CONF_SERIAL_NUMBER_KEY,
    DOMAIN,
)

LOCK_TYPES: dict[str, LockEntityDescription] = {
    CONF_LOCKED_UNLOCKED_KEY: LockEntityDescription(
        key=CONF_LOCKED_UNLOCKED_KEY,
        name="Locked/Unlocked",
    ),
}


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Create wallbox lock entities in HASS."""
    coordinator: WallboxCoordinator = hass.data[DOMAIN][entry.entry_id]
    # Check if the user is authorized to lock, if so, add lock component
    try:
        await coordinator.async_set_lock_unlock(
            coordinator.data[CONF_LOCKED_UNLOCKED_KEY]
        )
    except InvalidAuth:
        return

    async_add_entities(
        [
            WallboxLock(coordinator, entry, description)
            for ent in coordinator.data
            if (description := LOCK_TYPES.get(ent))
        ]
    )


class WallboxLock(WallboxEntity, LockEntity):
    """Representation of a wallbox lock."""

    def __init__(
        self,
        coordinator: WallboxCoordinator,
        entry: ConfigEntry,
        description: LockEntityDescription,
    ) -> None:
        """Initialize a Wallbox lock."""

        super().__init__(coordinator)
        self.entity_description = description
        self._attr_name = f"{entry.title} {description.name}"
        self._attr_unique_id = f"{description.key}-{coordinator.data[CONF_DATA_KEY][CONF_SERIAL_NUMBER_KEY]}"

    @property
    def is_locked(self) -> bool:
        """Return the status of the lock."""
        return self.coordinator.data[CONF_LOCKED_UNLOCKED_KEY]  # type: ignore[no-any-return]

    async def async_lock(self, **kwargs: Any) -> None:
        """Lock charger."""
        await self.coordinator.async_set_lock_unlock(True)

    async def async_unlock(self, **kwargs: Any) -> None:
        """Unlock charger."""
        await self.coordinator.async_set_lock_unlock(False)
