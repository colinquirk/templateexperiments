import time

from psychopy import core
from psychopy import monitors
from psychopy import visual

import eyelinker


monitor = monitors.Monitor('test_monitor', width=53, distance=70)
monitor.setSizePix([1920, 1080])

win = visual.Window([800, 600], units="pix", color=[0, 0, 0], monitor=monitor)

# Will default to MockEyeLinker if no tracker connected
tracker = eyelinker.EyeLinker(win, 'test.edf', 'BOTH')

# initialize
tracker.initialize_graphics()
tracker.open_edf()
tracker.initialize_tracker()
tracker.send_calibration_settings()
print('Initalization tests passed...')
time.sleep(1)

# most basic functionality
tracker.display_eyetracking_instructions()
tracker.setup_tracker()  # forced setup
tracker.calibrate()  # choice given
tracker.send_status('Recording...')
tracker.send_message('TRIALID 1')
tracker.start_recording()
time.sleep(2)
tracker.stop_recording()
print('Basic functionality tests passed...')
time.sleep(1)


# decorator test
@tracker.record
def my_trial():
    time.sleep(2)


my_trial()
print('Decorator test passed.')
time.sleep(1)

# real time data
left_eye_gaze, right_eye_gaze = tracker.gaze_data
print(left_eye_gaze)
print(right_eye_gaze)

left_eye_pupil, right_eye_pupil = tracker.pupil_size
print(left_eye_pupil)
print(right_eye_pupil)
print('Real time tests passed...')
time.sleep(1)

# continuous real time data
real_time_data = []
tracker.start_recording()

print('Continuous data start time:')
start_time = core.getTime()
print(start_time)

while core.getTime() < start_time + 1:  # seconds
    real_time_data.append(tracker.gaze_data)
    core.wait(0.01)  # Get a sample every 10 ms

print('Continuous data end time:')
print(core.getTime())

tracker.stop_recording()

print('Number of samples:')
print(len(real_time_data))

print('Continuous data head:')
print(real_time_data[:10])

# test drift correct
tracker.drift_correct()
print('Drift correct tests passed...')
time.sleep(1)

# clean up
tracker.close_edf()
tracker.transfer_edf()
tracker.close_connection()
print('\nClean up tests passed...')

time.sleep(1)
print('All tests passed.')
