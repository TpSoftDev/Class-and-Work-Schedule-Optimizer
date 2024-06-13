# Class and Work Schedule Optimizer

The Class and Work Schedule Optimizer is a powerful Python application developed for Iowa State University's Dining Student Services Office. It revolutionizes the scheduling process by seamlessly integrating with Iowa State's Workday API for student schedules and ISU Dining's Schedule Source API for available work shifts.

## Overview

Managing student schedules and work shifts is a complex task that often involves manual effort and the potential for errors. The Class and Work Schedule Optimizer simplifies this process by automating the collection of student schedules from Iowa State's Workday API. It then cross-references this information with available shifts from ISU Dining's Schedule Source API to identify optimal work schedules that do not conflict with class times.

By leveraging these APIs, the optimizer ensures that schedules are always up-to-date, reducing the administrative burden on staff and minimizing scheduling conflicts for students. This sophisticated solution not only saves time and effort but also improves overall efficiency and accuracy in scheduling, ultimately enhancing the student and staff experience at Iowa State University.

## Features

- **User Input Interface**: The application begins with a user-friendly window where student coordinators and admin coordinators from the Dining Student Office can enter the student IDs, work facility names, and schedule templates for the students they are scheduling.
- **Class Schedule Integration**: Retrieves student class schedules using the Workday REST API, ensuring up-to-date and accurate information.
- **Work Shift Integration**: Retrieves available work shifts using the Schedule Source API, providing a comprehensive list of potential work times.
- **Excel Schedule Generation**: Automatically generates an Excel spreadsheet marking all class times as unavailable, allowing coordinators to see students' commitments at a glance.
- **Conflict Resolution**: Filters out work shifts that overlap with class times, presenting coordinators with only the shifts that students can realistically work.
- **File Path Display**: After generating the schedule, a new window pops up to display the file path of the generated Excel sheet, making it easy for coordinators to locate and use the file.

![diagram-export-11-06-2024-13_20_06](https://github.com/TpSoftDev/Class-and-Work-Schedule-Optimizer/assets/170199259/1e1cb687-3173-4260-8f13-4d3b2d481024)

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

## Usage

1. Run the main application script:
   ```bash
   python application.py
   ```
2. A window will prompt you to enter the following information:
   - **Student ID**: The unique student identifier.
   - **Work Facility Name**: The name of the work facility.
   - **Schedule Template**: The template for the schedule.

3. After entering the required information, press "OK" to proceed.
4. The application will:
   - Make an API call to the Workday REST API to retrieve the class schedule.
   - Generate an Excel spreadsheet (`Timetable.xlsx`) with class times marked as unavailable.
   - Make an API call to the Schedule Source website to retrieve available work shifts.
   - Filter out work shifts that conflict with class times.
   - Display a new window with the file path of the generated Excel sheet.

## Project Structure

- `application.py`: The main script that launches the application and handles the user interface.
- `availabilityCalculator/`: Contains modules for calculating availability based on the class schedule.
- `utils/`: Utility scripts and helper functions used throughout the project.
- `gridGenerator/`: Modules responsible for generating the timetable grid in the Excel spreadsheet.
- `Timetable.xlsx`: An example or template Excel file for the timetable.
- `api_calls/`: Scripts for handling API calls to external services (Workday REST API and Schedule Source API).
- `classSchedule.json`: A sample JSON file containing a class schedule for testing purposes.
- `.idea/`: Directory containing project-specific settings for IDEs like PyCharm.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions, support, or to report issues, please open an issue in the repository or contact the project maintainer.
