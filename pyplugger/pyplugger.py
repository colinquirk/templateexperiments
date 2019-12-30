"""A module for managing the interaction between pycorder and psychopy.

Author - Colin Quirk (cquirk@uchicago.edu)

Repo: https://github.com/colinquirk/templateexperiments

Pyplugger provides functions to control EEG recordings through the BrainVision software pycorder.
In order to use pylugger, a network connection between the computer running pycorder and the
 computer running psychopy.

Important note: You cannot open pycorder normally, you must open it in remote mode for this
 module to work. See the pycorder documentation for notes about how to do this.

Functions:
PyPlugger -- This is a factory function that returns either a ConnectedPyPlugger or, if a
 connection cannot be made, a MockPyPlugger. All other functions are internal.

Classes:
ConnectedPyPlugger -- Returned if a connection is possible. Provides high-level functionality
 through pycorder.
MockPyPlugger-- Has the same attributes and methods as ConnectedPyPlugger, but all functions
 simply pass and no checks are made to the attributes. This makes it easier to debug the psychopy
 code if there is no connection.
"""


import socket
import time

import psychopy.event
import psychopy.parallel
import psychopy.visual


def _try_connection(tcp_ip, tcp_port):
    """Attempts to connect to pycorder.

    Returns a bool indicating if a connection was made and an exception if applicable.
    If there's no exeception, the second return value will be None.

    Parameters:
    tcp_ip -- the ip address of the pycorder computer
    tcp_port -- the port to connect to, should always be 6700
    """
    print('Attempting to connect to EEG system...')
    try:
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((tcp_ip, tcp_port))
        return True, None
    except socket.timeout as e:
        return False, e


def _display_not_connected_text(window):
    """Displays the text objects describing available interactions.

    Parameters:
    window -- a psychopy.visual.Window
    """
    warning_text = ('WARNING: EEG system not connected.\n\n'
                    'Press "R" to retry connecting\n'
                    'Press "Q" to quit\n'
                    'Press "D" to continue in debug mode')

    bg = psychopy.visual.Rect(window, units='norm', width=2, height=2, fillColor=(0.0, 0.0, 0.0))
    text_stim = psychopy.visual.TextStim(window, warning_text, color=(1.0, 1.0, 1.0))

    bg.draw()
    text_stim.draw()

    window.flip(clearBuffer=False)


def _get_connection_failure_response():
    """Returns a key press, 'r', 'q', or 'd'"""
    return psychopy.event.waitKeys(keyList=['r', 'q', 'd'])[0]


# A factory function disguised as a class
def PyPlugger(window, config_file, tcp_ip="100.1.1.3",
              tcp_port=6700, parallel_port_address=53328, text_color=None):
    """A factory function that either returns a ConnectedPyPlugger or MockPyPlugger.

    Parameters:
    window -- A psychopy.visual.Window object
    config_file -- An xml config file created by pycorder
    tcp_ip -- the ip address of the pycorder computer
    tcp_port -- the port to connect to, should always be 6700
    parallel_port_address -- the address of the parallel port as required by psychopy.parallel
    text_color -- Defined using window color to black or white, but can be overwritten by
     providing a (r,g,b) tuple with values between -1 and 1
    """
    connected, e = _try_connection(tcp_ip, tcp_port)

    if connected:
        return ConnectedPyPlugger(window, config_file, tcp_ip="100.1.1.3",
                                  tcp_port=6700, parallel_port_address=53328, text_color=None)
    else:
        _display_not_connected_text(window)

    response = _get_connection_failure_response()

    while response == 'r':
        connected, e = _try_connection(tcp_ip, tcp_port)
        if connected:
            window.flip()
            return ConnectedPyPlugger(window, config_file, tcp_ip="100.1.1.3",
                                      tcp_port=6700, parallel_port_address=53328, text_color=None)
        else:
            print('Could not connect, select again.')
            response = _get_connection_failure_response()

    if response == 'q':
        window.flip()
        raise e
    elif response == 'd':
        window.flip()
        print('Continuing with mock eeg. EEG data will not be saved!')
        return MockPyPlugger(window, config_file, tcp_ip="100.1.1.3",
                             tcp_port=6700, parallel_port_address=53328, text_color=None)


