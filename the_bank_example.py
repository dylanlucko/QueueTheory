

#%%
import simpy

class Customer:
    """Customer arrives, looks around, and leaves"""

    def __init__(self, env, name):
        self.env = env
        self.name = name

    def visit(self, time_in_bank):
        print(self.env.now, self.name, "Here I am")
        yield self.env.timeout(time_in_bank)
        print(self.env.now, self.name, "I must leave")

# Experiment data
max_time = 100.0  # minutes
time_in_bank = 10.0  # minutes

# Model/Experiment
env = simpy.Environment()

c = Customer(env, name="Klaus")
env.process(c.visit(time_in_bank))

env.run(until=max_time)

# %%
import simpy
from random import expovariate, seed
#%%
import simpy
from random import expovariate, seed

class Customer:
    """Customer arrives at a random time, looks around, and then leaves"""

    def __init__(self, env, name):
        self.env = env
        self.name = name

    def visit(self, time_in_bank):
        print(self.env.now, self.name, "Here I am")
        yield self.env.timeout(time_in_bank)
        print(self.env.now, self.name, "I must leave")

# Experiment data
max_time = 100.0  # minutes
time_in_bank = 10.0  # minutes

# Model/Experiment
seed(99999)
env = simpy.Environment()

def customer_generator(env):
    c = Customer(env, name="Klaus")
    while True:
        t = expovariate(1.0 / 5.0)
        yield env.timeout(t)
        env.process(c.visit(time_in_bank))

env.process(customer_generator(env))
env.run(until=max_time)


# %%
import simpy
import simpy

class Customer:
    """Customer arrives, looks around, and leaves"""

    def __init__(self, env, name, time_in_bank):
        self.env = env
        self.name = name
        self.time_in_bank = time_in_bank

    def visit(self):
        print(f"{self.env.now:.4f} {self.name}: Here I am")
        yield self.env.timeout(self.time_in_bank)
        print(f"{self.env.now:.4f} {self.name}: I must leave")

def delayed_arrival(env, customer, arrival_time):
    yield env.timeout(arrival_time)
    env.process(customer.visit())

# Experiment data
max_time = 400.0  # minutes
time_in_bank = [10.0, 7.0, 20.0]
arrival_times = [5.0, 2.0, 12.0]
customer_names = ["Klaus", "Tony", "Evelyn"]

# Model/Experiment
env = simpy.Environment()

customers = [Customer(env, name, time_in_bank[i]) for i, name in enumerate(customer_names)]

for customer, arrival_time in zip(customers, arrival_times):
    env.process(customer.visit())
    env.process(delayed_arrival(env, customer, arrival_time))

env.run(until=max_time)


# %%
import simpy

class Source:
    """Source generates customers regularly"""

    def __init__(self, env):
        self.env = env

    def generate(self, number, tba):
        for i in range(number):
            c = Customer(self.env, name=f"Customer{str(i).zfill(2)}")
            self.env.process(c.visit(time_in_bank=12.0))
            yield self.env.timeout(tba)

class Customer:
    """Customer arrives, looks around, and leaves"""

    def __init__(self, env, name):
        self.env = env
        self.name = name

    def visit(self, time_in_bank):
        print(f"{self.env.now:.4f} {self.name}: Here I am")
        yield self.env.timeout(time_in_bank)
        print(f"{self.env.now:.4f} {self.name}: I must leave")

# Experiment data
max_number = 5
max_time = 400.0  # minutes
arrival_time = 10.0  # time between arrivals, minutes

# Model/Experiment
env = simpy.Environment()

s = Source(env)
env.process(s.generate(number=max_number, tba=arrival_time))

env.run(until=max_time)

# %%
import simpy
from random import expovariate, seed

class Source:
    """Source generates customers at random"""

    def __init__(self, env):
        self.env = env

    def generate(self, number, mean_tba):
        for i in range(number):
            c = Customer(self.env, name=f"Customer{str(i).zfill(2)}")
            self.env.process(c.visit(time_in_bank=12.0))
            t = expovariate(1.0 / mean_tba)
            yield self.env.timeout(t)

class Customer:
    """Customer arrives, looks around, and leaves"""

    def __init__(self, env, name):
        self.env = env
        self.name = name

    def visit(self, time_in_bank):
        print(f"{self.env.now:.4f} {self.name}: Here I am")
        yield self.env.timeout(time_in_bank)
        print(f"{self.env.now:.4f} {self.name}: I must leave")

# Experiment data
max_number = 5
max_time = 400.0  # minutes
arrival_interval = 10.0  # mean arrival interval, minutes

# Model/Experiment
seed(99999)
env = simpy.Environment()

s = Source(env)
env.process(s.generate(number=max_number, mean_tba=arrival_interval))

env.run(until=max_time)

# %%
import simpy
import random

class Source:
    """Source generates customers randomly"""

    def __init__(self, env, number, mean_tba, resource):
        self.env = env
        self.number = number
        self.mean_tba = mean_tba
        self.resource = resource

    def generate(self):
        for i in range(self.number):
            c = Customer(self.env, f"Customer{str(i).zfill(2)}")
            self.env.process(c.visit(time_in_bank=12.0, res=self.resource))
            t = random.expovariate(1.0 / self.mean_tba)
            yield self.env.timeout(t)

