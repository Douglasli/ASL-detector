import Predict
import FetchDataforUser
from datetime import date, time, datetime, timedelta
import sys
import socket
from websocket import create_connection
def Analysis():
	ws = create_connection("ws://127.0.0.1:8001/websocket")
	ws.send("Wait for fetching")
	FetchDataforUser.fetch()
	ws.send("Finish fetching and begin prediction")
	predict = Predict.Predict()
	ws.send("Finish prediction")
	result = {}
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
	ws.send(finalResult)
	

# # Make program realtime
# def work():
# 	userarray = FetchDataforUser.getDatacomponent()
# 	print userarray
# 	# raw_input('Press enter to begin: ')
# 	# predict = SVRAnalysis.AnalysisRealTime(userarray, "result/sample.csv")
# 	# print predict

# def runTask(func, day=0, hour=0, min=0, second=0):
# 	print "a"
#    	# Init time
#    	now = datetime.now()
#    	strnow = now.strftime('%Y-%m-%d %H:%M:%S')
#    	print "now:",strnow
#    	# First next run time
#    	period = timedelta(days=day, hours=hour, minutes=min, seconds=second)
#    	next_time = now + period
#    	strnext_time = next_time.strftime('%Y-%m-%d %H:%M:%S')
#    	print "next run:",strnext_time
#    	while True:
# 		# Get system current time
# 		iter_now = datetime.now()
# 		iter_now_time = iter_now.strftime('%Y-%m-%d %H:%M:%S')
# 		if str(iter_now_time) == str(strnext_time):
#    			func()
#    			continue

# def RealtimeAnalysis():
# 	try:
#    		thread.start_new_thread( FetchDataforUser.fetchRealTime() )
#    		thread.start_new_thread( runTask, (work,0,0,0,1) )
# 	except:
#    		print "Error: unable to start thread"

# def main(argv):
# 	if argv[0] == '-a':
# 		Analysis()
# 	elif argv[1] == '-r':
# 		RealtimeAnalysis()


# if __name__ == "__main__":
#     main(sys.argv[1:])
def main():
	Analysis()
if __name__ == "__main__":
    main()