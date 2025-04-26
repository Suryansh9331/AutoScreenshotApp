import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui
import threading
import time
import os
from datetime import datetime

# Create screenshots folder if it doesn't exist
if not os.path.exists("screenshots"):
    os.makedirs("screenshots")

class ScreenshotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Screenshot Capturer")
        self.root.geometry("400x250")
        self.root.configure(bg="#f2f2f2")

        self.running = False
        self.interval = 120  # Default to 2 minutes

        self.setup_ui()

    def setup_ui(self):
        title = tk.Label(self.root, text="Auto Screenshot Tool", font=("Helvetica", 16, "bold"), bg="#f2f2f2", fg="#333")
        title.pack(pady=10)

        # Dropdown label
        interval_label = tk.Label(self.root, text="Select Interval:", font=("Helvetica", 12), bg="#f2f2f2")
        interval_label.pack()

        # Dropdown for time intervals
        self.interval_var = tk.StringVar(value="2 min")
        interval_options = ["2 min", "5 min", "10 min", "15 min", "20 min"]
        dropdown = ttk.Combobox(self.root, textvariable=self.interval_var, values=interval_options, state="readonly", font=("Helvetica", 11))
        dropdown.pack(pady=5)

        # Start/Stop buttons
        self.start_button = tk.Button(self.root, text="Start", command=self.start_screenshots, bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"), width=10)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_screenshots, bg="#f44336", fg="white", font=("Helvetica", 12, "bold"), width=10)
        self.stop_button.pack()

        # Status
        self.status_label = tk.Label(self.root, text="Status: Not Running", font=("Helvetica", 10), bg="#f2f2f2", fg="gray")
        self.status_label.pack(pady=15)

    def get_interval_seconds(self):
        mapping = {
            "2 min": 120,
            "5 min": 300,
            "10 min": 600,
            "15 min": 900,
            "20 min": 1200,
        }
        return mapping.get(self.interval_var.get(), 120)

    def take_screenshot(self):
        while self.running:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filepath = os.path.join("screenshots", f"screenshot_{timestamp}.png")
            screenshot = pyautogui.screenshot()
            screenshot.save(filepath)
            print(f"Screenshot saved: {filepath}")
            time.sleep(self.get_interval_seconds())

    def start_screenshots(self):
        if not self.running:
            self.running = True
            self.status_label.config(text="Status: Running")
            threading.Thread(target=self.take_screenshot, daemon=True).start()
        else:
            messagebox.showinfo("Already Running", "Screenshot capture is already running.")

    def stop_screenshots(self):
        if self.running:
            self.running = False
            self.status_label.config(text="Status: Not Running")
            messagebox.showinfo("Stopped", "Screenshot capturing stopped.")
        else:
            messagebox.showinfo("Not Running", "Screenshot capture is not currently running.")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenshotApp(root)
    root.mainloop()
