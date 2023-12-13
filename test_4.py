
#%%
import simpy
import random
import matplotlib.pyplot as plt
#%%
class QueueSystem:
    def __init__(self, env, inter_arrival_time, service_time):
        self.env = env
        self.server = simpy.Resource(env, capacity=1)  # Single server
        self.inter_arrival_time = inter_arrival_time
        self.service_time = service_time
        self.total_customers = 0
        self.waiting_time = 0
        self.arrival_times = []
        self.departure_times = []

    def customer_arrival(self):
        while True:
            yield self.env.timeout(random.expovariate(1.0 / self.inter_arrival_time))
            self.total_customers += 1
            self.arrival_times.append(self.env.now)
            self.env.process(self.serve_customer(self.total_customers))

    def serve_customer(self, customer):
        arrival_time = self.env.now
        with self.server.request() as request:
            yield request
            service_start_time = self.env.now
            yield self.env.timeout(random.uniform(self.service_time[0], self.service_time[1]))
            service_end_time = self.env.now

            self.waiting_time += service_start_time - arrival_time
            self.departure_times.append(service_end_time)

            print(f"Customer {customer} served from {service_start_time} to {service_end_time}")

    def run_simulation(self, sim_time):
        self.env.process(self.customer_arrival())
        self.env.run(until=sim_time)

    def plot_simulation(self):
        plt.figure(figsize=(10, 6))
        plt.step(self.arrival_times, range(len(self.arrival_times)), label='Arrival', where='post')
        plt.step(self.departure_times, range(len(self.departure_times)), label='Departure', where='post')
        plt.xlabel('Time')
        plt.ylabel('Number of Customers')
        plt.title('Queueing System Simulation')
        plt.legend()
        plt.show()


# Simulation parameters
SIM_TIME = 1000  # Simulation time
INTER_ARRIVAL_TIME = 5  # Mean inter-arrival time
SERVICE_TIME = (2, 4)  # Range for service time

# Create an environment and start the simulation
env = simpy.Environment()
queue_system = QueueSystem(env, INTER_ARRIVAL_TIME, SERVICE_TIME)
queue_system.run_simulation(SIM_TIME)

# Plot the simulation
queue_system.plot_simulation()

# Calculate average waiting time
avg_waiting_time = queue_system.waiting_time / queue_system.total_customers if queue_system.total_customers else 0
print(f"Average waiting time: {avg_waiting_time}")

# %%
