

# %%

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

# Inputs
Number_of_Servers = 1
Queue_Capacity = 4
Arrival_Rate = 4
Service_Rate = 6

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

# Results
print(f"Average Rate Joining System (R): {R:.4f}")
print(f"Average Rate Leaving Without Service (RiPb): {RiPb:.4f}")
print(f"Average Number Waiting in Queue (Ii): {Ii:.4f}")
print(f"Average Waiting Time (Ti): {Ti:.4f}")
print(f"Probability that System is Full (Pb): {Pb * 100:.4f}%")

# %%
