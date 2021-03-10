# Wallbox Portal Component for Home Assistant
Home Assistant component for accessing the Wallbox Portal API.

This component consists of a sensor component, a switch to pause charging, a lock to lock the charger and a number component to set the max current.

NEW VERSION: now using the Home Assistant Integration config flow. Just add it as an integration (MyWallbox) and fill in wallbox serial, username and password. Pausing is now changed in that it is only available when charging / connected.

<del>TODO: 
<del>1. Look into creating multiple sensor entities (instead of one containing all the data)
<del>2. Look into combining the different platforms into 1 configuration entry.

<del>Installation of this component is done by copying the sensor.py, switch.py, number.py, lock.py, __init__.py and manifest.json files to <del>[homeassistant_config]/custom_components/wallbox folder.

