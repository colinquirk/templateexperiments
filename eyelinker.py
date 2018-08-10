import time

import pylink as pl
from EyeLinkCoreGraphicsPsychoPy import EyeLinkCoreGraphicsPsychoPy


class EyeLinker(object):
    def __init__(self, window, filename, resolution):
        self.window = window
        self.edf_filename = filename
        self.resolution = resolution
        self.tracker = pl.EyeLink()
        self.genv = EyeLinkCoreGraphicsPsychoPy(self.tracker, self.window)

    def initialize_graphics(self):
        self.tracker.setOfflineMode()
        pl.openGraphicsEx(self.genv)

    def initialize_tracker(self):
        pl.pylink.flushGetkeyQueue()
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
        pass

    def open_edf(self):
        self.tracker.openDataFile(self.edf_filename)

    def close_edf(self):
        self.tracker.closeDataFile()

    def transfer_edf(self):
        self.tracker.receiveDataFile(self.edf_filename, self.edf_filename)

    def calibrate(self):
        self.tracker.doTrackerSetup()

    def drift_correct(self, resolution=None):
        if resolution is None:
            resolution = self.resolution

        self.tracker.doDriftCorrect(resolution[0], resolution[1], 0, 0)

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
        pl.pylink.closeGraphics()
