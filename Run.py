import pickle
import random
import time
import tkinter as tk
from tkinter import *
from cefpython3 import cefpython as cef
import ctypes
from flask import Flask, render_template, request, current_app, g
import mysql.connector as mysqlot

# Components
import Components.WebRenderer as WebRenderer

# Imports
import multiprocessing
from datetime import datetime
import logging
import sys

app = Flask(__name__)

app.config['DB_HOST'] = 'localhost'
app.config['DB_USER'] = 'root'
app.config['DB_PASSWORD'] = 'VN@220508'
app.config['DB_DATABASE'] = 'coffee'

def get_db():
    try:
        if 'db' not in g or not getattr(g, 'db', None) or not g.db.is_connected():
            g.db = mysqlot.connect(
                host=current_app.config['DB_HOST'],
                user=current_app.config['DB_USER'],
                password=current_app.config['DB_PASSWORD'],
                database=current_app.config['DB_DATABASE']
            )
        return g.db
    except Exception as e:
        app.logger.exception("get_db() failed")
        raise

def runFlaskBackend():
    
    # simple file + console logging
    logging.basicConfig(filename='flask.log', level=logging.INFO,
                        format='%(asctime)s %(levelname)s: %(message)s')
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    logging.getLogger().addHandler(console)
    app.logger.setLevel(logging.INFO)

    app.logger.info("Starting Flask backend")
    @app.teardown_appcontext
    def close_db(exception):    
        db = g.pop('db', None)
        if db is not None:
            try:
                db.close()
            except Exception:
                pass

    @app.route("/ping")
    def ping():
        app.logger.info("PING received")
        return "ok", 200

    @app.route("/")
    def hello_world():
        app.logger.info("Index requested")
        # do not call ping() here; it's a separate route
        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute("SELECT username FROM users")
            rows = cursor.fetchall()
            users = [r[0] for r in rows]
            cursor.close()
            app.logger.info("Loaded %d users", len(users))
            return render_template('index.html', users=users)
        except Exception as e:
            # log full exception and return helpful text for debugging
            app.logger.exception("Failed to load users: %s", e)
            # return plain text fallback so you can see something in the browser/CEF
            return f"Error loading users: {type(e).__name__} - {e}", 500

    @app.route('/create_account', methods=['POST'])
    def create_account():
        username = request.form.get('username_input')
        password = request.form.get('password_input')
        try:
            db = get_db()
            cursor = db.cursor()
            # ensure table exists with AUTO_INCREMENT to avoid PK collisions
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS users ("
                " userID INT AUTO_INCREMENT PRIMARY KEY,"
                " username VARCHAR(50),"
                " password VARCHAR(255)"
                ")"
            )
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s)",
                (username, password)
            )
            db.commit()
            cursor.close()
            return render_template('Account.html')
        except Exception:
            app.logger.exception("Failed to create account")
            return "Database error", 500

    # IMPORTANT: disable the reloader in a child process
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)

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
    # creating processes
    flaskBackend = multiprocessing.Process(target=runFlaskBackend)
    openUserWindow = multiprocessing.Process(target=window)

    # Start the backend first so the server is ready when the GUI opens
    flaskBackend.start()
    time.sleep(5)  # increase from 1 to 2-3 seconds if needed
    openUserWindow.start()

    # Optionally remove the unused parent DB connection -- it's not used by Flask process
    # Wait until both processes are finished.
    
    flaskBackend.join()
    openUserWindow.join()

    epochtime = time.time()
    timestamp = datetime.fromtimestamp(epochtime).strftime('%Y-%m-%d %H:%M:%S')
    print(timestamp,": Application execution successful with exit code 0.")