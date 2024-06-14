########################################### This File is for the Python UI #############################################
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import Toplevel, Text
import subprocess
import os
from utils.Paths import Paths
from utils.helperFunctions import convert_to_readable_time, quicksort_shifts, format_schedule_name, getLocationNames
from api_calls.schedule_source_api.schedule_source_api import getScheduleId, getEmptyShiftsForDay, getLocations, getScheduleNames
from availabilityCalculator.main import filterEmptyShiftsForDay

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

########################################### execute_backend_script #####################################################
# Function to execute the backend script and return the path to the generated timetable
def execute_backend_script():
    # Get the current working directory
    current_dir = os.getcwd()

    # Get the directory of the currently running Python script
    current_pyDirectory = os.path.dirname(os.path.abspath(__file__))

    # Get the path to the Python interpreter
    python_executable = sys.executable

    # Run the backend script
    subprocess.run([python_executable, os.path.join(current_pyDirectory, "gridGenerator/gridGenerator.py")])

    print(f"{current_dir}")
    print(f"{current_pyDirectory }")
    print(f"{python_executable}")


    # Return the path to the generated timetable file in the current working directory
    return os.path.join(current_dir, "Timetable.xlsx")


#########################################  show_file_path Window  #######################################################
# Function to create a new window displaying the file path
def show_file_path(file_path):
    # Create a new top-level window
    new_window = tk.Toplevel(root)
    new_window.title("Generated Timetable")
    new_window.geometry("600x200")

    # Display the file path
    ttk.Label(new_window, text="Timetable generated at:").pack(pady=10)

    # Display the file path in a larger white font
    file_path_label = tk.Label(new_window, text=file_path, fg="black", font=("Helvetica", 15, "bold"))
    file_path_label.pack(pady=10)

    # Button to close the new window and terminate the program
    ttk.Button(new_window, text="OK", command=root.quit).pack(pady=10)


# Function to be called when the OK button is pressed
def on_ok():
    # Print the values entered in the entry fields
    print(f"Facility Name: {selected_facility_var.get()}")
    print(f"Schedule Name: {selected_schedule_var.get()}")
    print(f"External ID: {external_id.get()}")
    
    try :
        #Retrieve the schedule ID number based on the user input
        scheduleId = getScheduleId(selected_facility_var.get().rstrip(), selected_schedule_var.get().rstrip())
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch Schedule ID: {e}")
   
    #Show that the program is loading/executing
    print("Loading Window...")

    # Withdraw the main window
    root.withdraw()

    # Execute the backend script and get the file path
    file_path = execute_backend_script()
    
    #Open window for listing available empty shifts
    if scheduleId:
        open_empty_shifts_window(0, scheduleId)
        
    else:
        print("Error Retrieving the Schedule ID Number")

    # Show the file path in a new window
    show_file_path(file_path)

       
#Opens a new window when the schedule is generated that shows the list of available shifts the employee can work
def open_empty_shifts_window(studentId, scheduleId):
    new_window = Toplevel(root)
    
    new_window.title("Availble Shifts")
    new_window.geometry("600x400")
    label = tk.Label(new_window, text="Shifts Available To Work")
    label.pack(pady=20)
    
    text_widget = Text(new_window)
    text_widget.pack(expand=True, fill='both')
    
    def printAllEmptyShifts(studentId, scheduleId):
        text_widget.insert(tk.END, " Day\t\t  Start\t\t  End\t\t  Station\n\n")
        for dayId in range(1, 8):
            printEmptyShiftsForDay(studentId, scheduleId, dayId)
            text_widget.insert(tk.END, "\n")
            
            
    def printEmptyShiftsForDay(studentId, scheduleId, dayId):
        dayString = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"][dayId-1]
        emptyShifts = getEmptyShiftsForDay(scheduleId, dayId)
        emptyShifts = filterEmptyShiftsForDay(studentId, emptyShifts)
        emptyShifts = quicksort_shifts(emptyShifts)

        for shift in emptyShifts:
            readableStart = convert_to_readable_time(shift["ShiftStart"])
            readableEnd = convert_to_readable_time(shift["ShiftEnd"])
            text_widget.insert(tk.END,
                f"{dayString}\t\t{readableStart}\t\t{readableEnd}\t\t{shift['StationName']}\n"
            )
            
    printAllEmptyShifts(studentId, scheduleId)

    # Add a button to close the new window
    close_button = tk.Button(new_window, text="Close", command=new_window.destroy)
    close_button.pack(pady=10)

   
#Triggers a function that retrieves the list of schedules when an option is changed
#Used to allow us to pass in the location's name as a parameter to the actual function
def select_location(event):
    selected_facility = selected_facility_var.get()
    on_location_change(selected_facility)


#Search function that will display the list of schedules for the location selected in the first input
def on_location_change(newLocation):
    global schedule_name_list  # Declare that we are using the global variable
    schedule_name_list = getScheduleNames(newLocation)
    initDropdowns()
    print("Location Changed to " + newLocation)


#Set the dropdown menu input fields and their respective values
#Called each time the location is changed in the first dropdown to re-update the schedules
def initDropdowns():
    # Label and Entry widget for Facility Name
    ttk.Label(root, text="Facility Name:").grid(column=0, row=0, padx=10, pady=5, sticky=tk.W)
    facility_name = ttk.Combobox(root, textvariable=selected_facility_var, values=sorted(location_name_list), width=30)
    facility_name.bind('<<ComboboxSelected>>', select_location)
    facility_name.grid(column=1, row=0, padx=10, pady=5)
    
    # Label and Entry widget for Schedule Name
    ttk.Label(root, text="Schedule Name:").grid(column=0, row=1, padx=10, pady=5, sticky=tk.W)
    schedule_name = ttk.Combobox(root, textvariable=selected_schedule_var, values=schedule_name_list, width=30)
    schedule_name.grid(column=1, row=1, padx=10, pady=5)

# Create the main window
root = tk.Tk()
root.title("Class Schedule Generator")
root.geometry("440x160")

#Create lists of locations for the first dropdown menu
location_list = getLocations()
location_name_list = getLocationNames(location_list)

#Keeps track of the location and schedule selected from the dropdown menu
selected_facility_var = tk.StringVar(root)
selected_schedule_var = tk.StringVar(root)

#Set the initital dropdown value
selected_facility_var.set("Select a location")


#Declare variables that will get initialized in initDropdowns()
schedule_name_list = []

initDropdowns()

# Label and Entry widget for External ID
ttk.Label(root, text="External ID:").grid(column=0, row=2, padx=10, pady=5, sticky=tk.W)
external_id = ttk.Entry(root, width=30)
external_id.grid(column=1, row=2, padx=10, pady=5)

# Button to generate the schedule
generate_button = ttk.Button(root, text="Generate Schedule", command=on_ok)
generate_button.grid(column=0, row=3, columnspan=2, pady=10)

# Add padding around the entire grid
for child in root.winfo_children():
    child.grid_configure(padx=10, pady=5)

# Run the application
root.mainloop()