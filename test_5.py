
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
        self.queue_length = []

    def customer_arrival(self):
        while True:
            yield self.env.timeout(random.expovariate(1.0 / self.inter_arrival_time))
            self.total_customers += 1
            self.arrival_times.append(self.env.now)
            self.queue_length.append(len(self.server.queue) + len(self.server.users))
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
        plt.figure(figsize=(12, 6))

        plt.subplot(1, 2, 1)
        plt.step(self.arrival_times, range(len(self.arrival_times)), label='Arrival', where='post')
        plt.step(self.departure_times, range(len(self.departure_times)), label='Departure', where='post')
        plt.xlabel('Time')
        plt.ylabel('Number of Customers')
        plt.title('Arrivals and Departures')
        plt.legend()

        plt.subplot(1, 2, 2)
        plt.step(self.arrival_times, self.queue_length, where='post')
        plt.xlabel('Time')
        plt.ylabel('Queue Length')
        plt.title('Queue Length over Time')

        plt.tight_layout()
        plt.show()


# Simulation parameters
SIM
