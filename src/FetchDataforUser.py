###########################
import os, sys, thread, time
sys.path.insert(0, "../lib")
import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import io,csv

#Sample
data = []
datacomponent = []
count = 0
class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    bone_angle_name = ['MetacarpaltoProximal', 'ProximaltoIntermediate', 'IntermediatetoDistal' ]
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    global data
    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()
        if len(frame.hands)==0:
        	return
        	
        # Get hands
        for hand in frame.hands:
            global datacomponent
            global count
            datacomponent = []
            handDirection = hand.direction

            # Get fingers
            for finger in hand.fingers:
                fingerName = self.finger_names[finger.type]
                # Get bones
                for b in range(0, 3):
                    bone = finger.bone(b)
                    bonenext = finger.bone(b+1)
                    bone_angle_name = self.bone_angle_name[bone.type]
                    angle = bone.direction.dot(bonenext.direction)
                    datacomponent.append(angle)

                # Get the angle between finger and hand
                bone = finger.bone(3)
                angle = bone.direction.dot(handDirection)
                datacomponent.append(angle)
            # Get the number of extended fingers
            hand_pointables = hand.pointables.extended()
            numberExtendedFinger = len(hand_pointables)
            datacomponent.append(numberExtendedFinger)
            data.append(datacomponent)
            count = count +1
        if not (frame.hands.is_empty and frame.gestures().is_empty):
            pass

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"

def fetch():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()
    global count
    # Have the sample listener receive events from the controller
    # raw_input('Press enter to begin: ')
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Wait for fetching data"
    while True:
        if count == 60:
            return data

def fetchRealTime():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    raw_input('Press enter to begin: ')
    controller.add_listener(listener)
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done and save data to CSV
        controller.remove_listener(listener)

def getDatacomponent():
    return datacomponent