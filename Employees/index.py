import mysql.connector
from flask import Flask, render_template

app = Flask(__name__)

# xmpp MySQL connection details
db_config = {
    "host": "localhost",
    "user": "root",  # Default XAMPP username
    "password": "",  # Default XAMPP password is empty
    "database": "employee_management"  # Replace with your database name
}

# Function to connect to the database
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=db_config["host"],
            user=db_config["user"],
            password=db_config["password"],
            database=db_config["database"]
        )
        return connection
    except mysql.connector.Error as e:
        print("Error connecting to the database:", e)
        return None

# Flask route to display data from the database
@app.route("/")
def home():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM employees")  # Replace with your table name
            data = cursor.fetchall()  # Fetch all rows from the query
            cursor.close()
            return render_template('index.html', data=data)
        finally:
            connection.close()
    else:
        return "Failed to connect to the database."

if __name__ == "__main__":
    app.run(debug=True)
