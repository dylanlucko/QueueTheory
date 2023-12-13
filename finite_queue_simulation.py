

#%%
import simpy
import random

class QueueSystem:
    def __init__(self, env, c, K, Ri, Rp):
        self.env = env
        self.servers = simpy.Resource(env, capacity=c)
        self.queue = simpy.FilterStore(env, capacity=K)
        self.Ri = Ri
        self.Rp = Rp
        self.lost_customers = 0

    def customer_arrival(self):
        while True:
            yield self.env.timeout(random.expovariate(self.Ri))
            if len(self.queue.items) + len(self.servers.users) < self.queue.capacity + self.servers.capacity:
                self.env.process(self.customer_service())

    def customer_service(self):
        with self.servers.request() as request:
            yield request
            if len(self.queue.items) > 0:
                customer = self.queue.get()
                service_time = random.expovariate(self.Rp)
                yield self.env.timeout(service_time)
            else:
                service_time = random.expovariate(self.Rp)
                yield self.env.timeout(service_time)

    def run_simulation(self, sim_time):
        self.env.process(self.customer_arrival())
        self.env.run(until=sim_time)
        self.lost_customers = len(self.queue.items)

# Inputs
c = 1  # Number of servers
K = 3  # Maximum queue size
Ri = 4  # Arrival rate of customers
Rp = 6  # Service rate of each server

# Simulation time
simulation_time = 100

# Run simulation
env = simpy.Environment()
queue_system = QueueSystem(env, c, K, Ri, Rp)
queue_system.run_simulation(simulation_time)

# Results
print(f"Customers lost: {queue_system.lost_customers}")

# %%
#### Version 2
################

#%%
import simpy
import random

class QueueSystem:
    def __init__(self, env, c, K, Ri, Rp):
        self.env = env
        self.servers = simpy.Resource(env, capacity=c)
        self.queue = simpy.FilterStore(env, capacity=K)
        self.Ri = Ri
        self.Rp = Rp
        self.lost_customers = 0
        self.total_customers = 0
        self.total_time_spent_in_queue = 0

    def customer_arrival(self):
        while True:
            yield self.env.timeout(random.expovariate(self.Ri))
            if len(self.queue.items) + len(self.servers.users) < self.queue.capacity + self.servers.capacity:
                self.total_customers += 1
                self.env.process(self.customer_service())

    def customer_service(self):
        arrival_time = self.env.now
        with self.servers.request() as request:
            yield request
            if len(self.queue.items) > 0:
                customer = self.queue.get()
                service_time = random.expovariate(self.Rp)
                yield self.env.timeout(service_time)
                self.total_time_spent_in_queue += self.env.now - arrival_time
            else:
                service_time = random.expovariate(self.Rp)
                yield self.env.timeout(service_time)

    def run_simulation(self, sim_time):
        self.env.process(self.customer_arrival())
        self.env.run(until=sim_time)
        self.lost_customers = len(self.queue.items)

    def calculate_balk_probability(self):
        return self.lost_customers / self.total_customers if self.total_customers > 0 else 0

    def calculate_average_rate_joining_system(self):
        Pb = self.calculate_balk_probability()
        return self.Ri - (1 - Pb)

    def calculate_average_leaving_rate_without_service(self):
        return self.Ri - self.calculate_average_rate_joining_system()

    def calculate_average_number_waiting_in_queue(self):
        return len(self.queue.items) / self.env.now

    def calculate_average_waiting_time(self):
        Ii = self.calculate_average_number_waiting_in_queue()
        if Ii == 0:
            return float('inf')  # No customers waiting, so waiting time is infinite
        else:
            return self.calculate_average_rate_joining_system() / Ii

#%%
# Inputs
c = 1  # Number of servers
K = 4  # Maximum queue size
Ri = 4  # Arrival rate of customers
Rp = 6  # Service rate of each server

# Simulation time
simulation_time = 10

