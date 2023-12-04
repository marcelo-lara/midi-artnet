import mido

# open midi port
port = "loopMIDI Port 0"
midi_in = mido.open_input(port)
try:
    for msg in midi_in:
        if msg.is_cc:
            if msg.type=="clock":
                continue
            print("ctrl:" + msg.type)
        if msg.type == 'note_on':
            print(msg)
except KeyboardInterrupt:
    print('')
finally:
    print("Exit.")