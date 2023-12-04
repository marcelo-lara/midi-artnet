import time
import rtmidi

midi_in = rtmidi.MidiIn()
available_ports = midi_in.get_ports()

print(available_ports)
if available_ports:
    midi_in.open_port(0)
else:
    midi_in.open_virtual_port("My virtual output")

# with midi_in:
#     # channel 1, middle C, velocity 112
#     note_on = [0x90, 60, 112]
#     note_off = [0x80, 60, 0]
#     midi_in.send_message(note_on)
#     time.sleep(0.5)
#     midi_in.send_message(note_off)
#     time.sleep(0.1)

# del midi_in