from flask import Flask, render_template, request, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flaskext.mysql import MySQL

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management and flashing messages

# Configure MySQL connection
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'bvm'
app.config['MYSQL_DATABASE_DB'] = 'auto_records'

# Initialize MySQL
mysql = MySQL()
mysql.init_app(app)

@app.route('/')
def index():
    return render_template('customersignup.html')


@app.route('/signup', methods=['POST'])
def signup():
    try:
        # Get form data
        full_name = request.form['full_name']
        email = request.form['email']
        contact_number = request.form['contact_number']
        emergency_number = request.form['emergency_number']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if passwords match
        if password != confirm_password:
            flash("Passwords do not match, please try again.", "danger")
            return redirect('/')

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Establish MySQL connection
        connection = mysql.connect()
        cursor = connection.cursor()

        # Insert data into MySQL
        cursor.execute(""" 
            INSERT INTO customer (full_name, email, contact_number, emergency_number, password)
            VALUES (%s, %s, %s, %s, %s)
        """, (full_name, email, contact_number, emergency_number, hashed_password))

        # Commit and close connection
        connection.commit()
        cursor.close()
        connection.close()

        flash("Signup successful! Please log in.", "success")
        return redirect('/login')

    except Exception as e:
        print(f"Error: {e}")
        flash("An error occurred during signup. Please try again later.", "danger")
        return redirect('/')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        print(f"Username provided: {username}")  # Debug log
        print(f"Password provided: {password}")  # Debug log

        # Establish MySQL connection
        connection = mysql.connect()
        print("Database connection established.")  # Debug log

        with connection.cursor() as cursor:
            try:
                # Check if the username exists (we are using email as the unique identifier)
                cursor.execute("SELECT * FROM customer WHERE email = %s", (username,))
                user = cursor.fetchone()
                print(f"User fetched from DB: {user}")  # Debug log

                if user:
                    # Check if the password matches
                    if check_password_hash(user[5], password):  # Assuming password is in 5th column
                        flash("Login successful!", "success")
                        session['user_id'] = user[0]  # Save user ID in session (first column)
                        session['email'] = user[1]  # Optionally save email (second column)
                        return redirect('/qr')  # Redirect to the QR page after successful login
                    else:
                        flash('Invalid password!', 'danger')
                        print("Invalid password provided.")  # Debug log
                else:
                    flash('Username not found!', 'danger')
                    print("User with provided username not found.")  # Debug log

            except Exception as e:
                print(f"Login Error: {e}")
                flash("An error occurred during login. Please try again later.", "danger")
                return render_template('customerlogin.html')

            finally:
                connection.close()
                print("Database connection closed.")  # Debug log

    return render_template('customerlogin.html')

# Define the route for /qr
@app.route('/qr')
def qr():
    if 'user_id' in session:  # Ensure the user is logged in
        return render_template('qr.html')  # Render the QR page
    else:
        flash("You need to log in to access the QR page.", "danger")
        return redirect('/login')  # Redirect to login if not logged in

@app.route('/dashboard')
def dashboard():
    return "Welcome to your dashboard!"  # Replace with actual dashboard page

if __name__ == '__main__':
    app.run(debug=True)


