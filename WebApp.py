import logging
import random
import sys
from tkinter import *
from flask import Flask, jsonify, redirect, render_template, request, flash, session
from flask_mysqldb import MySQL
import string
import secrets


# Random String Generator for OrderKey
def generate_random_string(length, characters=None):
    """
    Generates a random string of a specified length.
    Args:
        length (int): The desired length of the random string.
        characters (str, optional): A string containing the characters to choose from.
                                    Defaults to all ASCII letters and digits.
    Returns:
        str: The generated random string.
    """
    if characters is None:
        characters = string.ascii_letters + string.digits  # Default to alphanumeric characters

    return ''.join(random.choice(characters) for _ in range(length))

def runFlaskBackend(passwd, debugMode):
    
    app = Flask(__name__)
    # allow both /login and /login/ without 405 errors
    app.url_map.strict_slashes = False
    # Generate a secret key for user sessions.
    app.config['SECRET_KEY'] = secrets.token_hex(32) # app.config is a directory-like object for Flask settings.
    app.config['MYSQL_HOST'] = 'localhost' # Database host
    app.config['MYSQL_USER'] = 'root'  # Database user
    
    app.config['MYSQL_PASSWORD'] = passwd # Database password
    app.config['MYSQL_DB'] = 'coffee' # Database name
    
    mysql = MySQL(app)
    
    # simple file + console logging
    logging.basicConfig(filename='flask.log', level=logging.INFO,
                        format='%(asctime)s %(levelname)s: %(message)s')
    console = logging.StreamHandler(sys.stdout)
    orderKey = ""
    console.setLevel(logging.INFO)
    logging.getLogger().addHandler(console)
    app.logger.setLevel(logging.INFO)

    app.logger.info("Starting Flask backend")
    
    
    @app.route('/')
    # Route: Home page
    def hello_world():
        app.logger.info("Index requested")
        # do not call ping() here; it's a separate route
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT userID, username FROM users;")
        users = cursor.fetchall() 
        # Render the index.html template with the user list.
        uname = str(session.get('username')).partition('@')[0]
        if '.' in uname:
            uname = uname.partition('.')[0]
        return render_template('index.html', userlist=users, username=uname, sessionstate=session.get('logged_in', False))

    @app.route('/menu')
    def menu():
        uname = str(session.get('username')).partition('@')[0]
        if '.' in uname:
            uname = uname.partition('.')[0]
        print(session.get('logged_in', False))
        return render_template('Menu.html', sessionstate=session.get('logged_in', False), username=uname)

    @app.route('/menu-cold')
    def menu_cold():
        uname = str(session.get('username')).partition('@')[0]
        if '.' in uname:
            uname = uname.partition('.')[0]
        return render_template('Menu-Cold.html', sessionstate=session.get('logged_in', False), username=uname)

    @app.route('/menu-delights')
    def menu_delights():
        uname = str(session.get('username')).partition('@')[0]
        if '.' in uname:
            uname = uname.partition('.')[0]
        return render_template('Menu-Delights.html', sessionstate=session.get('logged_in', False), username=uname)

    @app.route('/menu-desserts')
    def menu_desserts():
        uname = str(session.get('username')).partition('@')[0]
        if '.' in uname:
            uname = uname.partition('.')[0]
        return render_template('Menu-Desserts.html', sessionstate=session.get('logged_in', False), username=uname)
    @app.route('/about-us')
    def about_us():
        uname = str(session.get('username')).partition('@')[0]
        if '.' in uname:
            uname = uname.partition('.')[0]
        return render_template('About.html', username=uname)

    
    @app.route('/Signup', methods=['GET','POST'])
    def signup():
        print(session.get('logged_in', False))
        nonlocal orderKey
        if session.get('logged_in', False) == True:
            return redirect('/')
        else:
            # show form on GET, create account on POST
            if request.method == 'GET':
                return render_template("Signup.html")
            # POST -> create account
            username = request.form.get('username')
            password = request.form.get('password')
            app.logger.info("signup called (username=%r)", username)
            if not username or not password:
                app.logger.info("signup: missing fields")
                return render_template("Signup.html", error="Missing username or password")

            try:
                cursor = mysql.connection.cursor()
                orderKey = generate_random_string(12)
                
                cursor.execute("SELECT * FROM users")
                usernames = []
                for user in cursor.fetchall():
                    usernames.append(user[1])
                
                if username not in usernames:
                    cursor.execute("INSERT INTO users VALUES (%s, %s, %s, %s)", (random.randrange(1000, 9999), username, password, orderKey))
                    mysql.connection.commit()
                    cursor.close()
                    session['logged_in'] = True
                    session['username'] = username
                    
                    app.logger.info("User %s created", username)
                    return redirect('/')
                else:
                    flash('User already exists!', 'error')
                    return render_template("Signup.html", error="User already exists!")

            except Exception:
                app.logger.exception("signup DB error")
                return render_template("Signup.html", error="Database error")

            # Always pass userlist (empty if not available) so templates that call len() won't crash
            
    

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        app.logger.info("login route hit, method=%s", request.method)

        if request.method == 'GET':
            return render_template("Login.html")

        # POST
        username = request.form.get('username')
        password = request.form.get('password')
        app.logger.info("login attempt username=%r", username)

        if not username or not password:
            return render_template("Login.html", error="Missing username or password")

        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM users")
            users = cur.fetchall()
            cur.close()

            for user in users:
                db_username = user[1]
                db_password = user[2]
                
                if db_username == username and db_password == password:
                    session['logged_in'] = True  # Store the state
                    session['username'] = username # Store the username
                    session['order-key'] = user[3] # store the order key.
                    app.logger.info("User %s authenticated", username)
                    
                    return redirect('/') # Redirect to home, which will read the session

            app.logger.info("Invalid credentials for %s", username)
            return render_template("Login.html", error="Invalid username or password")

        except Exception:
            app.logger.exception("login DB error")
            return render_template("Login.html", error="Database error")
    @app.route('/logout')
    def logout():
        cur = mysql.connection.cursor()
        orderKey = session.get('order-key')
        cur.execute(f"DELETE FROM cart_for_{orderKey}")
        mysql.connection.commit()
        session.pop('logged_in', None)
        session.pop('username', None)
        session.pop('order-key', "")
        return redirect('/')
    
    @app.route('/add-to-cart', methods=['POST'])
    def add_to_cart():
        orderKey = session.get('order-key')
        current_username = str(session.get('username'))
        isLoggedIn = session.get('logged_in', False)
        # 2. Check the user state
        if not isLoggedIn or not current_username:
            # app.logger.warning("add_to_cart: user not logged in")
            app.logger.warning("add_to_cart: user not logged in or missing username")
            print(f"DEBUG REDIRECT: logged_in={isLoggedIn}, username={current_username}")
            return redirect('/login')
        else:
            app.logger.info("add_to_cart called by user %s", current_username)
            data = request.get_json(silent=True)
            if not data:
                app.logger.error("add_to_cart: no JSON received")
                return jsonify({'status': 'error', 'message': 'Invalid JSON'}), 400
            
            item_name = str(data.get('itemName'))
            item_price = str(data.get('price'))
            item_quantity = str(data.get('qty'))  # default to 1 if not provided

            app.logger.info(
                "Item added to cart: %s, Price: %s, User: %s, Qty: %s",
                item_name, item_price, session.get('username'), item_quantity
            )

            # optionally persist to DB
            try:
                cur = mysql.connection.cursor()
                # Receive data from menu
                orderKey = session.get('order-key')
                ordermap = (str(session.get('username')), orderKey)
                # Create a user-specific cart table if it doesn't exist
                cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS cart_for_{orderKey} (
                        orderID INT PRIMARY KEY AUTO_INCREMENT,
                        orderKey VARCHAR(32),
                        user_name VARCHAR(100),
                        item VARCHAR(255),
                        quantity INT,
                        price FLOAT,
                        added_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                cur.execute(
                    f"INSERT INTO cart_for_{orderKey} (orderID, orderKey, user_name, item, quantity, price) VALUES (%s, %s, %s, %s, %s, %s)",
                    # The actual data is passed as a separate tuple, which prevents SQL injection
                    (random.randrange(1000,9999), orderKey, session.get('username'), item_name, item_quantity, item_price)
                )
                mysql.connection.commit()
                cur.close()
            except Exception:
                app.logger.exception("DB error persisting cart item")
                # don't fail the response; just log the error

            return jsonify({'status': 'success', 'message': 'Item added to cart'}), 200
    @app.route('/orders')
    def orders(): 
        # 1. Check state and username from current session.
        orderKey = session.get('order-key')
        current_username = str(session.get('username'))
        isLoggedIn = session.get('logged_in', False)
        if not isLoggedIn or not current_username:
            app.logger.warning("add_to_cart: user not logged in or missing username")
            print(f"DEBUG REDIRECT: logged_in={isLoggedIn}, username={current_username}")
            return redirect('/login')
        else:
                
            uname = str(session.get('username')).partition('@')[0]
            if '.' in uname:
                uname = uname.partition('.')[0]
            print(session.get('logged_in', False))
            orderKey = session.get('order-key')
            cur = mysql.connection.cursor()
            cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS cart_for_{orderKey} (
                        orderID INT PRIMARY KEY AUTO_INCREMENT,
                        orderKey VARCHAR(32),
                        user_name VARCHAR(100),
                        item VARCHAR(255),
                        quantity INT,
                        price FLOAT,
                        added_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
            """)
            cur.execute(f'SELECT * FROM cart_for_{orderKey};')
            orders = cur.fetchall()
            # Calculate the total cost of Products.
            print(orders)
            sum = 0
            for order in orders:
                sum += int(order[4])*int(order[5])
            return render_template('Orders.html', session=session.get('logged_in', False), items=orders, cost=sum)

    # IMPORTANT: disable the reloader in a child process
    app.run(host='localhost', port=5000, debug=debugMode, use_reloader=False)

if __name__ == '__main__':
    db_password = input("Enter database password: ")
    debugMode = input("Enable debug mode? (y/n): ").lower() == 'y'
    runFlaskBackend(db_password, debugMode)