import sys
import time

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule
import argparse
import sys,time,globalVar
import naoChat,naoVision
from naoMotion import Motion
from tools import voice2txt

# Global variable to store the ReactToTouch module instance
reactToTouch = None
memory = None
count = 0
right = 0
left = 0
# State Machine
FACE_RECO_STATE = 0
CHAT_STATE = 1

currentState = FACE_RECO_STATE
motion = None


class ReactToTouch(ALModule):
    """ A simple module able to react
        to touch events.
    """
    def __init__(self, name):
        ALModule.__init__(self, name)
        # No need for IP and port here because
        # we have our Python broker connected to NAOqi broker
        head_touch = 0
        right_touch = 0
        left_touch = 0
        # Subscribe to TouchChanged event:
        global memory
        memory = ALProxy("ALMemory")
        memory.subscribeToEvent("MiddleTactilTouched","ReactToTouch","onheadTouched")
        # memory.subscribeToEvent("FrontTactilTouched",
        #                         "ReactToTouch",
        #                         "onheadTouched")
        # memory.subscribeToEvent("RearTactilTouched",
        #                         "ReactToTouch",
        #                         "onheadTouched")
        memory.subscribeToEvent("HandRightBackTouched","ReactToTouch","onrightTouched")
        #memory.subscribeToEvent("HandRightLeftTouched",
        #                         "ReactToTouch",
        #                         "onrightTouched")
        #memory.subscribeToEvent("HandRightRightTouched",
        #                         "ReactToTouch",
        #                         "onrightTouched")
        memory.subscribeToEvent("HandLeftBackTouched","ReactToTouch","onleftTouched")
        # memory.subscribeToEvent("HandLeftLeftTouched",
        #                         "ReactToTouch",
        #                         "onleftTouched")
        # memory.subscribeToEvent("HandLeftRightTouched",
        #                         "ReactToTouch",
        #                         "onleftTouched")

    def onheadTouched(self, strVarName, value):
        """ This will be called each time a touch
        is detected.
        """
        # Unsubscribe to the event when talking,
        # to avoid repetitions
        global count
        count = (count + 1)%2
        print count
        if(count == 0):
            memory.unsubscribeToEvent("MiddleTactilTouched","ReactToTouch")
        # head_touch = 1
            print ("head is touched")
            global currentState,motion
            if currentState == CHAT_STATE:
                naoChat.chat(motion)
            else:
                naoVision.faceRecongnition(motion)
        #Subscribe again to the event
            memory.subscribeToEvent("MiddleTactilTouched","ReactToTouch","onheadTouched")

    def onrightTouched(self, strVarName, value):
        """ This will be called each time a touch
        is detected.

        """
        # Unsubscribe to the event when talking,
        # to avoid repetitions
        global right
        right = (right + 1) % 2
        if (right == 0):
            memory.unsubscribeToEvent("HandRightBackTouched","ReactToTouch")
        # right_touch = 2
            print ("right is touched")
            changeState()
            memory.subscribeToEvent("HandRightBackTouched","ReactToTouch","onrightTouched")

    def onleftTouched(self, strVarName, value):
        """ This will be called each time a touch
        is detected.

        """
        # Unsubscribe to the event when talking,
        # to avoid repetitions
        global left
        left = (left + 1) % 2
        if (left == 0):
            memory.unsubscribeToEvent("HandLeftBackTouched", "ReactToTouch")
        # left_touch = 3
            print ("left is touched")
            memory.subscribeToEvent("HandLeftBackTouched","ReactToTouch","onleftTouched")

def changeState():
    global currentState
    if currentState == FACE_RECO_STATE:
        currentState = CHAT_STATE
    else:
        currentState = FACE_RECO_STATE

def main(ip, port):
    """ Main entry point
    """
    # We need this broker to be able to construct
    # NAOqi modules and subscribe to other modules
    # The broker must stay alive until the program exists
    myBroker = ALBroker("myBroker",
       "0.0.0.0",   # listen to anyone
       0,           # find a free port and use it
       ip,          # parent broker IP
       port)        # parent broker port
    global motion
    motion = Motion(ip,port)


    global reactToTouch
    reactToTouch = ReactToTouch("ReactToTouch")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print
        print "Interrupted by user, shutting down"
        myBroker.shutdown()
        sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="101.5.211.149",
                        help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559,
                        help="Robot port number")
    args = parser.parse_args()
    main(args.ip, args.port)
