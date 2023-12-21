import requests

try:
    import inky_frame
    led_wifi_on = inky_frame.led_wifi.on
    led_wifi_off = inky_frame.led_wifi.off
    print('imported inky_frame.')
except:
    print('import inky_frame error. Use dummy function.')
    led_wifi_on = lambda: None
    led_wifi_off = lambda: None

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
        # TODO: Error check
        return req.json()['state']
        
