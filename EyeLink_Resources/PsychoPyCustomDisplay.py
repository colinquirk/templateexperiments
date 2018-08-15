from __future__ import print_function
from __future__ import division

import string
import warnings

import pylink

import psychopy.event
import psychopy.sound
import psychopy.tools
import psychopy.visual


class EyeLinkCoreGraphicsPsychoPy(pylink.EyeLinkCustomDisplay):
    def __init__(self, window, tracker):
        pylink.EyeLinkCustomDisplay.__init__(self)
        self.window = window
        self.tracker = tracker

        if all(i >= 0.5 for i in self.window.color):
            self.text_color = (-1, -1, -1)
        else:
            self.text_color = (1, 1, 1)

        self.beeps = {
            pylink.CAL_TARG_BEEP: psychopy.sound.Sound('type.wav'),
            pylink.DC_TARG_BEEP: psychopy.sound.Sound('type.wav'),
            pylink.CAL_GOOD_BEEP: psychopy.sound.Sound('qbeep.wav'),
            pylink.DC_GOOD_BEEP: psychopy.sound.Sound('qbeep.wav'),
            pylink.CAL_ERR_BEEP: psychopy.sound.Sound('error.wav'),
            pylink.DC_ERR_BEEP: psychopy.sound.Sound('error.wav')
        }

        self.keys = {
            'f1': pylink.F1_KEY,
            'f2': pylink.F2_KEY,
            'f3': pylink.F3_KEY,
            'f4': pylink.F4_KEY,
            'f5': pylink.F5_KEY,
            'f6': pylink.F6_KEY,
            'f7': pylink.F7_KEY,
            'f8': pylink.F8_KEY,
            'f9': pylink.F9_KEY,
            'f10': pylink.F10_KEY,
            'pageup': pylink.PAGE_UP,
            'pagedown': pylink.PAGE_DOWN,
            'up': pylink.CURS_UP,
            'down': pylink.CURS_DOWN,
            'left': pylink.CURS_LEFT,
            'right': pylink.CURS_RIGHT,
            'return': pylink.ENTER_KEY,
            'escape': pylink.ESC_KEY,
            'backspace': ord('\b'),
            'space': ord(' '),
            'tab': ord('\t')
        }

        self.mouse = psychopy.event.Mouse(visible=False)

        self.image_title = psychopy.visual.TextStim(
            self.window, text='', pos=(0, -0.2), units='norm', color=self.text_color
        )

        self.cal_target_outer = psychopy.visual.Circle(
            self.window, units='pix', radius=10, lineColor='black', fillColor='white'
        )

        self.cal_target_inner = psychopy.visual.Circle(
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
        raise NotImplementedError('This should probably pass')

    def setup_image_display(self, width, height):
        print('setup_image_display')
        self.window.flip()

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
        self.beeps[beepid].play()

    def get_input_key(self):
        print('get_input_key')
        keys = []

        for keycode, modifiers in psychopy.event.getKeys(modifiers=True):
            print(keycode)
            print(modifiers)
            if keycode in self.keys:
                key = self.keys[keycode]
            elif keycode in string.ascii_letters:
                key = ord(keycode)
            else:
                key = pylink.JUNK_KEY

            mod = 256 if modifiers['alt'] else 0

            keys.append(pylink.KeyInput(key, mod))

        return keys

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
        mouse_pos = self.mouse.getPos()
        mouse_pos = psychopy.tools.monitorunittools.convertToPix(
            [mouse_pos], mouse_pos, self.window.units, self.window)
        print(mouse_pos)
        mouse_click = 1 if self.mouse.getPressed()[0] else 0
        return (mouse_pos, mouse_click)

    def draw_cross_hair(self):
        print('draw_cross_hair')
        raise NotImplementedError('TODO')
