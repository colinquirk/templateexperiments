This is a collection of modules I use to help me write experiments. Please look in the folder for readmes the specifics of using each module. A brief description of each is below:

template/template.py -- This module provides a class that all of my experiments inherit from. You will need it to run any of my experiment code.

eyelinker/eyelinker.py -- This is a wrapper for pylink (from SR research) that makes it easy to control basic eyetracking experiments using eyelink trackers.

eyelinker/PsychoPyCustomDisplay.py -- This is a module that connects psychopy and pylink so that eyelink can show graphics, play sounds, etc. If you use eyelinker, have it avaliable on the path and you will never need to use it directly.