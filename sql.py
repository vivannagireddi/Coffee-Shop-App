# To Check MySQL Connection.

import mysql.connector
conn = mysql.connector.connect(
    host='127.0.0.1', user='root', password='VN@220508', database='coffee', port=3306
)
cur = conn.cursor()
cur.execute("INSERT INTO users (userID, username, password) VALUES (%s,%s, %s)", ("FLWO10","dbg_user", "dbg_pass"))
conn.commit()
cur.execute("SELECT userID, username FROM users;")
print(cur.fetchall())
cur.close()
conn.close()