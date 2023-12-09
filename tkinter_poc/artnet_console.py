"""(Very) Simple Example of using Tkinter with StupidArtnet.

It creates a simple window with a slider of value 0-255
This value is streamed in universe 0 channel 1

Note: The example imports stupid artnet locally from
a parent folder, real use import would be simpler

"""
import time

from tkinter import *

from stupidArtnet import StupidArtnet

# Declare globals
artnet = None
window = None

_timer = None

from threading import Timer

def updateValue(slider_value):
    """Callback from slider onchange.
    Sends the value of the slider to the artnet channel.
    """
    global artnet
    print("updateValue: ", slider_value)
    artnet.set_single_value(17, int(slider_value))


def cleanup():
    """Cleanup function for when window is closed.
    Closes socket and destroys object.
    """
    print('cleanup')

    global artnet
    artnet.stop()
    del artnet

    global window
    window.destroy()


def _fade_handler(ch:int, value:int, interval_ms:int):
    #curr_value = 255 artnet.buffer[channel-1]
    global _timer
    global artnet
    if value < 0:
        _timer.cancel()
        return

    print("ch:",ch,"fade_handler:", value)

    #send value
    artnet.set_single_value(ch, value)
    
    _timer = Timer((interval_ms/1000), _fade_handler, args=[ch, value-1, interval_ms])
    _timer.daemon = True
    _timer.start()
            

def buttonCallback():
    """Callback for button press.
    Sends a random value to the artnet channel.
    """
    global artnet
    _fade_handler(18, 255, 10)


# ARTNET CODE
# -------------

# Create artnet object
target_ip = '255.255.255.255' # typically in 2.x or 10.x range
universe = 0 				  # see docs
packet_size = 64			  # it is not necessary to send whole universe
artnet = StupidArtnet(target_ip, universe, packet_size, 50, True, True)

# Start persistent thread
artnet.start()
artnet.set_single_value(16, 255)
artnet.show()


# TKINTER CODE
# --------------

# Create window object
window = Tk()

# Hold value of the slider
slider_val = IntVar()

# Create slider
scale = Scale(window, variable=slider_val, command=updateValue, from_=255, to=0)
scale.pack(anchor=CENTER)

# Create label with value
label = Label(window)
label.pack()


B = Button(window, text ="Hello", command = buttonCallback)
B.pack()

# Cleanup on exit
window.protocol("WM_DELETE_WINDOW", cleanup)



# Start
window.mainloop()