# Run simulation
env = simpy.Environment()
queue_system = QueueSystem(env, c, K, Ri, Rp)
queue_system.run_simulation(simulation_time)

# Calculate metrics
Pb = queue_system.calculate_balk_probability()
R = queue_system.calculate_average_rate_joining_system()
R_without_service = queue_system.calculate_average_leaving_rate_without_service()
Ii = queue_system.calculate_average_number_waiting_in_queue()
Ti = queue_system.calculate_average_waiting_time()

# Results
print(f"Customers lost (Balked): {queue_system.lost_customers}")
print(f"Customers who Balk (Pb): {Pb}")
print(f"Average Rate Joining System (R): {R}")
print(f"Average leaving rate without service (Ri-R): {R_without_service}")
print(f"Average number waiting in Queue (Ii): {Ii}")
print(f"Average waiting time (Ti): {Ti}")

# %%
###############
# Version 3
###############
class QueueSystem:
    def __init__(self, c, K, Ri, Rp):
        self.c = c
        self.K = K
        self.Ri = Ri
        self.Rp = Rp
        self.lost_customers = 0
        self.total_customers = 0

    def simulate(self, simulation_time):
        current_time = 0
        while current_time < simulation_time:
            if self.total_customers < self.K + self.c:
                self.total_customers += 1
                if self.total_customers > self.c:
                    if random.random() > (self.K / (self.K + self.c)):
                        self.lost_customers += 1
                        self.total_customers -= 1

            if self.total_customers > 0 and random.random() < (self.Rp / (self.Ri)):
                self.total_customers -= 1
            
            current_time += 1  # Increment time (adjust as needed based on time unit)


    def calculate_balk_probability(self):
        return (self.lost_customers / self.total_customers) * 100 if self.total_customers > 0 else 0

    def calculate_average_rate_joining_system(self):
        Pb = self.calculate_balk_probability() / 100
        return self.Ri - (1 - Pb)

    def calculate_average_leaving_rate_without_service(self):
        return self.Ri - self.calculate_average_rate_joining_system()

    def calculate_average_number_waiting_in_queue(self):
        return max(0, self.total_customers - self.c)

    def calculate_average_waiting_time(self):
        Ii = self.calculate_average_number_waiting_in_queue()
        if Ii == 0:
            return float('inf')  # No customers waiting, so waiting time is infinite
        else:
            return 1 / (self.Ri - self.calculate_average_rate_joining_system())
#%%
# Inputs
c = 1  # Number of servers
K = 4  # Maximum queue size
Ri = 4  # Arrival rate of customers
Rp = 6  # Service rate of each server
simulation_time = 10
# Initialize queue system
queue_system = QueueSystem(c, K, Ri, Rp)

# Run simulation
queue_system.simulate(simulation_time)

# Calculate metrics
Pb = queue_system.calculate_balk_probability()
R = queue_system.calculate_average_rate_joining_system()
R_without_service = queue_system.calculate_average_leaving_rate_without_service()
Ii = queue_system.calculate_average_number_waiting_in_queue()
Ti = queue_system.calculate_average_waiting_time()

# Results
print(f"Customers who Balk (Pb): {Pb:.2f}%")
print(f"Average Rate Joining System (R): {R:.5f}")
print(f"Average leaving rate without service (Ri-R): {R_without_service:.5f}")
print(f"Average number waiting in Queue (Ii): {Ii:.3f}")
print(f"Average waiting time (Ti): {Ti:.5f}")

# %%
################
################
################
import random

