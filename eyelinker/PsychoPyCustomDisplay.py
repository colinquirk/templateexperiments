"""A module for managing the interaction between pylink and psychopy.

Author - Colin Quirk (cquirk@uchicago.edu)

Repo: https://github.com/colinquirk/templateexperiments

This class is designed to be used by the eyelinker module. If you use it, you won't need
to call any of these functions or change any of this code. If you prefer not to use eyelinker,
simply use `pl.openGraphicsEx(PsychoPyCustomDisplay)` to connect pylink to psychopy. These
 functions are then called by interactions with the tracker.

Classes:
PsychoPyCustomDisplay -- inherited from pylink.EyeLinkCustomDisplay. Defines how pylink events
 should be handled by psychopy.
"""

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
    """Defines how pylink events should be handled by psychopy.

    For more information, see the pylink documentation for custom displays. These docs
    are available on the SR Research forum.

    Parameters:
    window -- A psychopy.visual.Window object
    tracker -- A pylink.EyeLink object

    Methods:
    setup_cal_display -- Clears window on calibration setup.
    exit_cal_display -- Clears window on calibration exit.
    record_abort_hide -- Not implimented.
    setup_image_display -- Shows mouse when camera images are visible.
    image_title -- Updates title text.
    draw_image_line -- Draws image from buffer.
    set_image_palette -- Defines image colors.
    exit_image_display -- Hides mouse when camera images are no longer visible.
    clear_cal_display -- Clears calibration targets.
    erase_cal_target -- Clears a individual calibration target.
    draw_cal_target -- Draws calibration targets.
    play_beep -- Provides audio feedback.
    get_input_key -- Handles key events.
    alert_printf -- Prints warnings, but doesn't kill session.
    draw_line -- Draws crosshair lines.
    draw_lozenge -- Draws ovals on image.
    get_mouse_state -- Gets mouse position.
    """
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
            pylink.CAL_TARG_BEEP: psychopy.sound.Sound(value='C', secs=0.2, octave=5),
            pylink.DC_TARG_BEEP: psychopy.sound.Sound(value='C', secs=0.2, octave=5),
            pylink.CAL_GOOD_BEEP: psychopy.sound.Sound(value='A', secs=0.2, octave=6),
            pylink.DC_GOOD_BEEP: psychopy.sound.Sound(value='A', secs=0.2, octave=6),
            pylink.CAL_ERR_BEEP: psychopy.sound.Sound(value='E', secs=0.5, octave=4),
            pylink.DC_ERR_BEEP: psychopy.sound.Sound(value='E', secs=0.5, octave=4)
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
            self.window, text='', pos=(0, -200), height=20, units='pix', color=self.text_color
        )

        self.cal_target_outer = psychopy.visual.Circle(
            self.window, units='pix', radius=18, lineColor='black', fillColor='white'
        )

        self.cal_target_inner = psychopy.visual.Circle(
            self.window, units='pix', radius=6, lineColor='black', fillColor='black'
        )

    def setup_cal_display(self):
        """Clears window on calibration setup."""
        self.window.flip()

    def exit_cal_display(self):
        """Clears window on calibration exit."""
        self.window.flip()

    def record_abort_hide(self):
        """Not implimented."""
        pass

    def setup_image_display(self, width, height):
        """Shows mouse when camera images are visible."""
        psychopy.event.Mouse(visible=True)
        self.window.flip()

    def image_title(self, title):
        """Updates title text."""
        self.image_title_object.text = title

    def draw_image_line(self, width, line, totlines, buff):
        """Draws image from buffer."""
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
        """Defines image colors."""
        self.pal = []

        # Code taken from pylink docs and altered
        for r_, g_, b_ in zip(r, g, b):
            self.pal.append((b_ << 16) | g_ << 8 | r_)

    def exit_image_display(self):
        """Hides mouse when camera images are no longer visible."""
        psychopy.event.Mouse(visible=False)
        self.window.flip()

    def clear_cal_display(self):
        """Clears calibration targets."""
        self.window.flip()

    def erase_cal_target(self):
        """Clears a individual calibration target."""
        self.window.flip()

    def draw_cal_target(self, x, y):
        """Draws calibration targets."""
        self.cal_target_outer.pos = (x - self.window_adj[0], y - self.window_adj[1])
        self.cal_target_inner.pos = (x - self.window_adj[0], y - self.window_adj[1])

        self.cal_target_outer.draw()
        self.cal_target_inner.draw()

        self.window.flip()

    def play_beep(self, beepid):
        """Provides audio feedback."""
        self.beeps[beepid].play()

    def get_input_key(self):
        """Handles key events."""
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
        """Prints warnings, but doesn't kill session."""
        warnings.warn(msg, RuntimeWarning)

    def draw_line(self, x1, y1, x2, y2, colorindex):
        """Draws crosshair lines."""
        # For some reason the crosshairs need to be fixed like this
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
        """Draws ovals on image."""
        if colorindex in self.colors:
            color = self.colors[colorindex]
        else:
            color = (0, 0, 0)

        # Adjustments are made so that center is (0,0) and y is flipped
        x = round(x + (0.5 * width)) - 96
        y = round((160 - y) - (0.5 * height)) - 80

        psychopy.visual.Circle(
            self.window, units='pix', lineColor=color, pos=(x, y), size=(width, height)).draw()

    def get_mouse_state(self):
        """Gets mouse position."""
        mouse_pos = self.mouse.getPos()
        mouse_pos = psychopy.tools.monitorunittools.convertToPix(
            mouse_pos, [0, 0], self.window.units, self.window
        )
        # Adjustments are made so that center is (0,0) and y is flipped
        mouse_pos = (mouse_pos[0] + 96, (160 - mouse_pos[1]) - 80)
        mouse_click = 1 if self.mouse.getPressed()[0] else 0
        return (mouse_pos, mouse_click)
