#!/usr/bin/env python

import os
import time

def process_text(values):
    ''' Take in a tuple of the confidence and result and do the appropriate 
        action '''

    confidence, text = values
    print 'Result: \'' + text + '\' with confidence', confidence

    # Open a process 
    if text.startswith('open'):
        t = text[5:]
        # Firefox
        if t == 'firefox':
            os.system('nightly')
        # Chrome
        elif t == 'chrome':
            os.system('google-chrome 2>/dev/null')
        elif t == 'chromium':
            os.system('chromium-browser')
        # Gnome-Terminal
        elif t == 'terminal':
            os.system('gnome-terminal')
        # Vim
        elif t == 'text':
            os.system('gnome-terminal -e \'vim\'')
        # Unsuccessful; display result
        else:
            time.sleep(2)
    # Compute a product or sum
    elif text.startswith('calculate '):
        os.system('echo \"' + text[10:] + '\" | bc')
        time.sleep(4)
    # Lock the screen
    elif text == 'lock screen':
        os.system('gnome-screensaver-command -l')
    # Unsuccessful; display result
    else:
        time.sleep(2)
