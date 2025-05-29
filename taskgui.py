import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

class TaskManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f0f0")
        
        # Initialize tasks list
        self.tasks = self.load_tasks()
        
        # Create GUI elements
        self.create_widgets()
        self.update_task_display()
    
    def load_tasks(self):
        """Load tasks from JSON file"""
        if os.path.exists("tasks.json"):
            try:
                with open("tasks.json", 'r') as file:
                    return json.load(file)
            except json.JSONDecodeError:
                return []
        return []
    
    def save_tasks(self):
        """Save tasks to JSON file"""
        with open("tasks.json", 'w') as file:
            json.dump(self.tasks, file, indent=2)
    
    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="📝 Task Manager", 
                              font=("Arial", 18, "bold"), 
                              bg="#f0f0f0", fg="#333")
        title_label.pack(pady=10)
        
        # Input frame
        input_frame = tk.Frame(self.root, bg="#f0f0f0")
        input_frame.pack(pady=10, padx=20, fill="x")
        
        tk.Label(input_frame, text="Enter Task:", 
                font=("Arial", 12), bg="#f0f0f0").pack(anchor="w")
        
        self.task_entry = tk.Entry(input_frame, font=("Arial", 12), width=50)
        self.task_entry.pack(pady=5, fill="x")
        self.task_entry.bind("<Return>", lambda event: self.add_task())
        
        # Buttons frame
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(pady=10)
        
        # Add button
        add_btn = tk.Button(button_frame, text="➕ Add Task", 
                           command=self.add_task,
                           bg="#4CAF50", fg="white", 
                           font=("Arial", 10, "bold"),
                           padx=15, pady=5)
        add_btn.pack(side="left", padx=5)
        
        # Mark Done button
        done_btn = tk.Button(button_frame, text="✅ Mark Done", 
                            command=self.mark_done,
                            bg="#2196F3", fg="white", 
                            font=("Arial", 10, "bold"),
                            padx=15, pady=5)
        done_btn.pack(side="left", padx=5)
        
        # Mark Undone button
        undone_btn = tk.Button(button_frame, text="🔄 Mark Undone", 
                              command=self.mark_undone,
                              bg="#FF9800", fg="white", 
                              font=("Arial", 10, "bold"),
                              padx=15, pady=5)
        undone_btn.pack(side="left", padx=5)
        
        # Delete button
        delete_btn = tk.Button(button_frame, text="🗑️ Delete", 
                              command=self.delete_task,
                              bg="#f44336", fg="white", 
                              font=("Arial", 10, "bold"),
                              padx=15, pady=5)
        delete_btn.pack(side="left", padx=5)
        
        # Filter frame
        filter_frame = tk.Frame(self.root, bg="#f0f0f0")
        filter_frame.pack(pady=10)
        
        tk.Label(filter_frame, text="Filter:", 
                font=("Arial", 10), bg="#f0f0f0").pack(side="left")
        
        self.filter_var = tk.StringVar(value="all")
        filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_var,
                                   values=["all", "pending", "completed"],
                                   state="readonly", width=15)
        filter_combo.pack(side="left", padx=5)
        filter_combo.bind("<<ComboboxSelected>>", lambda event: self.update_task_display())
        
        # Task list frame
        list_frame = tk.Frame(self.root, bg="#f0f0f0")
        list_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        tk.Label(list_frame, text="Tasks:", 
                font=("Arial", 12, "bold"), bg="#f0f0f0").pack(anchor="w")
        
        # Listbox with scrollbar
        listbox_frame = tk.Frame(list_frame)
        listbox_frame.pack(fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.task_listbox = tk.Listbox(listbox_frame, 
                                      yscrollcommand=scrollbar.set,
                                      font=("Arial", 11),
                                      selectmode="single",
                                      height=15)
        self.task_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.task_listbox.yview)
        
        # Status bar
        self.status_label = tk.Label(self.root, text="Ready", 
                                    font=("Arial", 9), 
                                    bg="#e0e0e0", relief="sunken")
        self.status_label.pack(side="bottom", fill="x")
    
    def add_task(self):
        task_text = self.task_entry.get().strip()
        if task_text:
            task = {
                "id": len(self.tasks) + 1,
                "description": task_text,
                "completed": False
            }
            self.tasks.append(task)
            self.task_entry.delete(0, tk.END)
            self.save_tasks()
            self.update_task_display()
            self.status_label.config(text=f"✅ Added: '{task_text}'")
        else:
            messagebox.showwarning("Warning", "Please enter a task description!")
    
    def get_selected_task_index(self):
        selection = self.task_listbox.curselection()
        if selection:
            display_index = selection[0]
            # Get the actual task index based on current filter
            filtered_tasks = self.get_filtered_tasks()
            if display_index < len(filtered_tasks):
                task_id = filtered_tasks[display_index]["id"]
                # Find the actual index in the main tasks list
                for i, task in enumerate(self.tasks):
                    if task["id"] == task_id:
                        return i
        return None
    
    def get_filtered_tasks(self):
        filter_type = self.filter_var.get()
        if filter_type == "completed":
            return [task for task in self.tasks if task["completed"]]
        elif filter_type == "pending":
            return [task for task in self.tasks if not task["completed"]]
        else:
            return self.tasks
    
    def mark_done(self):
        index = self.get_selected_task_index()
        if index is not None:
            task = self.tasks[index]
            if task["completed"]:
                messagebox.showinfo("Info", "Task is already completed!")
            else:
                task["completed"] = True
                self.save_tasks()
                self.update_task_display()
                self.status_label.config(text=f"✅ Marked done: '{task['description']}'")
        else:
            messagebox.showwarning("Warning", "Please select a task to mark as done!")
    
    def mark_undone(self):
        index = self.get_selected_task_index()
        if index is not None:
            task = self.tasks[index]
            if not task["completed"]:
                messagebox.showinfo("Info", "Task is already pending!")
            else:
                task["completed"] = False
                self.save_tasks()
                self.update_task_display()
                self.status_label.config(text=f"🔄 Marked undone: '{task['description']}'")
        else:
            messagebox.showwarning("Warning", "Please select a task to mark as undone!")
    
    def delete_task(self):
        index = self.get_selected_task_index()
        if index is not None:
            task = self.tasks[index]
            result = messagebox.askyesno("Confirm Delete", 
                                       f"Are you sure you want to delete:\n'{task['description']}'?")
            if result:
                deleted_task = self.tasks.pop(index)
                self.save_tasks()
                self.update_task_display()
                self.status_label.config(text=f"🗑️ Deleted: '{deleted_task['description']}'")
        else:
            messagebox.showwarning("Warning", "Please select a task to delete!")
    
    def update_task_display(self):
        self.task_listbox.delete(0, tk.END)
        filtered_tasks = self.get_filtered_tasks()
        
        if not filtered_tasks:
            self.task_listbox.insert(tk.END, "No tasks found")
            return
        
        for task in filtered_tasks:
            status = "✅ DONE" if task["completed"] else "⏳ PENDING"
            display_text = f"#{task['id']} | {status} | {task['description']}"
            self.task_listbox.insert(tk.END, display_text)
        
        # Update status bar with task count
        total_tasks = len(self.tasks)
        completed_tasks = len([t for t in self.tasks if t["completed"]])
        pending_tasks = total_tasks - completed_tasks
        self.status_label.config(text=f"Total: {total_tasks} | Completed: {completed_tasks} | Pending: {pending_tasks}")

def main():
    root = tk.Tk()
    app = TaskManagerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
