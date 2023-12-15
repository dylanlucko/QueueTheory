
###########################
##### START  HERE #########
###########################
##### CLICK  RUN ##########
########################### 


#%%

import math
Queue_Capacity = 10
Service_Rate = 60
Number_of_Servers= 2
Arrival_Rate = 40
x_q = 0
x_t = 0.1


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
    
    def customer_probability(self):
        r = self.lam / self.mu
        rho = r / self.s
        term = (1 - rho) / rho
        Q = term
        
        for k in range(1, self.s):
            term *= (self.s - k) / r
            Q += term
        Ii = (rho / (1 - rho)) / (1 + Q)
        AUS = (lam)/ (s*mu)
        return ((1 - AUS )*Ii *AUS**x_q)
    
    def time_probability(self):
        r = self.lam / self.mu
        rho = r / self.s
        term = (1 - rho) / rho
        Q = term
        
        for k in range(1, self.s):
            term *= (self.s - k) / r
            Q += term
        Ii = (rho / (1 - rho)) / (1 + Q)
        AUS = (lam)/ (s*mu)
        return ((1 - AUS )/AUS *Ii*math.exp((lam-s*mu)*x_t))
        


# Instantiate the class
queue_metrics = QueueMetrics(lam, mu, s, m)

# Calculate the average waiting time for an infinite queue
Ii_infinite = queue_metrics.average_number_waiting_infinite()
Ti_infinite = queue_metrics.average_time_waiting_infinite()
AUS = queue_metrics.calculate_average_server_utilization()
Ip_infinite = queue_metrics.average_num_customers_receiving_service()
I_infinite = queue_metrics.average_num_in_system()
T_infinite = queue_metrics.average_time_in_system()
Q = queue_metrics.customer_probability()
T = queue_metrics.time_probability()



print(f"{'Number of Servers':<20}= {Number_of_Servers}")
print(f"{'Queue Capacity':<20}= {Queue_Capacity}")
print(f"{'Arrival Rate':<20}= {Arrival_Rate}")
print(f"{'Service Rate':<20}= {Service_Rate}\n")
# Print the result

print('-' * 65)
print(f"{'Description':<50}{'Value'}")
print('-' * 65)
print(f"{'Average Number Waiting in Infinite Queue:':<50}{Ii_infinite:.4f}")
print(f"{'Average Time Waiting in Infinite Queue:':<50}{Ti_infinite:.4f}")
print(f"{'Average Server Utilization in Infinite Queue:':<50}{AUS*100:.4f}%")
print(f"{'Number of Customers Serviced in Infinite Queue:':<50}{Ip_infinite:.4f}")
print(f"{'Average Number in System in Infinite Queue:':<50}{I_infinite:.4f}")
print(f"{'Average Time in System in Infinite Queue:':<50}{T_infinite:.4f}")
print(f"{'Probability more than {x_q} customers waiting :':<50}{Q*100:.4f}%")
print(f"{'Probability more than {x_t} customers waiting :':<50}{T*100:.4f}%")








# %%
