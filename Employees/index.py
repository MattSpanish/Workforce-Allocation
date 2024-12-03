from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "employee_management"
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except mysql.connector.Error as e:
        print("Database connection failed:", e)
        return None

@app.route("/")
def home():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM employees")
            employees = cursor.fetchall()
            cursor.close()
            return render_template('index.html', employees=employees)
        finally:
            connection.close()
    else:
        return "Database connection error."

@app.route("/add_employee", methods=["GET", "POST"])
def add_employee():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        department = request.form["department"]
        subjects = request.form["subjects"]
        gender = request.form["gender"]
        status = request.form["status"]

        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT INTO employees (name, email, department, subjects, gender, status)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (name, email, department, subjects, gender, status))
                connection.commit()
                cursor.close()
                return redirect(url_for("home"))
            finally:
                connection.close()
    return render_template("add_employee.html")

@app.route("/edit_employee/<int:id>", methods=["GET", "POST"])
def edit_employee(id):
    connection = get_db_connection()
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        department = request.form["department"]
        subjects = request.form["subjects"]
        gender = request.form["gender"]
        status = request.form["status"]

        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("""
                    UPDATE employees
                    SET name = %s, email = %s, department = %s, subjects = %s, gender = %s, status = %s
                    WHERE id = %s
                """, (name, email, department, subjects, gender, status, id))
                connection.commit()
                cursor.close()
                return redirect(url_for("home"))
            finally:
                connection.close()
    else:
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM employees WHERE id = %s", (id,))
                employee = cursor.fetchone()
                cursor.close()
                return render_template("edit_employee.html", employee=employee)
            finally:
                connection.close()

@app.route("/delete_employee/<int:id>")
def delete_employee(id):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM employees WHERE id = %s", (id,))
            connection.commit()
            cursor.close()
            return redirect(url_for("home"))
        finally:
            connection.close()

if __name__ == "__main__":
    app.run(debug=True)
