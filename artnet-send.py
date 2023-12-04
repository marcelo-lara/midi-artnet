from stupidArtnet import StupidArtnet
import time
import random

# THESE ARE MOST LIKELY THE VALUES YOU WILL BE NEEDING
target_ip = '255.255.255.255'		# typically in 2.x or 10.x range
universe = 0 										# see docs
packet_size = 64								# it is not necessary to send whole universe

a = StupidArtnet(target_ip, universe, packet_size, 60, True, True)

# MORE ADVANCED CAN BE SET WITH SETTERS IF NEEDED
# NET         = DEFAULT 0
# SUBNET      = DEFAULT 0

# CHECK INIT
print(a)

# ALL PACKETS ARE SAVED IN THE CLASS, YOU CAN CHANGE SINGLE VALUES
a.set_single_value(16, 255)			# set channel 1 to 255
a.set_single_value(17, 255)			# set channel 1 to 255
a.set_single_value(18, 255)			# set channel 1 to 255
a.set_single_value(19, 255)			# set channel 1 to 255

# ... AND SEND
a.show()							# send data
print("show")

time.sleep(10)						# wait a bit, 1 sec

a.blackout()						# send single packet with all channels at 0
a.see_buffer()

# ALL THE ABOVE EXAMPLES SEND A SINGLE DATAPACKET
# STUPIDARTNET IS ALSO THREADABLE
# TO SEND PERSISTANT SIGNAL YOU CAN START THE THREAD
a.start()							# start continuos sendin
print("after start")
time.sleep(10)						# wait a bit, 1 sec

a.blackout()

# ... REMEMBER TO CLOSE THE THREAD ONCE YOU ARE DONE
a.stop()

# CLEANUP IN THE END
del a