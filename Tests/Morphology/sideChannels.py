from mlagents_envs.environment import UnityEnvironment
from mlagents_envs.side_channel.side_channel import (
    SideChannel,
    IncomingMessage,
    OutgoingMessage,
)
import time
import numpy as np
import uuid
from transform import positions, positionsToString

# Create the StringLogChannel class
class StringLogSideChannel(SideChannel):

    def __init__(self,id) -> None:
        super().__init__(uuid.UUID(id))

    def on_message_received(self, msg: IncomingMessage) -> None:
        """
        Note: We must implement this method of the SideChannel interface to
        receive messages from Unity
        """
        # We simply read a string from the message and print it.
        print(msg.read_string())

    def send_string(self, data: str) -> None:
        # Add the string to an OutgoingMessage
        msg = OutgoingMessage()
        msg.write_string(data)
        # We call this method to queue the data we want to send
        super().queue_message_to_send(msg)



legLengths=[1]*8
# range: [0.5 -3]
legLengths[0]=0.3883577355250894
legLengths[1]=1.2005288490743773 
legLengths[2]=0.5310972660331725
legLengths[3]=1.2786477345512561
#
legLengths[4]=legLengths[0] #leg1Upper
legLengths[5]=legLengths[1] #leg1Lower 
legLengths[6]=legLengths[2] #leg2Upper
legLengths[7]=legLengths[3] #leg2Lower

legs = positions(legLengths)
legsString = positionsToString(legs)

#print(legsString)

# Create the channel
string_log = StringLogSideChannel("621f0a70-4f87-11ea-a6bf-784f4387d1f7")
string_log_config = StringLogSideChannel("621f0a70-4f87-11ea-a6bf-784f4387d1f6")

BUILD_PATH = "C:\\Users\\stein\\Documents\\Unity\\builds\\windows\\Crawler"
# We start the communication with the Unity Editor and pass the string_log side channel as input
#env = UnityEnvironment(file_name=BUILD_PATH, side_channels=[string_log], no_graphics=False)
env = UnityEnvironment(side_channels=[string_log, string_log_config])
env.reset() 
#for i in range(100):
#    env.step()
#    print(i)
#env.reset() 
#for i in range(100):
#    env.step()
#    print(i)


# send string så reset for å bruke denne kroppen. Bare reset vil kjøre originalkroppen
string_log.send_string(
    legsString
    #"0,0,-1.0,-1.0,0,0,0,0,1.0,1.0,0,0,0.3,0.5,0.3,0.3,0.5,0.3,0.3,0.5,0.3,0.3,0.5,0.3,0,0,-2.0,-2.0,0,0,0,0,2.0,2.0,0,0,0.3,0.5,0.3,0.3,0.5,0.3,0.3,0.5,0.3,0.3,0.5,0.3"
    )
string_log_config.send_string("-9.81")
env.reset()# string_log.send_string("The environment was reset")

group_name = list(env.behavior_specs.keys())[0]  # Get the first group_name
group_spec = env.behavior_specs[group_name]

for i in range(100000):
    decision_steps, terminal_steps = env.get_steps(group_name)
    print(i)
    # We send data to Unity : A string with the number of Agent at each
    #string_log.send_string("0.0,0.0,-1.0,-1.0,0.0,0.0,0.0,0.0,1.0,1.0,0.0,0.0,0.3,0.5,0.3,0.3,0.5,0.3,0.3,0.5,0.3,0.3,0.5,0.3,0.0,0.0,-2.5,-2.5,0.0,0.0,0.0,0.0,2.5,2.5,0.0,0.0,0.3,1.0,0.3,0.3,1.0,0.3,0.3,1.0,0.3,0.3,1.0,0.3")
        #f"Step {i} occurred with {len(decision_steps)} deciding agents and "
        #f"{len(terminal_steps)} terminal agents"
    env.step()  # Move the simulation forward

env.close()