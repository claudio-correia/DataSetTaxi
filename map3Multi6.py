import folium
import osmnx as ox
import networkx as nx
import numpy as np
import pandas as pd
from datetime import datetime
import time
import calendar
import ast
from multiprocessing import Pool
import time

data = pd.read_csv("./train.csv", sep=",")

coordinates_interval = 15 #segundos em cada ponto


test_trace1 = "[[-8.660421,41.172516],[-8.660421,41.172516],[-8.660286,41.172282],[-8.660142,41.172084],[-8.660124,41.172075],[-8.660313,41.172426],[-8.660502,41.173623],[-8.660709,41.175207],[-8.660592,41.175621],[-8.659458,41.176197],[-8.657766,41.176224],[-8.656704,41.17599],[-8.655606,41.176251],[-8.654814,41.175855],[-8.653761,41.174991],[-8.653293,41.174991],[-8.652078,41.174991],[-8.651943,41.174928],[-8.651763,41.174802],[-8.651673,41.174739],[-8.650665,41.173965],[-8.649792,41.173254],[-8.648298,41.172066],[-8.647209,41.171166],[-8.645967,41.170167],[-8.644446,41.168925],[-8.643474,41.167044],[-8.641512,41.166144],[-8.640405,41.168178],[-8.639019,41.16933],[-8.637426,41.170356],[-8.634555,41.171364],[-8.631603,41.172003],[-8.628066,41.17275],[-8.624313,41.173182],[-8.620155,41.173587],[-8.616078,41.174028],[-8.612559,41.174451],[-8.608986,41.173812],[-8.607447,41.172867],[-8.606421,41.172165],[-8.605197,41.171679],[-8.60445,41.171526],[-8.603334,41.171409],[-8.601336,41.171193],[-8.599401,41.171211],[-8.598852,41.171301],[-8.59788,41.17149],[-8.595864,41.171796],[-8.594973,41.171715],[-8.594127,41.171337],[-8.59293,41.170509],[-8.590878,41.169195],[-8.588565,41.167845],[-8.585541,41.166549],[-8.582805,41.16537],[-8.582193,41.163471],[-8.581752,41.16321],[-8.581644,41.16321],[-8.581518,41.16321],[-8.581392,41.163237],[-8.580888,41.163588],[-8.580654,41.163903],[-8.579943,41.16402],[-8.578791,41.164749],[-8.577396,41.165667],[-8.577072,41.166198],[-8.576955,41.166396],[-8.576946,41.166405],[-8.576946,41.166405],[-8.576937,41.166414],[-8.576784,41.166621],[-8.576019,41.167179],[-8.574714,41.167836],[-8.573526,41.168754],[-8.572113,41.169375],[-8.5707,41.169924],[-8.570601,41.169717]]"
test_trace = ast.literal_eval(test_trace1)


ox.config(use_cache=True, log_console=False)

#G = ox.graph_from_point(( 41.1485873, -8.6109806), dist=2000, network_type='drive', simplify=False)


#ox.save_graphml(G, 'myGraphData.graphml')
G = ox.load_graphml('myGraphData.graphml')



G = ox.speed.add_edge_speeds(G)
G = ox.speed.add_edge_travel_times(G)




#orig = ox.distance.nearest_nodes(G, Y=41.172516, X=-8.660421,return_dist=False)
#dest = ox.distance.nearest_nodes(G, Y=41.169717, X=-8.570601,return_dist=False)
#route = nx.shortest_path(G, orig, dest, 'travel_time')

#print(orig)
#print(dest)


#route_map = ox.plot_route_folium(G, route)
#41,1404569, -8,6116866
	
#for point in route:
	#print(G.nodes[point])
	#print(G.__getitem__(point))
#	if(G.nodes[point]['street_count'] > 2):
#		folium.Marker( location=[ G.nodes[point]['y'], G.nodes[point]['x'] ], fill_color='#43d9de', radius=8 ).add_to( route_map )
		#print(G.nodes[point])
		#for n in G.neighbors(point):
			#print(n)		
		#	route_map = ox.plot_route_folium(G, [ point, n], route_map=route_map, color="black")
		#	break


