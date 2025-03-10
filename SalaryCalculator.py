import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import pandas as pd
from datetime import datetime  # Import datetime module

class SalaryCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Salary Calculator")
        root.geometry("1920x1080")
        root.resizable(True, True)
        self.data = []
        
        # Set the desired folder path
        self.file_path = r"C:\SCfiles\receipts"  # Path for the new folder structure
        
        # Create the directory structure if it doesn't exist
        if not os.path.exists(self.file_path):
            os.makedirs(self.file_path)
        
        self.finishing_employees = []
        self.carpentry_employees = []
        self.status_label = tk.Label(self.root, text="", font=("Arial", 14), fg="blue")
        self.status_label.pack(pady=5)  # Status label for messages
        
        # Load existing data
        self.load_data()
        self.create_widgets()
    
    def center_window(self, width, height, window=None):
        window = window or self.root
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        # Increase font size for better visibility
        tk.Label(self.root, text="Salary Calculator", font=("Arial", 30, "bold"), fg="green").pack(pady=20)
        frame_top = tk.Frame(self.root)
        frame_top.pack(pady=10)
        
        # Finishing Section
        frame_finishing = tk.LabelFrame(frame_top, text="Finishing", fg="green", font=("Arial", 24))
        frame_finishing.pack(side="left", padx=20, pady=10, fill="both", expand=True)
        ttk.Label(frame_finishing, text="Select Employee:", font=("Arial", 20)).pack(padx=10, pady=10)
        self.finishing_employee_dropdown = ttk.Combobox(frame_finishing, state="readonly", font=("Arial", 18), width=40)
        self.finishing_employee_dropdown.pack(padx=10)
        self.finishing_employee_dropdown['values'] = ["Unknown"] + [emp[0] for emp in self.finishing_employees]
        self.finishing_employee_dropdown.current(0)
        self.finishing_employee_dropdown.bind("<<ComboboxSelected>>", self.update_attendance_display)
        tk.Button(frame_finishing, text="Employee", command=lambda: self.open_employee_management("Finishing"), bg="green", fg="white", font=("Arial", 18), width=20).pack(pady=10)
        
        # Carpentry Section
        frame_carpentry = tk.LabelFrame(frame_top, text="Carpentry", fg="green", font=("Arial", 24))
        frame_carpentry.pack(side="right", padx=20, pady=10, fill="both", expand=True)
        ttk.Label(frame_carpentry, text="Select Employee:", font=("Arial", 20)).pack(padx=10, pady=10)
        self.carpentry_employee_dropdown = ttk.Combobox(frame_carpentry, state="readonly", font=("Arial", 18), width=40)
        self.carpentry_employee_dropdown.pack(padx=10)
        self.carpentry_employee_dropdown['values'] = ["Unknown"] + [emp[0] for emp in self.carpentry_employees]
        self.carpentry_employee_dropdown.current(0)
        self.carpentry_employee_dropdown.bind("<<ComboboxSelected>>", self.update_attendance_display)
        tk.Button(frame_carpentry, text="Employee", command=lambda: self.open_employee_management("Carpentry"), bg="green", fg="white", font=("Arial", 18), width=20).pack(pady=10)
        
        # Attendance Display
        self.attendance_frame = tk.LabelFrame(self.root, text="Attendance", fg="blue", font=("Arial", 20))
        self.attendance_frame.pack(pady=10, fill="x", padx=30)
        
        # Employee Name Display with increased font size
        self.employee_name_label = tk.Label(self.attendance_frame, text="Employee: None", font=("Arial", 18, "bold"), fg="black")
        self.employee_name_label.pack(side="left", padx=20)
        self.attendance_labels = []
        for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
            label = tk.Label(self.attendance_frame, text=f"{day}: Pending", fg="gray", font=("Arial", 18))
            label.pack(side="left", padx=10)
            self.attendance_labels.append(label)

        # Cash Advance and Incentive Display
        cash_incentive_frame = tk.Frame(self.root)
        cash_incentive_frame.pack(pady=1, anchor="w")
        self.cash_advance_label = tk.Label(cash_incentive_frame, text="Cash Advance: None", font=("Arial", 18, "bold"))
        self.cash_advance_label.pack(side="top", padx=52, pady=10)
        self.incentive_label = tk.Label(cash_incentive_frame, text="Incentive: None", font=("Arial", 18, "bold"))
        self.incentive_label.pack(side="top", padx=0.01, pady=10)

        # Button Frames
        button_frame_top = tk.Frame(self.root)
        button_frame_top.pack(pady=10)

        # First row of buttons
        button_width = 18
        tk.Button(button_frame_top, text="Track Attendance", command=self.track_attendance, bg="blue", fg="white", font=("Arial", 17), width=button_width).pack(side="left", padx=5)
        tk.Button(button_frame_top, text="Calculate Salary", command=self.calculate_salary, bg="green", fg="white", font=("Arial", 17), width=button_width).pack(side="left", padx=5)
        tk.Button(button_frame_top, text="Update Incentive", command=self.update_incentive, bg="green", fg="white", font=("Arial", 17), width=button_width).pack(side="left", padx=5)
        tk.Button(button_frame_top, text="Update Cash Advance", command=self.update_cash_advance, bg="purple", fg="white", font=("Arial", 17), width=button_width).pack(side="left", padx=5)

        # Second row of buttons
        button_frame_bottom = tk.Frame(self.root)
        button_frame_bottom.pack(pady=10)
        tk.Button(button_frame_bottom, text="Download Excel, txt File", command=self.export_to_excel, bg="lightblue", fg="black", font=("Arial", 17), width=button_width).pack(side="left", padx=5)
        tk.Button(button_frame_bottom, text="Reset", command=self.reset_attendance_and_cash_advance, bg="red", fg="white", font=("Arial", 17), width=button_width).pack(side="left", padx=5)
        tk.Button(button_frame_bottom, text="Refresh", command=self.refresh_data, bg="orange", fg="white", font=("Arial", 17), width=button_width).pack(side="left", padx=5)

        # Split Tables for Finishing and Carpentry
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill="x", pady=20, padx=30)
                
        # Initialize the style object
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("TkDefaultFont", 15))
        style.configure("Treeview", font=("TkDefaultFont", 14))
        
        # Finishing Table
        self.finishing_tree = ttk.Treeview(table_frame, columns=("Employee", "Work Status", "Salary", "Incentive", "Cash Advance"), show='headings')
        for col in self.finishing_tree['columns']:
            self.finishing_tree.heading(col, text=col, anchor='center')
            self.finishing_tree.column(col, anchor='center', width=150)
        self.finishing_tree.pack(side="left", fill="y", expand=True, padx=15)
        
        # Carpentry Table
        self.carpentry_tree = ttk.Treeview(table_frame, columns=("Employee", "Work Status", "Salary", "Incentive", "Cash Advance"), show='headings')
        for col in self.carpentry_tree['columns']:
            self.carpentry_tree.heading(col, text=col, anchor='center')
            self.carpentry_tree.column(col, anchor='center', width=150)
        self.carpentry_tree.pack(side="right", fill="y", expand=True, padx=15)

    def update_cash_advance_display(self):
        employee = self.finishing_employee_dropdown.get() if self.finishing_employee_dropdown.get() != "Unknown" else self.carpentry_employee_dropdown.get()
        
        if employee == "Unknown":
            self.cash_advance_label.config(text="Cash Advance: None")
            self.incentive_label.config(text="Incentive: None")
        else:
            cash_advance = next((emp[2] for emp in self.finishing_employees if emp[0] == employee), None)
            if cash_advance is None:
                cash_advance = next((emp[2] for emp in self.carpentry_employees if emp[0] == employee), None)
            incentive = self.get_incentive(employee)
            salary = next((emp[1] for emp in self.finishing_employees if emp[0] == employee), None)
            if salary is None:
                salary = next((emp[1] for emp in self.carpentry_employees if emp[0] == employee), None)
            self.cash_advance_label.config(text=f"Cash Advance: {cash_advance}")
            self.incentive_label.config(text=f"Incentive: {incentive}")
            self.employee_name_label.config(text=f"Employee: {employee}")  # add Salary: {salary} if need a salary labels

    def get_incentive(self, employee):
        for item in self.finishing_tree.get_children():
            if self.finishing_tree.item(item, "values")[0] == employee:
                return self.finishing_tree.item(item, "values")[3]
        for item in self.carpentry_tree.get_children():
            if self.carpentry_tree.item(item, "values")[0] == employee:
                return self.carpentry_tree.item(item, "values")[3]
        return 0

    def update_incentive(self):
        employee = self.finishing_employee_dropdown.get() if self.finishing_employee_dropdown.get() != "Unknown" else self.carpentry_employee_dropdown.get()
        if employee == "Unknown":
            self.status_label.config(text="Error: Please select an employee.")
            return
        current_incentive = self.get_incentive(employee)
        new_incentive = simpledialog.askfloat("Update Incentive", f"Enter new incentive for {employee}:", initialvalue=current_incentive)
        
        if new_incentive is not None:
            if employee in [emp[0] for emp in self.finishing_employees]:
                for item in self.finishing_tree.get_children():
                    if self.finishing_tree.item(item, "values")[0] == employee:
                        values = self.finishing_tree.item(item, "values")
                        self.finishing_tree.item(item, values=(values[0], values[1], values[2], new_incentive, values[4]))
                        break
            elif employee in [emp[0] for emp in self.carpentry_employees]:
                for item in self.carpentry_tree.get_children():
                    if self.carpentry_tree.item(item, "values")[0] == employee:
                        values = self.carpentry_tree.item(item, "values")
                        self.carpentry_tree.item(item, values=(values[0], values[1], values[2], new_incentive, values[4]))
                        break
            self.update_cash_advance_display()  # Refresh display
            self.save_data()
            self.export_to_excel()  # Also save to Excel and TXT when updating incentive

    def update_cash_advance(self):
        employee = self.finishing_employee_dropdown.get() if self.finishing_employee_dropdown.get() != "Unknown" else self.carpentry_employee_dropdown.get()
        if employee == "Unknown":
            self.status_label.config(text="Error: Please select an employee.")
            return
        current_cash_advance = next((emp[2] for emp in self.finishing_employees if emp[0] == employee), None)
        if current_cash_advance is None:
            current_cash_advance = next((emp[2] for emp in self.carpentry_employees if emp[0] == employee), None)
        new_cash_advance = simpledialog.askfloat("Update Cash Advance", f"Enter new cash advance for {employee}:", initialvalue=current_cash_advance)
        
        if new_cash_advance is not None:
            if employee in [emp[0] for emp in self.finishing_employees]:
                for i, emp in enumerate(self.finishing_employees):
                    if emp[0] == employee:
                        self.finishing_employees[i] = (emp[0], emp[1], new_cash_advance)
                        break
            elif employee in [emp[0] for emp in self.carpentry_employees]:
                for i, emp in enumerate(self.carpentry_employees):
                    if emp[0] == employee:
                        self.carpentry_employees[i] = (emp[0], emp[1], new_cash_advance)
                        break
            self.update_tree_cash_advance(employee, new_cash_advance)
            self.update_cash_advance_display()  # Refresh display
            self.save_data()
            self.export_to_excel()  # Also save to Excel and TXT when updating cash advance

    def update_tree_cash_advance(self, employee, new_cash_advance):
        for tree in (self.finishing_tree, self.carpentry_tree):
            for item in tree.get_children():
                if tree.item(item, "values")[0] == employee:
                    values = tree.item(item, "values")
                    tree.item(item, values=(values[0], values[1], values[2], values[3], new_cash_advance))

    def open_employee_management(self, category):
        employee_window = tk.Toplevel(self.root)
        employee_window.title(f"Manage {category} Employees")
        self.center_window(400, 400, employee_window)

        # Listbox to display employees
        self.employee_listbox = tk.Listbox(employee_window, height=10, width=50)
        self.employee_listbox.pack(pady=10)

        # Populate listbox based on category
        if category == "Finishing":
            employees = self.finishing_employees
        elif category == "Carpentry":
            employees = self.carpentry_employees
        self.update_employee_listbox(employees)

        # Buttons to manage employees
        tk.Button(employee_window, text="Add", command=lambda: self.add_employee(category), width=15).pack(pady=5)
        tk.Button(employee_window, text="Edit", command=lambda: self.edit_employee(category), width=15).pack(pady=5)
        tk.Button(employee_window, text="Delete", command=lambda: self.delete_employee(category), width=15).pack(pady=5)

    def update_employee_listbox(self, employees):
        self.employee_listbox.delete(0, tk.END)
        for employee in employees:
            self.employee_listbox.insert(tk.END, f"{employee[0]} - Salary: {employee[1]}, Cash Advance: {employee[2]}")

    def add_employee(self, category):
        name = simpledialog.askstring("Add Employee", "Enter employee name:")
        salary = simpledialog.askfloat("Add Salary", "Enter employee salary:")
        if name and salary:
            cash_advance = simpledialog.askfloat("Cash Advance", "Enter initial cash advance:", initialvalue=0.0)
            if cash_advance is not None:
                if category == "Finishing":
                    self.finishing_employees.append((name, salary, cash_advance))
                    self.data.append({"Employee": name, "Attendance": {day: "Pending" for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}})
                elif category == "Carpentry":
                    self.carpentry_employees.append((name, salary, cash_advance))
                    self.data.append({"Employee": name, "Attendance": {day: "Pending" for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}})
                self.update_employee_listbox(self.finishing_employees if category == "Finishing" else self.carpentry_employees)
                self.save_data()
                self.update_attendance_display()  # Update attendance display for the new employee

    def edit_employee(self, category):
        selected_employee = self.employee_listbox.curselection()
        if selected_employee:
            employee_data = self.employee_listbox.get(selected_employee)
            name, details = employee_data.split(" - ")
            salary_str, cash_advance_str = details.split(", Cash Advance: ")
            cash_advance = float(cash_advance_str)
            salary = float(salary_str.split(": ")[1])

            new_name = simpledialog.askstring("Edit Employee", f"Edit the name of {name}:", initialvalue=name)
            new_salary = simpledialog.askfloat("Edit Salary", f"Edit the salary of {name}:", initialvalue=salary)
            new_cash_advance = simpledialog.askfloat("Edit Cash Advance", f"Edit the cash advance of {name}:", initialvalue=cash_advance)
            
            if new_name and new_salary and new_cash_advance is not None:
                if category == "Finishing":
                    self.finishing_employees[selected_employee[0]] = (new_name, new_salary, new_cash_advance)
                elif category == "Carpentry":
                    self.carpentry_employees[selected_employee[0]] = (new_name, new_salary, new_cash_advance)
                self.update_employee_listbox(self.finishing_employees if category == "Finishing" else self.carpentry_employees)
                self.save_data()

    def delete_employee(self, category):
        selected_employee = self.employee_listbox.curselection()
        if selected_employee:
            employee_name = self.employee_listbox.get(selected_employee).split(" - ")[0]
            if messagebox.askyesno("Delete", f"Are you sure you want to delete {employee_name}?"):
                if category == "Finishing":
                    self.finishing_employees.pop(selected_employee[0])
                elif category == "Carpentry":
                    self.carpentry_employees.pop(selected_employee[0])
                self.update_employee_listbox(self.finishing_employees if category == "Finishing" else self.carpentry_employees)
                self.remove_employee_data(employee_name)  # Remove data from all associated files
                self.save_data()  # Save data after deletion

    def remove_employee_data(self, employee_name):
        # Remove attendance and cash advance data for the deleted employee
        self.data = [record for record in self.data if record["Employee"] != employee_name]
        self.save_data()  # Save changes to the JSON file

    def refresh_data(self):
        self.load_data()
        self.finishing_employee_dropdown['values'] = ["Unknown"] + [emp[0] for emp in self.finishing_employees]
        self.carpentry_employee_dropdown['values'] = ["Unknown"] + [emp[0] for emp in self.carpentry_employees]
        self.update_cash_advance_display()
        self.status_label.config(text="Employee data refreshed successfully.")

    def track_attendance(self):
        employee = self.finishing_employee_dropdown.get() if self.finishing_employee_dropdown.get() != "Unknown" else self.carpentry_employee_dropdown.get()
        if employee == "Unknown":
            self.status_label.config(text="Error: Please select an employee.")
            return

        attendance_window = tk.Toplevel(self.root)
        attendance_window.title(f"Attendance for {employee}")
        self.center_window(600, 300, attendance_window)
        attendance_window.geometry("600x300")

        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.attendance_vars = {day: tk.StringVar(value="Pending") for day in days}

        for day in days:
            frame = tk.Frame(attendance_window)
            frame.pack(fill="x", padx=5, pady=2)
            tk.Label(frame, text=day).pack(side="left")
            tk.Button(frame, text="Full", command=lambda d=day: self.set_attendance(d, "F")).pack(side="left", padx=5)
            tk.Button(frame, text="Half", command=lambda d=day: self.set_attendance(d, "H")).pack(side="left", padx=5)
            tk.Button(frame, text="Absent", command=lambda d=day: self.set_attendance(d, "A")).pack(side="left", padx=5)

        tk.Button(attendance_window, text="OK", command=lambda: self.submit_attendance(employee, attendance_window), width=15).pack(pady=10)

    def set_attendance(self, day, status):
        self.attendance_vars[day].set(status)

    def submit_attendance(self, employee, window):
        attendance_record = {day: var.get() for day, var in self.attendance_vars.items()}
        
        # Check if the employee already has attendance recorded
        existing_record = next((record for record in self.data if record["Employee"] == employee), None)
        if existing_record:
            existing_record["Attendance"] = attendance_record  # Update existing record
        else:
            self.data.append({"Employee": employee, "Attendance": attendance_record})  # Add new record

        self.status_label.config(text=f"Attendance for {employee} recorded successfully.")
        self.update_attendance_display()  # Update attendance display for the selected employee
        window.destroy()
        self.save_data()

    def update_attendance_display(self, event=None):
        employee = self.finishing_employee_dropdown.get() if self.finishing_employee_dropdown.get() != "Unknown" else self.carpentry_employee_dropdown.get()
        
        if employee == "Unknown":
            self.employee_name_label.config(text="Employee: None")
            for label in self.attendance_labels:
                label.config(text=f"{label.cget('text').split(':')[0]}: Pending", fg="gray")
            self.cash_advance_label.config(text="Cash Advance: None")
            self.incentive_label.config(text="Incentive: None")
            return

        self.employee_name_label.config(text=f"Employee: {employee}")
        
        # Initialize all labels to "Pending"
        for label in self.attendance_labels:
            label.config(text=f"{label.cget('text').split(':')[0]}: Pending", fg="gray")

        # Find the attendance record for the selected employee
        for record in self.data:
            if record["Employee"] == employee and "Attendance" in record:
                attendance = record["Attendance"]
                for day, status in attendance.items():
                    for label in self.attendance_labels:
                        if day in label.cget('text'):
                            label.config(text=f"{day}: {status}", fg="green" if status == "F" else "orange" if status == "H" else "red")
                            break

        self.update_cash_advance_display()  # Update cash advance and incentive display

    def calculate_salary(self):
        employee = self.finishing_employee_dropdown.get() if self.finishing_employee_dropdown.get() != "Unknown" else self.carpentry_employee_dropdown.get()
        if employee == "Unknown":
            self.status_label.config(text="Error: Please select an employee.")
            return
        salary = next((emp[1] for emp in self.finishing_employees if emp[0] == employee), None)
        if salary is None:
            salary = next((emp[1] for emp in self.carpentry_employees if emp[0] == employee), None)
        attendance = next((record["Attendance"] for record in self.data if record["Employee"] == employee and "Attendance" in record), {})
        total_salary = sum(salary if status == "F" else salary / 2 if status == "H" else 0 for status in attendance.values())
        if employee in [emp[0] for emp in self.finishing_employees]:
            self.finishing_tree.insert("", "end", values=(employee, "Calculated", total_salary, 0))
        elif employee in [emp[0] for emp in self.carpentry_employees]:
            self.carpentry_tree.insert("", "end", values=(employee, "Calculated", total_salary, 0))
        self.save_data()

    def calculate_incentives(self):
        for item in self.finishing_tree.get_children():
            values = self.finishing_tree.item(item, "values")
            if values[1] == "Calculated":
                base_salary = float(values[2])
                incentive = base_salary * 0.10
                self.finishing_tree.item(item, values=(values[0], values[1], values[2], incentive))
        for item in self.carpentry_tree.get_children():
            values = self.carpentry_tree.item(item, "values")
            if values[1] == "Calculated":
                base_salary = float(values[2])
                incentive = base_salary * 0.10
                self.carpentry_tree.item(item, values=(values[0], values[1], values[2], incentive))
        self.save_data()

    def reset_attendance_and_cash_advance(self):
        employee = self.finishing_employee_dropdown.get() if self.finishing_employee_dropdown.get() != "Unknown" else self.carpentry_employee_dropdown.get()
        if employee == "Unknown":
            self.status_label.config(text="Error: Please select an employee.")
            return
        if messagebox.askyesno("Confirm Reset", f"Are you sure you want to reset the attendance and cash advance for {employee}? This action cannot be undone."):
            for record in self.data:
                if record["Employee"] == employee:
                    record["Attendance"] = {day: "Pending" for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}
                    for emp in self.finishing_employees:
                        if emp[0] == employee:
                            emp[2] = 0  # Reset cash advance
                            break
                    for emp in self.carpentry_employees:
                        if emp[0] == employee:
                            emp[2] = 0  # Reset cash advance
                            break
                    self.status_label.config(text=f"Attendance and cash advance for {employee} have been reset.")
                    self.update_attendance_display()
                    self.save_data()  # Save changes to the JSON file
                    break

    def export_to_excel(self):
        employee = self.finishing_employee_dropdown.get() if self.finishing_employee_dropdown.get() != "Unknown" else self.carpentry_employee_dropdown.get()
        if employee == "Unknown":
            self.status_label.config(text="Error: Please select an employee.")
            return
        
        # Create a progress bar
        progress = ttk.Progressbar(self.root, orient="horizontal", length=300, mode="indeterminate")
        progress.pack(pady=10)
        progress.start()  # Start the progress bar

        self.root.update()  # Update the GUI to show the progress bar

        data = []
        for record in self.data:
            if record["Employee"] == employee:
                attendance = record["Attendance"]
                salary = next((emp[1] for emp in self.finishing_employees if emp[0] == employee), None)
                if salary is None:
                    salary = next((emp[1] for emp in self.carpentry_employees if emp[0] == employee), None)
                total_salary = sum(salary if status == "F" else salary / 2 if status == "H" else 0 for status in attendance.values())
                total_cash_advance = next((emp[2] for emp in self.finishing_employees if emp[0] == employee), 0)
                if total_cash_advance == 0:
                    total_cash_advance = next((emp[2] for emp in self.carpentry_employees if emp[0] == employee), 0)
                data.append({
                    "Employee": record["Employee"],
                    **attendance,
                    "Total Salary": total_salary,
                    "Total Cash Advance": total_cash_advance
                })
        
        df = pd.DataFrame(data)
        
        # Get current date and time for the filename
        current_time = datetime.now().strftime("%m-%d-%Y %H-%M-%S")
        excel_path = os.path.join(self.file_path, f"{employee}_attendance_receipt_{current_time}.xlsx")
        df.to_excel(excel_path, index=False)

        progress.stop()  # Stop the progress bar
        progress.pack_forget()  # Hide the progress bar

        self.status_label.config(text=f"Data exported to {excel_path}")
        self.export_to_text_file(employee)

    def export_to_text_file(self, employee):
        attendance_record = next((record["Attendance"] for record in self.data if record["Employee"] == employee), {})
        salary = next((emp[1] for emp in self.finishing_employees if emp[0] == employee), None)
        if salary is None:
            salary = next((emp[1] for emp in self.carpentry_employees if emp[0] == employee), None)
        total_cash_advance = next((emp[2] for emp in self.finishing_employees if emp[0] == employee), 0)
        if total_cash_advance == 0:
            total_cash_advance = next((emp[2] for emp in self.carpentry_employees if emp[0] == employee), 0)
        
        # Get current date and time for the filename
        current_time = datetime.now().strftime("%m-%d-%Y %H-%M-%S")
        receipt_lines = [f"{employee}:"]
        for day, status in attendance_record.items():
            if status == "F":
                receipt_lines.append(f"{day}: {salary} --- Full day")
            elif status == "H":
                receipt_lines.append(f"{day}: {salary / 2} --- Half day")
            else:
                receipt_lines.append(f"{day}: 0 --- Absent")
        total_salary = sum(salary if status == "F" else salary / 2 if status == "H" else 0 for status in attendance_record.values())
        receipt_lines.append(f"Total Salary for the week: {total_salary}")
        receipt_lines.append(f"Total Cash Advance: {total_cash_advance}")
        receipt_text = "\n".join(receipt_lines)
        
        text_file_path = os.path.join(self.file_path, f"{employee}_attendance_receipt_{current_time}.txt")
        with open(text_file_path, "w") as text_file:
            text_file.write(receipt_text)
        
        self.status_label.config(text=f"Receipt exported to {text_file_path}")

    def save_data(self):
        data = {
            "finishing_employees": self.finishing_employees,
            "carpentry_employees": self.carpentry_employees,
            "data": self.data
        }
        with open(os.path.join(self.file_path, "salary_data.json"), "w") as file:
            json.dump(data, file, indent=4)

    def load_data(self):
        try:
            with open(os.path.join(self.file_path, "salary_data.json"), "r") as file:
                data = json.load(file)
                self.finishing_employees = data.get("finishing_employees", [])
                self.carpentry_employees = data.get("carpentry_employees", [])
                self.data = data.get("data", [])
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = SalaryCalculator(root)
    root.mainloop()