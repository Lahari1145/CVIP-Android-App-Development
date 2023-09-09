import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3 as sql
from tkcalendar import DateEntry
import re  # Import the regular expression library

def add_task():
    task = task_entry.get()
    date = date_entry.get_date()
    time_input = time_entry.get()
    
    # Use regular expression to extract hours and minutes
    time_match = re.match(r'(\d+):(\d+)', time_input)
    
    if task and date and time_match:
        hours = time_match.group(1)
        minutes = time_match.group(2)
        time = f"{hours}:{minutes}"
        task_list.insert(tk.END, f"{len(task_list.get(0, tk.END)) + 1}. Date: {date}, Task: {task}, Time: {time}")
        save_task_to_database(task, date, time)
        task_entry.delete(0, tk.END)
        time_entry.delete(0, tk.END)
    else:
        messagebox.showinfo('Error', 'Please enter all task details in HH:MM format.')

def save_task_to_database(task, date, time):
    the_cursor.execute('INSERT INTO tasks (title, date, time) VALUES (?, ?, ?)', (task, date, time))
    the_connection.commit()

def delete_task():
    selected_task = task_list.get(tk.ACTIVE)
    if selected_task:
        task_list.delete(tk.ACTIVE)
        delete_task_from_database(selected_task)

def delete_task_from_database(task):
    task = task.split(". Date: ")[1]  # Extract the date part
    the_cursor.execute('DELETE FROM tasks WHERE date = ?', (task,))
    the_connection.commit()

def clear_all_tasks():
    message_box = messagebox.askyesno('Delete All', 'Are you sure you want to delete all tasks?')
    if message_box:
        task_list.delete(0, tk.END)
        the_cursor.execute('DELETE FROM tasks')
        the_connection.commit()

def update_task():
    selected_task = task_list.get(tk.ACTIVE)
    if selected_task:
        # Split the selected task to extract date and task details
        task_details = selected_task.split(". Date: ")
        date, task_time = task_details[0], task_details[1]

        # Create a new window or dialog for updating the task
        update_window = tk.Toplevel(guiWindow)
        update_window.title("Update Task")

        # Create labels and entry fields for updating task details
        update_task_label = tk.Label(update_window, text="Update Task:", font=("arial", "14", "bold"))
        update_task_label.pack()

        update_task_entry = tk.Entry(update_window, font=("Arial", "14"), width=42)
        update_task_entry.insert(0, task_time)
        update_task_entry.pack()

        update_date_label = tk.Label(update_window, text="Update Date:", font=("arial", "14", "bold"))
        update_date_label.pack()

        update_date_entry = DateEntry(
            update_window,
            font=("Arial", "14"),
            width=20,
            date_pattern="yyyy-mm-dd"
        )
        update_date_entry.insert(0, date)
        update_date_entry.pack()

        # Create an "Update" button to confirm changes
        update_confirm_button = tk.Button(
            update_window,
            text="Update",
            width=15,
            bg='#2196F3',  # Choose a suitable background color
            font=("arial", "14", "bold"),
            command=lambda: confirm_update_task(selected_task, update_task_entry.get(), update_date_entry.get_date())
        )
        update_confirm_button.pack()

def confirm_update_task(selected_task, updated_task, updated_date):
    # Remove the selected task from the list
    task_list.delete(tk.ACTIVE)

    # Add the updated task to the list
    updated_task_str = f"{len(task_list.get(0, tk.END)) + 1}. Date: {updated_date}, Task: {updated_task}"
    task_list.insert(tk.END, updated_task_str)

    # Update the task in the database
    update_task_in_database(selected_task, updated_task, updated_date)

def update_task_in_database(selected_task, updated_task, updated_date):
    # Extract the original date part from the selected task
    original_date = selected_task.split(". Date: ")[0]

    # Update the task in the database
    the_cursor.execute('UPDATE tasks SET title = ?, date = ? WHERE date = ?',
                       (updated_task, updated_date, original_date))
    the_connection.commit()

