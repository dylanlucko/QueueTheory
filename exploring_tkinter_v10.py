
#%%
import tkinter as tk
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



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
        self.root.geometry("1300x900")

        self.frame = tk.Frame(self.root)
        self.frame.pack(fill='both', expand=True)

        # Frame for input and text area
        input_frame = tk.Frame(self.frame)
        input_frame.pack(side='left', padx=10, pady=10)

        labels = ["Queue Capacity:", "Service Rate:", "Number of Servers:", "Arrival Rate:", "x_t:", "x_q:"]
        self.entries = {}
        for i, label_text in enumerate(labels):
            label = tk.Label(input_frame, text=label_text, font=("Arial", 12, "bold"))
            label.grid(row=i, column=0, sticky="w", padx=(5, 10), pady=(5, 20))

            entry = tk.Entry(input_frame, font=("Arial", 12))
            entry.grid(row=i, column=1, padx=(5, 10), pady=(5, 10))
            self.entries[label_text] = entry

        # Calculate Button
        #calculate_button = tk.Button(input_frame, text="Calculate", command=self.calculate_metrics, font=("Arial", 14, "bold"))
        #calculate_button.grid(row=len(labels), columnspan=2, sticky="ew", padx=5, pady=0)

        # Text Area for Results
        self.text_area = tk.Text(input_frame, width=60, height=20, font=("Arial", 12))
        self.text_area.grid(row=len(labels) + 1, columnspan=2, padx=50, pady=50)

        # Plot Area
        self.figure, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.frame)
        self.canvas.get_tk_widget().pack(side='right', padx=20, pady=(70, 70))

        # Initialize plot index and list of plot functions
        self.plot_index = 0
        self.plot_functions = [self.plot_1, self.plot_2, self.plot_3, self.plot_4]

                # Calculate Button
        calculate_button = tk.Button(input_frame, text="Calculate", command=self.calculate_metrics, font=("Arial", 14, "bold"))
        calculate_button.grid(row=len(labels) , column=0, sticky="ew", padx=(5, 2), pady=(10, 5))  # Half width

        # Next Button for changing plots
        self.next_button = tk.Button(input_frame, text="Next Graph", command=self.show_next_plot, font=("Arial", 14, "bold"))
        self.next_button.grid(row=len(labels) , column=1, sticky="ew", padx=(2, 5), pady=(10, 5))  # Half width


        
        


        
    def show_next_plot(self):
        # Increment the plot index to move to the next plot
        self.plot_index = (self.plot_index + 1) % len(self.plot_functions)

        # Call the corresponding plot function based on the updated plot index
        self.update_plot()

    def update_plot(self):
        # Clear the existing plot and draw the new one based on the plot index
        self.ax.clear()
        self.plot_functions[self.plot_index]()  # Call the corresponding plot function
        self.canvas.draw()


    def plot_1(self):
        self.ax.clear()
        # Code to generate plot 1 here...
        self.ax.plot([1, 2, 3], [4, 5, 6])  # Example data
        self.ax.set_title("Plot 1")
        self.ax.set_xlabel("X-axis")
        self.ax.set_ylabel("Y-axis")
        self.ax.grid(True)
        self.canvas.draw()

    def plot_2(self):
        self.ax.clear()
        # Code to generate plot 2 here...
        self.ax.plot([3, 2, 1], [6, 5, 4])  # Example data
        self.ax.set_title("Plot 2")
        self.ax.set_xlabel("X-axis")
        self.ax.set_ylabel("Y-axis")
        self.ax.grid(True)
        self.canvas.draw()

    def plot_3(self):
        self.ax.clear()
        # Code to generate plot 3 here...
        self.ax.plot([2, 3, 4], [5, 6, 7])  # Example data
        self.ax.set_title("Plot 3")
        self.ax.set_xlabel("X-axis")
        self.ax.set_ylabel("Y-axis")
        self.ax.grid(True)
        self.canvas.draw()

    def plot_4(self):
        self.ax.clear()
        # Code to generate plot 4 here...
        self.ax.plot([4, 3, 2], [7, 6, 5])  # Example data
        self.ax.set_title("Plot 4")
        self.ax.set_xlabel("X-axis")
        self.ax.set_ylabel("Y-axis")
        self.ax.grid(True)
        self.canvas.draw()



    def calculate_metrics(self):
        try:
        # Retrieve values from entries
            queue_capacity = int(self.entries["Queue Capacity:"].get())
            service_rate = int(self.entries["Service Rate:"].get())
            num_servers = int(self.entries["Number of Servers:"].get())
            arrival_rate = int(self.entries["Arrival Rate:"].get())
            x_t_value = float(self.entries["x_t:"].get())
            x_q_value = float(self.entries["x_q:"].get())

        # Instantiate QueueMetrics object with retrieved values
            queue_metrics = QueueMetrics(arrival_rate, service_rate, num_servers, queue_capacity, x_t_value, x_q_value)
        
        # Perform calculations using queue_metrics
        # Example calculations:
            Ii_infinite = round(queue_metrics.average_number_waiting_infinite(), 4)
            Ti_infinite = round(queue_metrics.average_time_waiting_infinite(), 4)
            AUS = round(queue_metrics.calculate_average_server_utilization(), 4)
            Ip_infinite = round(queue_metrics.average_num_customers_receiving_service(), 4)
            I_infinite = round(queue_metrics.average_num_in_system(), 4)
            Q = round(queue_metrics.customer_probability(), 4)
            T = round(queue_metrics.time_probability(), 4)

        # Clear the text area
            self.text_area.delete(1.0, tk.END)

        # Display calculated results in the text area using self.text_area.insert()
            descriptions = [
            "Average Number Waiting in Infinite Queue:",
            "Average Time Waiting in Infinite Queue:",
            "Average Server Utilization in Infinite Queue:",
            "Number of Customers Serviced in Infinite Queue:",
            "Average Number in System in Infinite Queue:",
            "Probability more than x customers waiting:",
            "Probability more than x time waiting:"
        ]

            values = [
            Ii_infinite, Ti_infinite, AUS * 100, Ip_infinite, I_infinite, Q * 100, T * 100
        ]

            max_desc_length = max(len(desc) for desc in descriptions)
            gap_length = 30  # Adjust the gap length as needed for even spacing

            for desc, val in zip(descriptions, values):
                spacing = ' ' * (max_desc_length - len(desc) + gap_length)
                output = f"{desc:<{max_desc_length}}{spacing}{val:.4f}%\n"
                self.text_area.insert(tk.END, output)

        # Plot calculations or results
            self.plot_functions[self.plot_index]()

        # Increment plot index to switch to the next plot
            self.plot_index = (self.plot_index + 1) % len(self.plot_functions)

        except Exception as e:
         print(f"Error occurred: {e}")



# Create the GUI window and run the application
root = tk.Tk()
app = GUI(root)
root.mainloop()



# %%
