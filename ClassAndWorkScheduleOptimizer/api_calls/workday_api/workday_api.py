import requests
import http
import json
import os
import sys


current_dir = os.path.dirname(os.path.abspath(__file__))
external_directory = os.path.join(current_dir, "../..")
sys.path.append(external_directory)

from utils.URLs import URLs


#Retrieve student's list of courses and their meeting days/times. 
#Param : "student_id" - the unique university ID number for a student 
#
#Returns a list of class sections the student is enrolled in for the semester
# This api call is to a mock url generated from post man. Once we get clearance to workdays servers, this will be changed
def getStudentSchedule(student_id):
    url = URLs.GET_CLASS_SCHEDULE_TEST.value
    response = requests.get(url)
    
    if response.status_code == 200:
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError as e:
            # Handle JSON decode error
            print(f"JSONDecodeError: {e}")
            print("Response content:", response.text)
            return None
    else:
        # Handle non-200 status codes
        print("Error:", response.status_code, response.reason)
        return None
    
    
    
    
    