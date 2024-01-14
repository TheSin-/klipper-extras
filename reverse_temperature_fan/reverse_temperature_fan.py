# Support fans that are enabled until a temperature threshold
#
# Copyright (C) 2024  Justin F. Hallett <thesin@southofheaven.org>
#
# This file may be distributed under the terms of the GNU GPLv3 license.
from .temperature_fan import TemperatureFan, ControlBangBang

PIN_MIN_TIME = 0.100

class ReverseTemperatureFan(TemperatureFan):
    def __init__(self, config):
        self.printer = config.get_printer()
        self.printer.load_object(config, 'heaters')
        self.printer.register_event_handler("klippy:ready", self.handle_ready)
        self.heater_names = config.getlist("heater", ("extruder",))
        self.heater_temp = config.getfloat("heater_temp", 50.0)
        self.heaters = []
        self.heater_ready = False
        super().__init__(config)
        algos = {'watermark': ReverseControlBangBang}
        algo = config.getchoice('control', algos)
        self.control = algo(self, config)
    def handle_ready(self):
        pheaters = self.printer.lookup_object('heaters')
        self.heaters = [pheaters.lookup_heater(n) for n in self.heater_names]
        reactor = self.printer.get_reactor()
        reactor.register_timer(self.callback, reactor.monotonic()+PIN_MIN_TIME)
    def callback(self, eventtime):
        for heater in self.heaters:
            current_temp, target_temp = heater.get_temp(eventtime)
            if (self.heater_ready
                and target_temp < self.heater_temp):
                self.heater_ready = False
            elif (not self.heater_ready
                and target_temp >= self.heater_temp):
                self.heater_ready = True
        return eventtime + 1.


######################################################################
# Reverse Bang-bang control algo
######################################################################

class ReverseControlBangBang(ControlBangBang):
    def __init__(self, temperature_fan, config):
        super().__init__(temperature_fan, config)
        self.circulate = False
    def temperature_callback(self, read_time, temp):
        current_temp, target_temp = self.temperature_fan.get_temp(read_time)
        if (self.circulate
            and temp >= target_temp+self.max_delta):
            self.circulate = False
        elif (not self.circulate
              and temp <= target_temp-self.max_delta):
            self.circulate = True
        if (self.temperature_fan.heater_ready and self.circulate):
            self.temperature_fan.set_speed(read_time,
                                           self.temperature_fan.get_max_speed())
        else:
            self.temperature_fan.set_speed(read_time, 0.)

def load_config_prefix(config):
    return ReverseTemperatureFan(config)
