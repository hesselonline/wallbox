""""Home Assistant component for accessing the Wallbox Portal API, the switch component allows pausing/resuming and lock/unlock.
    """

import logging

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.switch import PLATFORM_SCHEMA
from homeassistant.components.switch import SwitchEntity
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
    add_devices([WallboxPause(f"{config[CONF_NAME]} Pause", config)],
                True)


class WallboxPause(SwitchEntity):
    """Representation of the Wallbox Pause Switch."""

    def __init__(self, name, config):
        self._is_on = False
        self._name = name
        self._config = config

    def get_charging_status(self):
        """Get the latest data from the wallbox API and updates the state."""
        _LOGGER.debug("update called.")

        try:
            station = self._config[CONF_STATION_ID]
            user = self._config[CONF_USERNAME]
            password = self._config[CONF_PASSWORD]

            w = Wallbox(user, password)
            w.authenticate()
            data = w.getChargerStatus(station)
            charger_status = data['status_description']
            charger_paused = charger_status.lower() == "connected"
            return charger_paused

        except Exception as exception:
            _LOGGER.error(
                "Unable to fetch data from Wallbox. %s", exception)

    def pause_charger(self, pause):
        """Pause / Resume Charger using API"""

        try:
            station = self._config[CONF_STATION_ID]
            user = self._config[CONF_USERNAME]
            password = self._config[CONF_PASSWORD]

            w = Wallbox(user, password)
            w.authenticate()

            if pause is False:
                """"unlock charger"""
                _LOGGER.debug(
                    "Unlocking Wallbox")
                w.resumeChargingSession(station)

            elif pause is True:
                """"lock charger"""
                _LOGGER.debug(
                    "Locking Wallbox")
                w.pauseChargingSession(station)

        except Exception as exception:
            _LOGGER.error(
                "Unable to pause/resume Wallbox. %s", exception)

    @property
    def name(self):
        """Return the name of the switch."""
        return self._name

    @property
    def icon(self):
        if self._is_on:
            return 'mdi:motion-play-outline'
        else:
            return 'mdi:motion-pause-outline'

    @property
    def is_on(self):
        return self._is_on

    def turn_on(self, **kwargs):
        self.pause_charger(True)
        self._is_on = True

    def turn_off(self, **kwargs):
        self.pause_charger(False)
        self._is_on = False

    def update(self):
        if self.get_charging_status():
            self._is_on = True
        else:
            self._is_on = False
