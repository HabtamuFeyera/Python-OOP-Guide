from flask import Flask, render_template, request, redirect, url_for
from fulltimeemployee import FulltimeEmployee
from hourlyemployee import HourlyEmployee
from payroll import Payroll
import csv
import os


app = Flask(__name__)
payroll = Payroll()

# Function to write employee data to CSV file
def write_to_csv(filename, data):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['First Name', 'Last Name', 'position','age','level','Salary', 'Rate', 'Worked Hours'])  # Write header row
        writer.writerows(data)

# Function to read employee data from CSV file
def read_from_csv(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            data = list(reader)
        return data
    else:
        return []

# Route to add employee
@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        employee_type = request.form['employee_type']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        
        # Check if the employee already exists in the payroll
        for emp in payroll.employee_list:
            if emp.first_name == first_name and emp.last_name == last_name:
                return "Employee already exists!"
        
        if employee_type == 'fulltime':
            salary = float(request.form['salary'])
            employee = FulltimeEmployee(first_name, last_name, salary)
        elif employee_type == 'hourly':
            worked_hours = float(request.form['worked_hours']) if request.form['worked_hours'] else 0.0
            rate = float(request.form['rate']) if request.form['rate'] else 0.0
            employee = HourlyEmployee(first_name, last_name, worked_hours, rate)
        payroll.add(employee)

        # Update CSV file with new employee data
        employee_data = []
        for e in payroll.employee_list:
            if isinstance(e, FulltimeEmployee):
                employee_data.append([e.first_name, e.last_name, e.get_salary(), '', ''])
            elif isinstance(e, HourlyEmployee):
                employee_data.append([e.first_name, e.last_name, '', e.rate, e.worked_hours])
        write_to_csv('employees.csv', employee_data)
        return redirect(url_for('index'))
    return render_template('add_employee.html')

# Route to display employee list
# Route to display employee list
@app.route('/')
def index():
    # Read employee data from CSV file
    employee_data = read_from_csv('employees.csv')

    # Reconstruct Employee objects from CSV data
    for emp in employee_data[1:]:  # Skip header row
        first_name = emp[0]
        last_name = emp[1]
        # Check if the employee already exists in the payroll
        employee_exists = False
        for existing_emp in payroll.employee_list:
            if existing_emp.first_name == first_name and existing_emp.last_name == last_name:
                employee_exists = True
                break
        if not employee_exists:
            if len(emp) == 3:
                payroll.add(FulltimeEmployee(first_name, last_name, float(emp[2]) if emp[2] else 0.0))
            elif len(emp) == 5:
                worked_hours = float(emp[4]) if emp[4] else 0.0
                rate = float(emp[3]) if emp[3] else 0.0
                payroll.add(HourlyEmployee(first_name, last_name, worked_hours, rate))

    # Print employee details
    payroll.print()

    return render_template('index.html', employees=payroll.employee_list)


if __name__ == '__main__':
    app.run(debug=True)
