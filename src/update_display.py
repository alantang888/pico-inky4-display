from picographics import PicoGraphics, DISPLAY_INKY_FRAME_4, DISPLAY_PICO_EXPLORER
import qrcode

try:
    import inky_frame
    led_busy_on = inky_frame.led_busy.on
    led_busy_off = inky_frame.led_busy.off
    print('imported inky_frame.')
except:
    print('import inky_frame error. Use dummy function.')
    led_busy_on = lambda: None
    led_busy_off = lambda: None

# QR code related copy from pimoroni library
qr = qrcode.QRCode()


def measure_qr_code(size, code):
    w, h = code.get_size()
    module_size = int(size / w)
    return module_size * w, module_size


def draw_qr_code(graphics, ox, oy, size, code):
    size, module_size = measure_qr_code(size, code)
    graphics.set_pen(1)
    graphics.rectangle(ox, oy, size, size)
    graphics.set_pen(0)
    for x in range(size):
        for y in range(size):
            if code.get_module(x, y):
                graphics.rectangle(ox + x * module_size, oy + y * module_size, module_size, module_size)


class InkyFrame4():
    def __init__(self):
        self._display = PicoGraphics(display=DISPLAY_INKY_FRAME_4)
        self._last_co2_ppm = 0
        self._x, self._y = self._display.get_bounds()
        self._bottom_text_start_y = self._y-25
        self._co2_right_arrow_polygon = [
            (475, 75),
            (575, 75),
            (575, 25),
            (625, 100),
            (575, 175),
            (575, 125),
            (475, 125),
        ]
        self._co2_up_arrow_polygon = [
            (525, 175),
            (525, 75),
            (475, 75),
            (550, 25),
            (625, 75),
            (575, 75),
            (575, 175),
        ]
        self._co2_down_arrow_polygon = [
            (525, 25),
            (525, 125),
            (475, 125),
            (550, 175),
            (625, 125),
            (575, 125),
            (575, 25),
        ]
        
    def update_co2(self, co2_ppm):
        _co2_ppm = int(co2_ppm)
        if _co2_ppm < 2000:
            blackground = inky_frame.GREEN
            text = inky_frame.WHITE
        elif _co2_ppm < 3000:
            blackground = inky_frame.YELLOW
            text = inky_frame.BLUE
        else:
            blackground = inky_frame.RED
            text = inky_frame.YELLOW
        
        self._display.set_pen(blackground)
        self._display.rectangle(0, 0, 460, 200)
        self._display.set_pen(text)
        self._display.set_font('bitmap8')
        self._display.text('CO2', 20, 20, scale=4)
        self._display.text('ppm', 390, 140, scale=4)
        self._display.set_font('serif')
        self._display.set_thickness(3)
        self._display.text(co2_ppm, 75, 100, scale=4)
        
        if self._last_co2_ppm != 0:
            change_rator = abs(_co2_ppm - self._last_co2_ppm) / self._last_co2_ppm
            if _co2_ppm - self._last_co2_ppm < 0:
                arrow_colour = inky_frame.GREEN
                arrow = self._co2_down_arrow_polygon
            elif change_rator <= 0.02:
                arrow_colour = inky_frame.YELLOW
                arrow = self._co2_right_arrow_polygon
            else:
                arrow_colour = inky_frame.RED
                arrow = self._co2_up_arrow_polygon
            self._display.set_pen(arrow_colour)
            self._display.polygon(arrow)
            
        self._last_co2_ppm = _co2_ppm
    
    def update_rain(self, rain_mm):
        # TODO: Need implement
        pass
    
    # TODO: Not tested yet
    def print_night_heater(self):
        self._display.set_pen(inky_frame.GREEN)
        self._display.set_font('cursive')
        self._display.set_thickness(5)
        self._display.text('Night Heater is On!', 20, 30, scale=2)
    
    # TODO: Not tested yet
    def print_night_heater_got_error(self):
        self._display.set_pen(inky_frame.RED)
        self._display.set_font('cursive')
        self._display.set_thickness(2)
        self._display.text('Trigger "Night Heater" got error!', 20, 20, scale=1)
    
    def print_guest_wifi_info(self, guest_ssid, guest_password, disable_time):
        self._display.set_pen(inky_frame.BLACK)
        self._display.set_font('bitmap8')
        self._display.text(f'Will disabled at {disable_time[0]}-{disable_time[1]}-{disable_time[2]} {disable_time[3]}:{disable_time[4]} (UTC)', 20, self._bottom_text_start_y-105)
        self._display.line(0, self._bottom_text_start_y-85, self._x, self._bottom_text_start_y-85)
        self._display.set_font('serif_italic')
        self._display.set_thickness(2)
        self._display.text(f'SSID: {guest_ssid}', 20, self._bottom_text_start_y-64, scale=1)
        self._display.text(f'Password: {guest_password}', 20, self._bottom_text_start_y-24, scale=1)
        guest_wifi_qr_str = f'WIFI:S:{guest_ssid};T:WPA;P:{guest_password};;'
        qr.set_text(guest_wifi_qr_str)
        draw_qr_code(self._display, 190, 15, 260, qr)
        
    def print_guest_wifi_got_error(self):
        self._display.set_pen(inky_frame.RED)
        self._display.set_font('cursive')
        self._display.set_thickness(5)
        self._display.text('Trigger "Guest Wifi" got error!', 20, 20, scale=8)
    
    def print_bottom_text(self):
        self._display.set_pen(inky_frame.BLACK)
        self._display.line(0, self._bottom_text_start_y, self._x, self._bottom_text_start_y)
        self._display.set_font('bitmap8')
        self._display.text('A: Night Heater | B: Guest Wifi', 10, self._bottom_text_start_y+7)
    
    def clear(self):
        self._display.set_pen(inky_frame.WHITE)
        self._display.clear()
        
        
    
    def update(self):
        led_busy_on()
        self._display.update()
        led_busy_off()
        
        
        
    def test(self):
        import inky_frame
        BASE_X=80
        self._display.set_pen(1)
        self._display.clear()
        self._display.set_font("bitmap8")
        
        for i in range(8):
            self._display.set_pen(i)
            self._display.rectangle(BASE_X*i, 0, BASE_X, 350)
            if i != 1:
                t_c = i
            else:
                t_c = 0
            self._display.set_pen(t_c)
            
            self._display.text(f'{i}', BASE_X*i+5, 360, scale=5)
        
        inky_frame.led_busy.on()
        self._display.update()
        inky_frame.led_busy.off()

class PicoExplorer():
    def __init__(self):
        display = PicoGraphics(display=DISPLAY_PICO_EXPLORER)
