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

# most basic functionality
tracker.calibrate()
tracker.start_recording()
time.sleep(2)
tracker.stop_recording()

# test drawing
tracker.clear_screen()
tracker.draw_text(text='Hello World!')
time.sleep(2)
tracker.clear_screen()

# test drift correct
tracker.drift_correct()

# clean up
tracker.close_edf()
tracker.transfer_edf()
tracker.close_connection()

time.sleep(1)
