#! /usr/bin/python3

print("Content-Type: text/html")
print("Status: 200 OK")
print()

import passwords
import MySQLdb
import cgi 

form = cgi.FieldStorage()
query = ""
query_search = ""
if "command" in form:
  query = form.getvalue("command")
if "search" in form:
  query_search = form.getvalue("search")

conn = MySQLdb.connect(host = passwords.SQL_HOST,
                       user = passwords.SQL_USER,
                       passwd = passwords.SQL_PASSWD,
                       db = "store")

cursor = conn.cursor()
exc_stmnt = "SELECT * FROM customers WHERE %s='%s'"
cursor.execute(exc_stmnt, (query, query_search))
results = cursor.fetchall()
cursor.close()

print("""
<html>
<head>
<title>Customer Lookup</title>
</head>

<body>
<h1> Search Results </h1>""")

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
