from __future__ import print_function
from __future__ import division

import warnings

import pylink

import psychopy.visual
import psychopy.event


class EyeLinkCoreGraphicsPsychoPy(pylink.EyeLinkCustomDisplay):
    def __init__(self, window, tracker):
        pylink.EyeLinkCustomDisplay.__init__(self)
        self.window = window
        self.tracker = tracker

        if all(i >= 0.5 for i in self.window.color):
            self.text_color = (-1, -1, -1)
        else:
            self.text_color = (1, 1, 1)

        self.image_title = psychopy.visual.TextStim(
            self.window, text='', pos=(0, -0.2), units='norm', color=self.text_color
        )

        self.cal_target_outer = psychopy.visual.Circle(
            self.window, units='pix', radius=10, lineColor='black', fillColor='white'
        )

        self.cal_target_outer = psychopy.visual.Circle(
            self.window, units='pix', radius=4, lineColor='black', fillColor='black'
        )

    def setup_cal_display(self):
        print('setup_cal_display')
        self.window.flip()

    def exit_cal_display(self):
        print('exit_cal_display')
        self.window.flip()

    def record_abort_hide(self):
        print('record_abort_hide')
        raise NotImplementedError('TODO')

    def setup_image_display(self, width, height):
        print('setup_image_display')
        raise NotImplementedError('This should probably pass')

    def image_title(self, title):
        print('image_title')
        self.image_title.text = title

    def draw_image_line(self, width, line, totlines, buff):
        print('draw_image_line')
        raise NotImplementedError('TODO')

    def set_image_palette(self, r, g, b):
        print('set_image_palette')
        raise NotImplementedError('TODO')

    def exit_image_display(self):
        print('exit_image_display')
        self.window.flip()

    def clear_cal_display(self):
        print('clear_cal_display')
        self.window.flip()

    def erase_cal_target(self):
        print('erase_cal_target')
        self.window.flip()

    def draw_cal_target(self, x, y):
        self.cal_target_outer.pos = (x, y)
        self.cal_target_inner.pos = (x, y)

        self.cal_target_outer.draw()
        self.cal_target_inner.draw()

        self.display.flip()

    def play_beep(self, beepid):
        print('play_beep')
        raise NotImplementedError('TODO')

    def get_input_key(self):
        print('get_input_key')
        raise NotImplementedError('TODO')

    def alert_printf(self, msg):
        print('alert_printf')
        warnings.warn(msg, RuntimeWarning)

    def draw_line(self, x1, y1, x2, y2, colorindex):
        print('draw_line')
        raise NotImplementedError('TODO')

    def draw_lozenge(self, x, y, width, height, colorindex):
        print('draw_lozenge')
        raise NotImplementedError('Docs say this function is unused.')

    def get_mouse_state(self):
        print('get_mouse_state')
        raise NotImplementedError('TODO')

    def draw_cross_hair(self):
        print('draw_cross_hair')
        raise NotImplementedError('TODO')
