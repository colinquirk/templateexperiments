Basic experiment class that is designed to be extended.

Author - Colin Quirk (cquirk@uchicago.edu)

Repo: https://github.com/colinquirk/templateexperiments

This class provides basic utility functions that are needed by all
experiments. Specific experiment classes should inherit and extend/overwrite as needed.

Note for other experimenters -- My experiments all inherit from this class,
so changes in these functions may result in unexpected changes elsewhere. If
possible, changes to experiments should be made in the specific experiment
class by overwriting template experiment methods. Ideally, the only changes
that should be made to these classes are those that would need to be made for
every experiment of mine (e.g. to correct for system differences). Even those
types of changes may have unintended consequences so please be careful! If you
need help using this module, have requests or improvements, or found this code
useful please let me know through email or GitHub.

### Functions
* convert_color_value -- Converts a list of 3 values from 0 to 255 to -1 to 1.

### Classes
* BaseExperiment -- All experiments inherit from BaseExperiment. Provides basic
    functionality needed by all experiments.

### Parameters
* bg_color -- list of 3 values (0-255) defining the background color
* data_fields -- list of strings defining data fields
* experiment_name -- string defining the experiment title
* monitor_distance -- int describing participant distance from monitor in cm
* monitor_name -- name of the monitor to be used
* monitor_px -- list containing monitor resolution (x,y)
* monitor_width -- int describing length of display monitor in cm

### Methods
* display_text_screen -- draws a string centered on the screen.
* get_experiment_info_from_dialog -- gets subject info from a dialog box.
* open_csv_data_file -- opens a csv data file and writes the header.
* open_window -- open a psychopy window.
* quit_experiment -- ends the experiment.
* save_data_to_csv -- append new entries in experiment_data to csv data file.
* save_experiment_info -- write the info from the dialog box to a text file.
* save_experiment_pickle -- save a pickle so crashes can be recovered from.
* update_experiment_data -- extends any new data to the experiment_data list.