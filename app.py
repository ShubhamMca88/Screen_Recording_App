import tkinter as tk
from tkinter import messagebox, filedialog
import cv2
import numpy as np
import pyautogui
import threading
import time

class ScreenRecorder:
    def __init__(self, master):
        self.master = master
        self.master.title("Screen Recorder")
        self.master.geometry("300x150")
        self.recording = False
        self.output_filename = ""

        self.start_button = tk.Button(self.master, text="Start Recording", command=self.start_recording)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(self.master, text="Stop Recording", command=self.stop_recording)
        self.stop_button.pack(pady=10)
        self.stop_button.config(state=tk.DISABLED)

        self.save_button = tk.Button(self.master, text="Save As", command=self.save_as)
        self.save_button.pack(pady=10)

    def save_as(self):
        self.output_filename = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")])
        if self.output_filename:
            self.start_button.config(state=tk.NORMAL)

    def start_recording(self):
        if not self.output_filename:
            messagebox.showwarning("Warning", "Please select a file to save the recording.")
            return

        self.recording = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        self.screen_size = pyautogui.size()
        self.fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self.out = cv2.VideoWriter(self.output_filename, self.fourcc, 20.0, (self.screen_size.width, self.screen_size.height))

        self.thread = threading.Thread(target=self.record_screen)
        self.thread.start()

    def stop_recording(self):
        self.recording = False
        self.thread.join()
        self.out.release()
        cv2.destroyAllWindows()
        messagebox.showinfo("Screen Recorder", f"Recording stopped and saved as {self.output_filename}")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def record_screen(self):
        # Set frame rate
        fps = 20.0
        frame_duration = 1 / fps

        while self.recording:
            start_time = time.time()

            # Capture the screen
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            self.out.write(frame)

            # Calculate elapsed time and sleep to maintain frame rate
            elapsed_time = time.time() - start_time
            sleep_time = frame_duration - elapsed_time
            if sleep_time > 0: 
                time.sleep(sleep_time)

if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenRecorder(master=root)
    root.mainloop()