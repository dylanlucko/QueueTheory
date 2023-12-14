
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
    Ii = calculate_average_number_waiting_in_queue(lam, mu, s, m)
    return Ii / R

def calculate_average_number_of_customers_served(mu):
    return R/mu

def average_utilization_of_servers(lam, mu, s, m):
    Ip = R/mu
    return Ip/s

def average_number_in_system(lam, mu, s, m):
    I = Ip+Ii
    return Ip+Ii

def average_time_in_system(lam, mu, s, m):
    return I / R


#%%
# Inputs
Number_of_Servers = 1
Queue_Capacity = 4
Arrival_Rate = 4
Service_Rate = 6
########################
########################
########################
lam = Queue_Capacity  # Arrival rate of customers
mu = Service_Rate  # Service rate of each server
s = Number_of_Servers  # Number of servers
m = Queue_Capacity # Maximum queue size

# Calculate metrics
R = calculate_average_rate_joining_system(lam, mu, s, m)
RiPb = calculate_average_rate_leaving_without_service(lam, mu, s, m)
Ii = calculate_average_number_waiting_in_queue(lam, mu, s, m)
Ti = calculate_average_waiting_time(lam, mu, s, m)
Pb = queue_p_full(lam, mu, s, m)
Ip = calculate_average_number_of_customers_served(mu)
UoS = average_utilization_of_servers(lam, mu, s, m)
I = average_number_in_system(lam, mu, s, m)
T = average_time_in_system(lam, mu, s, m)


# Results
print(f"Average Rate Joining System (R): {R:.4f}")
print(f"Average Rate Leaving Without Service (RiPb): {RiPb:.4f}")
print(f"Average Number Waiting in Queue (Ii): {Ii:.4f}")
print(f"Average Waiting Time (Ti): {Ti:.4f}")
print(f"Probability that System is Full (Pb): {Pb*100:.4f}%")
print(f"Average Number of Customers Being Served (Ip): {Ip:.4f}")
print(f"Average Utilization of Servers: {UoS*100:.4f}%")
print(f"Average Number in the System (I): {I:.4f}")
print(f"Average Time in System: {T:.4f}")




# %%
def calculate_p_n(n, s, m, PFull, mu, lam):
    if n == s + M:
        return PFull
    else:
        return calculate_p_n(n + 1, s, M, PFull, mu, lam) * min(n + 1, s) * mu / lam

# Given values
s = 1  # Number of servers
M = 4  # Maximum queue size
PFull = Pb  # Example value for PFull
mu = 6  # Service rate of each server
lam = 4  # Arrival rate of customers

# Calculate P(n) for n = 0 through n = 5
probabilities_n = [calculate_p_n(n, s, M, PFull, mu, lam) for n in range(6)]
for n, p_n in enumerate(probabilities_n):
    print(f"P(n={n}): {p_n:.4f}")

# %%
##################33
####### Works #####
def calculate_p_n(n, s, M, PFull, mu, lam):
    if n == s + M:
        return PFull
    else:
        return calculate_p_n(n + 1, s, M, PFull, mu, lam) * min(n + 1, s) * mu / lam

# Given values
s = 1  # Number of servers
M = 4  # Maximum queue size
PFull = Pb  # Example value for PFull
mu = 6  # Service rate of each server
lam = 4  # Arrival rate of customers

# Calculate P(n) for n = 0 through n = 5 and cumulative probabilities
probabilities_n = [calculate_p_n(n, s, M, PFull, mu, lam) for n in range(6)]
cumulative_probabilities = [sum(probabilities_n[:i + 1]) for i in range(6)]

# Output probabilities and cumulative probabilities for n = 0 through n = 5
for n, (p_n, cumulative_p) in enumerate(zip(probabilities_n, cumulative_probabilities)):
    print(f"P(n={n}): {p_n:.4f} | Cumulative: {cumulative_p:.4f}")

# %%
def calculate_p_q(n, probabilities_n, cumulative_probabilities, s):
    if n >= s:
        if n == s:
            return cumulative_probabilities[n]
        else:
            return probabilities_n[n]
    else:
        return " "

# Use previously computed probabilities for P(n)
probabilities_n = [calculate_p_n(n, s, M, PFull, mu, lam) for n in range(6)]
cumulative_probabilities = [sum(probabilities_n[:i + 1]) for i in range(6)]

# Calculate P(q) for n = 0 through n = 5 (where q is the number of customers waiting in line)
probabilities_q = [calculate_p_q(n, probabilities_n, cumulative_probabilities, s) for n in range(6)]

# Output probabilities for P(q) for n = 0 through n = 5
for n, p_q in enumerate(probabilities_q):
    print(f"P(q={n}): {p_q}")

# %%

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
for n, p_q in enumerate(probabilities_q):
    print(f"P(q={n}): {p_q:.4f}")

# %%

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
