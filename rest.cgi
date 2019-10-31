#! /usr/bin/python3
import os 
import json
import passwords
import MySQLdb
import cgi

def main():
    #Checks to see if path_info is found in os.environ
    if "PATH_INFO" in os.environ:
        path_info = os.environ['PATH_INFO']
    else:
        path_info = "/"

    if path_info == "/":
        index()
    elif path_info == "/customers/" or path_info == "/customers":
        get_info(None)
    elif "/customers" in path_info and len(path_info) > len("/customers/"):
        cust_id = path_info.split("/")[2]
        get_info(cust_id)
    elif path_info == "/add_customers" or path_info == "/add_customers/":
        add_customer()
    elif path_info == "/update_customers":
        update_customers()

def index():
    #Main index page, has links to form and customers within database
    print("Content-Type: text/html")
    print("Status: 200 OK")
    print()
    print("""<html><body>
    <h1>Customer Lookup (Rest Lab)</h1>
    <p><a href="http://ec2-35-153-209-40.compute-1.amazonaws.com/cgi-bin/rest.cgi/customers/">customers/</a> Click here to see all customer data
    <br>
    <a href="http://ec2-35-153-209-40.compute-1.amazonaws.com/cgi-bin/rest.cgi/add_customers/">Add new customer</a> Click here to add a customer to database
    <hr>
    <p><a href="http://ec2-35-153-209-40.compute-1.amazonaws.com/cgi-bin/rest.cgi">Return Home</a> Click here for index
    </body></html>""")

def get_conn():
    #Establishing MySQL connection using passwords file
    conn = MySQLdb.connect(host = passwords.SQL_HOST,
    user = passwords.SQL_USER,
    passwd = passwords.SQL_PASSWD,
    db = "store")
    return conn

def get_info(id):
    # GET method, pulls information from database and displays it, either all or single row depending on id passed through
    print("Content-Type: application/json")
    print("Status: 200 OK")
    print() 

    conn = get_conn()
    cursor = conn.cursor()
    if id is not None:
        cursor.execute("SELECT * FROM customers WHERE id=%s", [id])
    else:
        cursor.execute("SELECT * FROM customers")
    results = cursor.fetchall()
    cursor.close()

    #Adding labels to information pulled from SQL customers table
    info = []
    for result in results:
        customer = []
        for i in range (0, len(result)):
           if i==0:
               customer.append("id = " + str(result[i]))
           elif i==1:
               customer.append("First Name = " + str(result[i]))
           elif i==2:
               customer.append("Last Name = " + str(result[i]))
           else:
               customer.append("Email = " + str(result[i]))
        info.append(customer)

    json_results = json.dumps(info, indent=2)
    print(json_results)

def add_customer():
    print("Content-Type: text/html")
    print("Status: 200 OK")
    print()

    print("""
    <html><body>
    <form action="/cgi-bin/rest.cgi/update_customers" method=POST>
        <p>First Name:
            <br><input type=text name="first">
        <p>Last Name:
            <br><input type=text name="last">
        <p>Email:
            <br><input type=text name="email">
        <input type=submit>
    </form>
    </body></html>""")

def update_customers():
    form = cgi.FieldStorage()
    form_values = []
    if "first" in form:
        form_values.append(form.getvalue("first"))
    if "last" in form:
        form_values.append(form.getvalue("last"))
    if "email" in form:
        form_values.append(form.getvalue("email"))
    #Checks to see if form values were passed in order to add new customer
    if len(form_values) != 0:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO customers (first, last, email)
        VALUES (%s, %s, %s)""",[form_values[0], form_values[1], form_values[2]])
        new_id = cursor.lastrowid
        cursor.close()
        conn.commit()

    print("Status: 302 Redirect")
    print("Location: /cgi-bin/rest.cgi/customers/" + str(new_id))
    print()

main()
