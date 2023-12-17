
#%%
import matplotlib.pyplot as plt
import tkinter as tk
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import random


#%%
class QueueMetrics:
    def __init__(self, lam, mu, s, m, x_t, x_q):
        self.lam = lam
        self.mu = mu
        self.s = s
        self.m = m
        self.x_t  = x_t
        self.x_q = x_q
        self.utilization_over_time = []  # Store utilization values here
        
    def queue_p_full(self):
        rho = self.lam / self.mu
        term = 1
        po = 1
        
        for k in range(1, self.s + self.m + 1):
            term *= rho / min(k, self.s)
            po += term
        return term / po


    def average_number_waiting_infinite(self):
        r = self.lam / self.mu
        rho = r / self.s
        term = (1 - rho) / rho
        Q = term
        
        for k in range(1, self.s):
            term *= (self.s - k) / r
            Q += term
        
        return (rho / (1 - rho)) / (1 + Q)
    
    def average_time_waiting_infinite(self):
        r = self.lam / self.mu
        rho = r / self.s
        term = (1 - rho) / rho
        Q = term
        
        for k in range(1, self.s):
            
            term *= (self.s - k) / r
            Q += term
        Ii = (rho / (1 - rho)) / (1 + Q)
        Ti = Ii/self.lam
        return Ti
    
    def calculate_average_server_utilization(self):
        AUS = (self.lam)/ (self.s*self.mu)
        return AUS
    
    
    def average_num_customers_receiving_service(self):
        AUS = (self.lam)/ (self.s*self.mu)
        Ip_infinite=AUS*self.s
        return Ip_infinite
    
    def average_num_in_system(self):
        r = self.lam / self.mu
        rho = r / self.s
        term = (1 - rho) / rho
        Q = term
        AUS = (self.lam)/ (self.s*self.mu)
        for k in range(1, self.s):
            
            term *= (self.s - k) / r
            Q += term
        Ii = (rho / (1 - rho)) / (1 + Q)
        return Ii +self.s*AUS
    
    #def average_time_in_system(self):
        #AUS = (self.lam)/ (self.s*self.mu)
        
    #    return I_infinite / self.lam
    
    def customer_probability(self):
        r = self.lam / self.mu
        rho = r / self.s
        term = (1 - rho) / rho
        Q = term
        
        for k in range(1, self.s):
            term *= (self.s - k) / r
            Q += term
        Ii = (rho / (1 - rho)) / (1 + Q)
        AUS = (self.lam)/ (self.s*self.mu)
        return ((1 - AUS )*Ii *AUS**self.x_q)
    
    def time_probability(self):
        r = self.lam / self.mu
        rho = r / self.s
        term = (1 - rho) / rho
        Q = term
        
        for k in range(1, self.s):
            term *= (self.s - k) / r
            Q += term
        Ii = (rho / (1 - rho)) / (1 + Q)
        AUS = (self.lam)/ (self.s*self.mu)
        return ((1 - AUS )/AUS *Ii*math.exp((self.lam-self.s*self.mu)*self.x_t))
    
    def calculate_queue_length_at_time(self, t):
        lam = self.lam
        mu = self.mu
        s = self.s

        # Checking if time (t) is non-negative
        if t < 0:
            return 0
        
        rho = lam / mu
        if rho >= 1:
            return s
        
        p0 = 1
        for i in range(s):
            p0 += (rho ** i) / math.factorial(i)
        
        p0 = 1 / p0

        queue_length = 0
        if t == 0:
            return queue_length
        
        for k in range(1, s + 1):
            queue_length += k * ((rho ** k) / math.factorial(k)) * p0
        
        queue_length += s * ((rho ** s) / (math.factorial(s) * (1 - rho)))

        return queue_length
    
    def queue_length_over_time(self, time_points):
        # Calculate queue lengths at different time points
        queue_lengths = []
        for t in time_points:
            queue_length_at_t = self.calculate_queue_length_at_time(t)
            queue_lengths.append(queue_length_at_t)
        return queue_lengths
    
    def plot_server_utilization(self, arrival_rates, service_rates):
        AUS_values = []
        for lam, mu in zip(arrival_rates, service_rates):
            self.lam = lam
            self.mu = mu
            AUS_values.append(self.calculate_average_server_utilization())
            
    def calculate_server_utilization_over_time(self, time_points):
        self.utilization_over_time.clear()  # Clear previous values if any
        for t in time_points:
            utilization = self.calculate_server_utilization_at_time(t)
            self.utilization_over_time.append(utilization)
        return self.utilization_over_time

    # Calculate server utilization at a specific time
    def calculate_server_utilization_at_time(self, t):
        # Your logic to calculate server utilization at time 't'
        # For example:
        if t < 0:
            return 0
        return (self.lam * t) / (self.s * self.mu)
    
    def simulate_real_time_utilization(self, total_time, time_interval):
        self.utilization_over_time.clear()
        current_time = 0

        while current_time <= total_time:
            # Calculate server utilization at current time
            utilization = self.calculate_server_utilization_at_time(current_time)
            self.utilization_over_time.append(utilization)

            # Update the GUI with the current server utilization
            self.update_gui_utilization(utilization)

            # Update current time
            current_time += time_interval

            # Sleep to create a delay for real-time simulation
            time.sleep(time_interval)
            
    def simulate_queue(self, total_time):
        current_time = 0
        while current_time <= total_time:
            # Simulate arrivals based on Poisson process
            inter_arrival_time = random.expovariate(self.lam)
            current_time += inter_arrival_time

            # Check if the next arrival time exceeds the total simulation time
            if current_time > total_time:
                break

            # Simulate a customer arrival at current_time
            self.events.append({'type': 'arrival', 'time': current_time})

            # Simulate service times based on exponential distribution
            for _ in range(self.num_servers):
                service_time = random.expovariate(self.mu)
                service_completion_time = current_time + service_time
                self.events.append({'type': 'departure', 'time': service_completion_time})

            # Sort the events based on time
            self.events.sort(key=lambda x: x['time'])
            
    def plot_queue_length_over_time(self):
        # Sort events based on time
        self.events.sort(key=lambda x: x['time'])

        time_points = []
        queue_lengths = []
        current_queue = 0

        for event in self.events:
            time_points.append(event['time'])
            if event['type'] == 'arrival':
                current_queue += 1
            else:
                current_queue -= 1
            queue_lengths.append(current_queue)

        plt.figure(figsize=(8, 6))
        plt.plot(time_points, queue_lengths)
        plt.title('Queue Length over Time')
        plt.xlabel('Time')
        plt.ylabel('Queue Length')
        plt.grid(True)
        plt.show()
        
    

