import time

from psychopy import monitors
from psychopy import visual

import pyplugger

# Necessary psychopy setup
monitor = monitors.Monitor('test_monitor', width=53, distance=70)
monitor.setSizePix([1920, 1080])

win = visual.Window([800, 600], units="pix", color=[0, 0, 0], monitor=monitor)

visual.TextStim(win, 'Beginning PyPlugger test...').draw()
win.flip()

# Initialization
eeg = pyplugger.PyPlugger(win, config_file='C:\\Users\\AwhVogel\\Desktop\\Colin\\default.xml')

eeg.initialize_session('test_exp', 0)
print('Initalization tests passed...')

eeg.display_eeg_instructions()
eeg.display_interactive_switch_screen()  # End in monitoring mode

eeg.start_recording()
for i in range(5):
    eeg.draw_photodiode_stimuli()
    win.flip()
    eeg.start_event(i)
    time.sleep(0.5)
    eeg.end_event()
    win.flip()
    time.sleep(0.5)

print('Basic functionality tests passed...')

eeg.display_interactive_switch_screen()  # End in monitoring mode

# Minimum delay testing
for i in range(5):
    eeg.start_event(i)
    time.sleep(0.05)
    eeg.end_event()
    time.sleep(0.05)
eeg.stop_recording(exit_mode=True)

print('Tests complete.')
time.sleep(5)
