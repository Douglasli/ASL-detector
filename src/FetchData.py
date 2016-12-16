################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################
import os, sys, thread, time
sys.path.insert(0, "../lib")
import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import io,json

#Sample
Sample = ""

class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    bone_angle_name = ['MetacarpaltoProximal', 'ProximaltoIntermediate', 'IntermediatetoDistal' ]
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    global Sample

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
        data={
    "Thumb" : 
        {"MetacarpaltoProximal":0,"ProximaltoIntermediate":0,"IntermediatetoDistal":0 }
    ,
    "Index" : 
        {"MetacarpaltoProximal":0,"ProximaltoIntermediate":0,"IntermediatetoDistal":0 }
    ,
    "Middle" : 
        {"MetacarpaltoProximal":0,"ProximaltoIntermediate":0,"IntermediatetoDistal":0 }
    ,
    "Ring" : 
        {"MetacarpaltoProximal":0,"ProximaltoIntermediate":0,"IntermediatetoDistal":0 }
    ,
    "Pinky" : 
        {"MetacarpaltoProximal":0,"ProximaltoIntermediate":0,"IntermediatetoDistal":0 }
    }
        # Get the most recent frame and report some basic information
        frame = controller.frame()
        if len(frame.hands)==0:
        	return
        	
        print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d" % (
              frame.id, frame.timestamp, len(frame.hands), len(frame.fingers))

        # Get hands
        for hand in frame.hands:
            # Get fingers
            for finger in hand.fingers:
                fingerName = self.finger_names[finger.type]
                print "    %s finger" % (
                    fingerName)
                # Get bones
                for b in range(0, 3):
                    bone = finger.bone(b)
                    bonenext = finger.bone(b+1)
                    bone_angle_name = self.bone_angle_name[bone.type]
                    angle = bone.direction.dot(bonenext.direction)
                    print "      Bone: %s, Angle: %s" % (
                        bone_angle_name,
                        angle)
                    data[fingerName][bone_angle_name] = angle
                    with io.open('data.json', 'w', encoding='utf-8') as f:
                        f.write(unicode(json.dumps(data, ensure_ascii=False)))

        if not (frame.hands.is_empty and frame.gestures().is_empty):
            print ""

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"

def main():
    # Input test alphabet
    global Sample 
    Sample = raw_input("Please figure out which alphabet you want to test:")

    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    raw_input('Press enter to begin: ')
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()
