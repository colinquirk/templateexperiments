from __future__ import print_function
from __future__ import division

import pylink


class EyeLinkCoreGraphicsPsychoPy(pylink.EyeLinkCustomDisplay):
    def __init__(self, window, tracker):
        pylink.EyeLinkCustomDisplay.__init__(self)
        self.window = window
        self.tracker = tracker

    def setup_cal_display(self):
        print('setup_cal_display')
        self.window.flip()

    def exit_cal_display(self):
        print('exit_cal_display')
        self.window.flip()

    def record_abort_hide(self):
        print('record_abort_hide')

    def setup_image_display(self, width, height):
        print('setup_image_display')

    def image_title(self, title):
        print('image_title')

    def draw_image_line(self, width, line, totlines, buff):
        print('draw_image_line')

    def set_image_palette(self, r, g, b):
        print('set_image_palette')

    def exit_image_display(self):
        print('exit_image_display')

    def clear_cal_display(self):
        print('clear_cal_display')

    def erase_cal_target(self):
        print('erase_cal_target')

    def draw_cal_target(self, x, y):
        print('draw_cal_target')

    def play_beep(self, beepid):
        print('play_beep')

    def get_input_key(self):
        print('get_input_key')

    def alert_printf(self, msg):
        print('alert_printf')

    def draw_line(self, x1, y1, x2, y2, colorindex):
        print('draw_line')

    def draw_lozenge(self, x, y, width, height, colorindex):
        print('draw_lozenge')

    def get_mouse_state(self):
        print('get_mouse_state')

    def draw_cross_hair(self):
        print('draw_cross_hair')
