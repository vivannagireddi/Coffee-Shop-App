import logging
import random
import sys
from tkinter import *
from flask import Flask, render_template, request
from flask_mysqldb import MySQL


def runFlaskBackend(passwd, debugMode):
    
    app = Flask(__name__)
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
    @app.route("/")
    def hello_world():
        app.logger.info("Index requested")
        # do not call ping() here; it's a separate route
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT userID, username FROM users;")
        users = cursor.fetchall() 
        # Render the index.html template with the user list. And, Copilot did help me!

        return render_template('index.html', userlist=users)


    @app.route('/menu')
    def menu():
        # render templates/menu.html if it exists, otherwise return a simple placeholder
        try:
            return render_template('Menu.html', session=isLoggedIn)
        
        except Exception:
            return "<h1>Menu</h1><p>Menu page coming soon.</p>", 200
    
    @app.route('/about-us')
    def about_us():
        # render templates/about_us.html if it exists, otherwise return a simple placeholder
        try:
            return render_template('About.html')
        
        except Exception:
            return "<h1>About Us</h1><p>About Us page coming soon.</p>", 200

    
    
    # Render the Rendering Page
    @app.route('/ThreeJS.html')
    def threejs():
        app.logger.info("ThreeJS requested")
        return render_template('ThreeJS.html')
    
    @app.route('/Signup', methods=['GET', 'POST'])
    def signup():
        global isLoggedIn
        if request.method == 'POST':
            username = request.form['username_input']
            password = request.form['password_input']
            app.logger.info("create_account called (username=%r)", username)
            cursor = mysql.connection.cursor()
            cursor.execute(''' INSERT INTO users VALUES(%s,%s,%s)''',(random.randrange(1000,9999),username,password))
            mysql.connection.commit()
            cursor.close()
            isLoggedIn = True
            return render_template("Account.html", user_name=username)
        else:
            return render_template("Signup.html")
    
    # IMPORTANT: disable the reloader in a child process
    app.run(host='localhost', port=5000, debug=debugMode, use_reloader=False)

if __name__ == '__main__':
    db_password = input("Enter database password: ")
    debugMode = input("Enable debug mode? (y/n): ").lower() == 'y'
    runFlaskBackend(db_password, debugMode)