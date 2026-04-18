
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox, filedialog
import tkinter as tk
from process_manager import get_running_processes, terminate_process, get_process_rank
from injector import inject_dll
from debuggersee import get_process_modules

class AdminDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Absolute Admin | System Core")
        self.root.geometry("700x500")
        self.style = tb.Style(theme="darkly")
        
        header = tb.Label(root, text="Absolute Admin System", font=("Helvetica", 16, "bold"), bootstyle="inverse-primary")
        header.pack(fill=X, pady=10, padx=10)
        
        self.tree = tb.Treeview(root, columns=("PID", "Name", "Rank"), show="headings", bootstyle="info")
        self.tree.heading("PID", text="PID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Rank", text="Safety Rank")
        self.tree.column("PID", width=80)
        self.tree.pack(fill=BOTH, expand=True, padx=10, pady=5)
        
        btn_frame = tb.Frame(root, padding=10)
        btn_frame.pack(fill=X)
        
        tb.Button(btn_frame, text="Refresh", command=self.load_procs, bootstyle="outline-primary").pack(side=LEFT, padx=5)
        tb.Button(btn_frame, text="View Details", command=self.show_details, bootstyle="info").pack(side=LEFT, padx=5)
        tb.Button(btn_frame, text="Inject DLL", command=self.select_and_inject, bootstyle="warning").pack(side=LEFT, padx=5)
        tb.Button(btn_frame, text="Terminate", command=self.kill_proc, bootstyle="danger").pack(side=RIGHT, padx=5)

        self.load_procs()

    def load_procs(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        for p in get_running_processes():
            rank = get_process_rank(p['pid'])
            self.tree.insert("", "end", values=(p['pid'], p['name'], rank))

    def show_details(self):
        selected = self.tree.selection()
        if not selected: return
        pid = int(self.tree.item(selected[0])['values'][0])
        modules = get_process_modules(pid)
        
        win = tb.Toplevel(self.root)
        win.title("Details")
        txt = tb.Text(win)
        txt.pack(fill=BOTH, expand=True)
        for m in modules: txt.insert(END, m + "\n")

    def select_and_inject(self):
        selected = self.tree.selection()
        if not selected: return
        pid = int(self.tree.item(selected[0])['values'][0])
        dll = filedialog.askopenfilename(filetypes=[("DLL Files", "*.dll")])
        if dll:
            success, msg = inject_dll(pid, dll)
            messagebox.showinfo("Result", msg)

    def kill_proc(self):
        selected = self.tree.selection()
        if not selected: return
        pid = int(self.tree.item(selected[0])['values'][0])
        if messagebox.askyesno("Confirm", f"Terminate PID {pid}?"):
            success, msg = terminate_process(pid)
            if success: self.load_procs()
            else: messagebox.showerror("Error", msg)

if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    app = AdminDashboard(root)
    root.mainloop()