class QueueSystem:
    def __init__(self, c, K, Ri, Rp):
        self.c = c
        self.K = K
        self.Ri = Ri
        self.Rp = Rp
        self.balked_customers = 0
        self.total_attempted_customers = 0
        self.customers_in_queue = 0

    def simulate(self, simulation_time):
        current_time = 0
        while current_time < simulation_time:
            if self.total_attempted_customers < simulation_time * self.Ri:
                self.total_attempted_customers += 1
                if self.customers_in_queue < self.K + self.c:
                    self.customers_in_queue += 1
                else:
                    self.balked_customers += 1

            if self.customers_in_queue > 0 and random.random() < (self.Rp / self.Ri):
                self.customers_in_queue -= 1
            
            current_time += 1  # Increment time (adjust as needed based on time unit)

    def calculate_balk_probability(self):
        return (self.balked_customers / self.total_attempted_customers) * 100 if self.total_attempted_customers > 0 else 0

    # Other calculation methods...

# Inputs
c = 1  # Number of servers
K = 4  # Maximum queue size
Ri = 4  # Arrival rate of customers
Rp = 6  # Service rate of each server
simulation_time = 10000  # Duration of simulation

# Initialize queue system
queue_system = QueueSystem(c, K, Ri, Rp)

# Run simulation with a specified time
queue_system.simulate(simulation_time)

# Calculate Pb and print the result
Pb = queue_system.calculate_balk_probability()
print(f"Customers who Balk (Pb): {Pb:.2f}%")

# %%
def calculate_balk_probability(c, K, Ri, Rp):
    if K >= c:
        return ((K - c) / (K + c)) * (Ri / Rp) * 100
    else:
        return 0

# Inputs
c = 1  # Number of servers
K = 4  # Maximum queue size
Ri = 4  # Arrival rate of customers
Rp = 6  # Service rate of each server

# Calculate Pb
Pb = calculate_balk_probability(c, K, Ri, Rp)
print(f"Customers who Balk (Pb): {Pb:.2f}%")


# %%
def calculate_average_rate_joining_system(c, K, Ri, Rp):
    Pb = calculate_balk_probability(c, K, Ri, Rp)
    return Ri - (1 - (Pb / 100))

def calculate_average_rate_leaving_without_service(Ri, Pb):
    return Ri * (Pb / 100)

def calculate_average_number_waiting_in_queue(c, K, Ri, Rp):
    return (K - c) * (Ri / Rp)

def calculate_average_waiting_time(Ri, Pb):
    return (1 / Ri) * (Pb / 100)

def calculate_probability_of_more_than_q_customers_waiting(c, K, Ri, Rp, q):
    Pb = calculate_balk_probability(c, K, Ri, Rp)
    return (K - c) / (K + c) * (Ri / Rp) ** q

# Inputs
c = 1  # Number of servers
K = 4  # Maximum queue size
Ri = 4  # Arrival rate of customers
Rp = 6  # Service rate of each server

# Calculate metrics
Pb = calculate_balk_probability(c, K, Ri, Rp)
R = calculate_average_rate_joining_system(c, K, Ri, Rp)
RiPb = calculate_average_rate_leaving_without_service(Ri, Pb)
Ii = calculate_average_number_waiting_in_queue(c, K, Ri, Rp)
Ti = calculate_average_waiting_time(Ri, Pb)
Q = calculate_probability_of_more_than_q_customers_waiting(c, K, Ri, Rp, 0) * 100  # Probability of more than 0 customers waiting

# Results
print(f"Customers who Balk (Pb): {Pb:.2f}%")
print(f"Average Rate Joining System (R): {R:.9f}")
print(f"Average Rate Leaving Without Service (RiPb): {RiPb:.9f}")
print(f"Average Number Waiting in Queue (Ii): {Ii:.3f}")
print(f"Average Waiting Time (Ti): {Ti:.9f}")
print(f"Q: Probability of more than 0 customers waiting: {Q:.1f}%")

# %%


# %%
import math

def calculate_full_probability(arrival_rate, service_rate, num_servers, queue_capacity):
    traffic_intensity = arrival_rate / (service_rate * num_servers)
    
    numerator = (traffic_intensity ** num_servers) / math.factorial(num_servers)
    
    denominator_sum = sum([(traffic_intensity ** n) / math.factorial(n) for n in range(queue_capacity)])
    denominator_last_term = (traffic_intensity ** queue_capacity) / math.factorial(queue_capacity)
    
    probability_full = numerator / (denominator_sum + denominator_last_term)
    return probability_full

