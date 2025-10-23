import pickle
import time
import tkinter as tk
from tkinter import *
from cefpython3 import cefpython as cef
import ctypes
from flask import Flask, render_template, request
import Components.WebRenderer as WebRenderer
# Very useful import!!!!!!
import multiprocessing

def runFlaskBackend():
    app = Flask(__name__)
    @app.route("/")
    def hello_world():
        return render_template('index.html')
    # Get form data.
    @app.route('/submit_data', methods=['POST'])
    def submit_data():
        username = request.form.get('username_input')
        password = request.form.get('password_input')
        # Process the retrieved data (e.g., save to database, validate)
        userDict = {'username': username, 'password': password}
        with open('user.dat', 'wb') as userdata_file:
            pickle.dump(userDict, userdata_file)
        return 'Done!'

    app.run()
    
def main():
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
    openUserWindow = multiprocessing.Process(target=main)

    # Start the processes.
    openUserWindow.start()
    flaskBackend.start()
    # Wait until both processes are finished.
    openUserWindow.join()
    flaskBackend.join()

    print(time.time(),": Application execution successful with exit code 0.")