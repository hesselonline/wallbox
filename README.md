# Wallbox Portal Component for Home Assistant
Home Assistant component for accessing the Wallbox Portal API.

This component consists of a sensor component, a switch to pause charging, a lock to lock the charger and a number component to set the max current.

TODO: 
1. Look into creating multiple sensor entities (instead of one containing all the data)
2. Look into combining the different platforms into 1 configuration entry.

Installation of this component is done by copying the sensor.py, switch.py, number.py, lock.py, __init__.py and manifest.json files to [homeassistant_config]/custom_components/wallbox folder.

In configuration.yaml add the sensor as follows:
```
  sensor:
    - platform: wallbox 
      username: youremailaddresshere
      password: secretpasswordfromwallboxportal
      station_id: stationidhere
      name: (optional, name for sensor)
  
  switch:
    - platform: wallbox 
      username: youremailaddresshere
      password: secretpasswordfromwallboxportal
      station_id: stationidhere
      name: (optional, name for switch)

  number:
    - platform: wallbox 
      username: youremailaddresshere
      password: secretpasswordfromwallboxportal
      station_id: stationidhere
      name: (optional, name for number)
  
  lock:
    - platform: wallbox 
      username: youremailaddresshere
      password: secretpasswordfromwallboxportal
      station_id: stationidhere
      name: (optional, name for lock)
 ```