# Example values
arrival_rate = 4  # Replace with your arrival rate
service_rate = 6  # Replace with your service rate
num_servers = 1    # Replace with the number of servers
queue_capacity = 4  # Replace with the queue capacity

result = calculate_full_probability(arrival_rate, service_rate, num_servers, queue_capacity)
print(f"The probability that the system is full: {result:.4f}")

# %%
lam = 4
mu = 6
c= 1
K = 4

frac1 = ((lam/mu)**c)/((math.factorial(c)))
#%%
frac2 = ((lam/mu**n)/ (math.factorial(n))) + ((lam/mu)**K/ (math.factorial(K)))

# %%
import math

def calculate_expression_sum(lam, mu, K):
    expression_sum = sum(((lam / mu) ** n) / math.factorial(n) for n in range(K))
    expression_sum += ((lam / mu) ** K) / math.factorial(K)
    return expression_sum

# Example values
lam = 4  # Replace with your value for lambda
mu = 6   # Replace with your value for mu
K = 3    # Replace with your value for K

frac2 = calculate_expression_sum(lam, mu, K)
print(f"The sum of the expression is: {frac2:.4f}")

# %%
(frac1/frac2)*100
# %%
n_0 = 0
n_1= 1
n_2= 2
n_3= 3



frac2_0 = ((lam/mu**n_0)/ (math.factorial(n_0))) 
print(frac2_0)
#%%
frac2_1 = ((lam/mu**n_1)/ (math.factorial(n_1))) 
print(frac2_1)

#%%
frac2_2 = ((lam/mu**n_2)/ (math.factorial(n_2))) 
print(frac2_2)

#%%
frac2_3 = ((lam/mu**n_3)/ (math.factorial(n_3))) 
print(frac2_3)

#%%
# %%
frac2 = frac2_0+frac2_1+frac2_2+frac2_3
print(frac2)


#%%
frac2_a = frac2 +  ((lam/mu)**K/ (math.factorial(K)))


#%%
frac1/frac2_a
# %%
frac2

#%%
import math

# Given values
lam = 4
mu = 6
K = 4
c = 1

# Calculate the traffic intensity
traffic_intensity = lam / mu

# Calculate the numerator: ((λ/μ)^c / c!)
numerator = (traffic_intensity ** c) / math.factorial(c)

# Calculate the denominator terms: Σ(λ/μ)^n / n! for n = 0 to K-1 and (λ/μ)^K / K!
denominator_sum = sum((traffic_intensity ** n) / math.factorial(n) for n in range(K))
denominator_last_term = (traffic_intensity ** K) / math.factorial(K)

# Calculate P_full
P_full = numerator / (denominator_sum + denominator_last_term)

# Convert to percentage for comparison
P_full_percentage = P_full * 100

print(f"The probability that the system is full: {P_full_percentage:.2f}%")

# %%
import math

# Given values
lam = 4
mu = 6
K = 4
c = 1

# Calculate the traffic intensity
traffic_intensity = lam / mu

# Calculate the numerator: ((λ/μ)^c / c!)
numerator = ((traffic_intensity ** c) / math.factorial(c))

# Calculate the denominator terms: Σ(λ/μ)^n / n! for n = 0 to c-1 and (λ/μ)^c / c!
denominator_sum = sum((traffic_intensity ** n) / math.factorial(n) for n in range(c))
denominator_last_term = (traffic_intensity ** c) / math.factorial(c)

# Calculate P_full
P_full = numerator / (denominator_sum + denominator_last_term)

# Convert to percentage for comparison
P_full_percentage = P_full * 100

print(f"The probability that the system is full: {P_full_percentage:.2f}%")

# %%import math

# Given values
lam = 4
mu = 6
K = 4
c = 1

