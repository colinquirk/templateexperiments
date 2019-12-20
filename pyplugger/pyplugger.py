import socket
import time

import psychopy.event
import psychopy.parallel
import psychopy.visual


class PyPlugger:
    def __init__(self, config_file='default.xml', tcp_ip="100.1.1.3",
                 tcp_port=6700, parallel_port_address=53328, text_color=None):
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
                    '2' + experiment_name,
                    '3' + subject_number,
                    '4']

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(timeout)
        self.socket.connect((self.tcp_ip, self.tcp_port))

        for tcp_message in messages:
            self.socket.send(tcp_message)
            time.sleep(1)

    def switch_mode(self, mode, delay=5):
        self.socket.send(mode)
        self.current_mode = mode
        time.sleep(delay)

    def start_recording(self, delay=5):
        self.socket.send("S")
        time.sleep(delay)  # Ensure recording has started

    def stop_recording(self, delay=5, exit_mode=False):
        if exit_mode:
            cmd = 'X'
        else:
            cmd = 'Q'

        self.socket.send(cmd)
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

    def display_interactive_switch_screen(self):
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
