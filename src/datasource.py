import requests
import re

re_ha_time = re.compile(r'(\d+)-(\d+)-(\d+)T(\d+):(\d+):(\d+).*')

try:
    import inky_frame
    led_wifi_on = inky_frame.led_wifi.on
    led_wifi_off = inky_frame.led_wifi.off
    print('imported inky_frame.')
except:
    print('import inky_frame error. Use dummy function.')
    led_wifi_on = lambda: None
    led_wifi_off = lambda: None


def get_datetime_tuple(datetime_str):
    re_result = re_ha_time.search(datetime_str)
    return tuple(int(i) for i in re_result.groups()) + (0, 0)

class HomeAssistantApi():
    def __init__(self, url_base: str, api_key: str, entities: dict):
        self._url_base = url_base
        self._api_key = api_key
        self._entities = entities
        self._http_req_header = {'Authorization': f'Bearer {self._api_key}', 'Content-Type': 'application/json'}
        
    def get_state(self, entity: str) -> str:
        if entity not in self._entities:
            print(f'{entity} not inside entities. Return 0')
            return '0'
        led_wifi_on()
        req = requests.get(f'{self._url_base}api/states/{self._entities[entity]}', headers=self._http_req_header)
        led_wifi_off()
        if req.status_code < 300:
            return req.json()['state']
        else:
            print(f'Error getting {entity} state: {req.content}')
            return '0'
    
    def press_button(self, entity: str) -> bool:
        if entity not in self._entities:
            print(f'{entity} not inside entities. Return 0')
            return False
        led_wifi_on()
        data = {'entity_id': self._entities[entity]}
        req = requests.post(f'{self._url_base}api/services/input_button/press', json=data, headers=self._http_req_header)
        led_wifi_off()
        if req.status_code < 300:
            print(f'Pressed button {entity}')
            return True
        else:
            print(f'Error press button {entity} state: {req.content}')
            return False
        
    def get_timer_finish_time(self, entity: str):
        if entity not in self._entities:
            print(f'{entity} not inside entities. Return 0')
            return '0'
        led_wifi_on()
        req = requests.get(f'{self._url_base}api/states/{self._entities[entity]}', headers=self._http_req_header)
        led_wifi_off()
        if req.status_code < 300 and req.json()['state'] == 'active':
            finish_time = req.json()['attributes']['finishes_at']
            print(f'Got {entity} finish time: {finish_time}')
            return get_datetime_tuple(finish_time)
        else:
            print(f'Error getting {entity} state: {req.content}')
            return (0,) * 8
