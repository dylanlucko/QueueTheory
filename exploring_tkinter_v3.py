
#%%
import tkinter as tk
import math

class QueueMetrics:
    def __init__(self, lam, mu, s, m, x_t, x_q):
        self.lam = lam
        self.mu = mu
        self.s = s
        self.m = m
        self.x_t  = x_t
        self.x_q = x_q
        
    def queue_p_full(self):
        rho = self.lam / self.mu
        term = 1
        po = 1
        
        for k in range(1, self.s + self.m + 1):
            term *= rho / min(k, self.s)
            po += term
        return term / po


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
        Ti = Ii/self.lam
        return Ti
    
    def calculate_average_server_utilization(self):
        AUS = (self.lam)/ (self.s*self.mu)
        return AUS
    
    
    def average_num_customers_receiving_service(self):
        AUS = (self.lam)/ (self.s*self.mu)
        Ip_infinite=AUS*self.s
        return Ip_infinite
    
    def average_num_in_system(self):
        r = self.lam / self.mu
        rho = r / self.s
        term = (1 - rho) / rho
        Q = term
        AUS = (self.lam)/ (self.s*self.mu)
        for k in range(1, self.s):
            
            term *= (self.s - k) / r
            Q += term
        Ii = (rho / (1 - rho)) / (1 + Q)
        return Ii +self.s*AUS
    
    #def average_time_in_system(self):
        #AUS = (self.lam)/ (self.s*self.mu)
        
    #    return I_infinite / self.lam
    
    def customer_probability(self):
        r = self.lam / self.mu
        rho = r / self.s
        term = (1 - rho) / rho
        Q = term
        
        for k in range(1, self.s):
            term *= (self.s - k) / r
            Q += term
        Ii = (rho / (1 - rho)) / (1 + Q)
        AUS = (self.lam)/ (self.s*self.mu)
        return ((1 - AUS )*Ii *AUS**self.x_q)
    
    def time_probability(self):
        r = self.lam / self.mu
        rho = r / self.s
        term = (1 - rho) / rho
        Q = term
        
        for k in range(1, self.s):
            term *= (self.s - k) / r
            Q += term
        Ii = (rho / (1 - rho)) / (1 + Q)
        AUS = (self.lam)/ (self.s*self.mu)
        return ((1 - AUS )/AUS *Ii*math.exp((self.lam-self.s*self.mu)*self.x_t))

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Queue Metrics Calculator")

        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=20, pady=20)

        # Labels and Entries
        labels = ["Queue Capacity:", "Service Rate:", "Number of Servers:", "Arrival Rate:", "x_t:", "x_q:"]
        self.entries = {}
        for i, label_text in enumerate(labels):
            label = tk.Label(self.frame, text=label_text, font=("Arial", 12, "bold"))
            label.grid(row=i, column=0, sticky="w", padx=5, pady=5)

            entry = tk.Entry(self.frame, font=("Arial", 12))
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[label_text] = entry

        # Calculate Button
        self.calculate_button = tk.Button(self.frame, text="Calculate", command=self.calculate_metrics, font=("Arial", 14, "bold"))
        self.calculate_button.grid(row=len(labels), columnspan=2, padx=5, pady=20)

        # Text Area for Results
        self.text_area = tk.Text(self.frame, width=60, height=20, font=("Arial", 12))
        self.text_area.grid(row=len(labels) + 1, columnspan=2, padx=5, pady=5)


    def calculate_metrics(self):
        queue_capacity = int(self.entries["Queue Capacity:"].get())
        service_rate = int(self.entries["Service Rate:"].get())
        num_servers = int(self.entries["Number of Servers:"].get())
        arrival_rate = int(self.entries["Arrival Rate:"].get())
        x_t_value = float(self.entries["x_t:"].get())  # Changed to float
        x_q_value = float(self.entries["x_q:"].get())  # Changed to float

        # Instantiate QueueMetrics and perform calculations
        queue_metrics = QueueMetrics(arrival_rate, service_rate, num_servers, queue_capacity, x_t_value, x_q_value)
        
        # Perform calculations
        Ii_infinite = round(queue_metrics.average_number_waiting_infinite(), 4)
        Ti_infinite = round(queue_metrics.average_time_waiting_infinite(), 4)
        AUS = round(queue_metrics.calculate_average_server_utilization(), 4)
        Ip_infinite = round(queue_metrics.average_num_customers_receiving_service(), 4)
        I_infinite = round(queue_metrics.average_num_in_system(), 4)
        Q = round(queue_metrics.customer_probability(), 4)
        T = round(queue_metrics.time_probability(), 4)

        # Clear the text area
        self.text_area.delete(1.0, tk.END)

       
        # Display calculated values in the text area
        self.text_area.insert(tk.END, f"{'Average Number Waiting in Infinite Queue:'<30} {Ii_infinite}\n")
        self.text_area.insert(tk.END, f"Average Time Waiting in Infinite Queue: {Ti_infinite}\n")
        self.text_area.insert(tk.END, f"Average Server Utilization in Infinite Queue: {AUS * 100:.4f}%{' ':30}\n")
        self.text_area.insert(tk.END, f"Number of Customers Serviced in Infinite Queue: {Ip_infinite}\n")
        self.text_area.insert(tk.END, f"Average Number in System in Infinite Queue: {I_infinite}\n")
        self.text_area.insert(tk.END, f"Probability more than x customers waiting: {Q * 100:.4f}%{' ':30}\n")
        self.text_area.insert(tk.END, f"Probability more than x time waiting: {T * 100:.4f}%{' ':30}\n")

# Create the GUI window and run the application
root = tk.Tk()
app = GUI(root)
root.mainloop()



# %%
