"""Contains all basic experiment classes."""

from __future__ import division

import os
import pickle
import time

import psychopy.gui
import psychopy.monitors
import psychopy.visual


class BaseExperiment(object):
    """This is the BaseExperiment class
    Parameters:
    experiment_name -- A string for the experiment title that also defines
        the filename the experiment info from the dialog box is saved to.
    data_fields -- list of strings containing the data fields to be stored
    bg_color -- A list of 3 values between 0 and 255 defining the
        background color.
    monitor_name -- The name of the monitor to be used
        Psychpy will search for the provided name to see if it was defined
        in monitor center. If it is not defined, a temporary monitor will
        be created.
    monitor_width -- An int describing the length of the display monitor
        in cm (default 53).
    monitor_distance -- An int describing the distance the participant sits
        from the monitor in cm (default 70).
    """
    def __init__(self, experiment_name, data_fields, bg_color=[128, 128, 128],
                 monitor_name="Experiment Monitor", monitor_width=53,
                 monitor_distance=70):
        """Creates a new BaseExperiment object.

        Parameters:
        experiment_name -- A string for the experiment title that also defines
            the filename the experiment info from the dialog box is saved to.
        data_fields -- list of strings containing the data fields to be stored
        bg_color -- A list of 3 values between 0 and 255 defining the
            background color.
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
        self.experiment_data_filename = None
        self.data_lines_written = 0
        self.experiment_info = {}
        self.experiment_window = None

        self.experiment_monitor = psychopy.monitors.Monitor(
            self.monitor_name, width=self.monitor_width,
            distance=self.monitor_distance)

    @staticmethod
    def __confirm_overwrite():
        """Private, static method that shows a dialog asking if a file can be
        overwritten.

        Returns a bool describing if the file should be overwritten.
        """

        overwrite_dlg = psychopy.gui.Dlg(
            'Overwrite?', labelButtonOK='Overwrite',
            labelButtonCancel='New File')
        overwrite_dlg.addText('File already exists. Overwrite?')
        overwrite_dlg.show()

        return overwrite_dlg.OK

    @staticmethod
    def convert_color_value(color):
        """Converts a list of 3 values from 0 to 255 to -1 to 1.

        Parameters:
        color -- A list of 3 ints between 0 and 255 to be converted.
        """

        new_color = []

        for value in color:
            new_value = (value/127.5)-1
            new_value = round(new_value, 2)
            new_color.append(new_value)

        return new_color

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

    def save_experiment_info(self):
        """Writes the info from the dialog box to a text file.
        """
        filename = (self.experiment_name + '_' +
                    self.experiment_info['Subject Number'].zfill(3) +
                    '_info.txt')

        with open(filename, 'a') as info_file:
            for key, value in self.experiment_info.iteritems():
                info_file.write(key + ':' + value + '\n')
            info_file.write('\n')

    def open_csv_data_file(self, data_filename=None):
        """Opens the csv file and writes the header.

        Parameters:
        data_filename -- name of the csv file with no extension
            (defaults to experimentname_subjectnumber).
        """

        if data_filename is None:
            data_filename = (self.experiment_name + '_' +
                             self.experiment_info['Subject Number'].zfill(3))
        elif data_filename[-4:] == '.csv':
            data_filename = data_filename[:-4]

        if os.path.isfile(data_filename + '.csv'):
            if not self.__confirm_overwrite():
                # If the file exists and we can't overwrite make a new filename
                i = 1
                new_filename = data_filename + '(' + str(i) + ')'
                while os.path.isfile(new_filename + '.csv'):
                    i += 1
                    new_filename = data_filename + '(' + str(i) + ')'
                data_filename = new_filename

        self.experiment_data_filename = data_filename + '.csv'

        # Write the header
        with open(self.experiment_data_filename, 'w+') as data_file:
            for field in self.data_fields:
                data_file.write(field)
                if field != self.data_fields[-1]:
                    data_file.write(',')
            data_file.write('\n')

    def update_experiment_data(self, new_data):
        """Extends any new data to the experiment_data list.

        Parameters:
        new_data -- A list of dictionaries that are extended to
            experiment_data. Only keys that are included in data_fields should
            be included, as only those will be written in save_data_to_csv()
        """

        self.experiment_data.extend(new_data)

    def save_data_to_csv(self):
        """Opens the data file and appends new entries in experiment_data.

        Only appends lines (tracked by data_lines_written) that have not yet
        been written to the csv.

        Update the experiment data to be written with update_experiment_data.
        """
        with open(self.experiment_data_filename, 'a') as data_file:
            for trial in range(
                    self.data_lines_written, len(self.experiment_data)):
                for field in self.data_fields:
                    try:
                        data_file.write(
                            str(self.experiment_data[trial][field]))
                    except KeyError:
                        data_file.write('NA')
                    if field != self.data_fields[-1]:
                        data_file.write(',')
                data_file.write('\n')

        self.data_lines_written = len(self.experiment_data)

    def save_experiment_pickle(self, additional_fields_dict=None):
        """Saves the pickle containing the experiment data so that a crash can
        be recovered from.

        This method uses dict.update() so if any keys in the
        additional_fields_dict are in the default dictionary the new values
        will be used.

        Parameters:
        additional_fields_dict -- An optional dictionary that updates the
            dictionary that is saved in the pickle file.
        """

        pickle_dict = {
            'experiment_name': self.experiment_name,
            'data_fields': self.data_fields,
            'bg_color': self.bg_color,
            'monitor_name': self.monitor_name,
            'monitor_width': self.monitor_width,
            'monitor_distance': self.monitor_distance,
            'experiment_data': self.experiment_data,
            'experiment_data_filename': self.experiment_data_filename,
            'data_lines_written': self.data_lines_written,
            'experiment_info': self.experiment_info,
        }

        if additional_fields_dict is not None:
            pickle_dict.update()

        pickle.dump(pickle_dict, open(
            self.experiment_name + '_' +
            self.experiment_info['Subject Number'].zfill(3) + '.pickle',
            'wb+'))

    def open_window(self):
        """Opens the psychopy window."""

        self.experiment_window = psychopy.visual.Window(
            monitor=self.experiment_monitor, fullscr=True, color=self.bg_color,
            colorSpace='rgb', allowGUI=False, winType='pyglet', units='deg',
            screen=0)

    def display_text_screen(
            self, text="", text_color=[0, 0, 0], text_height=36,
            bg_color=None, wait_for_input=True):
        """Takes a string as input and draws it centered on the screen.

        Allows for simple writing of text to a screen with a background color
        other than the normal one. Switches back to the default background
        color after any keyboard input.

        This works by drawing a rect on top of the background
        that fills the whole screen with the selected color.

        Parameters:
        text -- A string containing the text to be displayed.
        text_color -- A list of 3 values between 0 and 255
            (default is [0, 0, 0]).
        text_height --- An int that defines the height of the text in pix.
        bg_color -- A list of 3 values between 0 and 255 (default is default
            background color).
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
            time.sleep(.2)  # Prevents accidental key presses
            psychopy.event.waitKeys()

    def quit_experiment(self):
        """Completes anything that must occur when the experiment ends."""
        self.experiment_window.close()


class EEGExperiment(BaseExperiment):
    """This is an EEG experiment."""
    def __init__(self):
        pass


class EyeTrackingExperiment(BaseExperiment):
    """This is an eye tracking experiment."""
    def __init__(self):
        pass


class EEGandEyeTrackingExperiment(EEGExperiment, EyeTrackingExperiment):
    """This is just inherits from EEGExperiment and EyeTrackingExperiment,
    for convinence.
    """
    pass
