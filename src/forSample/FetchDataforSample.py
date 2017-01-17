###########################
import os, sys, thread, time
sys.path.insert(0, "../../lib")
import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import io,csv

#Sample
Sample = 0
data = []
datacomponent = []

class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    bone_angle_name = ['MetacarpaltoProximal', 'ProximaltoIntermediate', 'IntermediatetoDistal' ]
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    global Sample
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
            datacomponent = []
            datacomponent.append(Sample)
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

            data.append(datacomponent)

                    

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

def main():
    # Input test alphabet
    global Sample
    global data 
    alphabet = raw_input("Please figure out which alphabet you want to test:\n")
    datalist = {'a':1,'b':2,'c':3,'d':4,'e':5,'f':6,'g':7,'h':8,'i':9,'j':10,'k':11,'l':12,'m':13,'n':14,'o':15,'p':16,'q':17,'r':18,'s':19,'t':20,'u':21,'v':22,'w':23,'x':24,'y':25,'z':26,'0':27,'1':28,'2':29,'3':30,'4':31,'5':32,'6':33,'7':34,'8':35,'9':36}
    Sample = datalist.get(alphabet)
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
        # Remove the sample listener when done and save data to CSV
        controller.remove_listener(listener)
        with open("../result/sample.csv", "a") as f:
            writer = csv.writer(f)
            writer.writerows(data)
        print("Save successfully")
if __name__ == "__main__":
    main()
