A module for managing the interaction between pylink and psychopy.

Author - Colin Quirk (cquirk@uchicago.edu)

Repo: https://github.com/colinquirk/templateexperiments

This class is designed to be used by the eyelinker module. If you use it, you won't need
to call any of these functions or change any of this code. If you prefer not to use eyelinker,
simply use `pl.openGraphicsEx(PsychoPyCustomDisplay)` to connect pylink to psychopy. These
 functions are then called by interactions with the tracker.

Classes:
PsychoPyCustomDisplay -- inherited from pylink.EyeLinkCustomDisplay. Defines how pylink events
 should be handled by psychopy.

For more information, see the pylink documentation for custom displays. These docs
are available on the SR Research forum.

Parameters:
window -- A psychopy.visual.Window object
tracker -- A pylink.EyeLink object

Methods:
setup_cal_display -- Clears window on calibration setup.
exit_cal_display -- Clears window on calibration exit.
record_abort_hide -- Not implimented.
setup_image_display -- Shows mouse when camera images are visible.
image_title -- Updates title text.
draw_image_line -- Draws image from buffer.
set_image_palette -- Defines image colors.
exit_image_display -- Hides mouse when camera images are no longer visible.
clear_cal_display -- Clears calibration targets.
erase_cal_target -- Clears a individual calibration target.
draw_cal_target -- Draws calibration targets.
play_beep -- Provides audio feedback.
get_input_key -- Handles key events.
alert_printf -- Prints warnings, but doesn't kill session.
draw_line -- Draws crosshair lines.
draw_lozenge -- Draws ovals on image.
get_mouse_state -- Gets mouse position.
