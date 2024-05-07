# Add M0 (Unconditional Stop) to klipper
#
# Copyright (C) 2024 Justin F. Hallett <thesin@gmail.com>
#
# This file may be distributed under the terms of the GNU GPLv3 license.

class UnconditionalStop:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.gcode = self.printer.lookup_object('gcode')
        self.gcode.register_command('M0',
                                    self.cmd_M0,
                                    desc=self.cmd_M0_help)

    cmd_M0_help = "Unconditional stop"
    def cmd_M0(self, gcmd):
        pause_resume = self.printer.lookup_object('pause_resume')
        if pause_resume:
            gcmd.respond_info(self.cmd_M0_help)
            pause_resume.cmd_PAUSE(gcmd)
        else:
            gcmd.respond_info("PauseResume module not loaded")

def load_config(config):
    return UnconditionalStop(config)
