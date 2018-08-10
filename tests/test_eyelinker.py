from __future__ import print_function

import time

from psychopy import visual

import eyelinker


win = visual.Window([1920, 1080], units="pix", fullscr=True, color=[0, 0, 0])
tracker = eyelinker.EyeLinker(win, 'test.edf', 'BOTH')

# initialize
tracker.initialize_graphics()
tracker.open_edf()
tracker.initialize_tracker()
tracker.send_calibration_settings()
print('Initalization tests passed...')
time.sleep(1)

# most basic functionality
tracker.calibrate()
tracker.start_recording()
time.sleep(2)
tracker.stop_recording()
print('Basic functionality tests passed...')
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

# test drift correct
tracker.drift_correct()
print('Drift correct tests passed...')
time.sleep(1)

# clean up
tracker.close_edf()
tracker.transfer_edf()
time.sleep(2)
tracker.close_connection()
print('\nClean up tests passed...')

time.sleep(1)
print('All tests passed.')