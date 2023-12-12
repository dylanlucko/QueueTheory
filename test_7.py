
#%%
from random import expovariate, seed
import simpy
#%%

class Source(simpy.Process):
    """Source generates customers randomly"""

    def __init__(self, env, *args, **kwargs):
        super().__init__(env=env, *args, **kwargs)
        self.env = env

    def generate(self, number, meanTBA, resource):
        for i in range(number):
            c = Customer(name="Customer%02d" % (i,))
            self.env.process(c.visit(b=resource))
            t = expovariate(1.0 / meanTBA)
            yield self.env.timeout(t)

    def run(self, number, meanTBA, resource):
        self.env.process(self.generate(number, meanTBA, resource))

class Customer(simpy.Process):
    """Customer arrives, is served, and leaves"""

    def __init__(self, env, *args, **kwargs):
        super().__init__(env=env, *args, **kwargs)
        self.env = env

    def visit(self, b):
        arrive = self.env.now
        print("%8.4f %s: Here I am" % (self.env.now, self.name))
        with b.request() as req:
            yield req
            wait = self.env.now - arrive
            print("%8.4f %s: Waited %6.3f" % (self.env.now, self.name, wait))
            tib = expovariate(1.0 / timeInBank)
            yield self.env.timeout(tib)
        print("%8.4f %s: Finished" % (self.env.now, self.name))

# Experiment data
maxNumber = 5
maxTime = 400.0  # minutes
timeInBank = 12.0  # mean, minutes
ARRint = 10.0  # mean, minutes
theseed = 12345

# Model/Experiment
seed(theseed)
env = simpy.Environment()
k = simpy.Resource(env, capacity=1)

s = Source(env)
env.process(s.run(number=maxNumber, meanTBA=ARRint, resource=k))
env.run(until=maxTime)
# %%
