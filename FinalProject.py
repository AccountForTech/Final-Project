import tkinter as tk
from tkinter import messagebox

# Color constants for program
PRIMARY_COLOR = "#4A90E2"  # Light Blue 
BACKGROUND_COLOR = "#F4F7FA"  # Light Grayish Blue 
TEXT_COLOR = "#333333"  # Dark Gray for text
ALTERNATE_BG_COLOR = "#E1EFFF"  # Light Blue 
HIGHLIGHT_COLOR = "#F5A623"  # Golden Yellow 

# Function to save different entry types
def save_entry(entry_type, description, time, date, entry_list):
    if description and time and date:
        # Validate date format (YYYY-MM-DD)
        if "-" in date and len(date.split("-")) == 3:
            
            # Validate time format (12-hour format with AM/PM)
            time_parts = time.split(" ")
            if len(time_parts) == 2 and time_parts[1].upper() in ["AM", "PM"]:
                time_value = time_parts[0]
                am_pm = time_parts[1].upper()
                time_digits = time_value.split(":")
                if len(time_digits) == 2 and time_digits[0].isdigit() and time_digits[1].isdigit():
                    hour = int(time_digits[0])
                    minute = int(time_digits[1])
                    if 0 < hour < 13 and minute >= 0:
                        entry_list.append(f"{description} - Date: {date} Time: {time}")
                        messagebox.showinfo("Success", f"{entry_type} saved successfully!")
                    else:
                        messagebox.showerror("Invalid Format", "Please enter valid time (1-12 for hour, 0-59 for minute).")
                else:
                    messagebox.showerror("Invalid Format", "Please enter valid time (HH:MM).")
            else:
                messagebox.showerror("Invalid Format", "Please enter valid time (HH:MM AM/PM).")
        else:
            messagebox.showerror("Invalid Format", "Please enter valid date (YYYY-MM-DD).")
    else:
        messagebox.showerror("Input Error", f"{entry_type} cannot be empty!")

# Function that prompts the removal of a saved entry
def remove_entry(entry_type, entry_list, index, frame):
    confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete this {entry_type}?")
    if confirm:
        entry_list.pop(index)  
        [widget.destroy() for widget in frame.winfo_children()]
        display_entries(entry_type, entry_list, frame)  
