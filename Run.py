import pickle
import random
import time
import tkinter as tk
from tkinter import *
from cefpython3 import cefpython as cef
import ctypes
from flask import Flask, render_template, request, current_app, g
from flask.templating import _render
import mysql
import mysql.connector as mysqlot
from flask_mysqldb import MySQL
import Components.WebRenderer as WebRenderer

# Imports
import multiprocessing
from datetime import datetime
import logging
import sys


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

def window():
    win = Tk()
    cef.Initialize()
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    win.minsize(screen_width, screen_height)
    win.grid_columnconfigure(0, weight=1)
    win.grid_rowconfigure(0, weight=1)

    # Create Frame
    frame = Frame(win, bg='black')
    frame.grid(row=0, column=0, sticky=('NSWE'))

    # Create Browser Frame
    browser_frame = WebRenderer.BrowserFrame(frame)
    browser_frame.pack(fill=tk.BOTH, expand=tk.YES)

    win.mainloop()
    cef.Shutdown()

if __name__ == '__main__':
    db_password = input("Enter database password: ")
    debugMode = input("Enable debug mode? (y/n): ").lower() == 'y'
    # start Flask in background process (pass function, not call it)
    flaskBackend = multiprocessing.Process(target=runFlaskBackend, args=(db_password,debugMode), daemon=True)
    flaskBackend.start()

    try:
        # Run GUI in the main thread (Tkinter/CEF require main thread on Windows)
        window()
    finally:
        # Ensure backend is stopped when GUI closes
        if flaskBackend.is_alive():
            flaskBackend.terminate()
            flaskBackend.join()

    epochtime = time.time()
    timestamp = datetime.fromtimestamp(epochtime).strftime('%Y-%m-%d %H:%M:%S')
    print(timestamp, ": Application execution successful with exit code 0.")
