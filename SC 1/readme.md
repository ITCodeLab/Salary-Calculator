# Salary Calculator System

## Overview
The Salary Calculator System is a Python-based desktop application designed to manage employee salaries, track attendance, and handle cash advances and incentives. Built with Tkinter for the GUI, the system supports both finishing and carpentry employees, providing an efficient way to maintain payroll records.

## Features
- **Employee Management**: Add, edit, and delete employee records.
- **Attendance Tracking**: Record full-day, half-day, or absence for each employee across the week.
- **Salary Calculation**: Automatically calculates salaries based on attendance.
- **Cash Advance and Incentives**: Update and track cash advances and incentives.
- **Data Export**: Export salary and attendance records to Excel and text files.
- **Responsive UI**: Resizable GUI with intuitive buttons and tables.

## Technologies Used
- **Python 3.x**
- **Tkinter** for the graphical user interface.
- **Pandas** for data manipulation and Excel export.
- **JSON** for data storage.
- **OS and Datetime** for file handling and timestamping.

## Installation
1. Clone the repository or download the source code.
2. Install the required dependencies using pip:
   ```bash
   pip install pandas
   ```
3. Run the program:
   ```bash
   python SalaryCalculator.py
   ```

## Usage
- **Employee Management**: Use the 'Employee' buttons to add, edit, or delete employee details.
- **Attendance**: Select an employee and click 'Track Attendance' to log their daily attendance.
- **Salary Calculation**: Click 'Calculate Salary' after tracking attendance to compute salaries.
- **Export Data**: Use 'Download Excel, txt File' to save attendance and salary data.
- **Reset Data**: The 'Reset' button clears attendance and cash advances for selected employees.

## File Structure
- **SalaryCalculator.py**: Main application script.
- **C:\SCfiles\receipts**: Directory for storing JSON data, Excel files, and text receipts.

## Future Enhancements
- Implement QR code scanning for automated attendance logging.
- Add real-time dashboards and automated report generation with email notifications.

## License
This project is licensed under the MIT License.

## Contact
For inquiries or contributions, please contact Ian Tolentino at iantolentino0110@gmail.com 

