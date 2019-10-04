#! /usr/bin/python3

import passwords
import MySQLdb

print("Content-Type: text/html")
print("Status: 200 OK")
print()

conn = MySQLdb.connect(host = passwords.SQL_HOST,
                       user = passwords.SQL_USER,
                       passwd = passwords.SQL_PASSWD,
                       db = "store")

cursor = conn.cursor()

cursor.execute("SELECT * FROM customers")
results = cursor.fetchall()
cursor.close()

print("""
<html>
<head>
<title>Store</title>
</head>

<body>
<h1> Customers </h1>""")

print("""
<table border="1">
  <tr>
    <th>idNumber</th>
    <th>First Name</th>
    <th>Last Name</th>
    <th>Email address</th>
  </tr>""")

for cust in results:
  print("<tr>")
  for info in cust:
    print("<td>" + str(info) + "</td>")
  print("</tr>")

print("""
</table>

</body>
</html>
""")
