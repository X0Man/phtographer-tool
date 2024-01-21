import os
import shutil
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

class FileCopyTool:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("File Copy Tool")
        self.create_widgets()
        self.dark_mode = False

    def create_widgets(self):
        self.style = ttk.Style(self.window)
        self.style.theme_use('clam')
        self.style.configure("TLabel", font=("Helvetica", 12), padding=5, background="#1e1e1e", foreground="white")
        self.style.configure("TEntry", font=("Helvetica", 12), padding=5, background="#1e1e1e", foreground="white")
        self.style.configure("TCheckbutton", font=("Helvetica", 12), background="#1e1e1e", foreground="white")
        self.style.configure("TButton", font=("Helvetica", 12), padding=10, background="#1e1e1e", foreground="white")
        self.style.configure("TButton.Hover", background="blue", foreground="white")
        self.style.map("TButton", background=[("active", "!disabled", "blue")])
        self.style.configure("TProgressbar", thickness=10, troughcolor="black", background="darkorange")

        self.img_prefix_var = tk.BooleanVar()
        img_prefix_checkbox = ttk.Checkbutton(self.window, text="Add 'IMG_' Prefix", variable=self.img_prefix_var)
        img_prefix_checkbox.pack()

        self.f87a_prefix_var = tk.BooleanVar()
        f87a_prefix_checkbox = ttk.Checkbutton(self.window, text="Add 'F87A' Prefix", variable=self.f87a_prefix_var)
        f87a_prefix_checkbox.pack()

        self.fitshare_var = tk.BooleanVar()
        fitshare_checkbox = ttk.Checkbutton(self.window, text="Enable FitShare", variable=self.fitshare_var)
        fitshare_checkbox.pack()

        self.custom_prefix_var = tk.BooleanVar()
        custom_prefix_checkbox = ttk.Checkbutton(self.window, text="Use Custom Prefix", variable=self.custom_prefix_var)
        custom_prefix_checkbox.pack()

        custom_prefix_label = ttk.Label(self.window, text="Custom Prefix:")
        custom_prefix_label.pack()
        self.custom_prefix_entry = ttk.Entry(self.window)
        self.custom_prefix_entry.pack()

        numbers_label = ttk.Label(self.window, text="List of Numbers:")
        numbers_label.pack()
        self.numbers_entry = ttk.Entry(self.window)
        self.numbers_entry.pack()

        extension_label = ttk.Label(self.window, text="File Extension:")
        extension_label.pack()
        self.extension_entry = ttk.Entry(self.window)
        self.extension_entry.pack()

        src_folder_button = ttk.Button(self.window, text="Select Source Folder", command=self.select_source_folder, style="TButton")
        src_folder_button.pack()
        dst_folder_button = ttk.Button(self.window, text="Select Destination Folder", command=self.select_destination_folder, style="TButton")
        dst_folder_button.pack()

        self.copy_button = ttk.Button(self.window, text="Copy Files", command=self.copy_files, style="TButton")
        self.copy_button.pack()

        self.progress_bar = ttk.Progressbar(self.window, orient=tk.HORIZONTAL, mode='determinate', style="TProgressbar")
        self.progress_bar.pack(fill=tk.X, padx=10, pady=10)

        dark_mode_button = ttk.Button(self.window, text="Dark Mode", command=self.toggle_dark_mode, style="TButton")
        dark_mode_button.pack()

        self.window.configure(background="#1e1e1e")

    def toggle_dark_mode(self):
        if not self.dark_mode:
            self.style.configure("TLabel", background="black", foreground="white")
            self.style.configure("TEntry", background="black", foreground="white")
            self.style.configure("TCheckbutton", background="black", foreground="white")
            self.style.configure("TButton", background="black", foreground="white")
            self.window.configure(background="black")
            self.dark_mode = True
        else:
            self.style.configure("TLabel", background="#1e1e1e", foreground="white")
            self.style.configure("TEntry", background="#1e1e1e", foreground="white")
            self.style.configure("TCheckbutton", background="#1e1e1e", foreground="white")
            self.style.configure("TButton", background="#1e1e1e", foreground="white")
            self.window.configure(background="#1e1e1e")
            self.dark_mode = False

    def select_source_folder(self):
        src_folder = filedialog.askdirectory(title="Select Source Folder")
        self.src_folder = src_folder

    def select_destination_folder(self):
        dst_folder = filedialog.askdirectory(title="Select Destination Folder")
        self.dst_folder = dst_folder

    def copy_files(self):
        numbers_str = self.numbers_entry.get()
        numbers = numbers_str.split()

        img_prefix = self.img_prefix_var.get()
        f87a_prefix = self.f87a_prefix_var.get()
        fitshare_enabled = self.fitshare_var.get()
        file_extension = self.extension_entry.get()
        use_custom_prefix = self.custom_prefix_var.get()
        custom_prefix = self.custom_prefix_entry.get()

        total_files = len(numbers)
        self.progress_bar['maximum'] = total_files
        self.progress_bar['value'] = 0
        self.window.update()

        copied_files = []
        failed_files = []
        for i, num in enumerate(numbers):
            file_name = num

            if fitshare_enabled:
                file_name = file_name.lower()

            if f87a_prefix:
                file_name = "F87A" + file_name

            if img_prefix:
                file_name = "IMG_" + file_name

            if use_custom_prefix and custom_prefix:
                file_name = custom_prefix + file_name

            if file_extension:
                file_name += "." + file_extension

            src_file = os.path.join(self.src_folder, file_name)
            dst_file = os.path.join(self.dst_folder, file_name)

            if os.path.exists(src_file):
                try:
                    shutil.copy(src_file, dst_file)
                    copied_files.append((src_file, dst_file))
                except:
                    failed_files.append(src_file)
            else:
                failed
