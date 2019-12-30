"""A module for managing the interaction between pylink and psychopy.

Author - Colin Quirk (cquirk@uchicago.edu)

Repo: https://github.com/colinquirk/templateexperiments

Eyelinker provides a few high level functions designed to make it a bit easier to do common tasks.
For a high level overview, see the readme and example script.

Functions:
EyeLinker -- This is a factory function that returns either a ConnectedEyeLinker or, if a
 connection cannot be made, a MockEyeLinker. All other functions are internal.

Classes:
ConnectedEyeLinker -- Returned if a connection is possible. Provides high-level functionality
 on top of pylink.
MockEyelinker -- Has the same attributes and methods as ConnectedEyeLinker, but all functions
 simply pass and no checks are made to the attributes. This makes it easier to debug the psychopy
 code if there is no tracker connected.
"""

import os
import sys
import time

import pylink as pl
from PsychoPyCustomDisplay import PsychoPyCustomDisplay

import psychopy.event
import psychopy.visual


def _try_connection():
    """Attempts to connect to eyetracker.

    Returns a bool indicating if a connection was made and an exception if applicable.
    If there's no exeception, the second return value will be None.
    """
    print('Attempting to connect to eye tracker...')
    try:
        pl.EyeLink()
        return True, None
    except RuntimeError as e:
        return False, e


def _display_not_connected_text(window):
    """Displays the text objects describing available interactions.
    
    Parameters:
    window -- a psychopy.visual.Window
    """
    warning_text = ('WARNING: Eyetracker not connected.\n\n'
                    'Press "R" to retry connecting\n'
                    'Press "Q" to quit\n'
                    'Press "D" to continue in debug mode')

    bg = psychopy.visual.Rect(window, units='norm', width=2, height=2, fillColor=(0.0, 0.0, 0.0))
    text_stim = psychopy.visual.TextStim(window, warning_text, color=(1.0, 1.0, 1.0))

    bg.draw()
    text_stim.draw()

    window.flip(clearBuffer=False)


def _get_connection_failure_response():
    """Returns a key press."""
    return psychopy.event.waitKeys(keyList=['r', 'q', 'd'])[0]


def EyeLinker(window, filename, eye, text_color=None):
    """A factory function that either returns a ConnectedEyeLinker or MockEyeLinker.

    Parameters:
    window -- A psychopy.visual.Window object
    filename -- EDF filename, max 12 characters with extension
    eye -- Which eye(s) to track, either "LEFT", "RIGHT" or "BOTH"
    text_color -- Defined using window color to black or white, but can be overwritten by
     providing a (r,g,b) tuple with values between -1 and 1
    """
    connected, e = _try_connection(window)

    if connected:
        return ConnectedEyeLinker(window, filename, eye, text_color=None)
    else:
        _display_not_connected_text(window)

    response = _get_connection_failure_response()

    while response == 'r':
        connected, e = _try_connection(window)
        if connected:
            window.flip()
            return ConnectedEyeLinker(window, filename, eye, text_color=None)
        else:
            print('Could not connect to tracker. Select again.')
            response = _get_connection_failure_response()

    if response == 'q':
        window.flip()
        raise e
    elif response == 'd':
        window.flip()
        print('Continuing with mock eyetracking. Eyetracking data will not be saved!')
        return MockEyeLinker(window, filename, eye, text_color=None)


