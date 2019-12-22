A module for managing the interaction between pylink and psychopy.

PsychoPyCustomDisplay -- inherited from pylink.EyeLinkCustomDisplay.

Defines how pylink events should be handled by psychopy.

This class is designed to be used by the eyelinker module. If you use it, you won't need
to call any of these functions or change any of this code. If you prefer not to use eyelinker,
simply use `pl.openGraphicsEx(PsychoPyCustomDisplay)` to connect pylink to psychopy. These 
functions are then called by interactions with the tracker.

For more information, see the pylink documentation for custom displays. These docs
are available on the SR Research forum.
