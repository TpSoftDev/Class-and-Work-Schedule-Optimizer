import requests
import json
import http
from urllib.parse import urlencode

import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
external_directory = os.path.join(current_dir, "../..")
sys.path.append(external_directory)

from utils.Paths import Paths
from utils.URLs import URLs


#Used to sign in to mgr portal of schedule source. 
#Params: "code" - facility code used to sign in ("ISU For all")
#        "username" - mgr username used to sign in 
#        "password" - mgr password used to sign in
#
#  Returns: API token and Session ID codes. Needed to be used as headers to retrieve information from API
def authenticate(code, username, password):
    ##########  Part 1 #########
    url = URLs.AUTHENTICATE.value
    payload = json.dumps(
        {
            "ExternalId": "",
            "Request": {
                "Portal": "mgr",
                "Code": code,
                "Username": username,
                "Password": password,
            },
        }
    )
    headers = {
        "Content-Type": "application/json",
        "BuildCookie": "24060420361420.32735534d2ac453faeb6fc50bf314f4d",
        "Cookie": "BuildCookie=24060420361420.32735534d2ac453faeb6fc50bf314f4d",
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    response_json = response.json()
    api_token = response_json["Response"]["APIToken"]
    session_id = response_json["Response"]["SessionId"]
    return {"sessionId": session_id, "apiToken": api_token}


#Get the specific schedule ID from the facility name and the name of the schedule. 
#ID will be used to get shift information of the schedule
#Params: "facilityName" - the name of the facility we are pulling the schedule from (e.g "dsso", "udm", "friley", etc)
#        "scheduleName" - the name of the schedule we want to pull shifts from (e.g "UDM Spring 2024 Master")
#
# Returns the schedule ID used to access the shift information of the specific schedule
def getScheduleId(facilityName, scheduleName):
    credentials = authenticate("ISU", "seans3", "8032")
    conn = http.client.HTTPSConnection("test.tmwork.net")
    payload = ""

    headers = {
        "Content-Type": "application/json",
        "x-session-id": credentials["sessionId"],
        "x-api-token": credentials["apiToken"],
    }
    
    path = Paths.SS_SCHEDULE.value
    query_params = {
        "Fields": "Name,ScheduleId",
        "MinDate": "2023-08-10",
        "MaxDate": "2030-05-10",
        "BusinessExternalId": facilityName,
        "Name": scheduleName
    }

    encoded_query_params = urlencode(query_params)
    url = f"{path}?{encoded_query_params}"
    

    conn.request(
        "GET",
        url,
        payload,
        headers,
    )

    res = conn.getresponse()
    data = res.read()
    try:
        json_data = json.loads(data)
        json_object = json_data[0]
        scheduleId = json_object.get("ScheduleId")
        print("Schedule ID: " + str(scheduleId))
        return scheduleId
    except Exception as e:
        print("An error has occurred while fetching Schedule ID: " + e)
        return None


#Used to pull all empty shifts for the specific schedule. Needed for computing the available shifts a new hire can work
#Params: "scheduleId" - the unique id number for a schedule (retrieved from getSchedueleId)
#        "dayId"  - the number representing the day of the week (1="Sunday" ; 2="Monday" ...)
#
#Returns a list of empty shift objects in a JSON format
def getEmptyShiftsForDay(scheduleId, dayId):
    credentials = authenticate("ISU", "seans3", "8032")
    conn = http.client.HTTPSConnection("test.tmwork.net")
    payload = ""

    headers = {
        "Content-Type": "application/json",
        "x-session-id": credentials["sessionId"],
        "x-api-token": credentials["apiToken"],
    }

    path = Paths.SS_SCHEDULE_SHIFTS.value
    query_params = {
        "Fields": "ShiftStart,ShiftEnd,StationName,DayId,EmployeeExternalId",
        "MinDate": "2024-01-10",
        "MaxDate": "2024-01-16",
        "DayId": dayId,
        "ScheduleId": scheduleId,
        "EmployeeExternalId": "{NULL}",
    }

    encoded_query_params = urlencode(query_params)
    url = f"{path}?{encoded_query_params}"

    conn.request(
        "GET",
        url,
        payload,
        headers,
    )
    res = conn.getresponse()
    data = res.read()
    return json.loads(data)


#Direct API Call to retrieve a list of locations and their respective ID's
#Returns a list of the json data retrieved from the API call
def getLocations():
    credentials = authenticate("ISU", "seans3", "8032")
    conn = http.client.HTTPSConnection("test.tmwork.net")
    payload = ""

    headers = {
        "Content-Type": "application/json",
        "x-session-id": credentials["sessionId"],
        "x-api-token": credentials["apiToken"],
    }

    base_url = Paths.SS_LOCATIONS.value
    url = (
        f"{base_url}"
        "?Fields=ExternalBusinessId"
    )
    
    conn.request(
        "GET",
        url,
        payload,
        headers,
    )
    
    res = conn.getresponse()
    data = res.read()
    json_data = json.loads(data)
    filtered_data = []
    for item in json_data:
        if item["ExternalBusinessId"] is not None:
            if not(isinstance(item["ExternalBusinessId"], int)):
                filtered_data.append(item)
                
    return filtered_data


#API call to get the list of all schedules active in a specific date range (now to 6 years in the future)
def getScheduleNames(location):
    credentials = authenticate("ISU", "seans3", "8032")
    conn = http.client.HTTPSConnection("test.tmwork.net")
    payload = ""

    headers = {
        "Content-Type": "application/json",
        "x-session-id": credentials["sessionId"],
        "x-api-token": credentials["apiToken"],
    }

    path = Paths.SS_SCHEDULE.value
    query_params = {
        "Fields": "Name",
        "MinDate": "2023-08-10",
        "MaxDate": "2030-05-10",
        "BusinessExternalId": location
    }

    encoded_query_params = urlencode(query_params)
    url = f"{path}?{encoded_query_params}"
    
    conn.request(
        "GET",
        url,
        payload,
        headers,
    )
    
    res = conn.getresponse()
    data = res.read()
    json_data = json.loads(data)
    names = []
    for item in json_data:
        names.append(item["Name"])
    return names


# API call to update (PUT) the availability of a student employee
def updateAvailability(newAvailability):
    credentials = authenticate("ISU", "seans3", "8032")
    conn = http.client.HTTPSConnection("test.tmwork.net")
    payload = newAvailability

    headers = {
        "Content-Type": "application/json",
        "x-session-id": credentials["sessionId"],
        "x-api-token": credentials["apiToken"],
    }

    payload_json = json.dumps(payload)
    
    url = Paths.SS_AVAILABILITY.value
    conn.request("PUT", url, payload_json, headers)
    res = conn.getresponse()
    data = res.read()
    print(data)
        
