# Coffee Shop App

Small desktop app that embeds a Chromium browser (CEF) and runs a Flask backend to manage users in a MySQL database.

## Features
- Embedded Chromium UI (cefpython3)
- Flask backend for routes and DB operations
- MySQL storage for users (users table)
- Simple create-account form

## Prerequisites
- Windows 10+
- Python 3.8+
- MySQL server running (accessible from localhost / 127.0.0.1)
- Visual Studio Code (recommended)

## Python packages
Minimal dependencies (example):
- Flask
- flask-mysqldb (or mysql-connector-python)
- mysql-connector-python (if not using flask-mysqldb)
- cefpython3
- other stdlib modules: multiprocessing, tkinter

Create a venv and install:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
# or
pip install flask flask-mysqldb mysql-connector-python cefpython3
```

## Project layout
- Run.py — application entry (starts Flask backend and GUI process)
- templates/
  - index.html — main UI form and pages
- Components/
  - WebRenderer.py — embeds CEF browser into Tkinter
- sql.py — quick DB test script
- flask.log — application log file (created at runtime)

## Configuration
- The app reads DB settings from the Flask app config in `Run.py`. Prefer using explicit keys:
  - DB host: use `127.0.0.1` instead of `localhost` to avoid socket/IPv6 issues.
  - Provide `DB_USER`, `DB_PASSWORD`, `DB_DATABASE`, `DB_PORT` (3306).
- Do not store credentials in source control. Consider using environment variables and reading them into app.config.

## Database setup
Create the `coffee` database (example using mysql CLI):

```sql
CREATE DATABASE coffee;
USE coffee;

CREATE TABLE IF NOT EXISTS users (
  userID INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(100),
  password VARCHAR(255)
);
```

You can run the quick test script `sql.py` to verify connectivity.

## Running the app
1. Start the app from the project folder (with venv activated):
```powershell
python Run.py
```
2. The script starts a Flask backend in a background process and then opens the Tk window with the embedded browser.

Important runtime notes:
- Flask must be started with `use_reloader=False` when used inside a multiprocessing child to avoid multiple processes and route registration issues.
- Ensure the embedded browser loads `http://127.0.0.1:5000` (not a file:// path) so forms post to the running Flask server.

## Debugging & Logs
- Flask logs are written to `flask.log`. Tail them in PowerShell:
```powershell
Get-Content .\flask.log -Wait
```
- Test routes directly (bypass embedded UI):
```powershell
# ping
Invoke-RestMethod -Uri http://127.0.0.1:5000/ping -Method Get
# create_account
Invoke-RestMethod -Uri http://127.0.0.1:5000/create_account -Method Post -Body @{ username_input='test'; password_input='p' }
```
- If POSTs do not appear in the logs, the embedded browser is probably loading the wrong URL (edit Components/WebRenderer.py).

## Common issues & fixes
- Nothing appears in the UI:
  - Confirm Flask is running (visit `http://127.0.0.1:5000` in an external browser).
  - Confirm embedded browser URL is `http://127.0.0.1:5000`.
- No DB inserts:
  - Confirm `create_account` route logs appear in `flask.log`.
  - Use `127.0.0.1` for DB host to avoid hostname resolution differences.
  - Check that the Flask route does a `conn.commit()` after INSERT and that exceptions are logged.
- Flask reloader causes missing routes / duplicate processes:
  - Run Flask with `debug=False` and `use_reloader=False` when embedding or using multiprocessing.

## Quick verification
- Manual DB insert test: run `sql.py`. If it inserts and prints rows, DB credentials and server are OK.
- If Flask route is reached but insert does not persist, add temporary logging and return plain text on success to verify the code path is reached.

## Contributing
- Keep changes small and test GUI + backend together.
- If modifying the Flask app, ensure `if __name__ == '__main__':` guards and `use_reloader=False` in `app.run()` when used with multiprocessing.

## License
Project for school. Check with the author for reuse or distribution.
