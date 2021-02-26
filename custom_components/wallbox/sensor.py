""""Home Assistant component for accessing the Wallbox Portal API.
    """

import json
import logging
import time
from datetime import datetime, timedelta
import requests
import logging
import voluptuous as vol
from wallbox import Wallbox
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, CONF_NAME, POWER_WATT
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity

DOMAIN = "wallbox"

CONF_STATION_ID = 'station_id'

DEFAULTNAME = "Wallbox Portal"

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULTNAME): cv.string,
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
    vol.Required(CONF_STATION_ID): cv.string
})

_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the Wallbox portal scraper platform."""
    # Add devices
    add_devices([WallboxSensor(config[CONF_NAME], config)], True)


class WallboxSensor(Entity):
    """Representation of the Wallbox portal."""

    def __init__(self, name, config):
        """Initialize a Wallbox sensor."""
        # self.rest = rest
        self._name = name
        self._config = config
        self._attributes = {}

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def unit_of_measurement(self):
        "Return the unit of measurement of the sensor"
        return POWER_WATT

    @property
    def state(self):
        return self._attributes['charging_power']

    @property
    def icon(self):
        return 'mdi:ev-station'

    @property
    def device_state_attributes(self):
        """Return the state attributes of the monitored installation."""
        return self._attributes

    def update(self):
        """Get the latest data from the SEMS API and updates the state."""
        _LOGGER.debug("update called.")

        try:
            station = self._config[CONF_STATION_ID]
            user = self._config[CONF_USERNAME]
            password = self._config[CONF_PASSWORD]

            w = Wallbox(user, password)
            w.authenticate()
            data = w.getChargerStatus(station)
            key_list = ['user_id', 'user_name', 'car_id', 'car_plate', 'last_sync', 'depot_price', 'status_description',
                        'charging_power',
                        'max_available_power', 'charging_speed', 'added_range', 'added_energy', 'charging_time', 'cost',
                        'current_mode', 'state_of_charge']
            filtered_status = dict((k, data[k]) for k in key_list if k in data)

            for key, value in filtered_status.items():
                self._attributes[key] = value
                _LOGGER.debug("Updated attribute %s: %s", key, value)
        except Exception as exception:
            _LOGGER.error(
                "Unable to fetch data from Wallbox. %s", exception)
