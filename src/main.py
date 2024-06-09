import time
import asyncio
import machine

import inky_frame
from lib.network_manager import NetworkManager

import secrets
from datasource import *
from update_display import *

CO2 = 'co2'
RAIN = 'rain'
BTN_NIGHT_HEATER = 'btn_night_heater'
BTN_GUEST_WIFI = 'btn_guest_wifi'
TIMER_NIGHT_HEATER = 'timer_night_heater'
TIMER_GUEST_WIFI = 'timer_guest_wifi'
SLEEP_SEC = 540


HA_BASE_URL = 'http://homeassistant.lan:8123/'
HA_ENTITIES = {
    CO2: 'sensor.weather_station_co2',
    RAIN: 'sensor.weather_station_weather_station_weather_station_rain_gauge_rain',
    BTN_NIGHT_HEATER: 'input_button.night_heater',
    BTN_GUEST_WIFI: 'input_button.enable_guest_wifi',
    TIMER_NIGHT_HEATER: 'timer.night_heater_timer',
    TIMER_GUEST_WIFI: 'timer.guest_wifi_timer',
}

events = {}
next_normal_update = (0,) * 8

def status_handler(mode, status, ip):
    print(mode, status, ip)
network_manager = NetworkManager('UK', status_handler=status_handler)
asyncio.get_event_loop().run_until_complete(network_manager.client(secrets.WIFI_SSID, secrets.WIFI_PASSWD))
print('Wifi connected')
inky_frame.set_time()
print(f'Start work at {time.gmtime()}.')


def get_data_and_update(source, display):
    global next_normal_update
    
    co2_ppm = source.get_state(CO2)
    rain_mm = source.get_state(RAIN)
    
    print(f'Got CO2 is {co2_ppm}, rain is {rain_mm}')
    
    display.clear()
    display.update_co2(co2_ppm)
    # TODO: Should update multiple entities on display
    # display.update_rain(rain_mm)
    display.print_bottom_text()
    display.update()
    
    next_normal_update = time.gmtime(time.time() + SLEEP_SEC)
    
    
def get_datetime_tuple(datetime_str):
    re_result = re_ha_time.search(datetime_str)
    return tuple(int(i) for i in re_result.groups()) + (0, 0)
    
    
def sleep():
    if len(events) > 0:
        next_event_time = sorted(events.items())[0]
        if next_event_time < next_normal_update:
            time.sleep(time.mktime(next_event_time))
            return
        
    time.sleep(time.mktime(next_normal_update))
    
    
def check_not_update_too_long(t):
    # If didn't update for 5 mins. That should have issue
    print(f'timer happened at {time.gmtime()}, t: {t}')
    if time.gmtime(time.time()-300) > next_normal_update:
        machine.reset()
        
    
    
# For USB powered use. So only time.sleep, not using RTC. If battery, should use deep sleep. But need also change Wifi logic?
def main():
    global next_normal_update
    
    ha = HomeAssistantApi(HA_BASE_URL, secrets.HA_API_KEY, HA_ENTITIES)
    display = InkyFrame4()
    
    health_checker_timer = machine.Timer()
    health_checker_timer.init(period=600000, mode=machine.Timer.PERIODIC, callback=check_not_update_too_long)
    
    print('Start main loop.')

    while True:
        # TODO: Not tested yet
        if inky_frame.button_a.read():
            print('Button A pressed.')
            inky_frame.button_a.led_on()
            display.clear()
            if ha.press_button(BTN_NIGHT_HEATER):
                finish_time = ha.get_timer_finish_time(TIMER_NIGHT_HEATER)
                if finish_time[0] == 0:
                    print('Get night heater timer error.')
                else:
                    events[finish_time] = inky_frame.button_a.led_off
                display.print_night_heater()
            else:
                print('Enable night heater error.')
                inky_frame.button_a.led_off()
                display.print_night_heater_got_error()
            display.print_bottom_text()
            display.update()
        elif inky_frame.button_b.read():
            print('Button B pressed.')
            inky_frame.button_b.led_on()
            if ha.press_button(BTN_GUEST_WIFI):
                finish_time = ha.get_timer_finish_time(TIMER_GUEST_WIFI)
                if finish_time[0] == 0:
                    print('Get guest wifi timer error.')
                else:
                    events[finish_time] = inky_frame.button_b.led_off
                    display.clear()
                    display.print_guest_wifi_info(secrets.GUEST_WIFI_SSID, secrets.GUEST_WIFI_PASSWD, finish_time)
                    display.print_bottom_text()
                    display.update()
                    # Push next normal update to 5 mins later (if it will happen in next 5 mins)
                    if time.mktime(next_normal_update) < time.time()+300:
                        next_normal_update = time.gmtime(time.time()+300)
            else:
                print('Enable guest wifi error.')
                inky_frame.button_b.led_off()
        elif inky_frame.button_c.read():
            print('Button C pressed.')
            inky_frame.button_c.led_on()
            events[time.gmtime(time.time()+10)] = inky_frame.button_c.led_off
        elif inky_frame.button_d.read():
            print('Button D pressed.')
            inky_frame.button_d.led_on()
            events[time.gmtime(time.time()+10)] = inky_frame.button_d.led_off
        elif inky_frame.button_e.read():
            print('Button E pressed.')
            inky_frame.button_e.led_on()
            events[time.gmtime(time.time()+10)] = inky_frame.button_e.led_off
        else:
            if len(events) > 0:
                next_event_time = sorted(events.keys())[0]
                if next_event_time < next_normal_update:
                    if time.gmtime() > next_event_time:
                        print('Got time event')
                        e = events.pop(next_event_time)
                        e()
            if time.gmtime() > next_normal_update:
                print('Reach normal update time')
                get_data_and_update(ha, display)


if __name__ == '__main__':
    main()
