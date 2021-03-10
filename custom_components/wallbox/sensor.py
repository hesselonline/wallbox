""""Home Assistant component for accessing the Wallbox Portal API.
    """

import logging

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from datetime import timedelta
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, CONF_NAME
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.helpers.entity import Entity
from wallbox import Wallbox

from .const import DOMAIN, SENSOR_TYPES, CONF_CONNECTIONS

CONF_STATION = "station"

DEFAULTNAME = "Wallbox Portal"

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_NAME, default=DEFAULTNAME): cv.string,
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Required(CONF_STATION): cv.string,
    }
)

_LOGGER = logging.getLogger(__name__)


def wallbox_updater(wallbox, station):

    w = wallbox
    data = w.getChargerStatus(station)

    return dict((k, data[k]) for k in SENSOR_TYPES if k in data)


async def async_setup_entry(hass, config, async_add_entities):

    wallbox = hass.data[DOMAIN][CONF_CONNECTIONS][config.entry_id]

    station = config.data[CONF_STATION]

    async def async_update_data():

        try:
            return await hass.async_add_executor_job(wallbox_updater, wallbox, station)

        except:
            _LOGGER.error("Error getting data from wallbox API")
            return

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        # Name of the data. For logging purposes.
        name="wallbox",
        update_method=async_update_data,
        # Polling interval. Will only be polled if there are subscribers.
        update_interval=timedelta(seconds=30),
    )

    await coordinator.async_refresh()

    async_add_entities(
        WallboxSensor(coordinator, idx, ent) for idx, ent in enumerate(coordinator.data)
    )


class WallboxSensor(CoordinatorEntity, Entity):
    """Representation of the Wallbox portal."""

    def __init__(self, coordinator, idx, ent):
        """Initialize a Wallbox sensor."""
        super().__init__(coordinator)
        self._properties = SENSOR_TYPES[ent]
        self._name = f"Wallbox {self._properties['ATTR_LABEL']}"
        self._icon = self._properties["ATTR_ICON"]
        self._unit = self._properties["ATTR_UNIT"]
        self._ent = ent

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        return self.coordinator.data[self._ent]

    @property
    def unit_of_measurement(self):
        return self._unit

    @property
    def icon(self):
        return self._icon
