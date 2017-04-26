"""Contains all basic experiment classes"""

import psychopy.gui


class BaseExperiment(object):
    """This is the BaseExperiment class"""
    def __init__(self, data_fields):
        """Creates a new BaseExperiment object

        Parameters:
        data_fields -- list of strings containing the data fields to be stored
        """
        experiment_data = []
        self.data_fields = data_fields

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
        experiment_info = {'Subject Number': '0',
                           'Age': '0',
                           'Experimenter Initials': 'CQ',
                           'Unique Subject Identifier': '000000',
                           'Pickle File': '',
                           }

        if additional_fields_dict is not None:
            experiment_info.update(additional_fields_dict)

        # Modifies experiment_info dict directly
        psychopy.gui.DlgFromDict(
            experiment_info, title="Experiment Info",
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

    def open_csv_data_file(self):
        pass

    def open_window(self):
        """Opens the psychopy window."""
        pass

    def save_data_to_csv(self):
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

