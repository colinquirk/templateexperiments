import time

import pylink as pl
from EyeLinkCoreGraphicsPsychoPy import EyeLinkCoreGraphicsPsychoPy


class EyeLinker(object):
    def __init__(self, window, filename, resolution):
        self.window = window

        if len(filename > 12) or filename[-4:] != '.edf':
            raise ValueError(
                'EDF filename must be at most 12 characters long including the extension.')

        self.edf_filename = filename
        self.edf_open = False
        self.resolution = resolution
        self.tracker = pl.EyeLink()
        self.genv = EyeLinkCoreGraphicsPsychoPy(self.tracker, self.window)

    def initialize_graphics(self):
        self.tracker.setOfflineMode()
        pl.openGraphicsEx(self.genv)

    def initialize_tracker(self):
        if not self.edf_open:
            raise RuntimeError('EDF file must be open before tracker can be initialized.')

        pl.flushGetkeyQueue()
        self.tracker.setOfflineMode()

        self.sendCommand("screen_pixel_coords = 0 0 %d %d" % self.resolution)
        self.sendMessage("DISPLAY_COORDS 0 0 %d %d" % self.resolution)

        self.tracker.setFileEventFilter(
            "LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON")
        self.tracker.setFileSampleFilter(
            "LEFT,RIGHT,GAZE,AREA,GAZERES,STATUS")
        self.tracker.setLinkEventFilter(
            "LEFT,RIGHT,FIXATION,SACCADE,BLINK,BUTTON")
        self.tracker.setLinkSampleFilter(
            "LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS")

    def send_calibration_settings(self, settings):
        defaults = {
            'active_eye': 'RIGHT',
            'automatic_calibration_pacing': 1000,
            'background_color': (0, 0, 0),
            'binocular_enabled': 'NO',
            'calibration_type': 'HV9',
            'enable_automatic_calibration': 'YES',
            'error_sound': 'off',
            'foreground_color': (0, 0, 0),
            'good_sound': 'off',
            'pupil_size_diameter': 'NO',
            'saccade_acceleration_threshold': 9500,
            'saccade_motion_threshold': 0.15,
            'saccade_pursuit_fixup': 60,
            'saccade_velocity_threshold': 30,
            'target_sound': 'off',
        }

        settings.update(defaults)

        pl.setCalibrationColors(settings['foreground_color'], settings['background_color'])
        pl.setCalibrationSounds(
            settings['target_sound'], settings['good_sound'], settings['error_sound'])

        self.send_command('active_eye = %s' % settings['active_eye'])
        self.send_command(
            'automatic_calibration_pacing = %i' % settings['automatic_calibration_pacing'])
        self.send_command('binocular_enabled = %s' % settings['binocular_enabled'])
        self.send_command('calibration_type = %s' % settings['calibration_type'])
        self.send_command(
            'enable_automatic_calibration = %s' % settings['enable_automatic_calibration'])
        self.send_command('pupil_size_diameter = %s' % settings['pupil_size_diameter'])
        self.send_command(
            'saccade_acceleration_threshold = %i' % settings['saccade_acceleration_threshold'])
        self.send_command('saccade_motion_threshold = %i' % settings['saccade_motion_threshold'])
        self.send_command('saccade_pursuit_fixup = %i' % settings['saccade_pursuit_fixup'])
        self.send_command(
            'saccade_velocity_threshold = %i' % settings['saccade_velocity_threshold'])

    def open_edf(self):
        self.tracker.openDataFile(self.edf_filename)

    def close_edf(self):
        self.tracker.closeDataFile()

    def transfer_edf(self, newFilename=None):
        if not newFilename:
            newFilename = self.edf_filename

        self.tracker.receiveDataFile(self.edf_filename, self.edf_filename)

    def calibrate(self):
        self.tracker.doTrackerSetup()

    def clear_screen(self, color=0):
        self.send_command('clear_screen %i' % color)

    def draw_text(self, text, x=None, y=None, color=0):
        if x is None:
            x = self.resolution[0] / 2

        if y is None:
            y = self.resolution[1] / 2

        cmd = 'draw_text %i %i %i %s' % (x, y, color, '"' + text + '"')

        self.send_command(cmd)

    def drift_correct(self, position=None):
        if position is None:
            position = tuple([round(i/2) for i in self.resolution])

        self.tracker.doDriftCorrect(position[0], position[1], 1, 1)
        self.tracker.applyDriftCorrect()

    def start_recording(self):
        self.tracker.startRecording(1, 1, 1, 1)
        time.sleep(.1)  # required

    def stop_recording(self):
        time.sleep(.1)  # required
        self.tracker.stopRecording()

    def send_command(self, cmd):
        self.tracker.sendCommand(cmd)

    def send_message(self, msg):
        self.tracker.sendMessage(msg)

    def close_connection(self):
        self.tracker.close()
        pl.closeGraphics()
