# Wallbox Portal Component for Home Assistant
Home Assistant component for accessing the Wallbox Portal API.

Installation of this component is done by copying the sensor.py, __init__.py and manifest.json files to [homeassistant_config]/custom_components/wallbox folder.

In configuration.yaml add the sensor as follows:

    - platform: wallbox 
      username: youremailaddresshere
      password: secretpasswordfromsemsportal
      station_id: stationidhere
      name: (optional, name for sensor)
<br>

