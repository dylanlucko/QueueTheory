
###########################
##### START  HERE #########
###########################
##### CLICK  RUN ##########
########################### 



#%%

# Get user input for the number of servers
Number_of_Servers = int(input("Enter the number of servers: "))

# Get user input for queue capacity
Queue_Capacity = int(input("Enter the queue capacity: "))

# Get user input for arrival rate
Arrival_Rate = int(input("Enter the arrival rate: "))

# Get user input for service rate
Service_Rate = int(input("Enter the service rate: "))


#######################
#######################
#######################
#######################
#######################
#######################
#######################
#######################
#######################
#######################
#######################
#######################


class QueueMetrics:
    def __init__(self, lam, mu, s, m):
        self.lam = lam
        self.mu = mu
        self.s = s
        self.m = m

    def queue_p_full(self):
        rho = self.lam / self.mu
        term = 1
        po = 1
        
        for k in range(1, self.s + self.m + 1):
            term *= rho / min(k, self.s)
            po += term
        
        return term / po

    def calculate_average_rate_joining_system(self):
        Pb = self.queue_p_full()
        return self.lam * (1 - Pb)

    def calculate_average_rate_leaving_without_service(self):
        Pb = self.queue_p_full()
        return self.lam - (self.lam * (1 - Pb))

    def calculate_average_number_waiting_in_queue(self):
        r = self.lam / self.mu
        term = 1
        fq = 0
        po = 1
        
        for k in range(1, self.s + self.m + 1):
            term *= r / min(k, self.s)
            po += term
            fq += term * max(0, k - self.s)
        
        return fq / po

    def calculate_average_waiting_time(self):
        Ii = self.calculate_average_number_waiting_in_queue()
        R = self.calculate_average_rate_joining_system()
        return Ii / R if R != 0 else float('inf')

    def calculate_average_number_of_customers_served(self):
        return self.calculate_average_rate_joining_system() / self.mu

    def average_utilization_of_servers(self):
        Ip = self.calculate_average_number_of_customers_served()
        return Ip / self.s if self.s != 0 else 0

    def average_number_in_system(self):
        Ip = self.calculate_average_number_of_customers_served()
        Ii = self.calculate_average_number_waiting_in_queue()
        return Ip + Ii

    def average_time_in_system(self):
        I = self.average_number_in_system()
        R = self.calculate_average_rate_joining_system()
        return I / R if R != 0 else float('inf')


lam = Queue_Capacity  # Arrival rate of customers
mu = Service_Rate  # Service rate of each server
s = Number_of_Servers  # Number of servers
m = Queue_Capacity  # Maximum queue size

# Instantiate the class
queue_metrics = QueueMetrics(lam, mu, s, m)

# Calculate metrics
R = queue_metrics.calculate_average_rate_joining_system()
RiPb = queue_metrics.calculate_average_rate_leaving_without_service()
Ii = queue_metrics.calculate_average_number_waiting_in_queue()
Ti = queue_metrics.calculate_average_waiting_time()
Pb = queue_metrics.queue_p_full()
Ip = queue_metrics.calculate_average_number_of_customers_served()
UoS = queue_metrics.average_utilization_of_servers()
I = queue_metrics.average_number_in_system()
T = queue_metrics.average_time_in_system()

# Results
print(f"{'Number of Servers':<20}= {Number_of_Servers}")
print(f"{'Queue Capacity':<20}= {Queue_Capacity}")
print(f"{'Arrival Rate':<20}= {Arrival_Rate}")
print(f"{'Service Rate':<20}= {Service_Rate}\n")

print(f"{'Description':<45}{'Abrv. in ()':<20}{'Value'}")
print('-' * 65)
print(f"{'Average Rate Joining System':<45}{'(R)':<20}{R:.4f}")
print(f"{'Average Rate Leaving Without Service':<45}{'(RiPb)':<20}{RiPb:.4f}")
print(f"{'Average Number Waiting in Queue':<45}{'(Ii)':<20}{Ii:.4f}")
print(f"{'Average Waiting Time':<45}{'(Ti)':<20}{Ti:.4f}")
print(f"{'Probability that System is Full':<45}{'(Pb)':<20}{Pb * 100:.4f}%")
print(f"{'Average Number of Customers Being Served':<45}{'(Ip)':<20}{Ip:.4f}")
print(f"{'Average Utilization of Servers':<45}{'':<20}{UoS * 100:.4f}%")
print(f"{'Average Number in the System':<45}{'(I)':<20}{I:.4f}")
print(f"{'Average Time in System':<45}{'(T)':<20}{T:.4f}")

print ( " ------------------------------")
##################33
####### Works #####
def calculate_p_n(n, s, M, PFull, mu, lam):
    if n == s + M:
        return PFull
    else:
        return calculate_p_n(n + 1, s, M, PFull, mu, lam) * min(n + 1, s) * mu / lam

# Given values
s = s  # Number of servers
M = m  # Maximum queue size
PFull = Pb  # Example value for PFull
mu = mu  # Service rate of each server
lam = lam  # Arrival rate of customers

# Calculate P(n) for n = 0 through n = 5 and cumulative probabilities
probabilities_n = [calculate_p_n(n, s, M, PFull, mu, lam) for n in range(6)]
cumulative_probabilities = [sum(probabilities_n[:i + 1]) for i in range(6)]

# Output probabilities and cumulative probabilities for n = 0 through n = 5
for n, (p_n, cumulative_p) in enumerate(zip(probabilities_n, cumulative_probabilities)):
    print(f"P(n={n}): {p_n:.4f} | Cumulative: {cumulative_p:.4f}")
#####################
####################
def calculate_p_q(n, probabilities_n, cumulative_probabilities, s):
    if n >= s:
        if n == s:
            return round(cumulative_probabilities[n], 4)
        else:
            return round(probabilities_n[n], 4)
    else:
        return 0.0  # Returning 0 instead of " "

# Use previously computed probabilities for P(n)
probabilities_n = [calculate_p_n(n, s, M, PFull, mu, lam) for n in range(6)]
cumulative_probabilities = [sum(probabilities_n[:i + 1]) for i in range(6)]

# Calculate P(q) for n = 0 through n = 5 (where q is the number of customers waiting in line)
probabilities_q = [calculate_p_q(n, probabilities_n, cumulative_probabilities, s) for n in range(6)]

# Output probabilities for P(q) for n = 0 through n = 5
print ("-----------------")
for n, p_q in enumerate(probabilities_q):
    print(f"P(q={n}): {p_q:.4f}")


import matplotlib.pyplot as plt

# Your code for calculating probabilities_n goes here...

# Plotting P(n) for n = 0 through n = 5
n_values = list(range(6))

plt.bar(n_values, probabilities_n)
plt.xlabel('n')
plt.ylabel('P(n)')
plt.title('Probabilities for n')
plt.xticks(n_values)  # Ensure all integer values are displayed on x-axis
plt.show()

# %%