class ConnectedPyPlugger:
    """Returned if a connection is possible."""
    def __init__(self, window, config_file, tcp_ip="100.1.1.3",
                 tcp_port=6700, parallel_port_address=53328, text_color=None):
        self.window = window
        self.config_file = config_file
        self.tcp_ip = tcp_ip
        self.tcp_port = tcp_port
        self.current_mode = None
        self.socket = None
        self.mock = False

        psychopy.parallel.setPortAddress(parallel_port_address)
        psychopy.parallel.setData(0)

        if text_color is None:
            if all(i >= 0.5 for i in self.window.color):
                self.text_color = (-1, -1, -1)
            else:
                self.text_color = (1, 1, 1)
        else:
            self.text_color = text_color

    def initialize_session(self, experiment_name, subject_number, timeout=5):
        """Sets up the socket connection.

        Parameters:
        experiment_name -- the name of the experiment to be used in the filename
        subject_number -- the subject number to be used in the filename
        timeout -- an int describing how long in seconds to wait for a connection
        """
        messages = ['1' + self.config_file,
                    '2' + str(experiment_name),
                    '3' + str(subject_number),
                    '4']

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(timeout)
        self.socket.connect((self.tcp_ip, self.tcp_port))

        for tcp_message in messages:
            self.socket.send(tcp_message.encode())
            time.sleep(1)

    def switch_mode(self, mode, delay=5):
        """Switches between recording modes.

        Parameters:
        mode -- A string containing the mode, "M" for monitoring or "I" for impedance
        delay -- how long to wait after sending the command
        """
        self.socket.send(mode.encode())
        self.current_mode = mode
        time.sleep(delay)

    def start_recording(self, delay=5):
        """Starts saving the recording.

        Not to be confused with switching to monitor mode, which does not start saving the data.

        Parameters:
        delay -- how long to wait after sending the command
        """
        self.socket.send("S".encode())
        time.sleep(delay)  # Ensure recording has started

    def stop_recording(self, delay=5, exit_mode=False):
        """Stops saving the recording.

        Parameters:
        delay -- how long to wait after sending the command
        exit_mode -- whether to leave the current mode after this command is sent
        """
        if exit_mode:
            cmd = 'X'
        else:
            cmd = 'Q'

        self.socket.send(cmd.encode())
        time.sleep(delay)  # Ensure recording has ended

    @staticmethod
    def start_event(event):
        """Sends an event to the parallel port.

        Parameters:
        event -- data describing how pins should be set, see parallel docs for details
        """
        psychopy.parallel.setData(event)

    @staticmethod
    def end_event():
        """Resets the parallel port to 0.

        To be called some time after an event has been sent. Not strictly necessary if all that
        matters is the start of your events."""
        psychopy.parallel.setData(0)

    def display_eeg_instructions(self, eeg_instruction_text=None):
        """Displays a window with some generic EEG instructions.

        Parameters:
        eeg_instruction_text -- a string containing text to be displayed
        """
        self.window.flip()

        if eeg_instruction_text is None:
            eeg_instruction_text = ('We will be recording EEG in this experiment. '
                                    'In order to prevent artifacts due to muscle movements, please'
                                    ' try to avoid moving your head and clenching your jaw.\n\n'
                                    'Please avoid blinking while performing the task. '
                                    'Try to blink only in between trials.')

        psychopy.visual.TextStim(self.window, color=self.text_color, units='norm', pos=(0, 0.22),
                                 height=0.05, text=eeg_instruction_text).draw()

        psychopy.visual.TextStim(self.window, color=self.text_color, units='norm', pos=(0, -0.28),
                                 height=0.05, text='Press any key to continue.').draw()

        self.window.flip()
        psychopy.event.waitKeys()
        self.window.flip()

    def display_interactive_switch_screen(self, require_monitoring=True):
        """Allows the experimenter to switch modes from the experiment computer.

        Using this function with require_monitoring=True will ensure that pycorder will always be
        able to record data when it is supposed to, as determined by the experiment code.

        Parameters:
        require_monitoring -- If true, forces monitor mode at the end of the function execution.
        """
        switch_text = ('You may switch modes now.\n\n'
                       'Press "M" for monitor mode.\n'
                       'Press "I" for impedance mode.\n'
                       'Press "Q" to continue with the experiment.')

        psychopy.visual.TextStim(self.window, switch_text, color=self.text_color).draw()
        self.window.flip()

        response = None
        while response != 'q':
            response = psychopy.event.waitKeys(keyList=['m', 'i', 'q'])[0]
            if response != 'q':
                self.switch_mode(response.upper())

        if require_monitoring:
            if self.current_mode != 'M':
                self.switch_mode('M')

        self.window.flip()


# Creates a mock object to be used if tracker doesn't connect for debug purposes
method_list = [fn_name for fn_name in dir(ConnectedPyPlugger)
               if callable(getattr(ConnectedPyPlugger, fn_name)) and not fn_name.startswith("__")]


def _mock_func(*args, **kwargs):
    pass


class MockPyPlugger:
    """Returned if a connection could not be made, useful for debugging away from the trackers."""
    def __init__(self, window, config_file, tcp_ip="100.1.1.3",
                 tcp_port=6700, parallel_port_address=53328, text_color=None):
        self.window = window
        self.config_file = config_file
        self.tcp_ip = tcp_ip
        self.tcp_port = tcp_port
        self.current_mode = None
        self.socket = None
        self.mock = True

        if text_color is None:
            if all(i >= 0.5 for i in self.window.color):
                self.text_color = (-1, -1, -1)
            else:
                self.text_color = (1, 1, 1)
        else:
            self.text_color = text_color

        for fn_name in method_list:
            setattr(self, fn_name, _mock_func)