#%%
# Create an instance of QueueMetrics
queue = QueueMetrics(lam=40, mu=60, s=2, m=0, x_t=0.1, x_q=0)

# Calculate queue length over time
time_points = [t for t in range(100)]  # Time points
queue_lengths = queue.queue_length_over_time(time_points)

# Plot queue length over time
plt.figure(figsize=(8, 6))
plt.plot(time_points, queue_lengths)
plt.title('Queue Length over Time')
plt.xlabel('Time')
plt.ylabel('Queue Length')
plt.grid(True)
plt.show()

# Calculate server utilization over time
utilization_values = queue.calculate_server_utilization_over_time(time_points)

# Plot server utilization over time
plt.figure(figsize=(8, 6))
plt.plot(time_points, utilization_values)
plt.title('Server Utilization over Time')
plt.xlabel('Time')
plt.ylabel('Server Utilization')
plt.grid(True)
plt.show()

# %%
import matplotlib.pyplot as plt

def plot_queue_length_over_time(events):
    events.sort(key=lambda x: x['time'])

    time_points = []
    queue_lengths = []
    current_queue = 0

    for event in events:
        time_points.append(event['time'])
        if event['type'] == 'arrival':
            current_queue += 1
        else:
            current_queue -= 1
        queue_lengths.append(current_queue)

    plt.figure(figsize=(8, 6))
    plt.plot(time_points, queue_lengths)
    plt.title('Queue Length over Time')
    plt.xlabel('Time')
    plt.ylabel('Queue Length')
    plt.grid(True)
    plt.show()

# %%

def generate_events(arrival_rate, service_rate, num_servers, sim_time):
    events = []
    arrival_time = 0
    departure_time = float('inf')

    while arrival_time < sim_time:
        if arrival_time < departure_time:
            events.append({'time': arrival_time, 'type': 'arrival'})
            arrival_time += random.expovariate(arrival_rate)
        else:
            events.append({'time': departure_time, 'type': 'departure'})
            departure_time += random.expovariate(service_rate * num_servers)

    return events

# Parameters
arrival_rate = 0.4
service_rate = 0.2
num_servers = 2
simulation_time = 100

# Generate events
events = generate_events(arrival_rate, service_rate, num_servers, simulation_time)

# Plot the queue length over time
plot_queue_length_over_time(events)
# %%
