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
from WebApp import runFlaskBackend

# Imports
import multiprocessing
from datetime import datetime
import logging
import sys




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
