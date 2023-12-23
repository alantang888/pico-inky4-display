from picographics import PicoGraphics, DISPLAY_INKY_FRAME_4, DISPLAY_PICO_EXPLORER

try:
    import inky_frame
    led_busy_on = inky_frame.led_busy.on
    led_busy_off = inky_frame.led_busy.off
    print('imported inky_frame.')
except:
    print('import inky_frame error. Use dummy function.')
    led_busy_on = lambda: None
    led_busy_off = lambda: None


class InkyFrame4():
    def __init__(self):
        self._display = PicoGraphics(display=DISPLAY_INKY_FRAME_4)
        self._last_co2_ppm = 0
        self._x, self._y = self._display.get_bounds()
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
