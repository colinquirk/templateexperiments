import time

import pylink as pl


class EyeLinker(object):
    def __init__(self, filename, res):
        self.edf_filename = filename
        self.res = res

    def init_graphics(self):
        # pl.pylink.openGraphics()
        # pl.EYELINK.sendCommand("screen_pixel_coords = 0 0 %d %d" % self.res)
        # pl.EYELINK.sendMessage("DISPLAY_COORDS 0 0 %d %d" % self.res)
        pass

    def initialize_tracker(self):
        pl.pylink.flushGetkeyQueue()
        pl.EYELINK.setOfflineMode()

        pl.EYELINK.setFileEventFilter(
            "LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON")
        pl.EYELINK.setFileSampleFilter(
            "LEFT,RIGHT,GAZE,AREA,GAZERES,STATUS")
        pl.EYELINK.setLinkEventFilter(
            "LEFT,RIGHT,FIXATION,SACCADE,BLINK,BUTTON")
        pl.EYELINK.setLinkSampleFilter(
            "LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS")

    def send_calibration_settings(self, settings):
        pass

    def open_edf(self):
        pl.EYELINK.openDataFile(self.edf_filename)

    def close_edf(self):
        pl.EYELINK.closeDataFile()

    def transfer_edf(self):
        pl.EYELINK.receiveDataFile(self.edf_filename, self.edf_filename)

    def calibrate(self):
        pl.EYELINK.doTrackerSetup()

    def drift_correct(self, res=None):
        if res is None:
            res = self.res

        pl.EYELINK.doDriftCorrect(res[0], res[1], 0, 0)

    def start_recording(self):
        pl.EYELINK.startRecording(1, 1, 1, 1)
        time.sleep(.1)  # required

    def stop_recording(self):
        time.sleep(.1)  # required
        pl.EYELINK.stopRecording()

    def send_command(self, cmd):
        pl.EYELINK.sendCommand(cmd)

    def send_message(self, msg):
        pl.EYELINK.sendMessage(msg)

    def close_connection(self):
        pl.EYELINK.close()
        pl.pylink.closeGraphics()
