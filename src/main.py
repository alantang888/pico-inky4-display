import time

from lib.network_manager import NetworkManager
import asyncio
import secrets

from datasource import *
from update_display import *

CO2 = 'co2'
RAIN = 'rain'
SLEEP_SEC = 600


HA_BASE_URL = 'http://homeassistant.lan:8123/'
HA_ENTITIES = {
    CO2: 'sensor.weather_station_co2',
    RAIN: 'sensor.weather_station_weather_station_weather_station_rain_gauge_rain'
}

def status_handler(mode, status, ip):
    print(mode, status, ip)
network_manager = NetworkManager('UK', status_handler=status_handler)
asyncio.get_event_loop().run_until_complete(network_manager.client(secrets.WIFI_SSID, secrets.WIFI_PASSWD))
print('Wifi connected')
time.sleep(5)
print('Start work!')

ha_api = HomeAssistantApi(HA_BASE_URL, secrets.HA_API_KEY, HA_ENTITIES)
if4 = InkyFrame4()


def get_data_and_update(source, display):
    co2_ppm = source.get_state(CO2)
    rain_mm = source.get_state(RAIN)
    
    print(f'Got CO2 is {co2_ppm}, rain is {rain_mm}')
    
    display.clear()
    display.update_co2(co2_ppm)
    # TODO: Should update multiple entities on display
    # display.update_rain(rain_mm)
    display.update()


while True:
    get_data_and_update(ha_api, if4)
    print(f'Done, sleep {SLEEP_SEC}s.')
    time.sleep(SLEEP_SEC)
