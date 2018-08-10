import time

from psychopy import visual

import eyelinker


win = visual.Window([1920, 1080], units="pix", fullscr=True, color=[0, 0, 0])

tracker = eyelinker.EyeLinker(win, 'filename', (1920,1080))

tracker.initialize_graphics()

tracker.calibrate()

tracker.start_recording()

time.sleep(2)

tracker.stop_recording()