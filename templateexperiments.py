"""Contains all basic experiment classes"""

import time
import pickle
import os

import psychopy.gui
import psychopy.monitors
import psychopy.visual


class BaseExperiment(object):
    """This is the BaseExperiment class"""
    def __init__(self, experiment_name, data_fields, bg_color=[128, 128, 128],
                 monitor_name="Experiment Monitor", monitor_width=53,
                 monitor_distance=70):
        """Creates a new BaseExperiment object.

        Parameters:
        bg_color -- A list of 3 values between 0 and 255 defining the
            background color.
        data_fields -- list of strings containing the data fields to be stored
        experiment_name -- A string for the experiment title that also defines
            the filename the experiment info from the dialog box is saved to.
        monitor_name -- The name of the monitor to be used
            Psychpy will search for the provided name to see if it was defined
            in monitor center. If it is not defined, a temporary monitor will
            be created.
        monitor_width -- An int describing the length of the display monitor
            in cm (default 53).
        monitor_distance -- An int describing the distance the participant sits
            from the monitor in cm (default 70).
        """

        self.experiment_name = experiment_name
        self.data_fields = data_fields
        self.bg_color = self.convert_color_value(bg_color)
        self.monitor_name = monitor_name
        self.monitor_width = monitor_width
        self.monitor_distance = monitor_distance

        self.experiment_data = []
        self.experiment_info = {}
        self.experiment_info_file = None
        self.experiment_window = None

        self.experiment_monitor = psychopy.monitors.Monitor(
            self.monitor_name, width=self.monitor_width,
            distance=self.monitor_distance)

    @staticmethod
    def convert_color_value(color):
        """Converts a list of 3 values from 0 to 255 to -1 to 1.

        Note that middle grey will be slightly off.

        Parameters:
        color -- A list of 3 ints between 0 and 255 to be converted.
        """

        new_color = []

        for value in color:
            new_value = ((float(value)/127.5))-1
            new_color.append(new_value)

        return new_color

    def display_text_screen(
            self, text="", text_color=[0, 0, 0], text_height=36,
            bg_color=None, wait_for_input=True):
        """Takes a string as input and draws it centered on the screen.

        Allows for simple writing of text to a screen with a background color
        other than the normal one. Switches back to the default background
        color after any keyboard input.

        This works by drawing a rect that fills the whole screen with the
        selected color.

        Parameters:
        bg_color -- A list of 3 values between 0 and 255 (default is default
            background color).
        text -- A string containing the text to be displayed.
        text_color -- A list of 3 values between 0 and 255
            (default is [0, 0, 0]).
        text_height --- An int that defines the height of the text in pix.
        wait_for_input -- Bool that defines whether the screen will wait for
            keyboard input before continuing.
        """
        if bg_color is None:
            bg_color = self.bg_color
        else:
            bg_color = self.convert_color_value(bg_color)

        backgroundRect = psychopy.visual.Rect(
            self.experiment_window, fillColor=bg_color, units="norm", width=2,
            height=2)

        text_color = self.convert_color_value(text_color)

        textObject = psychopy.visual.TextStim(
            self.experiment_window, text=text, color=text_color, units='pix',
            height=text_height, alignHoriz='center', alignVert='center')

        backgroundRect.draw()
        textObject.draw()
        self.experiment_window.flip()

        if wait_for_input:
            time.sleep(.5)
            psychopy.event.waitKeys()

    @staticmethod
    def __confirm_overwrite():
        overwrite_dlg = psychopy.gui.Dlg(
            'Overwrite?', labelButtonOK='Overwrite',
            labelButtonCancel='New File')
        overwrite_dlg.addText('File already exists. Overwrite?')
        overwrite_dlg.show()

        if overwrite_dlg.OK:
            return True
        else:
            return False

    def get_experiment_info_from_dialog(self, additional_fields_dict=None):
        """Gets subject info from dialog box.

        Parameters:
        additional_fields_dict -- An optional dictionary containing more
            fields for the dialog box and output dictionary.
        """
        self.experiment_info = {'Subject Number': '0',
                                'Age': '0',
                                'Experimenter Initials': 'CQ',
                                'Unique Subject Identifier': '000000',
                                'Pickle File': '',
                                }

        if additional_fields_dict is not None:
            self.experiment_info.update(additional_fields_dict)

        # Modifies experiment_info dict directly
        psychopy.gui.DlgFromDict(
            self.experiment_info, title=self.experiment_name,
            order=['Subject Number',
                   'Age',
                   'Experimenter Initials',
                   'Unique Subject Identifier',
                   'Pickle File',
                   ],
            tip={'Unique Subject Identifier': 'From the cronus log',
                 'Pickle File': 'Load if restarting from a crash',
                 },
            screen=0
        )

    def open_csv_data_file(self, data_filename=None):
        """Opens the csv file and writes the header.

        Parameters:
        data_filename -- name of the csv file with no extension
            (defaults to experimentname_subjectnumber).
        """

        if data_filename is None:
            data_filename = (self.experiment_name + '_' +
                             self.experiment_info['Subject Number'].zfill(3))

        if os.path.isfile(data_filename + '.csv'):
            if not self.__confirm_overwrite():
                i = 1
                new_filename = data_filename + '(' + str(i) + ')'
                while os.path.isfile(new_filename + '.csv'):
                    i += 1
                    new_filename = data_filename + '(' + str(i) + ')'
                data_filename = new_filename

        self.experiment_info_file = open(data_filename + '.csv', 'w+')

    def open_window(self):
        """Opens the psychopy window."""

        self.experiment_window = psychopy.visual.Window(
            monitor=self.experiment_monitor, fullscr=True, color=self.bg_color,
            colorSpace='rgb', allowGUI=False, winType='pyglet', units='deg',
            screen=0)

    def quit_experiment(self):
        self.experiment_window.close()

    def save_data_to_csv(self):
        pass

    def save_experiment_info(self):
        filename = self.experiment_name + '_info.txt'
        with open(filename, 'a') as info_file:
            for key, value in self.experiment_info.iteritems():
                info_file.write(key + ':' + value + '\n')
            info_file.write('\n')

    def save_experiment_pickle(self):
        pass

    def update_experiment_data(self, new_data):
        """Attaches any new data to the experiment_data list.

        Parameters:
        new_data -- A list of dictionaries that are extended to
            experiment_data. Only keys that are included in data_fields are
            extended.
        """
        pass


# "tests"
MyExperiment = BaseExperiment('MyExperiment', [])
MyExperiment.get_experiment_info_from_dialog(additional_fields_dict={'t': ''})
MyExperiment.save_experiment_info()
MyExperiment.open_csv_data_file(data_filename="test_file")
MyExperiment.open_window()
time.sleep(.3)
MyExperiment.display_text_screen(
    text="Success!", bg_color=[220, 255, 220])
MyExperiment.quit_experiment()
