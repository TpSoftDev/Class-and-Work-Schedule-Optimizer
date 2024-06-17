############################################ Update Availability in Schedule Source ####################################
from datetime import datetime, timedelta
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
external_directory = os.path.join(current_dir, "..")
sys.path.append(external_directory)
from utils.helperFunctions import convert_to_availability
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
    {
        "subject": "Physics",
        "start": "12:00:00 PM",
        "end": "1:00:00 PM",
        "meetingDays": "M"
    },
    {
        "subject": "Math",
        "start": "7:00:00 AM",
        "end": "5:00:00 PM",
        "meetingDays": "T"
    },
    {
        "subject": "Hello",
        "start": "11:30:00 AM",
        "end": "12:45:00 PM",
        "meetingDays": "W"
    },
    {
        "subject": "Science",
        "start": "10:00:00 AM",
        "end": "8:00:00 PM",
        "meetingDays": "U"
    }
]

def generate_available_times_per_day():
    """
    Generate a dictionary with available times for each day of the week,
    where times are in 5-minute intervals from 00:00 to 23:59.

    Returns:
        dict: A dictionary with days of the week as keys and lists of available times as values.
    """
    available_times_per_day = {
        'Sunday': [],
        'Monday': [],
        'Tuesday': [],
        'Wednesday': [],
        'Thursday': [],
        'Friday': [],
        'Saturday': []
    }

    # Populate available times per day with 5-minute intervals
    for day in available_times_per_day:
        for hour in range(24):
            for minute in range(0, 60, 5):
                time_str = f"{hour:02d}:{minute:02d}"
                available_times_per_day[day].append(time_str)

    return available_times_per_day

def time_to_minutes(time_str):
    """
    Convert a time string in "HH:MM" format to minutes from midnight.

    Args:
        time_str (str): Time string in "HH:MM" format.

    Returns:
        int: Minutes since midnight.
    """
    time_obj = datetime.strptime(time_str, "%H:%M")
    return time_obj.hour * 60 + time_obj.minute

def remove_class_times(available_times, start, end):
    """
    Remove times from the available times list that fall within the class time range.

    Args:
        available_times (list): List of available times in "HH:MM" format.
        start (int): Start time in minutes since midnight.
        end (int): End time in minutes since midnight.

    Returns:
        list: Updated list of available times.
    """
    return [
        time for time in available_times
        if not (start <= time_to_minutes(time) < end)
    ]

def process_class_schedule(available_times_per_day, class_schedule):
    """
    Process the class schedule and update available times by removing class times.

    Args:
        available_times_per_day (dict): Dictionary with available times for each day.
        class_schedule (list): List of class schedules with start, end, and meeting days.

    Returns:
        dict: Updated available times per day.
    """
    days_map = {
        'U': 'Sunday',
        'M': 'Monday',
        'T': 'Tuesday',
        'W': 'Wednesday',
        'R': 'Thursday',
        'F': 'Friday',
        'A': 'Saturday'
    }

    for class_info in class_schedule:
        start_time_minutes = time_to_minutes(datetime.strptime(class_info["start"], "%I:%M:%S %p").strftime("%H:%M"))
        end_time_minutes = time_to_minutes(datetime.strptime(class_info["end"], "%I:%M:%S %p").strftime("%H:%M"))
        meeting_days = class_info["meetingDays"]

        for day in meeting_days:
            day_name = days_map[day]
            available_times_per_day[day_name] = remove_class_times(
                available_times_per_day[day_name],
                start_time_minutes,
                end_time_minutes
            )

    return available_times_per_day

def condense_times(times):
    """
    Condense a list of times into ranges.

    Args:
        times (list): List of times in "HH:MM" format.

    Returns:
        list: A list of time ranges in the format "HH:MM-HH:MM".
    """
    ranges = []
    if not times:
        return ranges

    start = times[0]
    previous = times[0]

    for time in times[1:]:
        current_hour, current_minute = map(int, time.split(':'))
        previous_hour, previous_minute = map(int, previous.split(':'))

        # Check if the current time is the next 5-minute interval after the previous time
        if not (current_hour == previous_hour and current_minute == previous_minute + 5) and not (
                current_hour == previous_hour + 1 and current_minute == 0 and previous_minute == 55):
            end = previous
            ranges.append(f"{start}-{end}")
            start = time

        previous = time

    ranges.append(f"{start}-{previous}")  # Add the last range
    return ranges

def condense_available_times_per_day(available_times_per_day):
    """
    Condense the available times into ranges for each day of the week.

    Args:
        available_times_per_day (dict): A dictionary with days of the week as keys and lists of available times as values.

    Returns:
        dict: A dictionary with days of the week as keys and lists of condensed time ranges as values.
    """
    return {day: condense_times(times) for day, times in available_times_per_day.items()}

# Generate available times per day
available_times_per_day = generate_available_times_per_day()

# Process the class schedule to update available times
available_times_per_day = process_class_schedule(available_times_per_day, employee_classSchedule)

# Condense available times into ranges for each day
condensed_available_times_per_day = condense_available_times_per_day(available_times_per_day)

employee_availability = []
# Output the condensed available times per day
for day, ranges in condensed_available_times_per_day.items():
    employee_availability.append(convert_to_availability(day, ranges, 170601496))

updateAvailability(employee_availability)