def retrieve_database():
    the_cursor.execute('PRAGMA table_info(tasks)')
    columns = [column[1] for column in the_cursor.fetchall()]
    if 'date' not in columns:
        the_cursor.execute('ALTER TABLE tasks ADD COLUMN date DATE')
    if 'time' not in columns:
        the_cursor.execute('ALTER TABLE tasks ADD COLUMN time TEXT')

    the_cursor.execute('SELECT date, title, time FROM tasks')
    for row in the_cursor.fetchall():
        date, task, hours = row
        task_list.insert(tk.END, f"{len(task_list.get(0, tk.END)) + 1}. Date: {date}, Task: {task}, Time: {hours} hours")

if _name_ == "_main_":
    guiWindow = tk.Tk()
    guiWindow.title("To-Do List with Calendar")
    guiWindow.geometry("1000x600")
    guiWindow.resizable(0, 0)
    guiWindow.configure(bg="#FAD02E")

    screen_width = guiWindow.winfo_screenwidth()
    screen_height = guiWindow.winfo_screenheight()
    x_position = (screen_width - 1000) // 2
    y_position = (screen_height - 600) // 2
    guiWindow.geometry(f"1000x600+{x_position}+{y_position}")

    the_connection = sql.connect('listOfTasks.db')
    the_cursor = the_connection.cursor()
    the_cursor.execute('CREATE TABLE IF NOT EXISTS tasks (title TEXT, date DATE, time TEXT)')

    functions_frame = tk.Frame(guiWindow, bg="black")
    functions_frame.pack(side="top", expand=True, fill="both")

    task_label = tk.Label(functions_frame, text="Enter the Task:", font=("arial", "14", "bold"), background="black",
                          foreground="white")
    task_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

    task_entry = tk.Entry(
        functions_frame,
        font=("Arial", "14"),
        width=42,
        foreground="black",
        background="white",
    )
    task_entry.grid(row=0, column=1, padx=20, pady=10, sticky="w")

    date_label = tk.Label(functions_frame, text="Select Date:", font=("arial", "14", "bold"), background="black",
                          foreground="white")
    date_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")

    date_entry = DateEntry(
        functions_frame,
        font=("Arial", "14"),
        width=20,
        foreground="black",
        background="white",
        date_pattern="yyyy-mm-dd"
    )
    date_entry.grid(row=1, column=1, padx=20, pady=10, sticky="w")

    time_label = tk.Label(functions_frame, text="Enter Time (HH:MM):", font=("arial", "14", "bold"), background="black",
                          foreground="white")
    time_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")

    time_entry = tk.Entry(
        functions_frame,
        font=("Arial", "14"),
        width=10,
        foreground="black",
        background="white",
    )
    time_entry.grid(row=2, column=1, padx=20, pady=10, sticky="w")

    add_button = tk.Button(
        functions_frame,
        text="Add Task",
        width=15,
        bg='#4CAF50',
        font=("arial", "14", "bold"),
        command=add_task,
    )
    del_button = tk.Button(
        functions_frame,
        text="Delete Task",
        width=15,
        bg='#F44336',
        font=("arial", "14", "bold"),
        command=delete_task,
    )
    update_button = tk.Button(
        functions_frame,
        text="Update Task",
        width=15,
        bg='#2196F3',
        font=("arial", "14", "bold"),
        command=update_task,
    )
    del_all_button = tk.Button(
        functions_frame,
        text="Delete All Tasks",
        width=15,
        font=("arial", "14", "bold"),
        bg='#F44336',
        command=clear_all_tasks
    )
    exit_button = tk.Button(
        functions_frame,
        text="Exit",
        width=15,
        bg='#BDBDBD',
        font=("arial", "14", "bold"),
        command=guiWindow.destroy
    )

    add_button.grid(row=3, column=0, padx=20, pady=10, sticky="w")
    del_button.grid(row=3, column=1, padx=20, pady=10, sticky="w")
    update_button.grid(row=3, column=2, padx=20, pady=10, sticky="w")
    del_all_button.grid(row=4, column=0, padx=20, pady=10, sticky="w")
    exit_button.grid(row=4, column=1, padx=20, pady=10, sticky="w")

    task_list = tk.Listbox(
        functions_frame,
        width=90,
        height=20,
        font=("Arial", "12"),
        selectmode='SINGLE',
        background="WHITE",
        foreground="BLACK",
        selectbackground="#4CAF50",
        selectforeground="WHITE"
    )
    task_list.grid(row=5, column=0, columnspan=3, padx=20, pady=10)

    retrieve_database()

    guiWindow.mainloop()
    the_connection.commit()
    the_connection.close()
