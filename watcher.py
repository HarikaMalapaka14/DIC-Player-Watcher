from kazoo.client import KazooClient
import sys
from kazoo.client import KazooState 
import time
import pandas as pd

import logging
logging.basicConfig()

port=sys.argv[1]
zk = KazooClient(hosts=port)

try:
	zk.start()


except:
	raise Exception("Please give valid port number")


n=int(sys.argv[2])
print("\n ")
#print("the max number list is ",n)
if(n>25):
	print("The maximum vakue of N is 25, so the watcher will diaplay maximum of 25")
	n=25



@zk.ChildrenWatch("/NN")
def watch_children(children):
	if(len(children)==0):
		print("There is nothing yet to display ")
	else:
		
		live_nodes=[]
		if(zk.exists("/DEAD")):
			#print("Live nodes :")
			live=zk.get_children("/DEAD")
			for q in live:
				live_nodes.append(str(q))

		
				
		time_node=[]
		data_in_node=[]
		name_node=[]
		stars=0
		for i in children:
			#print(i)
			ib=bytes(i)
			data,stat=zk.get("/NN/"+ib)
		
			if(data==''):
				stars=1
				continue
			name_node.append(str(i))
			data_in_node.append(int(data))
			time_node.append(stat.ctime)
			#print(i,": created at : ", stat.ctime," and data is ", data)
		df=pd.DataFrame(list(zip(time_node,data_in_node,name_node)))
		df.columns=['time_node','data_in_node','name_node']
		df_most_recent=df.sort_values(by='time_node', ascending=False)
		print("\n Most Recent Scores")
		print("\n ------------------------------")
		count=0
		for j in df_most_recent.values:
			count=count+1
			name_string=[]
			if(count==n+1):
				break
			for p in range(0,len(j[2])):
				a=ord(j[2][p])
				if(a in range(48,58)):
					break
				else:
					name_string.append(j[2][p])
			new_name=''
			for x in name_string:
				new_name+=x
			
			if(new_name in live_nodes):			
				print(new_name,j[1])
			else:
				print(new_name,j[1],"**")
	
		print("\n Top scores")
		print("\n-------------------------------")
		c=0
		df_highest_scores=df.sort_values(by='data_in_node',ascending=False)
		for k in df_highest_scores.values:
			c=c+1
			name_string_2=[]
			if(c==n+1):
				break

			for d in range(0,len(k[2])):
				b=ord(k[2][d])
				if(b in range(48,58)):
					break
				else:
					name_string_2.append(k[2][d])
			new_name_2=''
			for y in name_string_2:
				new_name_2+=y
			if(new_name_2 in live_nodes):
				print(new_name_2,k[1])
			else:
				print(new_name_2,k[1],"**")
	
	
		
		


if(zk.exists("/NN")):
	children = zk.get_children("/NN", watch=watch_children)


else:


	
	print("No scores to display yet, first start a player than run the watcher. For now program terminating")
	#zk.ensure_path("/N15/dummy")
	sys.exit(0)
	#children = zk.get_children("/N15", watch=watch_children)





try:
	while True:
		time.sleep(1)
except KeyboardInterrupt:
	pass	
