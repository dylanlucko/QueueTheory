
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
