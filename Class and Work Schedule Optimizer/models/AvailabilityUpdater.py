##################################################### Update Availability ##############################################
from datetime import datetime, timedelta
import os 
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
external_directory = os.path.join(current_dir, "..")
sys.path.append(external_directory)
from api_calls.schedule_source_api.schedule_source_api import updateAvailability

# Code Summary :
# This code will generate a list of available times for each day,
# remove times that overlap with the employee's class schedule,
# and then condense these times into ranges for easier readability.

# Define the employee availability data
employee_availability = [
    {
        "DayId": 1,
        "AvailableRanges": "5am-11am;1:45pm-5pm;6:15pm-11:15pm;",
        "LastName": "Abbasani",
        "FirstName": "Hari Preetham Reddy (Preetham)",
        "EmployeeExternalId": 170601496
    },
    {
        "DayId": 2,
        "AvailableRanges": "5am-9am",
        "LastName": "Abbasani",
        "FirstName": "Hari Preetham Reddy (Preetham)",
        "EmployeeExternalId": 170601496
    },
    {
        "DayId": 3,
        "AvailableRanges": "12:01am-11:59pm",
        "LastName": "Abbasani",
        "FirstName": "Hari Preetham Reddy (Preetham)",
        "EmployeeExternalId": 170601496
    },
    {
        "DayId": 4,
        "AvailableRanges": None,
        "LastName": "Abbasani",
        "FirstName": "Hari Preetham Reddy (Preetham)",
        "EmployeeExternalId": 170601496
    },
    {
        "DayId": 5,
        "AvailableRanges": None,
        "LastName": "Abbasani",
        "FirstName": "Hari Preetham Reddy (Preetham)",
        "EmployeeExternalId": 170601496
    },
    {
        "DayId": 6,
        "AvailableRanges": None,
        "LastName": "Abbasani",
        "FirstName": "Hari Preetham Reddy (Preetham)",
        "EmployeeExternalId": 170601496
    },
    {
        "DayId": 7,
        "AvailableRanges": None,
        "LastName": "Abbasani",
        "FirstName": "Hari Preetham Reddy (Preetham)",
        "EmployeeExternalId": 170601496
    }
]

# Define the employee class schedule data
employee_classSchedule = [
    {"subject": "Physics", "start": "09:15:00 AM", "end": "12:00:00 PM", "meetingDays": "UM"},
    {"subject": "Math", "start": "3:05:00 PM", "end": "4:15:00 PM", "meetingDays": "UR"},
    {"subject": "Hello", "start": "11:35:00 AM", "end": "9:45:00 PM", "meetingDays": "FA"},
    {"subject": "Science", "start": "05:00:00 AM", "end": "07:25:00 AM", "meetingDays": "T"}
]

def generate_available_times_per_day():
    """Generate a dictionary with available times for each day of the week."""
    available_times_per_day = {day: [f"{hour:02d}:{minute:02d}" for hour in range(24) for minute in range(0, 60, 5)] for day in ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]}
    return available_times_per_day

def time_to_minutes(time_str):
    """Convert a time string in "HH:MM" format to minutes from midnight."""
    time_obj = datetime.strptime(time_str, "%H:%M")
    return time_obj.hour * 60 + time_obj.minute

def remove_class_times(available_times, start, end):
    """Remove times from the available times list that fall within the class time range."""
    return [time for time in available_times if not (start <= time_to_minutes(time) < end)]

def process_class_schedule(available_times_per_day, class_schedule):
    """Process the class schedule and update available times by removing class times."""
    days_map = {'U': 'Sunday', 'M': 'Monday', 'T': 'Tuesday', 'W': 'Wednesday', 'R': 'Thursday', 'F': 'Friday', 'A': 'Saturday'}

    for class_info in class_schedule:
        start_time_minutes = time_to_minutes(datetime.strptime(class_info["start"], "%I:%M:%S %p").strftime("%H:%M"))
        end_time_minutes = time_to_minutes(datetime.strptime(class_info["end"], "%I:%M:%S %p").strftime("%H:%M"))
        meeting_days = class_info["meetingDays"]

        for day in meeting_days:
            day_name = days_map[day]
            available_times_per_day[day_name] = remove_class_times(available_times_per_day[day_name], start_time_minutes, end_time_minutes)

    return available_times_per_day

def condense_times(times):
    """Condense a list of times into ranges."""
    if not times:
        return []

    ranges = []
    start = previous = times[0]

    for time in times[1:]:
        if time_to_minutes(time) != time_to_minutes(previous) + 5:
            ranges.append(f"{start}-{previous}")
            start = time
        previous = time

    ranges.append(f"{start}-{previous}")
    return ranges

def condense_available_times_per_day(available_times_per_day):
    """Condense the available times into ranges for each day of the week."""
    return {day: condense_times(times) for day, times in available_times_per_day.items()}

def convert_to_12_hour_format(time_str):
    """Convert a time string from 24-hour format to 12-hour format."""
    time_obj = datetime.strptime(time_str, "%H:%M")
    return time_obj.strftime("%I:%M%p").lstrip('0').lower()

def format_ranges_12_hour(ranges):
    """Convert and format time ranges from 24-hour format to 12-hour format."""
    formatted_ranges = []
    for time_range in ranges:
        start, end = time_range.split('-')
        start_12 = convert_to_12_hour_format(start)
        end_12 = convert_to_12_hour_format(end)
        formatted_ranges.append(f"{start_12}-{end_12}")
    return ';'.join(formatted_ranges) + ';'

# Generate available times per day
available_times_per_day = generate_available_times_per_day()

# Process the class schedule to update available times
available_times_per_day = process_class_schedule(available_times_per_day, employee_classSchedule)

# Condense available times into ranges for each day
condensed_available_times_per_day = condense_available_times_per_day(available_times_per_day)

avail_ranges = []
# Convert to 12-hour format and add to list of available time ranges 
for day, ranges in condensed_available_times_per_day.items():
    formatted_ranges = format_ranges_12_hour(ranges)
    print(f"{day}: {formatted_ranges}")
    avail_ranges.append(formatted_ranges)

updatedData = []
for i in range(1, 8):
    updatedData.append({
        "DayId": i,
        "AvailableRanges": avail_ranges[i-1], 
        "EmployeeExternalId": 170601496   
    })

updateAvailability(updatedData)


    
    