# Function to display saved entries and make them clickable
def display_entries(entry_type, entry_list, frame):
    if not entry_list:
        no_entries_label = tk.Label(frame, text=f"No saved {entry_type}!", font=("Arial", 14), bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
        no_entries_label.pack(pady=10)
    else:
        for idx, entry in enumerate(entry_list):
            entry_label = tk.Label(frame, text=entry, font=("Arial", 12), bg=ALTERNATE_BG_COLOR if idx % 2 == 0 else BACKGROUND_COLOR, fg=TEXT_COLOR, width=50, anchor="w", justify="left", padx=10, pady=5)
            
            # Highlight the date/time section with a different color
            description, date_time = entry.split(" - ")
            date, time = date_time.split(" Time: ")
            highlighted_entry = f"{description} - Date: {date} Time: {time}"
            entry_label.config(text=highlighted_entry)
            
            # Make each label clickable to remove the entry
            entry_label.bind("<Button-1>", lambda e, idx=idx: remove_entry(entry_type, entry_list, idx, frame))
            
            entry_label.pack(fill="x")

# Function to view saved entries 
def view_saved_entries(entry_type, entry_list):
    saved_window = tk.Toplevel(window)
    saved_window.title(f"Saved {entry_type}s")
    saved_window.config(bg=BACKGROUND_COLOR)
    
    frame = tk.Frame(saved_window, bg=BACKGROUND_COLOR)
    frame.pack(padx=10, pady=10)
    
    display_entries(entry_type, entry_list, frame)

# Function to create a category window 
def create_category_window(entry_type, entry_list):
    create_category_window = tk.Toplevel(window)
    create_category_window.title(f"{entry_type} Management")
    create_category_window.config(bg=BACKGROUND_COLOR)
    
    saved_button = tk.Button(create_category_window, text=f"Saved {entry_type}", font=("Arial", 12), bg=PRIMARY_COLOR, fg="white", command=lambda: view_saved_entries(entry_type, entry_list))
    saved_button.pack(pady=10)
    
    add_button = tk.Button(create_category_window, text=f"New {entry_type}", font=("Arial", 12), bg=PRIMARY_COLOR, fg="white", command=lambda: add_new_window(entry_type, entry_list))
    add_button.pack(pady=10)

# Function to create a window for adding a new item 
def add_new_window(entry_type, entry_list):
    add_window = tk.Toplevel(window)
    add_window.title(f"Add New {entry_type}")
    add_window.config(bg=BACKGROUND_COLOR)
    
    label = tk.Label(add_window, text=f"Enter {entry_type}:", font=("Arial", 14, "bold"), bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
    label.pack(pady=10)
    
    description_label = tk.Label(add_window, text="Description:", font=("Arial", 12), bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
    description_label.pack(pady=5)
    description_entry = tk.Entry(add_window, font=("Arial", 12), width=30, bd=2, relief="solid", fg=TEXT_COLOR)
    description_entry.pack(pady=5)

    date_label = tk.Label(add_window, text="Date (YYYY-MM-DD):", font=("Arial", 12), bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
    date_label.pack(pady=5)
    date_entry = tk.Entry(add_window, font=("Arial", 12), width=30, bd=2, relief="solid", fg=TEXT_COLOR)
    date_entry.pack(pady=5)

    time_label = tk.Label(add_window, text="Time (HH:MM AM/PM):", font=("Arial", 12), bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
    time_label.pack(pady=5)
    time_entry = tk.Entry(add_window, font=("Arial", 12), width=30, bd=2, relief="solid", fg=TEXT_COLOR)
    time_entry.pack(pady=5)
    
    def save():
        description = description_entry.get()
        date = date_entry.get()
        time = time_entry.get()
        save_entry(entry_type, description, time, date, entry_list)
        description_entry.delete(0, tk.END)
        date_entry.delete(0, tk.END)
        time_entry.delete(0, tk.END)
    
    save_button = tk.Button(add_window, text=f"Save {entry_type}", font=("Arial", 12), bg=PRIMARY_COLOR, fg="white", command=save)
    save_button.pack(pady=10)

# Function to open the "Enter" window
def open_enter_window():
    enter_window = tk.Toplevel(window)
    enter_window.title("MyTask - Enter")
    enter_window.config(bg=BACKGROUND_COLOR)
    
    appointments_button = tk.Button(enter_window, text="Appointments", font=("Arial", 14), bg=PRIMARY_COLOR, fg="white", command=lambda: create_category_window("Appointment", appointments))
    appointments_button.pack(pady=20)
    
    goals_button = tk.Button(enter_window, text="Goals", font=("Arial", 14), bg=PRIMARY_COLOR, fg="white", command=lambda: create_category_window("Goal", goals))
    goals_button.pack(pady=20)
    
    schedules_button = tk.Button(enter_window, text="Schedules", font=("Arial", 14), bg=PRIMARY_COLOR, fg="white", command=lambda: create_category_window("Schedule", schedules))
    schedules_button.pack(pady=20)

# Main window 
window = tk.Tk()
window.title("MyTask")
window.config(bg=BACKGROUND_COLOR)

title_label = tk.Label(window, text="Welcome to MyTask", font=("Arial", 20, "bold"), bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
title_label.pack(pady=30)

# Main Menu
enter_button = tk.Button(window, text="Enter", font=("Arial", 14), bg=PRIMARY_COLOR, fg="white", command=open_enter_window)
enter_button.pack(pady=15)

settings_button = tk.Button(window, text="Settings", font=("Arial", 14), bg=PRIMARY_COLOR, fg="white", command=lambda: messagebox.showinfo("Settings", "Settings functionality can be added here."))
settings_button.pack(pady=15)

# Initialize empty lists for storing different task types
appointments = []
goals = []
schedules = []

# Run the application
window.mainloop()
