import time

from psychopy import visual

import eyelinker


win = visual.Window([1920, 1080], units="pix", fullscr=True, color=[0, 0, 0])
tracker = eyelinker.EyeLinker(win, 'test.edf', (1920, 1080))

# initialize
tracker.initialize_graphics()
tracker.open_edf()
tracker.initialize_tracker()
tracker.send_calibration_settings()
print 'Initalization tests passed...'
time.sleep(1)

# most basic functionality
tracker.calibrate()
tracker.start_recording()
time.sleep(2)
tracker.stop_recording()
print 'Basic functionality tests passed...'
time.sleep(1)

# test drift correct
tracker.drift_correct()
print 'Drift correct tests passed...'
time.sleep(1)

# clean up
tracker.close_edf()
tracker.transfer_edf()
time.sleep(2)
tracker.close_connection()
print '\nClean up tests passed...'

time.sleep(1)
print 'All tests passed.'