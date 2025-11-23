import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import json
import backend  # Your backend module
import psutil

class ProcessManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Process Management System Call Wrapper")

        self.cols = ['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'status']
        self.spawned_processes = []

        # --- Search Bar UI ---
        self.search_var = tk.StringVar()
        search_frame = tk.Frame(root)
        search_frame.pack(fill='x', padx=10, pady=5)
        tk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=50)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Find", command=self.perform_search).pack(side=tk.LEFT, padx=5)
        self.search_var.trace("w", self.debounce_search)
        self._search_after_id = None
        # --- End Search Bar ---

        self.tree = ttk.Treeview(root, columns=self.cols, show='headings', selectmode='browse')
        for col in self.cols:
            self.tree.heading(col, text=col.title())
            self.tree.column(col, width=120)
        self.tree.pack(expand=True, fill='both', pady=10)

        ctrl_frame = tk.Frame(root)
        ctrl_frame.pack(fill='x', padx=10, pady=5)

        tk.Label(ctrl_frame, text="Command:").pack(side=tk.LEFT)
        self.cmd_entry = tk.Entry(ctrl_frame, width=50)
        self.cmd_entry.pack(side=tk.LEFT, padx=5)

        tk.Button(ctrl_frame, text="Launch Process", command=self.launch_process).pack(side=tk.LEFT, padx=5)
        tk.Button(ctrl_frame, text="Kill Selected", command=self.kill_selected_process).pack(side=tk.LEFT, padx=5)
        tk.Button(ctrl_frame, text="Refresh List", command=self.refresh).pack(side=tk.LEFT, padx=5)

        self.processes = []  # Cache the current process list
        self.refresh()

    def refresh(self):
        """Refresh process list and cache data."""
        self.tree.delete(*self.tree.get_children())
        try:
            self.processes = json.loads(backend.list_processes())
            self.perform_search()  # Display filtered list according to search_var
        except Exception as e:
            messagebox.showerror("Error", f"Failed to list processes: {e}")

        # List spawned processes (update info)
        for p in self.spawned_processes[:]:
            try:
                proc = psutil.Process(p.pid)
                self.tree.insert("", "end", values=[
                    proc.pid, proc.name(), proc.username(),
                    proc.cpu_percent(), proc.memory_percent(), proc.status()
                ])
            except Exception:
                self.spawned_processes.remove(p)

    def perform_search(self):
        """Filter process list based on search bar input and update Treeview."""
        keyword = self.search_var.get().lower()
        self.tree.delete(*self.tree.get_children())
        for proc in self.processes:
            if any(keyword in str(proc.get(col, '')).lower() for col in self.cols):
                self.tree.insert("", "end", values=[proc.get(c, '') for c in self.cols])

    def debounce_search(self, *args):
        """Debounce user input in search bar to avoid excessive processing."""
        if self._search_after_id:
            self.root.after_cancel(self._search_after_id)
        self._search_after_id = self.root.after(300, self.perform_search)

    def launch_process(self):
        cmd = self.cmd_entry.get().strip()
        if not cmd:
            messagebox.showwarning("Input Error", "Please enter a command to launch.")
            return
        try:
            proc = subprocess.Popen(cmd, shell=True)
            self.spawned_processes.append(proc)
            # Schedule refresh after 500 ms to allow the process to appear
            self.root.after(500, self.refresh)
        except Exception as e:
            messagebox.showerror("Launch Failed", str(e))

    def kill_selected_process(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Select a process from the list to kill.")
            return
        pid_str = self.tree.item(selected[0])['values'][0]
        if not pid_str:
            messagebox.showerror("PID Error", "Cannot determine PID.")
            return
        try:
            pid = int(pid_str)
            success, msg = backend.kill_process(pid)
            if success:
                messagebox.showinfo("Success", msg)
                self.spawned_processes = [p for p in self.spawned_processes if p.pid != pid]
                self.refresh()
            else:
                messagebox.showerror("Kill Failed", msg)
        except Exception as e:
            messagebox.showerror("Error", f"Error killing process: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ProcessManagerApp(root)
    root.mainloop()
