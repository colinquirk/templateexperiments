"""Contains all basic experiment classes"""

import psychopy.gui
import psychopy.monitors
import psychopy.visual


class BaseExperiment(object):
    """This is the BaseExperiment class"""
    def __init__(self, experiment_name, data_fields,
                 monitor_name="Experiment Monitor", monitor_width=53,
                 monitor_distance=70,):
        """Creates a new BaseExperiment object.

        Parameters:
        data_fields -- list of strings containing the data fields to be stored
        experiment_name -- A title for the experiment that also defines the
            filename the experiment info from the dialog box is saved to
        monitor_width -- The length of the display monitor in cm
        monitor_distance -- The distance the participant sits
            from the monitor in cm
        """
        self.experiment_data = []
        self.experiment_window = None  # Set in open_window()

        self.experiment_name = experiment_name
        self.data_fields = data_fields
        self.monitor_name = monitor_name
        self.monitor_width = monitor_width

        self.experiment_monitor = psychopy.monitors.Monitor(
            self.monitor_name, width=monitor_width, distance=monitor_distance
        )

    def display_instructions(self, instruction_text=""):
        """Takes a string with instructions as input and prints them to the screen.

        Parameters:
        instruction_text -- A string containing the text to be displayed.
        """
        pass

    def display_loading_screen(self):
        pass

    def get_experiment_info_from_dialog(self, additional_fields_dict=None):
        """Gets subject info from dialog box.

        Parameters:
        additional_fields_dict -- An optional dictionary containing more
            fields for the dialog box and output dictionary
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
            experiment_info, title=self.experiment_name,
            order=['Subject Number',
                   'Age',
                   'Experimenter Initials',
                   'Unique Subject Identifier',
                   'Pickle File',
                   ],
            tip={'Unique Subject Identifier': 'From the cronus log',
                 'Pickle File': 'Load if restarting from a crash',
                 }
        )

        return experiment_info

    def __open_csv_data_file(self):
        pass

    def open_window(self):
        """Opens the psychopy window."""
        self.experiment_window = psychopy.visual.Window(
            monitor=self.experiment_monitor, fullscr=True, allowGUI=False,
            winType='pyglet', units='deg', screen=0)  # check screen=0 is correct
                                                      # check if waitBlanking is important

    def save_data_to_csv(self):
        pass

    def save_experiment_info(self):
        pass

    def save_experiment_pickle(self):
        pass

    def update_experiment_data(self, new_data):
        """Attaches any new data to the experiment_data list.

        Parameters:
        new_data -- A list of dictionaries that are extended to experiment_data
            Only keys that are included in data_fields are extended
        """
        pass
