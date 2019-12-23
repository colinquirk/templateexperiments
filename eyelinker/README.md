A module for managing the interaction between pylink and psychopy.

PsychoPyCustomDisplay -- inherited from pylink.EyeLinkCustomDisplay.

Defines how pylink events should be handled by psychopy.

This class is designed to be used by the eyelinker module. If you use it, you won't need
to call any of these functions or change any of this code. If you prefer not to use eyelinker,
simply use `pl.openGraphicsEx(PsychoPyCustomDisplay)` to connect pylink to psychopy. These 
functions are then called by interactions with the tracker.

For more information, see the pylink documentation for custom displays. These docs
are available on the SR Research forum.

EyeLinker -- If able to connect, returns a ConnectedEyeLinker

See eyelink_example.py for a tutorial and the source code for details about optional arguments.

Basic Usage:

Eyelinker requires a psychopy.visual.Window object, as well as an EDF filename (max 12 char with extenstion) and which eyes to track ("LEFT", "RIGHT", or "BOTH"). Some setup is required, which is handled by calling `initialize_graphics`, `open_edf`, `initialize_tracker`, and `send_tracking_settings`. These functions will work with no additional arguments, but you may want to change the default settings used in `send_tracking_settings`. At the beginning of the experiment, you may also want to use `display_eyetracking_instructions` to describe to the participant what to do when they see a target.

There are two ways to enter setup mode, `setup_tracker` or `calibrate`. `setup_tracker` is forced and is designed to be used once at the beginning of the experiment, whereas `calibrate` will give an option to the experimenter and is designed to be used at breaks. While in setup mode, the psychopy screen will be blank at first, but the eyelink hotkeys will be available. Some to note are enter to bring up the camera image, left and right arrow to move across images, c to calibrate, v to valiadate, and ESC to leave setup mode. Note that you can also click directly on the camera image in order to mark eye positions.

During the experiment, you can record by either directly calling the `start_recording` and `stop_recording` functions, or by decorating a function that you want to record with the `record` decorator. You may also want to use the `send_status` function for showing information to the experimenter, or the `send_message` function for sending markers to the EDF file (good for marking times of trial starts, etc). If you want regular adjustments to be made, `drift_correct` is faster than fully calibrating.

A few properties are also available if you are doing real-time work. `gaze_data` holds a tuple of (x,y) coordinates from the latest sample. If you are recording both eyes, you will get a tuple of tuples. Likewise, `pupil_size` contains the size of each pupil in a tuple if you are recording both eyes, otherwise a single value is returned.

At the end of the experiment, you must close the edf file with `close_edf`. Optionally, you may then transfer the file to the presentation computer with `transfer_edf`. Finally, you can close the connection with `close_connection`.
