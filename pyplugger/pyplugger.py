"""A module for managing the interaction between pycorder and psychopy.

Author - Colin Quirk (cquirk@uchicago.edu)

Repo: https://github.com/colinquirk/templateexperiments

Pyplugger provides functions to control EEG recordings through the BrainVision software pycorder.
In order to use pylugger, a network connection between the computer running pycorder and the
 computer running psychopy.

Important note: You cannot open pycorder normally, you must open it in remote mode for this
 module to work. See the pycorder documentation for notes about how to do this.



"""


import socket
import time

import psychopy.event
import psychopy.parallel
import psychopy.visual


def _try_connection(tcp_ip, tcp_port):
    print('Attempting to connect to EEG system...')
    try:
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((tcp_ip, tcp_port))
        return True, None
    except socket.timeout as e:
        return False, e


def _display_not_connected_text(window):
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
    return psychopy.event.waitKeys(keyList=['r', 'q', 'd'])[0]


# A factory function disguised as a class
def PyPlugger(window, config_file, tcp_ip="100.1.1.3",
              tcp_port=6700, parallel_port_address=53328, text_color=None):
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
    def __init__(self, window, config_file, tcp_ip="100.1.1.3",
                 tcp_port=6700, parallel_port_address=53328, text_color=None):
        self.window = window
        self.config_file = config_file
        self.tcp_ip = tcp_ip
        self.tcp_port = tcp_port
        self.current_mode = None
        self.socket = None

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
        self.socket.send(mode.encode())
        self.current_mode = mode
        time.sleep(delay)

    def start_recording(self, delay=5):
        self.socket.send("S".encode())
        time.sleep(delay)  # Ensure recording has started

    def stop_recording(self, delay=5, exit_mode=False):
        if exit_mode:
            cmd = 'X'
        else:
            cmd = 'Q'

        self.socket.send(cmd.encode())
        time.sleep(delay)  # Ensure recording has ended

    @staticmethod
    def start_event(event):
        psychopy.parallel.setData(event)

    @staticmethod
    def end_event():
        """To be called some time after an event has been sent"""
        psychopy.parallel.setData(0)

    def display_eeg_instructions(self, eeg_instruction_text=None):
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

        if self.current_mode != 'M':
            self.switch_mode('M')

        self.window.flip()


# Creates a mock object to be used if tracker doesn't connect for debug purposes
method_list = [fn_name for fn_name in dir(ConnectedPyPlugger)
               if callable(getattr(ConnectedPyPlugger, fn_name)) and not fn_name.startswith("__")]


def mock_func(*args, **kwargs):
    pass


class MockPyPlugger:
    def __init__(self, window, config_file, tcp_ip="100.1.1.3",
                 tcp_port=6700, parallel_port_address=53328, text_color=None):
        self.window = window
        self.config_file = config_file
        self.tcp_ip = tcp_ip
        self.tcp_port = tcp_port
        self.current_mode = None
        self.socket = None

        if text_color is None:
            if all(i >= 0.5 for i in self.window.color):
                self.text_color = (-1, -1, -1)
            else:
                self.text_color = (1, 1, 1)
        else:
            self.text_color = text_color

        for fn_name in method_list:
            setattr(self, fn_name, mock_func)