class ConnectedEyeLinker:
    """Returned if a connection is possible."""
    def __init__(self, window, filename, eye, text_color=None):
        """See Eyelinker factory function for parameter info."""
        if len(filename) > 12:
            raise ValueError(
                'EDF filename must be at most 12 characters long including the extension.')

        if filename[-4:] != '.edf':
            raise ValueError(
                'Please include the .edf extension in the filename.')

        if eye not in ('LEFT', 'RIGHT', 'BOTH'):
            raise ValueError('eye must be set to LEFT, RIGHT, or BOTH.')

        self.window = window
        self.edf_filename = filename
        self.edf_open = False
        self.eye = eye
        self.resolution = tuple(window.size)
        self.tracker = pl.EyeLink()
        self.genv = PsychoPyCustomDisplay(self.window, self.tracker)
        self.mock = False

        if text_color is None:
            if all(i >= 0.5 for i in self.window.color):
                self.text_color = (-1, -1, -1)
            else:
                self.text_color = (1, 1, 1)
        else:
            self.text_color = text_color

    def initialize_graphics(self):
        """Opens the PsychoPyCustomDisplay object.

        Must be called during setup phase.
        """
        self.set_offline_mode()
        pl.openGraphicsEx(self.genv)

    def initialize_tracker(self):
        """Sends commands setting up basic settings that are unlikely to be changed.

        EDF file must be open before this function is called. Must be called before
        starting to record.
        """
        if not self.edf_open:
            raise RuntimeError('EDF file must be open before tracker can be initialized.')

        pl.flushGetkeyQueue()
        self.set_offline_mode()

        self.send_command("screen_pixel_coords = 0 0 %d %d" % self.resolution)
        self.send_message("DISPLAY_COORDS 0 0 %d %d" % self.resolution)

        self.tracker.setFileEventFilter(
            "LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON")
        self.tracker.setFileSampleFilter(
            "LEFT,RIGHT,GAZE,AREA,GAZERES,STATUS")
        self.tracker.setLinkEventFilter(
            "LEFT,RIGHT,FIXATION,SACCADE,BLINK,BUTTON")
        self.tracker.setLinkSampleFilter(
            "LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS")

    def send_tracking_settings(self, settings=None):
        """Sends settings to tracker.

        Default settings are sent, but can be overwritten.

        Parameters:
        settings -- a dictionary of settings to overwrite the defaults.

        For information about settings, see the pylink docs.
        """
        defaults = {
            'automatic_calibration_pacing': 1000,
            'background_color': (0, 0, 0),
            'calibration_area_proportion': (0.5, 0.5),
            'calibration_type': 'HV9',
            'elcl_configuration': 'BTABLER',
            'enable_automatic_calibration': 'YES',
            'error_sound': '',
            'foreground_color': (255, 255, 255),
            'good_sound': '',
            'preamble_text': None,
            'pupil_size_diameter': 'NO',
            'saccade_acceleration_threshold': 9500,
            'saccade_motion_threshold': 0.15,
            'saccade_pursuit_fixup': 60,
            'saccade_velocity_threshold': 30,
            'sample_rate': 1000,
            'target_sound': '',
            'validation_area_proportion': (0.5, 0.5),
        }

        if settings is None:
            settings = {}

        defaults.update(settings)
        settings = defaults

        self.send_command('elcl_select_configuration = %s' % settings['elcl_configuration'])

        pl.setCalibrationColors(settings['foreground_color'], settings['background_color'])
        pl.setCalibrationSounds(
            settings['target_sound'], settings['good_sound'], settings['error_sound'])

        if self.eye in ('LEFT', 'RIGHT'):
            self.send_command('active_eye = %s' % self.eye)

        self.send_command(
            'automatic_calibration_pacing = %i' % settings['automatic_calibration_pacing'])

        if self.eye == 'BOTH':
            self.send_command('binocular_enabled = YES')
        else:
            self.send_command('binocular_enabled = NO')

        self.send_command(
            'calibration_area_proportion %f %f' % settings['calibration_area_proportion'])

        self.send_command('calibration_type = %s' % settings['calibration_type'])
        self.send_command(
            'enable_automatic_calibration = %s' % settings['enable_automatic_calibration'])
        if settings['preamble_text'] is not None:
            self.send_command('add_file_preamble_text %s' % '"' + settings['preamble_text'] + '"')
        self.send_command('pupil_size_diameter = %s' % settings['pupil_size_diameter'])
        self.send_command(
            'saccade_acceleration_threshold = %i' % settings['saccade_acceleration_threshold'])
        self.send_command('saccade_motion_threshold = %i' % settings['saccade_motion_threshold'])
        self.send_command('saccade_pursuit_fixup = %i' % settings['saccade_pursuit_fixup'])
        self.send_command(
            'saccade_velocity_threshold = %i' % settings['saccade_velocity_threshold'])
        self.send_command('sample_rate = %i' % settings['sample_rate'])
        self.send_command(
            'validation_area_proportion %f %f' % settings['validation_area_proportion'])

    def open_edf(self):
        """Opens the edf file, must be called before tracker is initialized."""
        self.tracker.openDataFile(self.edf_filename)
        self.edf_open = True

    def close_edf(self):
        """Closes the edf file at the end of the experiment."""
        self.tracker.closeDataFile()
        self.edf_open = False

    def transfer_edf(self, new_filename=None):
        """Transfers the edf file to the computer running psychopy.

        Parameters:
        new_filename -- optionally, a new filename for the edf file with no character restriciton.
        """
        if not new_filename:
            new_filename = self.edf_filename

        if new_filename[-4:] != '.edf':
            raise ValueError('Please include the .edf extension in the filename.')

        # Prevents timeouts due to excessive printing
        sys.stdout = open(os.devnull, "w")
        self.tracker.receiveDataFile(self.edf_filename, new_filename)
        sys.stdout = sys.__stdout__
        print(new_filename + ' has been transferred successfully.')

    def setup_tracker(self):
        """Enters setup menu on eyelink computer."""
        self.window.flip()
        self.tracker.doTrackerSetup()

    def display_eyetracking_instructions(self):
        """Displays basic instructions to participant."""
        self.window.flip()

        psychopy.visual.Circle(
            self.window, units='pix', radius=18, lineColor='black', fillColor='white'
        ).draw()
        psychopy.visual.Circle(
            self.window, units='pix', radius=6, lineColor='black', fillColor='black'
        ).draw()

        psychopy.visual.TextStim(
            self.window, text='Sometimes a target that looks like this will appear.',
            color=self.text_color, units='norm', pos=(0, 0.22), height=0.05
        ).draw()

        psychopy.visual.TextStim(
            self.window, color=self.text_color, units='norm', pos=(0, -0.18), height=0.05,
            text='We use it to calibrate the eye tracker. Stare at it whenever you see it.'
        ).draw()

        psychopy.visual.TextStim(
            self.window, color=self.text_color, units='norm', pos=(0, -0.28), height=0.05,
            text='Press any key to continue.'
        ).draw()

        self.window.flip()
        psychopy.event.waitKeys()
        self.window.flip()

    def calibrate(self, text=None):
        """Like setup_tracker, but gives the experimenter the option to skip.

        Parameters:
        text -- A string containing the text to display to the experimenter
        """
        self.window.flip()

        if text is None:
            text = (
                'Experimenter:\n'
                'If you would like to calibrate, press space.\n'
                'To skip calibration, press the escape key.'
            )

        psychopy.visual.TextStim(
            self.window, text=text, pos=(0, 0), height=0.05, units='norm', color=self.text_color
        ).draw()

        self.window.flip()

        keys = psychopy.event.waitKeys(keyList=['escape', 'space'])

        self.window.flip()

        if 'space' in keys:
            self.tracker.doTrackerSetup()

    def drift_correct(self, position=None, setup=1):
        """Enters into drift correct mode.

        Parameters:
        position -- A 2 item tuple describing where the target should be displayed in window units
        setup -- If the setup menu should be accessed after correction
        """
        if position is None:
            position = tuple([int(round(i/2)) for i in self.resolution])

        try:
            self.tracker.doDriftCorrect(position[0], position[1], 1, setup)
            self.tracker.applyDriftCorrect()
        except RuntimeError as e:
            print(e.message)

    def record(self, to_record_func):
        """A python decorator for if what you want to record is contained in a single function.

        See eyelinker_example.py for an example."""
        def wrapped_func():
            self.start_recording()
            to_record_func()
            self.stop_recording()
        return wrapped_func

    def start_recording(self):
        """Start the eyetracking recording.

        Requires a short delay after calling, so do not call this function during a timing
         specific part of the experiment.
        """
        self.tracker.startRecording(1, 1, 1, 1)
        time.sleep(.1)  # required

    def stop_recording(self):
        """Stops the eyetracking recording.

        Requires a short delay before calling, so do not call this function during a timing
         specific part of the experiment.
        """
        time.sleep(.1)  # required
        self.tracker.stopRecording()

    @property
    def gaze_data(self):
        """A property with the most recent gaze sample.

        Contains a tuple with gaze data. If both eyes are being tracked the tuple contains two
         tuples. Each tuple of gaze data contains an x and y value in pixels. Can be accessed
         with `tracker.gaze_data`

        See eyelinker_example.py for an example.
        """
        sample = self.tracker.getNewestSample()

        if self.eye == 'LEFT':
            return sample.getLeftEye().getGaze()
        elif self.eye == 'RIGHT':
            return sample.getRightEye().getGaze()
        else:
            return (sample.getLeftEye().getGaze(), sample.getRightEye().getGaze())

    @property
    def pupil_size(self):
        """A property with the most recent pupil size.

        If both eyes are being tracked, returns a tuple containing two values. Otherwise, returns
        a single value. Pupil sizes units can be controlled with `send_tracking_settings`.
         Eyelinker returns area by defult. See pylink docs about `setPupilSizeDiameter` for more
         info.

        See eyelinker_example.py for an example.
        """
        sample = self.tracker.getNewestSample()

        if self.eye == 'LEFT':
            return sample.getLeftEye().getPupilSize()
        elif self.eye == 'RIGHT':
            return sample.getRightEye().getPupilSize()
        else:
            return (sample.getLeftEye().getPupilSize(), sample.getRightEye().getPupilSize())

    def set_offline_mode(self):
        """Sets tracker to offline mode."""
        self.tracker.setOfflineMode()

    def send_command(self, cmd):
        """Sends a command to the tracker.

        Mostly used internally, but available if needed. See pylink docs for available commands.

        Parameters:
        cmd -- A string containing the command to be send to the tracker
        """
        self.tracker.sendCommand(cmd)

    def send_message(self, msg):
        """Sends a message to be saved to the EDF file.

        Not to be confused with send_status. Useful for marking specific times, e.g. trial start

        Parameters:
        msg -- A string containing information to be saved.
        """
        self.tracker.sendMessage(msg)

    def send_status(self, status):
        """Sends a status to be displayed to the experimenter.

        The status is displayed on the eyelink computer during the experiment. Useful for tracking
         information like the current experiment condition during recording.

        Parameters:
        status -- A string containing the info to be displayed. Should be less than 80 characters.
        """

        if len(status) >= 80:
            print('Warning: Status should be less than 80 characters.')

        self.send_command("record_status_message '%s'" % status)

    def close_connection(self):
        """Closes the connection to the tracker.

        Must be called at the end of the experiment."""
        self.tracker.close()
        pl.closeGraphics()


# Creates a mock object to be used if tracker doesn't connect for debug purposes
_method_list = [fn_name for fn_name in dir(ConnectedEyeLinker)
                if callable(getattr(ConnectedEyeLinker, fn_name)) and not fn_name.startswith("__")]


def _mock_func(*args, **kwargs):
    pass


class MockEyeLinker:
    """Returned if a connection could not be made, useful for debugging away from the trackers."""
    def __init__(self, window, filename, eye, text_color=None):
        self.window = window
        self.edf_filename = filename
        self.edf_open = False
        self.eye = eye
        self.resolution = tuple(window.size)
        self.tracker = None
        self.genv = None
        self.gaze_data = (None, None)
        self.pupil_size = (None, None)
        self.mock = True

        if text_color is None:
            if all(i >= 0.5 for i in self.window.color):
                self.text_color = (-1, -1, -1)
            else:
                self.text_color = (1, 1, 1)
        else:
            self.text_color = text_color

        for fn_name in _method_list:
            setattr(self, fn_name, _mock_func)

        # Decorator must return a function
        def record(*args, **kwargs):
            return _mock_func

        self.record = record