#folium.Marker( location=[ 41.172516, -8.660421 ], color='#de4343', radius=8 ).add_to( route_map )
#folium.Marker( location=[ 41.169717, -8.570601 ], color='#de4343', radius=8 ).add_to( route_map )



#for point1 in test_trace:
#	close_point = ox.get_nearest_node(G, (point1[1], point1[0]))
#	G.nodes[close_point]['y']

#	folium.Marker( location=[ G.nodes[close_point]['y'],G.nodes[close_point]['x']], radius=8 ).add_to( route_map )




def get_unix_day(time_stamp):
	ts = int(time_stamp)
	dt = datetime.utcfromtimestamp(ts)

	dt = dt.replace(hour=0, minute=0, second=0)
	begining_of_day_timestamp = calendar.timegm(dt.timetuple())
	return begining_of_day_timestamp

def fix_next_day_point(row, user, start_interval, end_interval, df):
	print("in fix_next_day_point")
	return


def required_pseudonym_for_trajectory(origin_point, end_point):
	#global route_map

	#print(origin_point)	
	#print(end_point)	

	orig = ox.nearest_nodes(G, Y=origin_point[1], X=origin_point[0])
	dest = ox.nearest_nodes(G, Y=end_point[1], X=end_point[0])

	if(orig == dest):
		return 1

	try:
		route = nx.shortest_path(G, orig, dest, 'travel_time')
	except Exception as e:
		print(e)
		print(" origin_point: ", origin_point, " end_point: ", end_point)
		return 1


	crossroad_count = 0
	for point in route:
		#print(G.nodes[point])
		#print(G.__getitem__(point))
		if(G.nodes[point]['street_count'] > 2):
			crossroad_count = crossroad_count +1
			#for n in G.neighbors(point):
				#print(n)		
			#	route_map = ox.plot_route_folium(G, [ point, n], route_map=route_map, color="black")
			#	break

	#route_map = ox.plot_route_folium(G, route, route_map=route_map)

	return crossroad_count 


def run_trace(row, user, start_interval, end_interval, df):
		#print("\n")
		#print(len(row['POLYLINE'])*coordinates_interval + start_interval)

		coordinates = ast.literal_eval(row['POLYLINE'])
		#print(len(coordinates))
		#print(coordinates)

		last_point_timestamp = len(coordinates)*coordinates_interval + start_interval
		if(last_point_timestamp > end_interval):
			fix_next_day_point(row, user, start_interval, end_interval, df)

		pseu_number =  required_pseudonym_for_trajectory(coordinates[0], coordinates[len(coordinates) - 1])


# este codigo era para saltar entre todos os pontos do trace
#		pseu_number = 0
#		for point_index in range(len(coordinates) - 1):
#			#print(point_index)
#	
#			point_timestamp = point_index*coordinates_interval + start_interval
#			if(point_timestamp > last_point_timestamp):
#				return pseu_number;	
#
#			pseu_number = pseu_number + required_pseudonym_for_trajectory(coordinates[point_index], coordinates[point_index + 1])


		return pseu_number


def run_user(user, start_interval, end_interval, df):
	traces = df[df.TAXI_ID == user]	
	#print(user)
	#print(traces)
	
	pseu_number = 0	
	for index, row in traces.iterrows():
		pseu_number = pseu_number + run_trace(row, user, start_interval, end_interval, df)

	return pseu_number




def run_interval(start_interval, end_interval, interval_delta, data):

	print("run_interval start: " ,start_interval, " end: ", start_interval + interval_delta)		

	#print("run_interval thread")
	df = data[data.TIMESTAMP > start_interval]	
	df = df[df.TIMESTAMP < start_interval + interval_delta ]	


	if(start_interval >= end_interval):
		return 1

	column = df['TAXI_ID']
	print(pd.unique(column))
	required_pseudonym_for_interval = 0;



	for user in pd.unique(column):
		required_pseudonym_for_interval = max(required_pseudonym_for_interval, run_user(user, start_interval, end_interval, df))



	return required_pseudonym_for_interval


