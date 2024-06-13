from datetime import datetime
import openpyxl

#Converts a string representing a time value and converts it to a programmable datetime.time() object
#Param: time_str - the time value in string format (e.g "12:00:00 AM" or "1900-05-10T13:00:00")
#Returns the same time, but as an instance datetime.time()
def convert_to_time(time_str):
    try:
        if "T" in time_str:  # Check if input is in "YYYY-MM-DDTHH:MM:SS" format
            datetime_obj = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S")
        else:  # Assuming the default format is "%I:%M:%S %p"
            datetime_obj = datetime.strptime(time_str, "%I:%M:%S %p")
        return datetime_obj.time()
    except ValueError:
        return None


def convert_to_readable_time(datetime_str):
    try:
        # Try to parse the datetime string with both date and time
        dt = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S")
        # Format the datetime object to a readable 12-hour time string
        readable_time = dt.strftime("%I:%M %p")
    except ValueError:
        # If the above fails, try to parse the string as a date only
        dt = datetime.strptime(datetime_str, "%Y-%m-%d")
        # Format the datetime object to indicate it's a whole day
        readable_time = "12:00 AM"  # Representing the start of the day

    return readable_time


def quicksort_shifts(shifts):
    if len(shifts) <= 1:
        return shifts
    else:
        pivot = shifts[len(shifts) // 2]["ShiftStart"]
        left = [x for x in shifts if x["ShiftStart"] < pivot]
        middle = [x for x in shifts if x["ShiftStart"] == pivot]
        right = [x for x in shifts if x["ShiftStart"] > pivot]
        return quicksort_shifts(left) + middle + quicksort_shifts(right)


def format_schedule_name(name):
    # Strip the whitespace at the end
    stripped_string = name.rstrip()
    
    # Replace the internal whitespaces with '+'
    replaced_string = stripped_string.replace(' ', '+')
    
    # Append back the original trailing whitespace
    trailing_whitespace = name[len(stripped_string):]
    
    # Combine the replaced string with the trailing whitespace removed
    final_string = replaced_string + trailing_whitespace
    return final_string


def getLocationNames(locations):
    string_list = []
    for item in locations:
        string_list.append(item["ExternalBusinessId"])
    return string_list

