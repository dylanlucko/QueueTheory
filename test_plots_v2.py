
#%%




import numpy as np
import matplotlib.pyplot as plt

def generate_infinite_queue(arrival_rate, service_rate, num_servers, sim_time):
    arrival_times = np.random.exponential(scale=1 / arrival_rate, size=sim_time)
    service_times = np.random.exponential(scale=1 / service_rate, size=(num_servers, sim_time))

    arrivals = np.cumsum(arrival_times)
    departures = np.zeros((num_servers, sim_time))
    queue_length_over_time = []

    for arrival in arrivals:
        served = False
        for i in range(num_servers):
            if arrival >= departures[i, 0]:
                departures[i] = np.maximum(arrival, departures[i]) + service_times[i]
                served = True
                break

        if not served:
            queue_length_over_time.append(len(arrivals[arrivals <= arrival]))

    return queue_length_over_time

# Parameters
arrival_rate = 0.2
service_rate = 0.3
num_servers = 2
simulation_time = 1000

# Generate queue length over time
queue_length = generate_infinite_queue(arrival_rate, service_rate, num_servers, simulation_time)

# Plot the queue length over time or perform analysis on the generated queue data
time_points = np.arange(len(queue_length))  # Generate time points for x-axis
plt.plot(time_points, queue_length)
plt.xlabel('Time')
plt.ylabel('Queue Length')
plt.title('Queue Length Over Time in an Infinite Queue System')
plt.show()




# %%


import numpy as np
import matplotlib.pyplot as plt

def generate_infinite_queue(arrival_rate, service_rate, num_servers, sim_time):
    arrival_times = np.random.exponential(scale=1 / arrival_rate, size=sim_time)
    service_times = np.random.exponential(scale=1 / service_rate, size=(num_servers, sim_time))

    arrivals = np.cumsum(arrival_times)
    departures = np.zeros((num_servers, sim_time))
    queue_length_over_time = []

    for arrival in arrivals:
        served = False
        for i in range(num_servers):
            if arrival >= departures[i, 0]:
                departures[i] = np.maximum(arrival, departures[i]) + service_times[i]
                served = True
                break

        if not served:
            queue_length_over_time.append(len(arrivals[arrivals <= arrival]))

    return arrivals, departures, queue_length_over_time

# Parameters
arrival_rate = 0.2
service_rate = 0.3
num_servers = 2
simulation_time = 1000

# Generate queue length over time
arrivals, departures, queue_length = generate_infinite_queue(arrival_rate, service_rate, num_servers, simulation_time)

# Plot arrivals vs departures
plt.plot(arrivals, np.sum(departures, axis=0), label='Departures', linestyle='-', marker='o')
plt.plot(arrivals, np.arange(len(arrivals)), label='Arrivals', linestyle='-', marker='o')
plt.xlabel('Time')
plt.ylabel('Count')
plt.title('Arrivals vs Departures Over Time')
plt.legend()
plt.show()

# %%import numpy as np
import matplotlib.pyplot as plt

def generate_infinite_queue(arrival_rate, service_rate, num_servers, sim_time):
    arrival_times = np.random.exponential(scale=1 / arrival_rate, size=sim_time)
    service_times = np.random.exponential(scale=1 / service_rate, size=(num_servers, sim_time))

    arrivals = np.cumsum(arrival_times)
    departures = np.zeros((num_servers, sim_time))
    queue_length_over_time = []

    for arrival in arrivals:
        served = False
        for i in range(num_servers):
            if arrival >= departures[i, 0]:
                departures[i] = np.maximum(arrival, departures[i]) + service_times[i]
                served = True
                break

        if not served:
            queue_length_over_time.append(len(arrivals[arrivals <= arrival]))

    return arrivals, departures, queue_length_over_time

# Parameters
arrival_rate = 0.2
service_rate = 0.3
num_servers = 2
simulation_time = 100

# Generate queue length over time
arrivals, departures, queue_length = generate_infinite_queue(arrival_rate, service_rate, num_servers, simulation_time)

# Plot arrivals
plt.figure(figsize=(8, 6))
plt.plot(arrivals, np.arange(len(arrivals)), label='Arrivals', linestyle='-', marker='o')
plt.xlabel('Time')
plt.ylabel('Count')
plt.title('Arrivals Over Time')
plt.legend()
plt.show()

# Plot departures
plt.figure(figsize=(8, 6))
plt.plot(arrivals, np.sum(departures, axis=0), label='Departures', linestyle='-', marker='o')
plt.xlabel('Time')
plt.ylabel('Count')
plt.title('Departures Over Time')
plt.legend()
plt.show()

# Plot queue length
plt.figure(figsize=(8, 6))
plt.plot(arrivals[:len(queue_length)], queue_length, label='Queue Length', linestyle='-', marker='o')
plt.xlabel('Time')
plt.ylabel('Queue Length')
plt.title('Queue Length Over Time')
plt.legend()
plt.show()

# %%


import numpy as np
import matplotlib.pyplot as plt

