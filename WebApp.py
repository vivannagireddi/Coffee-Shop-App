import logging
import pickle
import random
import sys
from tkinter import *
from flask import Flask, jsonify, redirect, render_template, request, flash
from flask_mysqldb import MySQL


def runFlaskBackend(passwd, debugMode):
    
    app = Flask(__name__)
    # allow both /login and /login/ without 405 errors
    app.url_map.strict_slashes = False
    
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    
    app.config['MYSQL_PASSWORD'] = passwd
    app.config['MYSQL_DB'] = 'coffee'
    
    mysql = MySQL(app)
    
    # simple file + console logging
    logging.basicConfig(filename='flask.log', level=logging.INFO,
                        format='%(asctime)s %(levelname)s: %(message)s')
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    logging.getLogger().addHandler(console)
    app.logger.setLevel(logging.INFO)

    app.logger.info("Starting Flask backend")
    isLoggedIn = False
    username = ""

    @app.route('/')
    # Route: Home page
    def hello_world():
        nonlocal isLoggedIn
        nonlocal username
        app.logger.info("Index requested")
        # do not call ping() here; it's a separate route
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT userID, username FROM users;")
        users = cursor.fetchall() 
        # Render the index.html template with the user list. And, Copilot did help me!

        return render_template('index.html', userlist=users, session=isLoggedIn)

    @app.route('/menu')
    def menu():
        nonlocal isLoggedIn
        nonlocal username
        return render_template('Menu.html', session=isLoggedIn)

    @app.route('/menu-cold')
    def menu_cold():
        nonlocal isLoggedIn
        return render_template('Menu-Cold.html', session=isLoggedIn)

    @app.route('/menu-delights')
    def menu_delights():
        nonlocal isLoggedIn
        return render_template('Menu-Delights.html', session=isLoggedIn)

    @app.route('/menu-desserts')
    def menu_desserts():
        nonlocal isLoggedIn
        return render_template('Menu-Desserts.html', session=isLoggedIn)
    @app.route('/about-us')
    def about_us():
        return render_template('About.html')

    
    @app.route('/Signup', methods=['GET','POST'])
    def signup():
        nonlocal isLoggedIn
        nonlocal username
        if isLoggedIn == True:
            return redirect('/menu')
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
                cursor.execute("INSERT INTO users VALUES (%s, %s, %s)", (random.randrange(1000, 9999), username, password))
                mysql.connection.commit()
                cursor.close()
                isLoggedIn = True
                app.logger.info("User %s created", username)
                return redirect('/menu')

            except Exception:
                app.logger.exception("signup DB error")
                return render_template("Signup.html", error="Database error")

            # Always pass userlist (empty if not available) so templates that call len() won't crash
            
    

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        nonlocal isLoggedIn
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
            cur.execute("SELECT userID, username, password FROM users")
            users = cur.fetchall()
            cur.close()

            for user in users:
                db_username = user[1]
                db_password = user[2]
                if db_username == username and db_password == password:
                    isLoggedIn = True
                    app.logger.info("User %s authenticated", username)
                    return render_template("Menu.html", session=isLoggedIn, username=username)

            app.logger.info("Invalid credentials for %s", username)
            return render_template("Login.html", error="Invalid username or password")

        except Exception:
            app.logger.exception("login DB error")
            return render_template("Login.html", error="Database error")
    @app.route('/logout')
    def logout():
        nonlocal isLoggedIn
        isLoggedIn = False
        return redirect('/')
    
    # Receive data from menu
    @app.route('/add-to-cart', methods=['POST'])
    def add_to_cart():
        nonlocal username
        data = request.get_json(silent=True)
        if not data:
            app.logger.error("add_to_cart: no JSON received")
            return jsonify({'status': 'error', 'message': 'Invalid JSON'}), 400

        item_name = data.get('itemName')
        item_size = data.get('size')  # match the key sent from Menu.js
        item_price = data.get('price')

        # validate required fields
        if not item_name or not item_size or item_price is None:
            app.logger.warning(
                "add_to_cart: missing fields - itemName=%r, size=%r, price=%r",
                item_name, item_size, item_price
            )
            return jsonify({
                'status': 'error',
                'message': 'Missing itemName, size, price, or qty'
            }), 400

        app.logger.info(
            "Item added to cart: %s, Size: %s, Price: %s, User: %s",
            item_name, item_size, item_price, username
        )

        # optionally persist to DB
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS cart (
                    cartID INT PRIMARY KEY AUTO_INCREMENT,
                    user_name VARCHAR(100),
                    item VARCHAR(255),
                    quantity INT,
                    size VARCHAR(32),
                    price FLOAT,
                    added_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cur.execute(
                "INSERT INTO cart (user_name, item, quantity, size, price) VALUES (%s, %s, %s, %s, %s)",
                (username or 'guest', item_name, item_quantity, item_size, item_price)
            )
            mysql.connection.commit()
            cur.close()
        except Exception:
            app.logger.exception("DB error persisting cart item")
            # don't fail the response; just log the error

        return jsonify({'status': 'success', 'message': 'Item added to cart'}), 200

    # IMPORTANT: disable the reloader in a child process
    app.run(host='localhost', port=5000, debug=debugMode, use_reloader=False)

if __name__ == '__main__':
    db_password = input("Enter database password: ")
    debugMode = input("Enable debug mode? (y/n): ").lower() == 'y'
    runFlaskBackend(db_password, debugMode)