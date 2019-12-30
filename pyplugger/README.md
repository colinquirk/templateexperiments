A module for managing the interaction between pycorder and psychopy.

Pyplugger provides functions to control EEG recordings through the BrainVision software pycorder.

Important notes:

-In order to use pylugger, a network connection between the computer running pycorder and the
 computer running psychopy.
-You cannot open pycorder normally, you must open it in remote mode for this
 module to work. See the pycorder documentation for notes about how to do this.
-In order to send events, you must have a parallel port set up. See the documentation about psychopy.parallel
for more information.

inpout32.dll -- place this file in the same directory as your experiment code as it is necessary for the parallel port.

PyPlugger -- If able to connect, returns a ConnectedPyPlugger

See pyplugger_example.py for a tutorial and the source code for details about optional arguments.

Basic Usage:
Pyplugger requires a psychopy.visual.Window, the path to an xml config file created by pycorder somewhere on the pycorder computer, the ip address (of the pycorder computer) and port to connect to, and the parallel_port_address in order to enable all functionality.

`initialize_session` should be called before any other functionality in order to initialize the tcp connection. At the beginning of the experiment, you may also want to use `display_eeg_instructions` to describe to the participant when they can and can't blink and move their eyes.

When setting up, you can use `display_interactive_switch_screen` to allow the experimenter to switch between modes on the psychopy computer. Behind the scenes, this is using `switch_mode`, which you can also call directly.

During the experiment and while in monitor mode, `start_recording` can be used to begin saving data, and `stop_recording` can be used to stop saving data. Unlike eyelinker, you will want to continuously record data for the entire experiment.

During trials, you can use `start_event` to send data to the parallel port and `end_event` to reset it to 0.

At the end of the experiment, simply use `stop_recording(exit_mode=True)`. No other shutdown is required.
