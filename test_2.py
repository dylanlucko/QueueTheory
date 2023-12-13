
#%%
import numpy as np
import pandas as pd
#%%
# Problem Parameters
inter_arrival_max = 5
inter_arrival_min = 3

service_time_max = 6
service_time_min = 2

n_events = 30
#%%
# Initializations
np.random.seed(42)
event = 0
time_ = 0
arrived_customers = 0
served_customers = 0
departed_customers = 0
queue = 0
#%%
# Time Series Columns
ts_columns = ['event', 'time', 'type', 'queue', 'arr cust', 'served cust', 'depar cust']
time_series = pd.DataFrame(columns=ts_columns)
#%%
# Simulation Loop
# ... (Previous code remains the same)

# Simulation Loop (Revised)
while event < n_events and event < len(time_series):
    event_type = time_series.at[event, 'type']
    time_ = time_series.at[event, 'time']

    if event_type == "arrival":
        arrived_customers += 1
        interarrival_time = np.random.uniform(inter_arrival_min, inter_arrival_max)
        next_arrival_time = time_ + interarrival_time

        if server_status == "idle":
            served_customers += 1
            service_time = np.random.uniform(service_time_min, service_time_max)
            departure_time = time_ + service_time
            departed_customers += 1

            generated_events = pd.DataFrame([
                [99, float(departure_time), "departure", 0, 0, 0, departed_customers],
                [99, float(next_arrival_time), "arrival", 0, arrived_customers, 0, 0]
            ], columns=ts_columns)

            time_series = pd.concat([time_series, generated_events])
            time_series = time_series.sort_values(['time']).reset_index(drop=True)
            event += 1
        else:
            queue += 1
            generated_events = pd.DataFrame([
                [99, float(next_arrival_time), "arrival", 0, arrived_customers, 0, 0]
            ], columns=ts_columns)

            time_series = pd.concat([time_series, generated_events])
            time_series = time_series.sort_values(['time']).reset_index(drop=True)
            time_series.at[event, 'queue'] = queue
            event += 1

    elif event_type == "departure":
        if queue == 0:
            server_status = "idle"
            event += 1
        else:
            served_customers += 1
            queue -= 1
            server_status = "busy"
            service_time = np.random.uniform(service_time_min, service_time_max)
            departure_time = time_ + service_time
            departed_customers += 1

            generated_events = pd.DataFrame([
                [99, float(departure_time), "departure", 0, 0, 0, departed_customers]
            ], columns=ts_columns)

            time_series = pd.concat([time_series, generated_events])
            time_series = time_series.sort_values(['time']).reset_index(drop=True)
            time_series.at[event, 'queue'] = queue
            event += 1

        # Update event and check conditions
event += 1
if event < len(time_series):
    next_arrival_time = time_series.at[event, 'time'] if time_series.at[event, 'type'] == 'arrival' else None
    departure_time = time_series.at[event, 'time'] if time_series.at[event, 'type'] == 'departure' else None
else:
    next_arrival_time = None
    departure_time = None

if next_arrival_time and next_arrival_time < departure_time:
    server_status = "busy"
else:
    server_status = "idle"


# Data Analysis
# (Your data analysis code goes here, followed by run_experiments function if needed)

# %%
# Assuming your simulation loop has completed and you have the time_series data

# Extracting relevant data for analysis
arrivals = time_series[time_series['type'] == 'arrival'][['time', 'arr cust']].rename(columns={'time': 'arrival_time', 'arr cust': 'customer'})
departures = time_series[time_series['type'] == 'departure'][['time', 'depar cust']].rename(columns={'time': 'departure_time', 'depar cust': 'customer'})
serving = time_series[time_series['served cust'] != 0][['time', 'served cust']].rename(columns={'time': 'serving_time', 'served cust': 'customer'})

# Merging the data to create a customer-wise view
customer_data = arrivals.merge(departures, on='customer').merge(serving, on='customer')
customer_data = customer_data[['customer', 'arrival_time', 'serving_time', 'departure_time']]

# Calculate additional metrics
customer_data['time_in_queue'] = customer_data['serving_time'] - customer_data['arrival_time']
customer_data['time_in_system'] = customer_data['departure_time'] - customer_data['arrival_time']
customer_data['time_in_server'] = customer_data['departure_time'] - customer_data['serving_time']
customer_data = customer_data.round(2)

# Basic statistics
average_time_in_queue = customer_data['time_in_queue'].mean()
average_time_in_system = customer_data['time_in_system'].mean()
average_time_in_server = customer_data['time_in_server'].mean()

max_time_in_queue = customer_data['time_in_queue'].max()
max_time_in_system = customer_data['time_in_system'].max()
max_time_in_server = customer_data['time_in_server'].max()

min_time_in_queue = customer_data['time_in_queue'].min()
min_time_in_system = customer_data['time_in_system'].min()
min_time_in_server = customer_data['time_in_server'].min()

# Displaying the results
print(f"Average Time in Queue: {average_time_in_queue}")
print(f"Average Time in System: {average_time_in_system}")
print(f"Average Time in Server: {average_time_in_server}")

print(f"Max Time in Queue: {max_time_in_queue}")
print(f"Max Time in System: {max_time_in_system}")
print(f"Max Time in Server: {max_time_in_server}")

print(f"Min Time in Queue: {min_time_in_queue}")
print(f"Min Time in System: {min_time_in_system}")
print(f"Min Time in Server: {min_time_in_server}")

# Further analysis as needed...

# %%
print(customer_data.head())
print(customer_data.info())

# %%
# Assuming you have the time_series DataFrame populated from the simulation
# Extracting relevant data for analysis
arrivals = time_series[time_series['type'] == 'arrival'][['time', 'arr cust']].rename(columns={'time': 'arrival_time', 'arr cust': 'customer'})
departures = time_series[time_series['type'] == 'departure'][['time', 'depar cust']].rename(columns={'time': 'departure_time', 'depar cust': 'customer'})
serving = time_series[time_series['served cust'] != 0][['time', 'served cust']].rename(columns={'time': 'serving_time', 'served cust': 'customer'})
#%%
# Merging the data to create a customer-wise view
customer_data = arrivals.merge(departures, on='customer').merge(serving, on='customer')
#%%
# Calculate additional metrics
customer_data['time_in_queue'] = customer_data['serving_time'] - customer_data['arrival_time']
customer_data['time_in_system'] = customer_data['departure_time'] - customer_data['arrival_time']
customer_data['time_in_server'] = customer_data['departure_time'] - customer_data['serving_time']
customer_data = customer_data.round(2)

# Displaying the extracted data for verification
print(customer_data.head())
print(customer_data.info())

# %%
