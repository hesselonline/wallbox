""""Home Assistant component for accessing the Wallbox Portal API, the switch component allows pausing/resuming and lock/unlock.
    """

import logging

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.number import NumberEntity
from homeassistant.components.number import PLATFORM_SCHEMA
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, CONF_NAME
from wallbox import Wallbox

from . import DOMAIN

CONF_STATION_ID = 'station_id'

DEFAULTNAME = "Wallbox"

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULTNAME): cv.string,
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
    vol.Required(CONF_STATION_ID): cv.string
})

_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the Wallbox portal switch platform."""
    # Add devices
    add_devices([WallboxMaxChargingCurrent(f"{config[CONF_NAME]} Max. Charging Current", config)],
                True)


class WallboxMaxChargingCurrent(NumberEntity):
    """Representation of the Wallbox Pause Switch."""

    def __init__(self, name, config):
        self._is_on = False
        self._name = name
        self._config = config
        self._value = 0
        self._uniqueid = f"{name}max_charging_current"

    def get_max_charging_current(self):
        """Get the latest data from the wallbox API and updates the state."""
        _LOGGER.debug("update called.")

        try:
            station = self._config[CONF_STATION_ID]
            user = self._config[CONF_USERNAME]
            password = self._config[CONF_PASSWORD]

            w = Wallbox(user, password)
            w.authenticate()
            data = w.getChargerStatus(station)
            max_charger_current = data['config_data']['max_charging_current']
            return max_charger_current

        except Exception as exception:
            _LOGGER.error(
                "Unable to fetch data from Wallbox. %s", exception)

    def set_max_charging_current(self, max_charging_current):
        """Pause / Resume Charger using API"""

        try:
            station = self._config[CONF_STATION_ID]
            user = self._config[CONF_USERNAME]
            password = self._config[CONF_PASSWORD]

            w = Wallbox(user, password)
            w.authenticate()

            """"unlock charger"""
            _LOGGER.debug(
                "Unlocking Wallbox")
            w.setMaxChargingCurrent(station,max_charging_current)

        except Exception as exception:
            _LOGGER.error(
                "Unable to pause/resume Wallbox. %s", exception)

    @property
    def name(self):
        """Return the name of the switch."""
        return self._name

    @property
    def icon(self):
        return 'mdi:ev-station'

    @property
    def value(self):
        return self._value

    def set_value(self,  value: float):
        self.set_max_charging_current(value)
        self._value = value

    def update(self):
        self._value = self.get_max_charging_current()

