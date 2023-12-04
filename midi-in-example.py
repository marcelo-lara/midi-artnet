#!/usr/bin/env python
#
# midiin_poll.py
#
"""Show how to receive MIDI input by polling an input port."""

# from __future__ import print_function

import logging
import sys
import time

from rtmidi.midiutil import open_midiinput


# log = logging.getLogger('midiin_poll')
# logging.basicConfig(level=logging.DEBUG)

# Prompts user for MIDI input port, unless a valid port number or name
# is given as the first argument on the command line.
# API backend defaults to ALSA on Linux.
port = sys.argv[1] if len(sys.argv) > 1 else None

try:
    midiin, port_name = open_midiinput(port)
except (EOFError, KeyboardInterrupt):
    sys.exit()

print("Entering main loop. Press Control-C to exit.")
try:
    timer = time.time()
    while True:
        msg = midiin.get_message()

        if msg:
            message, deltatime = msg
            timer += deltatime
            if message[0] == 144:
                print("k: %r" % message[1] + " v: %r" % message[2])

        time.sleep(0.001)
except KeyboardInterrupt:
    print('')
finally:
    print("Exit.")
    midiin.close_port()
    del midiin