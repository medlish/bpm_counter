import tkinter as tk
import threading
import keyboard
import time

class BPMCounter:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BPM Counter")

        self.dragging = False
        self.x, self.y = 0, 0

        # Bind mouse events to the root window
        self.root.bind("<ButtonPress-1>", self.on_mouse_press)
        self.root.bind("<ButtonRelease-1>", self.on_mouse_release)
        self.root.bind("<B1-Motion>", self.on_mouse_drag)

        self.bpm = 0
        self.bpm_label = tk.Label(self.root, text="BPM: 0")
        self.bpm_label.pack(pady=20)

        self.reset_button = tk.Button(self.root, text="Reset (Press 'Esc')", command=self.reset_counter)
        self.reset_button.pack()

        self.is_counting = False
        self.key_press_times = []  # Store key press times for averaging
        self.bpm_history = []  # Store BPM history for averaging

        # Register the 'Esc' key for resetting
        keyboard.on_press_key('esc', self.reset_counter)

        # Register 'B' key press event
        keyboard.on_press_key('b', self.on_key_press)

    def on_mouse_press(self, event):
        self.dragging = True
        self.x, self.y = event.x, event.y

    def on_mouse_release(self, event):
        self.dragging = False

    def on_mouse_drag(self, event):
        if self.dragging:
            x_offset, y_offset = event.x - self.x, event.y - self.y
            self.root.geometry(f"+{self.root.winfo_x() + x_offset}+{self.root.winfo_y() + y_offset}")

    def on_key_press(self, e):
        if not self.is_counting:
            self.is_counting = True
            self.bpm_label.config(text="BPM: Counting...")
            self.key_press_times = [time.time()]
        else:
            self.key_press_times.append(time.time())
            self.calculate_bpm()

    def calculate_bpm(self):
        if len(self.key_press_times) >= 2:
            elapsed_time = self.key_press_times[-1] - self.key_press_times[0]
            bpm = int(60 / (elapsed_time / (len(self.key_press_times) - 1)))  # Calculate BPM without the most recent key press
            self.bpm_history.append(bpm)
            if len(self.bpm_history) > 8:
                self.bpm_history.pop(0)  # Keep the last 5 BPM values for averaging
            avg_bpm = sum(self.bpm_history) / len(self.bpm_history)
            self.bpm_label.config(text=f"BPM: {int(avg_bpm)}")

    def reset_counter(self, e=None):
        self.is_counting = False
        self.key_press_times = []
        self.bpm_history = []
        self.bpm = 0
        self.bpm_label.config(text="BPM: 0")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    counter = BPMCounter()
    counter.run()
