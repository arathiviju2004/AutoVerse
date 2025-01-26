# from flask import Flask, render_template, request, redirect, flash
# import pymysql
# from werkzeug.security import generate_password_hash, check_password_hash

# app = Flask(__name__)
# app.secret_key = 'your_secret_key'  # Needed for session management and flashing messages

# # Configure MySQL connection using PyMySQL
# app.config['MYSQL_HOST'] ='localhost'  # Your MySQL host
# app.config['MYSQL_USER'] ='root'      # Your MySQL username
# app.config['MYSQL_PASSWORD'] ='bvme'   # Your MySQL password
# app.config['MYSQL_DB'] ='auto_records'  # The database to store user data

# # Establish the connection
# def get_db_connection():
#     try:
#         connection = pymysql.connect(
#             host=app.config['MYSQL_HOST'],
#             user=app.config['MYSQL_USER'],
#             password=app.config['MYSQL_PASSWORD'],
#             db=app.config['MYSQL_DB'],
#             cursorclass=pymysql.cursors.DictCursor
#         )
#         return connection
#     except pymysql.MySQLError as e:
#         print(f"MySQL Error: {e}")
#         return None
    
# connection = get_db_connection()
# if connection:
#     print(f"working")
    
# else:
#         print(f"MySQL Error:")

from flask import Flask, jsonify
from flaskext.mysql import MySQL

app = Flask(__name__)

# Configure MySQL
app.config['MYSQL_DATABASE_HOST'] = 'localhost'  # Replace with your host
app.config['MYSQL_DATABASE_USER'] = 'root'       # Replace with your MySQL username
app.config['MYSQL_DATABASE_PASSWORD'] = 'bvm'   # Replace with your MySQL password
app.config['MYSQL_DATABASE_DB'] = 'auto_records' # Replace with your database name

# Initialize MySQL
mysql = MySQL()
mysql.init_app(app)

@app.route('/test-connection', methods=['GET'])
def test_connection():
    try:
        # Establish database connection
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * from customer;')  # Simple query to test connection
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return jsonify({'status': 'success', 'result': result}), 200
    except Exception as e:
        return jsonify({'status': 'failed', 'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
