import mysql.connector
from 7 import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

# Database Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'employee_management'
}

# Route for displaying the form and handling submissions
@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        department = request.form['department']
        status = request.form['status']
        subjects = request.form['subject']
        gender = request.form['gender']

        try:
            # Establish DB Connection
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            # Insert employee into the employees table
            sql_employee = """
                INSERT INTO employees (name, email, department, status, subjects, gender)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql_employee, (name, email, department, status, subjects, gender))
            employee_id = cursor.lastrowid  # Get the last inserted employee ID

            # Insert initial time tracking record
            sql_time = """
                INSERT INTO time_tracking (employee_id, regular, overtime, sick_leave, pto, paid_holiday)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql_time, (employee_id, 0, 0, 0, 0, 0))

            # Commit the transaction
            conn.commit()

            return redirect(url_for('employee_list'))  # Redirect to the employee list page
        except mysql.connector.Error as err:
            return f"Error: {err}"
        finally:
            cursor.close()
            conn.close()

    # Render the form for GET request
    return render_template('add_employee.html')

# Dummy route for employee list (for redirection purposes)
@app.route('/employee_list')
def employee_list():
    return "<h1>Employee list page placeholder</h1>"

if __name__ == "__main__":
    app.run(debug=True)
