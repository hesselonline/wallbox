""""Home Assistant component for accessing the Wallbox Portal API.
    """

import logging

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from datetime import timedelta
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, CONF_NAME, POWER_WATT, ENERGY_KILO_WATT_HOUR, ELECTRICAL_CURRENT_AMPERE, LENGTH_KILOMETERS, PERCENTAGE
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.helpers.entity import Entity
from wallbox import Wallbox

from . import DOMAIN

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

SENSOR_TYPES = {
'charging_power': {
    'ATTR_ICON': 'mdi:ev-station',
    'ATTR_LABEL': 'Charging Power',
    'ATTR_UNIT': POWER_WATT,
    'ATTR_ENABLED': True
},
'max_available_power': {
    'ATTR_ICON': 'mdi:ev-station',
    'ATTR_LABEL': 'Max Available Power',
    'ATTR_UNIT': ELECTRICAL_CURRENT_AMPERE,
    'ATTR_ENABLED': True
},
'charging_speed': {
    'ATTR_ICON': 'mdi:speedometer',
    'ATTR_LABEL': 'Charging Speed',
    'ATTR_UNIT': None,
    'ATTR_ENABLED': True
},
'added_range': {
    'ATTR_ICON': 'mdi:map-marker-distance',
    'ATTR_LABEL': 'Added Range',
    'ATTR_UNIT': LENGTH_KILOMETERS,
    'ATTR_ENABLED': True
},
'added_energy': {
    'ATTR_ICON': 'mdi:battery-positive',
    'ATTR_LABEL': 'Added Energy',
    'ATTR_UNIT': ENERGY_KILO_WATT_HOUR,
    'ATTR_ENABLED': True
},
'charging_time': {
    'ATTR_ICON': 'mdi:timer',
    'ATTR_LABEL': 'Charging Time',
    'ATTR_UNIT': None,
    'ATTR_ENABLED': True
},
'cost': {
    'ATTR_ICON': 'mdi:ev-station',
    'ATTR_LABEL': 'Cost',
    'ATTR_UNIT': None,
    'ATTR_ENABLED': True
},
'state_of_charge': {
    'ATTR_ICON': 'mdi:battery-charging-80',
    'ATTR_LABEL': 'State of Charge',
    'ATTR_UNIT': PERCENTAGE,
    'ATTR_ENABLED': True
},
'current_mode': {
    'ATTR_ICON': 'mdi:ev-station',
    'ATTR_LABEL': 'Current Mode',
    'ATTR_UNIT': None,
    'ATTR_ENABLED': True
},
'depot_price': {
    'ATTR_ICON': 'mdi:ev-station',
    'ATTR_LABEL': 'Depot Price',
    'ATTR_UNIT': None,
    'ATTR_ENABLED': True
},
'status_description': {
    'ATTR_ICON': 'mdi:ev-station',
    'ATTR_LABEL': 'Status Description',
    'ATTR_UNIT': None,
    'ATTR_ENABLED': True
}}

def wallbox_updater(user, password, station):

    w = Wallbox(user, password)
    w.authenticate()

    data = w.getChargerStatus(station)

    return dict((k, data[k]) for k in SENSOR_TYPES if k in data)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):


    station = config.get(CONF_STATION_ID)
    user = config.get(CONF_USERNAME)
    password = config.get(CONF_PASSWORD)

    async def async_update_data():

        try:
            return await hass.async_add_executor_job(wallbox_updater,user,password,station)
           
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
        WallboxSensor(coordinator, idx, ent) for idx, ent in enumerate(coordinator.data))
    


class WallboxSensor(CoordinatorEntity,Entity):
    """Representation of the Wallbox portal."""

    def __init__(self, coordinator, idx, ent):
        """Initialize a Wallbox sensor."""
        super().__init__(coordinator)
        self._properties = SENSOR_TYPES[ent]
        self._name = f"Wallbox {self._properties['ATTR_LABEL']}"
        self._icon = self._properties['ATTR_ICON']
        self._unit = self._properties['ATTR_UNIT']
        self._value = self.coordinator.data[ent]

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        return self._value

    @property
    def unit_of_measurement(self):
        return self._unit

    @property
    def icon(self):
        return self._icon
