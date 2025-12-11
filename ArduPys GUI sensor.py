import tkinter as tk
from tkinter import ttk
import serial
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class SensorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sensor GUI")
        self.serial_port = serial.Serial('COM3', 9600, timeout=1)

        self.temperature_values = []
        self.time_values = []

        self.create_widgets()

    def create_widgets(self):
        self.lcd_frame = tk.Frame(self.root, bg="black", width=400, height=200)
        self.lcd_frame.pack()

        self.temperature_label = tk.Label(self.lcd_frame, text="Temperature: ", font=("Arial", 40), bg="black", fg="green")
        self.temperature_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.graph_frame = tk.Frame(self.root)
        self.graph_frame.pack()

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title('Temperature Graph')
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Temperature (°C)')

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

        self.update_temperature()

    def update_temperature(self):
        data = self.serial_port.readline().decode('utf-8').strip()
        if data:
            try:
                temperature = float(data)
                print(temperature)
                self.temperature_values.append(temperature)
                self.time_values.append(len(self.time_values))
                self.temperature_label.config(text=f"{temperature} °C")
                self.ax.clear()
                self.ax.plot(self.time_values, self.temperature_values)
                self.ax.set_title('Temperature Graph')
                self.ax.set_xlabel('Time')
                self.ax.set_ylabel('Temperature (°C)')
                self.ax.set_ylim(min(self.temperature_values) - 1, max(self.temperature_values) + 1)
                self.canvas.draw()
            except ValueError:
                pass
        self.root.after(100, self.update_temperature)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    app = SensorGUI(root)
    root.mainloop()