



#%%
Queue_Capacity = 10
Service_Rate = 60
Number_of_Servers= 1
Arrival_Rate = 40


lam = Arrival_Rate  # Arrival rate of customers
mu = Service_Rate  # Service rate of each server
s = Number_of_Servers  # Number of servers
m = Queue_Capacity  # Maximum queue size

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

    def average_number_waiting_infinite(self):
        r = self.lam / self.mu
        rho = r / self.s
        term = (1 - rho) / rho
        Q = term
        
        for k in range(1, self.s):
            term *= (self.s - k) / r
            Q += term
        
        return (rho / (1 - rho)) / (1 + Q)
    
    def average_time_waiting_infinite(self):
        r = self.lam / self.mu
        rho = r / self.s
        term = (1 - rho) / rho
        Q = term
        
        for k in range(1, self.s):
            term *= (self.s - k) / r
            Q += term
        Ii = (rho / (1 - rho)) / (1 + Q)
        Ti = Ii/lam
        return Ti
    
    def calculate_average_server_utilization(self):
        AUS = (lam)/ (s*mu)
        return AUS
    
    
    def average_num_customers_receiving_service(self):
        Ip_infinite=AUS*s
        return Ip_infinite
    
    def average_num_in_system(self):
        r = self.lam / self.mu
        rho = r / self.s
        term = (1 - rho) / rho
        Q = term
        
        for k in range(1, self.s):
            term *= (self.s - k) / r
            Q += term
        Ii = (rho / (1 - rho)) / (1 + Q)
        return Ii +s*AUS
    
    def average_time_in_system(self):
        return I_infinite / lam
        


# Instantiate the class
queue_metrics = QueueMetrics(lam, mu, s, m)

# Calculate the average waiting time for an infinite queue
Ii_infinite = queue_metrics.average_number_waiting_infinite()
Ti_infinite = queue_metrics.average_time_waiting_infinite()
AUS = queue_metrics.calculate_average_server_utilization()
Ip_infinite = queue_metrics.average_num_customers_receiving_service()
I_infinite = queue_metrics.average_num_in_system()
T_infinite = queue_metrics.average_time_in_system()



# Print the result
print(f"Average Number Waiting in Infinite Queue: {Ii_infinite:.4f}")
print(f"Average Time Waiting in Infinite Queue: {Ti_infinite:.4f}")
print(f"Average Server Utilization in Infinite Queue: {AUS*100:.4f}%")
print(f"Number of Customers Serviced in Infinite Queue: {Ip_infinite:.4f}")
print(f"Average Number in System in Infinite Queue: {I_infinite:.4f}")
print(f"Average Time in System in Infinite Queue: {T_infinite:.4f}")



# %%
