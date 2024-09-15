import json
from datetime import datetime
from tkinter import messagebox, simpledialog, END
from customtkinter import CTk, CTkLabel, CTkEntry, CTkButton, set_appearance_mode
from CTkListbox import CTkListbox

# Initialize the application window
app = CTk()
app.geometry("500x600")
app.title("TO DO LIST")

# Set the appearance of the window (light mode)
set_appearance_mode("light")

# Define the list to store tasks
tasks = []

# Refresh the task list display
def refresh_task_list():
    task_list.delete(0, END)
    for task in tasks:
        status = "Completed" if task['completed'] else "Pending"
        display_text = f"Task: {task['name']}\nDue Date: {task['due_date']}\nStatus: {status}\n"
        task_list.insert(END, display_text)

# Add a new task
def add_task():
    name = task_name_entry.get()
    due_date = task_due_date_entry.get()

    try:
        datetime.strptime(due_date, '%Y-%m-%d')
        tasks.append({'name': name, 'due_date': due_date, 'completed': False})
        messagebox.showinfo("Success", "Task added successfully!")
        refresh_task_list()
    except ValueError:
        messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD format.")

# Remove a task
def remove_task():
    name = simpledialog.askstring("Input", "Enter task name to remove:")
    global tasks
    tasks = [task for task in tasks if task['name'] != name]
    messagebox.showinfo("Success", "Task removed successfully!")
    refresh_task_list()

# Mark a task as completed
def mark_task_completed():
    name = simpledialog.askstring("Input", "Enter task name to mark as completed:")

    for task in tasks:
        if task['name'] == name:
            task['completed'] = True
            messagebox.showinfo("Success", "Task marked as completed!")
            refresh_task_list()
            return
    
    messagebox.showerror("Error", "Task not found.")

# Edit a task
def edit_task():
    name = simpledialog.askstring("Input", "Enter task name to edit:")

    for task in tasks:
        if task['name'] == name:
            new_name = simpledialog.askstring("Input", "Enter new task name:")
            new_due_date = simpledialog.askstring("Input", "Enter new due date (YYYY-MM-DD):")

            try:
                datetime.strptime(new_due_date, '%Y-%m-%d')
                task['name'] = new_name
                task['due_date'] = new_due_date
                messagebox.showinfo("Success", "Task updated successfully!")
                refresh_task_list()
                return

            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD format")

    messagebox.showerror("Error", "Task not found.")

# Sort tasks
def sort_tasks():
    criteria = simpledialog.askstring("Input", "Sort by name or due date? (name/date):")

    if criteria == "name":
        tasks.sort(key=lambda task: task['name'])
    elif criteria == "date":
        tasks.sort(key=lambda task: task['due_date'])
    else:
        messagebox.showerror("Error", "Invalid criteria.")
        return
    
    messagebox.showinfo("Success", "Tasks sorted successfully!")
    refresh_task_list()

# Save tasks to a file
def save_tasks():
    with open('tasks.txt', 'w') as file:
        json.dump(tasks, file)
        
    messagebox.showinfo("Success", "Tasks saved successfully!")

# Load tasks from a file
def load_tasks():
    global tasks

    try:
        with open('tasks.txt', 'r') as file:
            tasks = json.load(file)
            messagebox.showinfo("Success", "Tasks loaded successfully!")
            refresh_task_list()
    except FileNotFoundError:
        messagebox.showerror("Error", "No saved tasks found.")

# Create and place widgets
# sticky="w" for the labels: Aligns the labels to the left side of their grid cells.
# sticky="e" for the entry fields: Aligns the entry fields to the right side of their grid cells.
task_name_label = CTkLabel(master=app, text="Task Name:", font=("Roboto", 14, "bold"))
task_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

task_name_entry = CTkEntry(master=app, width=250)
task_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="e")

task_due_date_label = CTkLabel(master=app, text="Due Date (YYYY-MM-DD):", font=("Roboto", 14, "bold"))
task_due_date_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

task_due_date_entry = CTkEntry(master=app, width=250)
task_due_date_entry.grid(row=1, column=1, padx=10, pady=5, sticky="e")

# Create a Listbox for displaying tasks
task_list = CTkListbox(master=app, width=450, height=300)
task_list.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Define button style
button_style = {
    "corner_radius": 32,
    "fg_color": "#2C74B3",
    "hover_color": "#3FA2F6",
    "border_width": 2,
    "border_color": "#2C74B3",
    "text_color": "#ffffff"
}

# Create and place buttons
add_task_button = CTkButton(master=app, text="Add Task", command=add_task, **button_style)
add_task_button.grid(row=2, column=0, columnspan=2, pady=10)

load_tasks_button = CTkButton(master=app, text="Load Tasks", command=load_tasks, **button_style)
load_tasks_button.grid(row=4, column=0, pady=5)

save_tasks_button = CTkButton(master=app, text="Save Tasks", command=save_tasks, **button_style)
save_tasks_button.grid(row=4, column=1, pady=5)

remove_task_button = CTkButton(master=app, text="Remove Task", command=remove_task, **button_style)
remove_task_button.grid(row=5, column=0, pady=5)

mark_completed_button = CTkButton(master=app, text="Mark Task as Completed", command=mark_task_completed, **button_style)
mark_completed_button.grid(row=5, column=1, pady=5)

edit_task_button = CTkButton(master=app, text="Edit Task", command=edit_task, **button_style)
edit_task_button.grid(row=6, column=0, pady=5)

sort_tasks_button = CTkButton(master=app, text="Sort Tasks", command=sort_tasks, **button_style)
sort_tasks_button.grid(row=6, column=1, pady=5)

# Load tasks initially
load_tasks()

# Launch the window
app.mainloop()