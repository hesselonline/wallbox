"""Wallbox API Component."""
# import homeassistant.helpers.config_validation as cv
# import voluptuous as vol
# from homeassistant.components.number import PLATFORM_SCHEMA
# from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, CONF_NAME
#
# CONF_STATION_ID = 'station_id'
#
# DEFAULTNAME = "Wallbox"
#
DOMAIN = 'wallbox'
#
# PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
#     vol.Optional(CONF_NAME, default=DEFAULTNAME): cv.string,
#     vol.Required(CONF_USERNAME): cv.string,
#     vol.Required(CONF_PASSWORD): cv.string,
#     vol.Required(CONF_STATION_ID): cv.string
# })
#
# def setup(hass, config):
#     """Your controller/hub specific code."""
#     # Data that you want to share with your platforms
#
#     hass.data[DOMAIN] = {
#         'name': config[CONF_NAME],
#         'station' : config[CONF_STATION_ID],
#         'user' : config[CONF_USERNAME],
#         'password' : config[CONF_PASSWORD]
#     }
#
#     hass.helpers.discovery.load_platform('sensor', DOMAIN, {}, config)
#     hass.helpers.discovery.load_platform('switch', DOMAIN, {}, config)
#     hass.helpers.discovery.load_platform('number', DOMAIN, {}, config)
#
#     return True