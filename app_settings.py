MIDI_LOOPBACK = "Lo opBe"

import sys
import mido

def getLoopbackInterface(exit_if_not_found:bool=True) -> tuple[bool,str]:
    for port in mido.get_input_names():
        if str(port).startswith(MIDI_LOOPBACK):
            return True, port

    if exit_if_not_found: 
        print(f'[{MIDI_LOOPBACK}] port not found')
        print('available ports:')
        for port in mido.get_input_names():
            print("- ", port)
        sys.exit()

    return False, MIDI_LOOPBACK