def run(interval_delta):

	time_order = data.sort_values(by=['TIMESTAMP'])
	start_interval = get_unix_day(time_order.iloc[0]['TIMESTAMP'])
	end_interval = time_order.iloc[-1]['TIMESTAMP'] + interval_delta + 1

	#print(start_interval)
	#print(end_interval)

	max_required_pseudonym_for_interval = 0;
	current_interval = start_interval
	pool = Pool(6)
		
	time.sleep(10)
	print("Starting...")

	return_val0 = 1
	return_val1 = 1
	return_val2 = 1
	return_val3 = 1
	return_val4 = 1
	return_val5 = 1

	while(current_interval < end_interval): 	#for current_interval in range(start_interval, end_interval, interval_delta):
		
		print("start: " ,start_interval, " end: ", end_interval,  " current_interval: ", current_interval, " pseu: ", max_required_pseudonym_for_interval)		
		

		##new thread code##   
		while(current_interval < end_interval):
			df = data[data.TIMESTAMP > current_interval]	
			df = df[df.TIMESTAMP < current_interval + interval_delta ]			
			if df.empty:
				current_interval += interval_delta
			else:
				async_result0 = pool.apply_async(run_interval, (current_interval, end_interval, interval_delta, data))
				current_interval += interval_delta	
				break			
		##end new thread code##   


		##new thread code##   
		while(current_interval < end_interval):
			df = data[data.TIMESTAMP > current_interval]	
			df = df[df.TIMESTAMP < current_interval + interval_delta ]			
			if df.empty:
				current_interval += interval_delta
			else:
				async_result1 = pool.apply_async(run_interval, (current_interval, end_interval, interval_delta, data))
				current_interval += interval_delta
				break				
		##end new thread code##   

		##new thread code##   
		while(current_interval < end_interval):
			df = data[data.TIMESTAMP > current_interval]	
			df = df[df.TIMESTAMP < current_interval + interval_delta ]			
			if df.empty:
				current_interval += interval_delta
			else:
				async_result2 = pool.apply_async(run_interval, (current_interval, end_interval, interval_delta, data))
				current_interval += interval_delta
				break
		##end new thread code##   


		##new thread code##   
		while(current_interval < end_interval):
			df = data[data.TIMESTAMP > current_interval]	
			df = df[df.TIMESTAMP < current_interval + interval_delta ]			
			if df.empty:
				current_interval += interval_delta
			else:
				async_result3 = pool.apply_async(run_interval, (current_interval, end_interval, interval_delta, data))
				current_interval += interval_delta		
				break		
		##end new thread code##   
	
		##new thread code##   
		while(current_interval < end_interval):
			df = data[data.TIMESTAMP > current_interval]	
			df = df[df.TIMESTAMP < current_interval + interval_delta ]			
			if df.empty:
				current_interval += interval_delta
			else:
				async_result4 = pool.apply_async(run_interval, (current_interval, end_interval, interval_delta, data))
				current_interval += interval_delta		
				break		
		##end new thread code##   
	
		##new thread code##   
		while(current_interval < end_interval):
			df = data[data.TIMESTAMP > current_interval]	
			df = df[df.TIMESTAMP < current_interval + interval_delta ]			
			if df.empty:
				current_interval += interval_delta
			else:
				async_result5 = pool.apply_async(run_interval, (current_interval, end_interval, interval_delta, data))
				current_interval += interval_delta		
				break		
		##end new thread code##   

 
		if 'async_result0' in locals():
			return_val0 = async_result0.get() 
		if 'async_result1' in locals():		
			return_val1 = async_result1.get() 
		if 'async_result2' in locals():		
			return_val2 = async_result2.get() 
		if 'async_result3' in locals():
			return_val3 = async_result3.get() 
		if 'async_result4' in locals():		
			return_val4 = async_result4.get() 
		if 'async_result5' in locals():
			return_val5 = async_result5.get() 


		result = max([return_val0, return_val1, return_val2, return_val3, return_val4, return_val5] )
		max_required_pseudonym_for_interval = max(result, max_required_pseudonym_for_interval)


		

	return max_required_pseudonym_for_interval


if __name__ == '__main__':
	number_of_pseudonyms = run(86400) # um dia tem 86400 segundos
	print(number_of_pseudonyms)


#route_map.save('test.html')
#print(data)

































