from kazoo.client import KazooClient
from kazoo.client import KazooState 
import sys
import time
import numpy as np
import logging
logging.basicConfig()

port=sys.argv[1]
zk = KazooClient(hosts=port)
try:
	zk.start()


except:
	raise Exception("Please give valid port number")


if(len(sys.argv)==3):

	print("Correct no of arguments given - not batch mode")


	name=sys.argv[2]
	caps=range(97,123)
	small=range(65,91)

	for x in name:
	    if(ord(x) not in range(97,123) and ord(x) not in range(65,91) and ord(x)!=32):
		raise Exception('Please enter valid name')
	if(zk.exists("/NN/"+name)):
		print("\n This player already exists - program terminating")
		sys.exit()
	scores=[]
	zk.ensure_path("/NN/"+name)  #name added to path
	#print(zk.state)
	it=001

	while True:

		bt=bytes(it)
		try:
			score=abs(int(input(" enter a score : ")))
			scores.append(score)
			print("score added")
			sc=bytes(score)
			zk.create("/NN/"+name+bt,sc)
			it=it+1

		except KeyboardInterrupt:
	    
			zk.ensure_path("/DEAD/"+name)
			sys.exit()

			pass
		except:
			print("Please enter valid input")

	    
		 



elif(len(sys.argv)==6):
	print("correct no of arguments - batch mode")
	port=sys.argv[1]
	zk = KazooClient(hosts=port)
	zk.start()		
	name=sys.argv[2]
	for x in name:
	    if(ord(x) not in range(97,123) and ord(x) not in range(65,91) and ord(x)!=32):
		raise Exception('Please enter valid name')

	if(zk.exists("/NN/"+name)):
		print("\n This player already exists - program terminating")
		sys.exit()

	try:
		count=abs(int(sys.argv[3]))
		delay_mean=abs(int(sys.argv[4]))
		scores_mean=abs(int(sys.argv[5]))
		zk.ensure_path("/NN/"+name)
		#print("\n Path ensured")
		#print(zk.state)
		rand_float=np.random.normal(loc=scores_mean,scale=8,size=count)
		delay_float=np.random.normal(loc=delay_mean,scale=2,size=count)
		rand_string=[]
		for m in rand_float:
			rand_string.append(str(int(abs(round(m,3)))))
		inc=0
		for g in rand_string:
			print(g)
			del_for_score=int(delay_float[inc])
			time.sleep(del_for_score)
			inc=inc+1
			incb=bytes(inc)
			bt_batch=bytes(g)
			zk.create("/NN/"+name+incb,bt_batch)
		zk.ensure_path("/DEAD/"+name)
	except:
		print("Please enter valid input")

else:
	print("Incorrect no of args")
	sys.exit()


		
	

		  