# Calculate the traffic intensity
traffic_intensity = lam / mu

# Calculate the numerator: ((λ/μ)^c / c!)
numerator = (traffic_intensity ** c) / math.factorial(c)

# Calculate the denominator terms: Σ(λ/μ)^n / n! for n = 0 to c-1 and (λ/μ)^c / c!
denominator_sum = sum((traffic_intensity ** n) / math.factorial(n) for n in range(c))
denominator_last_term = (traffic_intensity ** c) / math.factorial(c)

# Calculate P_full
P_full = numerator / (denominator_sum + denominator_last_term)

# Convert to percentage for comparison
P_full_percentage = P_full * 100

print(f"The probability that the system is full (using Erlang-A): {P_full_percentage:.2f}%")


# %%
import math

# Given values
lam = 4
mu = 6
K = 4
c = 1

# Calculate the traffic intensity
traffic_intensity = lam / (c * mu)

# Calculate the Erlang-R formula for P_full
numerator = (c * traffic_intensity) ** c / math.factorial(c)
denominator_sum = sum(((c * traffic_intensity) ** n) / math.factorial(n) for n in range(c))
denominator_last_term = ((c * traffic_intensity) ** c) / (math.factorial(c) * (1 - traffic_intensity))

P_full = numerator / (denominator_sum + denominator_last_term)

# Convert to percentage for comparison
P_full_percentage = P_full * 100

print(f"The probability that the system is full (using Erlang-R): {P_full_percentage:.2f}%")

# %%
def queue_p_full(lam, mu, s, m):
    rho = lam / mu
    term = 1
    po = 1
    
    for k in range(1, s + m + 1):
        term *= rho / min(k, s)
        po += term
    
    return term / po

# Example usage with given values: lam=4, mu=6, s=1, m=3
lam = 4
mu = 6
s = 1
m = 4

result = queue_p_full(lam, mu, s, m)
print(f"The probability that the system is full: {result:.4f}")

# %%
def queue_p_full(lam, mu, s, m):
    rho = lam / mu
    term = 1
    po = 1
    
    for k in range(1, s + m + 1):
        term *= rho / min(k, s)
        po += term
    
    return term / po

def calculate_average_rate_joining_system(lam, mu, s, m):
    Pb = queue_p_full(lam, mu, s, m)
    return lam * (1 - Pb)

def calculate_average_rate_leaving_without_service(lam, mu, s, m):
    Pb = queue_p_full(lam, mu, s, m)
    return lam -  (lam * (1 - Pb))

def calculate_average_number_waiting_in_queue(lam, mu, s, m):
    r = lam / mu
    term = 1
    fq = 0
    po = 1
    for k in range(1, s + m + 1):
        term *= r / min(k, s)
        po += term
        fq += term * max(0, k - s)
    return fq / po


def calculate_average_waiting_time(lam, mu, s, m):
    rho = lam / mu
    return (rho ** (s + 1)) / (mu * (s * (1 - rho))) if rho < 1 else float('inf')


# Inputs
lam = 4  # Arrival rate of customers
mu = 6  # Service rate of each server
s = 1  # Number of servers
m = 4 # Maximum queue size

# Calculate metrics
R = calculate_average_rate_joining_system(lam, mu, s, m)
RiPb = calculate_average_rate_leaving_without_service(lam, mu, s, m)
Ii = calculate_average_number_waiting_in_queue(lam, mu, s, m)
Ti = calculate_average_waiting_time(lam, mu, s, m)
Pb = queue_p_full(lam, mu, s, m)

# Results
print(f"Average Rate Joining System (R): {R:.4f}")
print(f"Average Rate Leaving Without Service (RiPb): {RiPb:.4f}")
print(f"Average Number Waiting in Queue (Ii): {Ii:.4f}")
print(f"Average Waiting Time (Ti): {Ti:.4f}")
print(f"Probability that System is Full (Pb): {Pb*100:.4f}%")

# %%
