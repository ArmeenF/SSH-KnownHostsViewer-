import tkinter as tk
from tkinter import ttk
import os


class KnownHostsViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Known Hosts Viewer")
        self.root.geometry("600x400")

        # Create a treeview widget
        self.tree = ttk.Treeview(
            self.root, columns=("IP Address", "Key Type", "Key Value"), show="headings"
        )
        self.tree.heading("IP Address", text="IP Address")
        self.tree.heading("Key Type", text="Key Type")
        self.tree.heading("Key Value", text="Key Value")
        self.tree.pack(fill="both", expand=True)

        # Load known_hosts file
        self.load_known_hosts()

        # Create a delete button
        self.delete_button = ttk.Button(
            self.root, text="Delete Selected", command=self.delete_selected
        )
        self.delete_button.pack()

    def load_known_hosts(self):
        known_hosts_path = os.path.expanduser("~/.ssh/known_hosts")
        if os.path.exists(known_hosts_path):
            with open(known_hosts_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        ip, key_type, key_value = line.split(" ", 2)
                        self.tree.insert("", "end", values=(ip, key_type, key_value))

    def delete_selected(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item)["values"]
            ip, key_type, key_value = item_values
            known_hosts_path = os.path.expanduser("~/.ssh/known_hosts")
            with open(known_hosts_path, "r") as f:
                lines = f.readlines()
            with open(known_hosts_path, "w") as f:
                for line in lines:
                    if not line.startswith(ip):
                        f.write(line)
            self.tree.delete(selected_item)


if __name__ == "__main__":
    root = tk.Tk()
    app = KnownHostsViewer(root)
    root.mainloop()
