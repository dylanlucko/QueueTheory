

#%%
import tkinter as tk

# Create a window
root = tk.Tk()
root.title("My GUI")

# Create a label
label = tk.Label(root, text="Hello, Tkinter!")
label.pack()

# Create a button
button = tk.Button(root, text="Click Me!")
button.pack()

# Run the main loop
root.mainloop()
