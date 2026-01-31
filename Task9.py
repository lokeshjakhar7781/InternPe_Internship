import tkinter as tk
from tkinter import messagebox
import os
class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python To-Do List")
        self.root.geometry("400x500")
        self.root.configure(bg="#f0f0f0")
        self.filename = "tasks.txt"
        self.label = tk.Label(root, text="My Tasks", font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#333")
        self.label.pack(pady=10)
        input_frame = tk.Frame(root, bg="#f0f0f0")
        input_frame.pack(pady=10)
        self.task_entry = tk.Entry(input_frame, font=("Arial", 14), width=20)
        self.task_entry.pack(side=tk.LEFT, padx=5)
        self.task_entry.bind('<Return>', lambda event: self.add_task()) 
        add_btn = tk.Button(input_frame, text="+", font=("Arial", 12, "bold"), 
                            bg="#4caf50", fg="white", width=3, command=self.add_task)
        add_btn.pack(side=tk.LEFT)
        list_frame = tk.Frame(root)
        list_frame.pack(pady=10, padx=20, fill="both", expand=True)
        self.tasks_listbox = tk.Listbox(list_frame, font=("Arial", 12), 
                                        width=25, height=10, selectmode=tk.SINGLE,
                                        bd=0, highlightthickness=0, activestyle="none")
        self.tasks_listbox.pack(side=tk.LEFT, fill="both", expand=True)
        self.tasks_listbox.bind('<<ListboxSelect>>', self.fill_entry_on_select)
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        self.tasks_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tasks_listbox.yview)
        action_frame = tk.Frame(root, bg="#f0f0f0")
        action_frame.pack(pady=20)
        update_btn = tk.Button(action_frame, text="Update Selected", font=("Arial", 10), 
                               bg="#2196f3", fg="white", command=self.update_task)
        update_btn.pack(side=tk.LEFT, padx=10)
        delete_btn = tk.Button(action_frame, text="Delete Selected", font=("Arial", 10), 
                               bg="#f44336", fg="white", command=self.delete_task)
        delete_btn.pack(side=tk.LEFT, padx=10)
        self.load_tasks()
    def add_task(self):
        task = self.task_entry.get()
        if task != "":
            self.tasks_listbox.insert(tk.END, task)
            self.task_entry.delete(0, tk.END)
            self.save_tasks()
        else:
            messagebox.showwarning("Warning", "You must enter a task.")
    def delete_task(self):
        try:
            index = self.tasks_listbox.curselection()[0]
            self.tasks_listbox.delete(index)
            self.save_tasks()
            self.task_entry.delete(0, tk.END) 
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to delete.")
    def update_task(self):
        try:
            index = self.tasks_listbox.curselection()[0]
            new_text = self.task_entry.get()
            if new_text != "":
                self.tasks_listbox.delete(index)
                self.tasks_listbox.insert(index, new_text)
                self.save_tasks()
                self.tasks_listbox.select_set(index)
            else:
                messagebox.showwarning("Warning", "Task cannot be empty.")
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to update.")
    def fill_entry_on_select(self, event):
        """When a user clicks a list item, copy it to the entry box for easy editing."""
        try:
            index = self.tasks_listbox.curselection()[0]
            selected_task = self.tasks_listbox.get(index)
            self.task_entry.delete(0, tk.END)
            self.task_entry.insert(0, selected_task)
        except IndexError:
            pass
    def save_tasks(self):
        """Writes current listbox content to a text file."""
        tasks = self.tasks_listbox.get(0, tk.END)
        with open(self.filename, "w") as f:
            for task in tasks:
                f.write(task + "\n")
    def load_tasks(self):
        """Reads text file and populates listbox."""
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                for line in f:
                    self.tasks_listbox.insert(tk.END, line.strip())
if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()