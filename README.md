NOTE
====

**This application is just for fun and should not be used in any way that violates Google's Terms of Services. Do NOT rely on this API for any "real" application if you know what's good for you.**

------------
Introduction
============

This is a simple speech-to-command program in Python that uses Google's Speech
Recognition facility to convert speech into text and then execute a command, if
appropriate, on the local machine.

Dependencies
============

This program depends on [alsaaudio](http://pyalsaaudio.sourceforge.net/pyalsaaudio.html) 
and is designed to run on Linux. 

Tested on Ubuntu 11.04 in Gnome-Terminal.

Execution
=========

Just run ```python main.py``` and speak for up to three seconds. The audio will
be then processed and translated and an action may be taken.

Examples
========

py-command can be used to launch processes:

    $ python main.py
    * recording
    [===        ]
    <say "open firefox">
    * done recording
    <Firefox opens>

Or to do some math:

    $ python main.py
    * recording
    [===        ]
    <say "calcuate three times four">
    * done recording
    12

Or to lock the screen:

    $ python main.py
    * recording
    [===        ]
    <say "lock screen">
    * done recording
    <Screen is locked>
