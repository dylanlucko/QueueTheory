

#%%
import numpy as np
import pandas as pd
#%%
### problem PARAMETERS #######
inter_arrival_max = 5
inter_arrival_min = 3

service_time_max = 6
service_time_min = 2

n_events = 30

#%%
np.random.seed(42)
event = 0

#at event zero time is also zero
time_ = 0
#create counters for arrived and served customers
arrived_customers = 0
served_customers = 0
departed_customers = 0

#generate random variables for next events
interarrival_time = np.random.uniform(inter_arrival_min, inter_arrival_max)
next_arrival_time = time_ + interarrival_time
server_status = "idle"
queue = 0
arrived_customers += 1

### event zero done
event += 1  
#create timeseries and populate with event 1 details
ts_columns = ['event', 'time', 'type', 
              'queue', 'arr cust', 'served cust', 'depar cust']

time_series =  pd.DataFrame([[1, float(next_arrival_time), "arrival", 
                              queue, arrived_customers, 0, 0]],
                             columns = ts_columns) 
# %%
while event <= n_events:
    #event starts
    #parameters at event t
    event_type = time_series['type'].iloc[event-1]
    time_ = time_series['time'].iloc[event-1]

    #IF EVENT IS AN ARRIVAL #####################################
    if event_type == "arrival":
        #arrival event generate by default next arrival time
        
        #counter of arrived customers increases by 1
        arrived_customers += 1
        
        #generate next arrival time
        interarrival_time = np.random.uniform(inter_arrival_min, inter_arrival_max)
        next_arrival_time = time_ + interarrival_time  

        #if server status is idle customer is served immediatly 
        #and generates service time
        if server_status == "idle":
            #customer is served and counter of served customer increases by 1
            served_customers += 1
            #this customer number is added to the 'served customer' column at event n
            time_series['served cust'].iloc[event-1] =  served_customers

            #generate next events (service and departure time)
            service_time = np.random.uniform(service_time_min, service_time_max)
            departure_time = time_ + service_time
            departed_customers += 1 #same customer that is served at arrival time departs are departure time

            #add generated events to existing time series
            generated_events =  pd.DataFrame([
                          [99, float(departure_time), "departure", 0, 0,0,  departed_customers],
                          [99, float(next_arrival_time), "arrival", 0, arrived_customers, 0, 0]
                          ], columns = ts_columns) 
                          #Order doesnt matter because it's sorted next

            time_series =  pd.concat([time_series, generated_events])
            #events are sorted by time 
            time_series = time_series.sort_values(['time'])
            time_series.reset_index(drop=True, inplace=True)
            #event number is assigned by time order
            time_series['event'] = list(range(1, time_series.shape[0]+1))

            #event is finished and event counter increases
            event += 1 

        #if server status is busy increase queue and only generates arrival activity
        if server_status == "busy":
            queue += 1
            #add generated events to existing time series
            generated_events =  pd.DataFrame([
                                [99, float(next_arrival_time), "arrival", 
                                 0, arrived_customers,0, 0]]
                                , columns = ts_columns) 

            time_series =  pd.concat([time_series, generated_events])
            time_series = time_series.sort_values(['time'])
            time_series.reset_index(drop=True, inplace=True)
            time_series['event'] = list(range(1, time_series.shape[0]+1))
            time_series['queue'].iloc[event-1] = queue
            #event is finished and event counter increases
            event += 1 

    #IF EVENT IS A DEPARTURE ####################################
    if event_type == "departure":
        
        #if queue is zero and customer departs, server status remains idle and next event is an arrival
        if queue == 0 :
            server_status = "idle"
            #event is finished and event counter increases
            #nothing else happens untill next arrival
            event += 1

        #if there are customers in queue (>0), server changes to busy and queue decreases by one   
        if queue != 0 :
            #customer is served and counter of served customer increases by 1
            served_customers += 1
            #this customer number is added to the 'served customer' column at event n
            time_series['served cust'].iloc[event-1] =  served_customers           
            
            #queue decreases by one
            queue -= 1
            server_status = "busy"
            
            #generate next events (service and departure time)
            service_time = np.random.uniform(service_time_min, service_time_max)
            departure_time = time_ + service_time
            departed_customers += 1 #same customer that is served at arrival time departs are departure time

            #add generated events to existing time series
            generated_events =  pd.DataFrame([
                                    [99, float(departure_time), "departure", 0, 0, 0, departed_customers]
                                    ], columns = ts_columns) 

            time_series =  pd.concat([time_series, generated_events])
            time_series = time_series.sort_values(['time'])
            time_series.reset_index(drop=True, inplace=True)
            time_series['event'] = list(range(1, time_series.shape[0]+1)) 
            time_series['queue'].iloc[event-1] = queue

            #event is finished and event counter increases
            event += 1 

    #once event is finished, determine server status for next event
    #if the next arrival if before the departure of current customer, server will be busy at arrival
    if next_arrival_time < departure_time:
        server_status = "busy" 
    else: 
        server_status = "idle"
# %%
#create summary of customer data with results

#get arriving customers
arrivals = time_series.loc[time_series['type'] == 'arrival', ['time', 'arr cust' ]]
arrivals.columns = ['time', 'customer']
#get departing customers
depature = time_series.loc[time_series['type'] == 'departure', ['time', 'depar cust' ]]
depature.columns = ['time', 'customer']
#get customers being served
serving = time_series.loc[time_series['served cust'] != 0 , ['time', 'served cust' ]]
serving.columns = ['time', 'customer']

#merge 
customer_df = arrivals.merge(depature, on='customer')
customer_df = customer_df.merge(serving, on='customer')
customer_df.columns = ['arrival time', 'customer', 'departure time', 'serving time']
customer_df = customer_df[['customer', 'arrival time', 'serving time', 'departure time']] 

#get time in queue
customer_df['time in queue'] = customer_df['serving time'] - customer_df['arrival time'] 
#get time in system
customer_df['time in system'] = customer_df['departure time'] - customer_df['arrival time'] 
#get time in server
customer_df['time in server'] = customer_df['departure time'] - customer_df['serving time'] 
#round all floats to 2 digits
customer_df = customer_df.round(2)
# %%
def run_experiments(n_runs=50):
    df = pd.DataFrame(columns = ['time in queue', 'time in server', 'time in system'])
    for i in range(n_runs):
        run_result = pd.DataFrame([run_queue(seed = i)])
        df = df.append(run_result)
    df.reset_index(inplace=True, drop=True)
    df['run number'] = range(1, n_runs+1)
    df = df[['run number', 'time in queue', 'time in server', 'time in system']] #rearrange columns
    return df

experiments = run_experiments()
# %%