class Customer:
    """Customer arrives, is served, and leaves"""

    def __init__(self, env, name):
        self.env = env
        self.name = name

    def visit(self, time_in_bank, res):
        arrive = self.env.now
        print(f"{self.env.now:.3f} {self.name}: Here I am")

        with res.request() as req:
            yield req

            wait = self.env.now - arrive
            print(f"{self.env.now:.3f} {self.name}: Waited {wait:.3f}")

            yield self.env.timeout(time_in_bank)

        print(f"{self.env.now:.3f} {self.name}: Finished")

# Experiment data
max_number = 5
max_time = 400.0  # minutes
arrival_interval = 10.0  # mean, minutes

# Model/Experiment
env = simpy.Environment()
counter = simpy.Resource(env, capacity=1)

source = Source(env, max_number, arrival_interval, counter)
env.process(source.generate())

env.run(until=max_time)

# %%
#################################################
###### A server with a random service time ######
#################################################
import simpy
import random

class Source:
    """Source generates customers randomly"""

    def __init__(self, env, number, mean_tba, resource):
        self.env = env
        self.number = number
        self.mean_tba = mean_tba
        self.resource = resource

    def generate(self):
        for i in range(self.number):
            c = Customer(self.env, f"Customer{str(i).zfill(2)}")
            self.env.process(c.visit(self.resource))
            t = random.expovariate(1.0 / self.mean_tba)
            yield self.env.timeout(t)

class Customer:
    """Customer arrives, is served, and leaves"""

    def __init__(self, env, name):
        self.env = env
        self.name = name

    def visit(self, resource):
        arrive = self.env.now  # Record the arrival time
        print(f"{self.env.now:.4f} {self.name}: Here I am")

        with resource.request() as req:
            yield req

            wait = self.env.now - arrive  # Calculate the actual wait time
            print(f"{self.env.now:.4f} {self.name}: Waited {wait:.3f}")

            time_in_bank = random.expovariate(1.0 / 12.0)
            yield self.env.timeout(time_in_bank)

        print(f"{self.env.now:.4f} {self.name}: Finished")

# Experiment data
max_number = 50
max_time = 400.0  # minutes
mean_arrival_time = 10.0  # mean, minutes

# Model/Experiment
random.seed(12345)
env = simpy.Environment()
counter = simpy.Resource(env, capacity=1)

source = Source(env, max_number, mean_arrival_time, counter)
env.process(source.generate())

env.run(until=max_time)

# %%
###################################################
##### Several Service Counters, Single Queue ######
###################################################

import simpy
import random

class Source:
    """Source generates customers randomly"""

    def __init__(self, env, number, mean_tba, resource):
        self.env = env
        self.number = number
        self.mean_tba = mean_tba
        self.resource = resource

    def generate(self):
        for i in range(self.number):
            c = Customer(self.env, f"Customer{str(i).zfill(2)}")
            self.env.process(c.visit(self.resource))
            t = random.expovariate(1.0 / self.mean_tba)
            yield self.env.timeout(t)

class Customer:
    """Customer arrives, is served, and leaves"""

    def __init__(self, env, name):
        self.env = env
        self.name = name

    def visit(self, resource):
        arrive = self.env.now
        print(f"{self.env.now:.4f} {self.name}: Here I am")

        with resource.request() as req:
            yield req

            wait = self.env.now - arrive
            print(f"{self.env.now:.4f} {self.name}: Waited {wait:.3f}")

            time_in_bank = random.expovariate(1.0 / 12.0)
            yield self.env.timeout(time_in_bank)

        print(f"{self.env.now:.4f} {self.name}: Finished")

# Experiment data
max_number = 5
max_time = 400.0  # minutes
mean_arrival_time = 10.0  # mean, minutes

# Model/Experiment
random.seed(12345)
env = simpy.Environment()
counters = simpy.Resource(env, capacity=2, name="Counter", unitName="Clerk")

source = Source(env, max_number, mean_arrival_time, counters)
env.process(source.generate())

env.run(until=max_time)

# %%
import simpy
import random

class Source:
    """Source generates customers randomly"""

    def __init__(self, env, number, mean_tba, resource):
        self.env = env
        self.number = number
        self.mean_tba = mean_tba
        self.resource = resource

    def generate(self):
        for i in range(self.number):
            c = Customer(self.env, f"Customer{str(i).zfill(2)}")
            self.env.process(c.visit(self.resource))
            t = random.expovariate(1.0 / self.mean_tba)
            yield self.env.timeout(t)

class Customer:
    """Customer arrives, is served, and leaves"""

    def __init__(self, env, name):
        self.env = env
        self.name = name

    def visit(self, resource):
        arrive = self.env.now
        print(f"{self.env.now:.4f} {self.name}: Here I am")

        with resource.request() as req:
            yield req

            wait = self.env.now - arrive
            print(f"{self.env.now:.4f} {self.name}: Waited {wait:.3f}")

            time_in_bank = random.expovariate(1.0 / 12.0)
            yield self.env.timeout(time_in_bank)

        print(f"{self.env.now:.4f} {self.name}: Finished")

# Experiment data
max_number = 5
max_time = 400.0  # minutes
mean_arrival_time = 10.0  # mean, minutes

# Model/Experiment
random.seed(12345)
env = simpy.Environment()
counters = simpy.Resource(env, capacity=2)
counters.name = "Counter"
counters.unitName = "Clerk"

source = Source(env, max_number, mean_arrival_time, counters)
env.process(source.generate())

env.run(until=max_time)

# %%
