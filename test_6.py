#%%
import simpy
import random
import matplotlib.pyplot as plt

class QueueSystem:
    def __init__(self, env, inter_arrival_time, service_time, num_servers, queue_capacity):
        self.env = env
        self.servers = simpy.Resource(env, capacity=num_servers)  # Multiple servers
        self.inter_arrival_time = inter_arrival_time
        self.service_time = service_time
        self.queue = simpy.Store(env, capacity=queue_capacity)  # Limited queue capacity
        self.arrival_times = []
        self.departure_times = []
        self.waiting_times = []

    def customer_arrival(self):
        while True:
            yield self.env.timeout(random.expovariate(1.0 / self.inter_arrival_time))
            self.arrival_times.append(self.env.now)
            self.env.process(self.serve_customer())

    def serve_customer(self):
        arrival_time = self.env.now
        with self.servers.request() as request:
            yield request
            service_start_time = self.env.now
            yield self.env.timeout(random.uniform(*self.service_time))
            service_end_time = self.env.now

            self.waiting_times.append(service_start_time - arrival_time)

            self.departure_times.append(service_end_time)

            print(f"Customer served from {service_start_time} to {service_end_time}")

    def run_simulation(self, sim_time):
        self.env.process(self.customer_arrival())
        self.env.run(until=sim_time)

    def plot_simulation(self):
        plt.figure(figsize=(12, 6))

        plt.subplot(1, 2, 1)
        plt.step(self.arrival_times, range(len(self.arrival_times)), label='Arrival', where='post')
        plt.step(self.departure_times, range(len(self.departure_times)), label='Departure', where='post')
        plt.xlabel('Time')
        plt.ylabel('Number of Customers')
        plt.title('Arrivals and Departures')
        plt.legend()

        plt.subplot(1, 2, 2)
        plt.hist(self.waiting_times, bins=20, alpha=0.7)
        plt.xlabel('Waiting Time')
        plt.ylabel('Frequency')
        plt.title('Distribution of Waiting Times')

        plt.tight_layout()
        plt.show()


# Simulation parameters
SIM_TIME = 100  # Simulation time
INTER_ARRIVAL_TIME = 5  # Mean inter-arrival time
SERVICE_TIME = (2, 4)  # Range for service time
NUM_SERVERS = 2  # Number of servers
QUEUE_CAPACITY = 10  # Queue capacity

# Create an environment and start the simulation
env = simpy.Environment()
queue_system = QueueSystem(env, INTER_ARRIVAL_TIME, SERVICE_TIME, NUM_SERVERS, QUEUE_CAPACITY)
queue_system.run_simulation(SIM_TIME)

# Plot the simulation
queue_system.plot_simulation()
