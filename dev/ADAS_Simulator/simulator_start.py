import tkinter as tk
from tkinter import ttk, messagebox, font
from PIL import Image, ImageTk
import threading
import simulation_main  # your simulation script


class ADASSimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("University of Michigan ADAS Simulator")
        self.root.geometry("1280x720")
        self.root.configure(bg="#00274C")  # Set background color
        self.root.resizable(True, True)

        # === Background Image ===
        # self.bg_image = self.root.configure(bg="#00274C")  # Set background color
        # self.bg_image = self.bg_image.resize((1280, 720), Image.ANTIALIAS)
        # self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # self.bg_label = tk.Label(root, image=self.bg_photo)
        # self.bg_label.place(relwidth=1, relheight=1)

        # === Custom Styles ===
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabel", background="#00274C", foreground="white")
        style.configure("TCheckbutton", background="#00274C", foreground="white")
        style.configure("TButton", background="#00274C", foreground="white")
        style.configure("TCombobox", fieldbackground="white", background="white", foreground="black")

        # === Title ===
        self.title_label = tk.Label(root, text="University of Michigan ADAS Simulator",
                                    font=("Helvetica", 28, "bold"), bg='#00274C', fg='white')
        self.title_label.place(relx=0.5, rely=0.05, anchor='center')

        # === Layout Config ===
        left_x = 0.25
        right_x = 0.65
        top_y = 0.15
        step_y = 0.07
        font_inline = font.Font(size=14)

        # === Left Column: Player Vehicle ===
        ttk.Label(root, text="Player Vehicle:", font=font_inline).place(relx=left_x, rely=top_y, anchor='center')
        self.player_vehicle = ttk.Combobox(root, values=["Tesla Model 3", "Other Vehicle"], state="readonly")
        self.player_vehicle.current(0)
        self.player_vehicle.place(relx=left_x, rely=top_y + 0.03, anchor='center')

        # === Right Column Inputs ===
        inputs = [
            ("Initial Weather:", ["Clear Noon", "Cloudy Noon", "Wet Noon", "Mid Rain", "Hard Rain", "Soft Rain", "Clear Sunset"]),
            ("Lead Vehicle:", None),
            ("Number of Traffic Vehicles:", None),
            ("Number of Pedestrians:", None),
            ("Initial Scenario:", ["Urban", "Highway", "Intersection", "Custom"])
        ]

        self.weather = self.lead_vehicle = self.traffic_vehicles = self.pedestrians = self.scenario = None

        for i, (label, options) in enumerate(inputs):
            rely_label = top_y + i * step_y
            rely_widget = rely_label + 0.03
            ttk.Label(root, text=label,font=font_inline).place(relx=right_x, rely=rely_label, anchor='center')

            if label == "Lead Vehicle:":
                self.lead_vehicle = tk.BooleanVar()
                ttk.Checkbutton(root, text="Enable Lead Vehicle", variable=self.lead_vehicle).place(
                    relx=right_x, rely=rely_widget, anchor='center')
            elif label == "Number of Traffic Vehicles:":
                self.traffic_vehicles = tk.IntVar(value=10)
                ttk.Entry(root, textvariable=self.traffic_vehicles).place(
                    relx=right_x, rely=rely_widget, anchor='center')
            elif label == "Number of Pedestrians:":
                self.pedestrians = tk.IntVar(value=20)
                ttk.Entry(root, textvariable=self.pedestrians).place(
                    relx=right_x, rely=rely_widget, anchor='center')
            elif label == "Initial Weather:":
                self.weather = ttk.Combobox(root, values=options, state="readonly")
                self.weather.current(0)
                self.weather.place(relx=right_x, rely=rely_widget, anchor='center')
            elif label == "Initial Scenario:":
                self.scenario = ttk.Combobox(root, values=options, state="readonly")
                self.scenario.current(0)
                self.scenario.place(relx=right_x, rely=rely_widget, anchor='center')

        # === Log Box ===
        ttk.Label(root, text="Log:").place(relx=0.05, rely=0.65, anchor='w')
        self.log_box = tk.Text(root, height=3, width=95, state='disabled',
                               bg="#f0f0f0", fg="black", bd=0, highlightthickness=0)
        self.log_box.place(relx=0.5, rely=0.73, anchor='center')

        # === Start Button ===
        ttk.Button(root, text="Start Simulation", command=self.start_simulation).place(relx=0.5, rely=0.92, anchor='center')

    def log(self, message):
        self.log_box.configure(state='normal')
        self.log_box.insert(tk.END, message + "\n")
        self.log_box.configure(state='disabled')
        self.log_box.yview(tk.END)

    def start_simulation(self):
        self.log("Launching simulation with selected parameters...")
        params = {
            "vehicle_model": self.player_vehicle.get(),
            "weather": self.weather.get(),
            "lead_vehicle": self.lead_vehicle.get(),
            "traffic_count": self.traffic_vehicles.get(),
            "pedestrian_count": self.pedestrians.get(),
            "scenario": self.scenario.get()
        }
        threading.Thread(target=self.run_simulation, args=(params,), daemon=True).start()

    def run_simulation(self, params):
        try:
            simulation_main.main(params)
        except Exception as e:
            self.log(f"[ERROR] {e}")
            messagebox.showerror("Simulation Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = ADASSimulatorGUI(root)
    root.mainloop()
