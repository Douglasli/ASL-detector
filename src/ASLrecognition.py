import Predict
from datetime import date, time, datetime, timedelta
import sys
import socket
#from websocket import create_connection
from os import system
import os, sys, thread, time
sys.path.insert(0, "../lib")
import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import io,csv
from sklearn.svm import SVR
from sklearn.model_selection import cross_val_score
import numpy as np
from sklearn.externals import joblib


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
            datacomponent = []
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
        if count == 120:
			print "finish fetch"
			controller.remove_listener(listener)
			count = 0
			break

#Prediction
def ToChar(numberarray):
	datalist = {'a':1,'b':2,'c':3,'k':4,'e':5,'f':6,'g':7,'h':8,'i':9,'j':10,'d':11,'l':12,'m':13,'n':14,'o':15,'p':16,'q':17,'r':18,'s':19,'t':20,'u':21,'v':22,'w':23,'x':24,'y':25,'z':26,'0':27,'1':28,'2':29,'3':30,'4':31,'5':32,'6':33,'7':34,'8':35,'9':36}
	result = []
	for i in range(0,len(numberarray-1)):
		result.append(datalist.keys()[datalist.values().index(int(round(numberarray[i])))])
	
	return result
def Predict():
	global data
	#load Predict data
	print "ok "
	# datalist = list(data)
	# for row in datalist:
	#     for k in range(0,20):
	#         row[k] = float(row[k])
	dataset = np.array(data).astype(np.float)
	X2 = dataset[:, 0:20]  
	clf = SVR(kernel='rbf', C=1e3, gamma=0.1)
   	clf=joblib.load("predict/machine_SVR.pkl")
	predict_y=clf.predict(X2)
	predict = ToChar(predict_y)
	data = []
	return predict

def Analysis():
	fetch()
	#ws = create_connection("ws://127.0.0.1:8001/websocket")
	#ws.send("Wait for fetching")
	#ws.send
	print "Finish fetching and begin prediction"
	predict = Predict()
	#ws.send("Finish prediction")
	result = {}
	finalResult = ""
	for a in predict:
		if a in result:
			result[a] = result[a]+1
		else:
			result.update({a:0})
	total = 0.0
	for a in result:
		total = total+result[a]
	for a in result:
		b = float(result[a])
		poss = b/total
		print "Character: %s, possibility: %0.2f \n" % (
			a, poss)

	finalResult = max(result, key=result.get)
	print finalResult
# socket programming	
	#ws.send(finalResult)
	system('say ' + finalResult)


def main():
	while True:
		Analysis()
	#	time.sleep(1)
if __name__ == "__main__":
    main()