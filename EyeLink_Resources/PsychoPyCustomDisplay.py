from __future__ import print_function
from __future__ import division

import array
import string
import warnings

import PIL

import pylink

import psychopy.event
import psychopy.sound
import psychopy.tools
import psychopy.visual


class PsychoPyCustomDisplay(pylink.EyeLinkCustomDisplay):
    def __init__(self, window, tracker):
        pylink.EyeLinkCustomDisplay.__init__(self)
        self.window = window
        # adjusted to put center at (0,0)
        self.window_adj = [i / 2 for i in self.window.size]
        self.tracker = tracker

        self.pal = []
        self.image_buffer = array.array('I')

        if all(i >= 0.5 for i in self.window.color):
            self.text_color = (-1, -1, -1)
        else:
            self.text_color = (1, 1, 1)

        self.beeps = {
            pylink.CAL_TARG_BEEP: psychopy.sound.Sound(value='C', secs=0.05, octave=4),
            pylink.DC_TARG_BEEP: psychopy.sound.Sound(value='C', secs=0.05, octave=4),
            pylink.CAL_GOOD_BEEP: psychopy.sound.Sound(value='A', secs=0.1, octave=6),
            pylink.DC_GOOD_BEEP: psychopy.sound.Sound(value='A', secs=0.1, octave=6),
            pylink.CAL_ERR_BEEP: psychopy.sound.Sound(value='E'),
            pylink.DC_ERR_BEEP: psychopy.sound.Sound(value='E')
        }

        self.colors = {
            pylink.CR_HAIR_COLOR: (1, 1, 1),
            pylink.PUPIL_HAIR_COLOR: (1, 1, 1),
            pylink.PUPIL_BOX_COLOR: (-1, 1, -1),
            pylink.SEARCH_LIMIT_BOX_COLOR: (1, -1, -1),
            pylink.MOUSE_CURSOR_COLOR: (1, -1, -1)
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
            'num_add': 43,
            'equal': 43,
            'num_subtract': 45,
            'minus': 45,
            'backspace': ord('\b'),
            'space': ord(' '),
            'tab': ord('\t')
        }

        self.mouse = psychopy.event.Mouse(visible=False)

        self.image_title_object = psychopy.visual.TextStim(
            self.window, text='', pos=(0, -0.2), height=0.05, units='norm', color=self.text_color
        )

        self.cal_target_outer = psychopy.visual.Circle(
            self.window, units='pix', radius=18, lineColor='black', fillColor='white'
        )

        self.cal_target_inner = psychopy.visual.Circle(
            self.window, units='pix', radius=6, lineColor='black', fillColor='black'
        )

    def setup_cal_display(self):
        self.window.flip()

    def exit_cal_display(self):
        self.window.flip()

    def record_abort_hide(self):
        pass

    def setup_image_display(self, width, height):
        psychopy.event.Mouse(visible=True)
        self.window.flip()

    def image_title(self, title):
        self.image_title_object.text = title

    def draw_image_line(self, width, line, totlines, buff):
        for i in buff:
            if i >= len(self.pal):
                self.image_buffer.append(self.pal[-1])
            else:
                self.image_buffer.append(self.pal[i])

        if line == totlines:
            bufferv = self.image_buffer.tostring()
            image = PIL.Image.frombytes("RGBX", (width, totlines), bufferv)

            psychopy_image = psychopy.visual.ImageStim(self.window, image=image)

            psychopy_image.draw()
            self.draw_cross_hair()
            self.image_title_object.draw()
            self.window.flip()

            self.image_buffer = array.array('I')

    def set_image_palette(self, r, g, b):
        self.pal = []

        # Code taken from pylink docs and altered
        for r_, g_, b_ in zip(r, g, b):
            self.pal.append((b_ << 16) | g_ << 8 | r_)

    def exit_image_display(self):
        psychopy.event.Mouse(visible=False)
        self.window.flip()

    def clear_cal_display(self):
        self.window.flip()

    def erase_cal_target(self):
        self.window.flip()

    def draw_cal_target(self, x, y):
        self.cal_target_outer.pos = (x - self.window_adj[0], y - self.window_adj[1])
        self.cal_target_inner.pos = (x - self.window_adj[0], y - self.window_adj[1])

        self.cal_target_outer.draw()
        self.cal_target_inner.draw()

        self.window.flip()

    def play_beep(self, beepid):
        self.beeps[beepid].play()

    def get_input_key(self):
        keys = []

        for keycode, modifiers in psychopy.event.getKeys(modifiers=True):
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
        warnings.warn(msg, RuntimeWarning)

    def draw_line(self, x1, y1, x2, y2, colorindex):
        if x1 < 0:
            x1, x2 = x1 + 767, x2 + 767
            y1, y2 = y1 + 639, y2 + 639

        if colorindex in self.colors:
            color = self.colors[colorindex]
        else:
            color = (0, 0, 0)

        # Adjustments are made so that center is (0,0) and y is flipped
        x1, x2 = x1 - 96, x2 - 96
        y1, y2 = (160 - y1 - 80), (160 - y2 - 80)

        psychopy.visual.Line(
            self.window, units='pix', lineColor=color, start=(x1, y1), end=(x2, y2)
        ).draw()

    def draw_lozenge(self, x, y, width, height, colorindex):
        return

    def get_mouse_state(self):
        mouse_pos = self.mouse.getPos()
        # Adjustments are made so that center is (0,0) and y is flipped
        mouse_pos = (mouse_pos[0] + 96, (160 - mouse_pos[1]) - 80)
        mouse_click = 1 if self.mouse.getPressed()[0] else 0
        return (mouse_pos, mouse_click)
