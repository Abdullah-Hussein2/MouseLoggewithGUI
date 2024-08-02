     ###### the orignal code with no gui


# from pynput import mouse
# def on_click(x, y, button, pressed):
#     if pressed:
#         with open('click.txt', 'a') as file:
#             file.write(f'mouse clicked at {x,y} with {button}')
#
# def on_scroll(x, y, dx, dy):
#     with open('scroll.txt', 'a') as file:
#         file.write(f'Mouse scrolled at {x,y}{dx,dy}')
#
#
# def on_move(x,y):
#     with open('move.txt', 'a') as file:
#         file.write(f'Position of mouse: {x,y}')
#
# with mouse.Listener(on_click=on_click, on_scroll=on_scroll,on_move=on_move) as listener:
#     listener.join()


#######code with gui with the help of chatgpt



import subprocess
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
import os

def install_pynput():
    try:
        import pynput
    except ImportError:
        print("pynput is not installed. Installing now...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pynput"])
        print("pynput installed successfully.")

# Ensure pynput is installed
install_pynput()

from pynput import mouse

class MouseLoggerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mouse Logger")
        self.root.geometry("400x200")
        self.is_logging = False
        self.listener = None
        self.save_directory = ""

        self.setup_ui()

    def setup_ui(self):
        self.root.config(bg="#2E4053")

        self.start_button = tk.Button(self.root, text="Start Logging", command=self.start_logging, bg="#5DADE2", fg="white", font=("Helvetica", 12))
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(self.root, text="Stop Logging", command=self.stop_logging, state=tk.DISABLED, bg="#E74C3C", fg="white", font=("Helvetica", 12))
        self.stop_button.pack(pady=10)

        self.choose_dir_button = tk.Button(self.root, text="Choose Save Directory", command=self.choose_directory, bg="#58D68D", fg="white", font=("Helvetica", 12))
        self.choose_dir_button.pack(pady=10)

        self.status_label = tk.Label(self.root, text="Status: Not Logging", bg="#2E4053", fg="white", font=("Helvetica", 12))
        self.status_label.pack(pady=10)

    def start_logging(self):
        if not self.save_directory:
            messagebox.showwarning("Warning", "Please choose a directory to save the files.")
            return

        self.is_logging = True
        self.update_ui()
        self.listener = mouse.Listener(on_click=self.on_click, on_scroll=self.on_scroll, on_move=self.on_move)
        self.listener.start()

    def stop_logging(self):
        if self.listener:
            self.listener.stop()

        self.is_logging = False
        self.update_ui()

    def choose_directory(self):
        self.save_directory = filedialog.askdirectory()
        if self.save_directory:
            messagebox.showinfo("Directory Selected", f"Files will be saved in: {self.save_directory}")

    def update_ui(self):
        self.start_button.config(state=tk.DISABLED if self.is_logging else tk.NORMAL)
        self.stop_button.config(state=tk.NORMAL if self.is_logging else tk.DISABLED)
        self.status_label.config(text="Status: Logging" if self.is_logging else "Status: Not Logging")

    def log_event(self, filename, message):
        if self.save_directory:
            with open(os.path.join(self.save_directory, filename), 'a') as file:
                file.write(message + '\n')

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.log_event('click.txt', f'Mouse clicked at {x,y} with {button}')

    def on_scroll(self, x, y, dx, dy):
        self.log_event('scroll.txt', f'Mouse scrolled at {x,y} {dx,dy}')

    def on_move(self, x, y):
        self.log_event('move.txt', f'Position of mouse: {x,y}')

if __name__ == "__main__":
    root = tk.Tk()
    app = MouseLoggerGUI(root)
    root.mainloop()

