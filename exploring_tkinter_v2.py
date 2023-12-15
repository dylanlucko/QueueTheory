
# %%
import tkinter as tk

class QueueMetrics:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Queue Metrics Calculator")

        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=20, pady=20)

        # Labels and Entries
        labels = ["Queue Capacity:", "Service Rate:", "Number of Servers:", "Arrival Rate:"]
        for i, label_text in enumerate(labels):
            label = tk.Label(self.frame, text=label_text, font=("Arial", 12, "bold"))
            label.grid(row=i, column=0, sticky="w", padx=5, pady=5)

            entry = tk.Entry(self.frame, font=("Arial", 12))
            entry.grid(row=i, column=1, padx=5, pady=5)
            if label_text == "Queue Capacity:":
                self.queue_capacity_entry = entry
            elif label_text == "Service Rate:":
                self.service_rate_entry = entry
            elif label_text == "Number of Servers:":
                self.num_servers_entry = entry
            else:
                self.arrival_rate_entry = entry

        # Calculate Button
        self.calculate_button = tk.Button(self.frame, text="Calculate", command=self.calculate_metrics, font=("Arial", 14, "bold"))
        self.calculate_button.grid(row=4, columnspan=2, padx=5, pady=10)

        # Text Area for Results
        self.text_area = tk.Text(self.frame, width=40, height=10, font=("Arial", 12))
        self.text_area.grid(row=5, columnspan=2, padx=5, pady=5)

    def run_gui(self):
        self.root.mainloop()

    def calculate_metrics(self):
        queue_capacity = int(self.queue_capacity_entry.get())
        service_rate = int(self.service_rate_entry.get())
        num_servers = int(self.num_servers_entry.get())
        arrival_rate = int(self.arrival_rate_entry.get())

        # Perform example calculations for demonstration
        # Update this with your actual calculation functions
        result1 = arrival_rate * service_rate
        result2 = num_servers / queue_capacity

        # Clear the text area
        self.text_area.delete(1.0, tk.END)

        # Display results in the text area
        self.text_area.insert(tk.END, f"Queue Capacity: {queue_capacity}\n")
        self.text_area.insert(tk.END, f"Service Rate: {service_rate}\n")
        self.text_area.insert(tk.END, f"Number of Servers: {num_servers}\n")
        self.text_area.insert(tk.END, f"Arrival Rate: {arrival_rate}\n\n")

        self.text_area.insert(tk.END, f"Result 1: {result1}\n")
        self.text_area.insert(tk.END, f"Result 2: {result2}\n")

# Instantiate the class and run the GUI
queue_metrics = QueueMetrics()
queue_metrics.run_gui()

# %%
