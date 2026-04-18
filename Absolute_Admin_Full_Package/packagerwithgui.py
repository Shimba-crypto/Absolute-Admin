
import os
import zipfile
import subprocess
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox

class PackagerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Absolute Admin | Project Packager")
        self.root.geometry("500x350")
        tb.Style(theme="darkly")

        tb.Label(root, text="Select Project Folder:", font=("Helvetica", 10)).pack(pady=(20, 5))
        self.path_entry = tb.Entry(root, width=50)
        self.path_entry.pack(padx=20)
        tb.Button(root, text="Browse", command=self.browse, bootstyle="info-outline").pack(pady=5)

        tb.Label(root, text="Select Launch/Install Method:", font=("Helvetica", 10)).pack(pady=(10, 5))
        self.method_var = tb.StringVar(value="python")
        self.method_dropdown = tb.Combobox(root, textvariable=self.method_var, values=["py", "python", "pip"])
        self.method_dropdown.pack(pady=5)

        tb.Button(root, text="Package & Zip", command=self.package, bootstyle="success").pack(pady=30)

    def browse(self):
        folder = filedialog.askdirectory()
        if folder:
            self.path_entry.delete(0, END)
            self.path_entry.insert(0, folder)

    def package(self):
        source_dir = self.path_entry.get()
        if not os.path.isdir(source_dir):
            messagebox.showerror("Error", "Invalid Directory")
            return

        method = self.method_var.get()
        zip_name = "AbsoluteAdmin_Build.zip"

        if method in ["py", "python"]:
            with open(os.path.join(source_dir, "run.bat"), "w") as f:
                f.write(f"@echo off\n{method} ui_dashboard.py\npause")
        elif method == "pip":
            subprocess.run(["pip", "freeze"], stdout=open(os.path.join(source_dir, "requirements.txt"), "w"))

        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    if file != zip_name:
                        zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), source_dir))
        
        messagebox.showinfo("Success", f"Project packaged as {zip_name}")

if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    app = PackagerUI(root)
    root.mainloop()
