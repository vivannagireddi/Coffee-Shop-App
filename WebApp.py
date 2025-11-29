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

    @app.route("/")
    def hello_world():
        app.logger.info("Index requested")
        # do not call ping() here; it's a separate route
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT userID, username FROM users;")
        users = cursor.fetchall() 
        # Render the index.html template with the user list. And, Copilot did help me!

        return render_template('index.html', userlist=users)

    @app.route('/create_account', methods=['POST'])
    def create_account():
        
        if request.method == 'POST':
            username = request.form['username_input']
            password = request.form['password_input']
            app.logger.info("create_account called (username=%r)", username)
            cursor = mysql.connection.cursor()
            cursor.execute(''' INSERT INTO users VALUES(%s,%s,%s)''',(random.randrange(1000,9999),username,password))
            mysql.connection.commit()
            cursor.close()
            return render_template("Account.html", user_name=username)
    
    # Render the Rendering Page
    @app.route('/ThreeJS.html')
    def threejs():
        app.logger.info("ThreeJS requested")
        return render_template('ThreeJS.html')
    
    
    # IMPORTANT: disable the reloader in a child process
    app.run(host='localhost', port=5000, debug=debugMode, use_reloader=False)

if __name__ == '__main__':
    db_password = input("Enter database password: ")
    debugMode = input("Enable debug mode? (y/n): ").lower() == 'y'
    runFlaskBackend(db_password, debugMode)