def generate_infinite_queue(arrival_rate, service_rate, num_servers, sim_time):
    arrival_times = np.random.exponential(scale=1 / arrival_rate, size=sim_time)
    service_times = np.random.exponential(scale=1 / service_rate, size=(num_servers, sim_time))

    arrivals = np.cumsum(arrival_times)
    departures = np.zeros((num_servers, sim_time))
    queue_length_over_time = []

    for arrival in arrivals:
        served = False
        for i in range(num_servers):
            if arrival >= departures[i, 0]:
                departures[i] = np.maximum(arrival, departures[i]) + service_times[i]
                served = True
                break

        if not served:
            # Calculate the number of arrivals before the current arrival time
            num_waiting = np.sum(arrivals <= arrival)
            queue_length_over_time.append(num_waiting)

    return arrivals, departures, queue_length_over_time

# Parameters
arrival_rate = 
service_rate = 0.3
num_servers = 1
simulation_time = 100

# Generate queue length over time
arrivals, departures, queue_length_over_time = generate_infinite_queue(
    arrival_rate, service_rate, num_servers, simulation_time
)

import numpy as np
import matplotlib.pyplot as plt

# Assuming you have data for arrivals, queue_length, departures, queue_length_over_time

# Plot queue length
time_range = np.linspace(0, max(arrivals), len(queue_length))  # Time range based on arrivals

plt.figure(figsize=(8, 6))
plt.plot(time_range, queue_length, label='Queue Length', linestyle='-', marker='o')
plt.xlabel('Time')
plt.ylabel('Queue Length')
plt.title('Queue Length Over Time')
plt.legend()
plt.grid(True)
plt.show()

# Plot arrivals
plt.figure(figsize=(8, 6))
plt.plot(arrivals, np.arange(len(arrivals)), label='Arrivals', linestyle='-', marker='o')
plt.xlabel('Time')
plt.ylabel('Count')
plt.title('Arrivals Over Time')
plt.legend()
plt.grid(True)
plt.show()

# Plot departures
plt.figure(figsize=(8, 6))
plt.plot(arrivals, np.sum(departures, axis=0), label='Departures', linestyle='-', marker='o')
plt.xlabel('Time')
plt.ylabel('Count')
plt.title('Departures Over Time')
plt.legend()
plt.grid(True)
plt.show()

# Calculate average wait time at different time points
average_wait_times = []
for i in range(len(queue_length_over_time)):
    if i == 0:
        average_wait_times.append(0)  # Initial wait time is 0
    else:
        # Calculate average wait time up to the current time
        average_wait_times.append(np.mean(queue_length_over_time[:i]))

# Generate time range based on arrivals
time_range = np.linspace(0, max(arrivals), len(average_wait_times))

# Plotting average wait time over time
plt.figure(figsize=(8, 6))
plt.plot(time_range, average_wait_times)
plt.title('Average Wait Time Over Time')
plt.xlabel('Time')
plt.ylabel('Average Wait Time')
plt.grid(True)
plt.show()


def calculate_server_utilization(arrivals, departures, num_servers, sim_time):
    server_utilization = np.zeros(sim_time)
    for i in range(sim_time):
        for j in range(num_servers):
            if arrivals[i] >= departures[j, i]:  # Index departures correctly
                server_utilization[i] += 1
    server_utilization /= num_servers  # Calculate average utilization
    return server_utilization

# Set your simulation parameters
#arrival_rate = 5
#service_rate = 7
#num_servers = 3
sim_time = 500

arrivals, departures, queue_length_over_time = generate_infinite_queue(arrival_rate, service_rate, num_servers, sim_time)

# Calculate server utilization over time
server_utilization = calculate_server_utilization(arrivals, departures, num_servers, sim_time)
time = 400
# Plot Server Utilization Over Time
plt.figure(figsize=(8, 6))
plt.plot(server_utilization)
plt.title('Server Utilization Over Time')
plt.xlabel('Time')
plt.ylabel('Utilization')
plt.grid(True)
plt.show()


# %%



def calculate_server_utilization(arrivals, departures, num_servers, sim_time):
    server_utilization = np.zeros(sim_time)
    for i in range(sim_time):
        for j in range(num_servers):
            if arrivals[i] >= departures[j, i]:  # Index departures correctly
                server_utilization[i] += 1
    server_utilization /= num_servers  # Calculate average utilization
    return server_utilization

# Set your simulation parameters
arrival_rate = 5
service_rate = 7
num_servers = 3
sim_time = 1000

# Generate infinite queue simulation data
arrivals, departures, queue_length_over_time = generate_infinite_queue(arrival_rate, service_rate, num_servers, sim_time)

# Calculate server utilization over time
server_utilization = calculate_server_utilization(arrivals, departures, num_servers, sim_time)

# Plot Server Utilization Over Time
plt.figure(figsize=(8, 6))
plt.plot(server_utilization)
plt.title('Server Utilization Over Time')
plt.xlabel('Time')
plt.ylabel('Utilization')
plt.grid(True)
plt.show()
# %%
