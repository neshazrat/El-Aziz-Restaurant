import tkinter as tk
from tkinter import ttk
import sqlite3

def create_database():
    connection = sqlite3.connect("ElAziz.db")
    cursor = connection.cursor()

    #Customer table - store customer credentials and personal information
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tblCustomers (
    customerID TEXT PRIMARY KEY,
    firstName TEXT,
    surname TEXT,
    email TEXT,
    phone TEXT,
    username TEXT,
    password TEXT
    );
    """)

    #Staff table - store staff credentials and personal information
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tblStaff (
    staffID TEXT PRIMARY KEY,
    firstName TEXT,
    surname TEXT,
    email TEXT,
    phone TEXT,
    username TEXT,
    password TEXT
    );
    """)

    #Admin table - store admin credentials and personal information
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tblAdmin (
    adminID TEXT PRIMARY KEY,
    firstName TEXT,
    surname TEXT,
    email TEXT,
    phone TEXT,
    username TEXT,
    password TEXT
    );
    """)

    #Menu table - contains menu items, prices, categories, descriptions, availability
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tblMenu(
        menuItemID INTEGER PRIMARY KEY,
        itemName TEXT NOT NULL,
        itemCategory TEXT NOT NULL,
        itemPrice REAL NOT NULL,
        itemDescription TEXT,
        itemAvailability TEXT DEFAULT 'Available',
        preparationTime INTEGER
    );
    """)

    #Orders table - stores customer orders, including items, quantities, total price
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tblOrders(
        orderID INTEGER PRIMARY KEY,
        customerID TEXT,
        orderDate TEXT,
        orderTime TEXT,
        menuItem TEXT,
        quantity INTEGER,
        totalPrice REAL,
        orderStatus TEXT DEFAULT 'Pending',
        dietaryRequirement TEXT
    );
    """)

    #Reservations table - store booking information for tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tblReservations(
        reservationID INTEGER PRIMARY KEY,
        customerID TEXT,
        reservationDate TEXT NOT NULL,
        reservationTime TEXT NOT NULL,
        tableNumber INTEGER,
        numOfGuests INTEGER NOT NULL,
        specialRequest TEXT,
        status TEXT DEFAULT 'Confirmed'
    );
    """)

    #Shifts table - monitor working hours
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tblShifts(
        shiftID INTEGER PRIMARY KEY,
        staffID TEXT,
        shiftDate TEXT NOT NULL,
        startTime TEXT,
        endTime TEXT,
        hours INTEGER
    );
    """)

    #Stock table - track ingredients and their levels of amount
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tblStock(
        stockID INTEGER PRIMARY KEY,
        itemName TEXT NOT NULL,
        quantityAvailable INTEGER DEFAULT 0,
        reorderLevel INTEGER DEFAULT 5,
        unitPrice REAL,
        supplierName TEXT
    );
    """)

    #Payments table - logs payments for orders
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tblPayments(
        paymentID INTEGER PRIMARY KEY,
        orderID INTEGER,
        customerID TEXT,
        paymentDate TEXT,
        amountPaid REAL,
        paymentMethod TEXT,
        paymentStatus TEXT DEFAULT 'Pending'
    );
    """)

    #Analytics & Reports table - stores analytics on sales, orders, and popular items
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tblReports(
        reportID INTEGER PRIMARY KEY,
        reportType TEXT,
        dateGenerated TEXT,
        totalSales REAL DEFAULT 0.00,
        totalOrders INTEGER DEFAULT 0,
        mostPopularItem TEXT,
        startDate TEXT,
        endDate TEXT
    );
    """)

    #Login Logs table - records login history for security and tracking
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tblLoginLogs(
        logID INTEGER PRIMARY KEY,
        time TEXT,
        date TEXT,
        username TEXT,
        roleID TEXT
    );
    """)

    connection.commit()
    connection.close()


#Create an Account
def account_creation():
    accountScreen = tk.Toplevel(homeScreen)
    accountScreen.title("El Aziz")
    accountScreen.geometry("600x450")

    #Back button to improve navigation
    tk.Button(accountScreen, text="Back", command=accountScreen.destroy).pack(anchor="w", padx=10, pady=5)

    #Add a heading to inform the user of the process
    tk.Label(
        accountScreen,
        text="Create Account",
        bg="darkgrey",
        font=("Arial", 16, "bold"),
        height=3
    ).pack(fill="x", pady=10)

    #Role selection
    role_frame = tk.Frame(accountScreen)
    role_frame.pack(pady=10)

    role = tk.IntVar(value=0)

    tk.Radiobutton(role_frame, text="Customer", variable=role, value=1).pack(anchor="w")
    tk.Radiobutton(role_frame, text="Staff", variable=role, value=2).pack(anchor="w")
    tk.Radiobutton(role_frame, text="Admin", variable=role, value=3).pack(anchor="w")
    
    #Form
    form = tk.Frame(accountScreen)
    form.pack(pady=10)

    firstName = tk.StringVar()
    surname = tk.StringVar()
    email = tk.StringVar()
    phone = tk.StringVar()
    username = tk.StringVar()
    password = tk.StringVar()

    #Create bars for entry, for user to input details
    tk.Label(form, text="First Name:").grid(row=0, column=0, pady=2)
    tk.Entry(form, textvariable=firstName).grid(row=0, column=1)

    tk.Label(form, text="Surname:").grid(row=1, column=0, pady=2)
    tk.Entry(form, textvariable=surname).grid(row=1, column=1)

    tk.Label(form, text="Email:").grid(row=2, column=0, pady=2)
    tk.Entry(form, textvariable=email).grid(row=2, column=1)

    tk.Label(form, text="Phone:").grid(row=3, column=0, pady=2)
    tk.Entry(form, textvariable=phone).grid(row=3, column=1)

    tk.Label(form, text="Username:").grid(row=4, column=0, pady=2)
    tk.Entry(form, textvariable=username).grid(row=4, column=1)

    tk.Label(form, text="Password:").grid(row=5, column=0, pady=2)
    tk.Entry(form, textvariable=password, show="*").grid(row=5, column=1)


    #Submit User
    def submit_user():
        #Presence checks: ensure no fields are left empty
        if firstName.get() == "" or surname.get() == "" or email.get() == "" or phone.get() == "" or username.get() == "" or password.get() == "":
            tk.Label(accountScreen, text="All fields must be filled in", fg="red").pack()
            return

        #Length checks: username and password must be reasonable length
        if len(username.get()) < 3 or len(username.get()) > 20:
            tk.Label(accountScreen, text="Username must be between 3 and 20 characters", fg="red").pack()
            return

        if len(password.get()) < 6:
            tk.Label(accountScreen, text="Password must be at least 6 characters", fg="red").pack()
            return

        #Format check: email must contain @ and a .
        if "@" not in email.get() or "." not in email.get():
            tk.Label(accountScreen, text="Email must be a valid format e.g. name@email.com", fg="red").pack()
            return

        #Type check: phone number must contain only numbers
        if phone.get().isdigit() == False:
            tk.Label(accountScreen, text="Phone number must contain numbers only", fg="red").pack()
            return

        #Length check: phone number must be 11 digits
        if len(phone.get()) != 11:
            tk.Label(accountScreen, text="Phone number must be 11 digits", fg="red").pack()
            return

        #Role check: a role must be selected
        if role.get() == 0:
            tk.Label(accountScreen, text="Please select a role", fg="red").pack()
            return

        #Successful checks, insert into database
        connection = sqlite3.connect("ElAziz.db")
        cursor = connection.cursor()

        #Generate a unique ID
        if role.get() == 1:  #Customer
            userID = "CUST" + str(len(firstName.get()) * 100 + len(surname.get()) * 10 + ord(firstName.get()[0]))
            cursor.execute("""
                INSERT INTO tblCustomers (customerID, firstName, surname, email, phone, username, password)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (userID, firstName.get(), surname.get(), email.get(), phone.get(), username.get(), password.get()))

        elif role.get() == 2:  #Staff
            userID = "STAFF" + str(len(firstName.get()) * 100 + len(surname.get()) * 10 + ord(firstName.get()[0]))
            cursor.execute("""
                INSERT INTO tblStaff (staffID, firstName, surname, email, phone, username, password)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (userID, firstName.get(), surname.get(), email.get(), phone.get(), username.get(), password.get()))

        elif role.get() == 3:  #Admin
            cursor.execute("SELECT COUNT(*) FROM tblAdmin")
            count = cursor.fetchone()[0]
            userID = "ADMIN" + str(count + 1)
            cursor.execute("""
                INSERT INTO tblAdmin (adminID, firstName, surname, email, phone, username, password)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (userID, firstName.get(), surname.get(), email.get(), phone.get(), username.get(), password.get()))

        connection.commit()
        connection.close()

        accountScreen.destroy()

    #Submit Button
    tk.Button(accountScreen, text="Submit", command=submit_user).pack(pady=15)


#Login Window
def login():
    loginScreen = tk.Toplevel(homeScreen)
    loginScreen.title("El Aziz")
    loginScreen.geometry('600x400')

    #Back button to improve navigation
    tk.Button(loginScreen, text="Back", command=loginScreen.destroy).pack(anchor="w", padx=10, pady=5)

    #Create a heading to inform user of process
    tk.Label(
        loginScreen,
        text="Login",
        bg="darkgrey",
        font=("Arial", 16, "bold"),
        height=3
    ).pack(fill="x", pady=20)

    form = tk.Frame(loginScreen)
    form.pack(pady=20)

    #Create entry bars for user to input login
    tk.Label(form, text="Username: ").grid(row=0, column=0, pady=5)
    tk.Label(form, text="Password: ").grid(row=1, column=0, pady=5)

    entry_user = tk.Entry(form)
    entry_pass = tk.Entry(form, show="*")

    entry_user.grid(row=0, column=1, pady=5)
    entry_pass.grid(row=1, column=1, pady=5)

    #Separate subroutine to submit the login details
    def submit_login():
        username = entry_user.get()
        password = entry_pass.get()
        connection = sqlite3.connect("ElAziz.db")
        cursor = connection.cursor()
        role = ""
        roleID = ""

        #Check Customers
        cursor.execute("SELECT * FROM tblCustomers WHERE username=? AND password=?", (username, password))
        row = cursor.fetchone()
        if row:
            role = "Customer"
            roleID = row[0]
        else:
            #Check Staff
            cursor.execute("SELECT * FROM tblStaff WHERE username=? AND password=?", (username, password))
            row = cursor.fetchone()
            if row:
                role = "Staff"
                roleID = row[0]
            else:
                #Check Admin
                cursor.execute("SELECT * FROM tblAdmin WHERE username=? AND password=?", (username, password))
                row = cursor.fetchone()
                if row:
                    role = "Admin"
                    roleID = row[0]

        if role != "":
            #Save login log - this is data used to demonstrate its logging
            date = "18/01/2026"
            time = "16:22"
            try:
                cursor.execute(
                    "INSERT INTO tblLoginLogs (username, roleID, date, time) VALUES (?,?,?,?)",
                    (username, roleID, date, time))
                connection.commit()
            except:
                pass
            connection.close()
            dashboard(role, roleID)
            loginScreen.destroy()
        else:
            tk.Label(loginScreen, text="Login Failed!", fg="red").pack()
            connection.close()
            
    tk.Button(loginScreen, text="Login", command=submit_login).pack(pady=20)

#Inserting Menu Items into Database
def insert_menu_items():
    connection = sqlite3.connect("ElAziz.db")
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM tblMenu")
    if cursor.fetchone()[0] == 0:
        #Display menu item, Category, Price and item description
        menu_items = [
            ("Samsa", "Starter", 3.50, "Pastry with meat or pumpkin"),
            ("Mantu", "Starter", 4.00, "Steamed dumplings with lamb or beef"),
            ("Shakarob Salad", "Salad", 2.50, "Tomatoes, cucumber, onions and herbs"),
            ("Achichuk Salad", "Salad", 3.00, "Tomatoes, chili, onions and parsley"),
            ("Green Tea", "Drink", 1.50, "Traditional Uzbek green tea"),
            ("Kompot", "Drink", 2.00, "Homemade fruit drink"),
            ("Plov", "Main", 6.50, "Traditional Uzbek rice dish"),
            ("Lagman", "Main", 5.50, "Noodle soup"),
            ("Shurpa", "Main", 5.00, "Meat and vegetable soup")
        ]
        cursor.executemany(
            "INSERT INTO tblMenu (itemName, itemCategory, itemPrice, itemDescription) VALUES (?,?,?,?)",
            menu_items
        )
    connection.commit()
    connection.close()


#Separate subroutine to create the dashboard window
def dashboard(role, roleID):
    dashboardScreen = tk.Toplevel(homeScreen)
    dashboardScreen.title("El Aziz")
    dashboardScreen.geometry("600x450")

    #Back button to improve navigation
    tk.Button(dashboardScreen, text="Back", command=dashboardScreen.destroy).pack(anchor="w", padx=10, pady=5)

    tk.Label(
        dashboardScreen,
        text="Welcome to your dashboard!",
        bg="darkgrey",
        font=("Arial", 16, "bold"),
        height=3
    ).pack(fill="x", pady=20)

    
    #CUSTOMER TASKS

    def browse_menu():
        #Opens a new window showing all menu items sorted by price
        menuScreen = tk.Toplevel(dashboardScreen)
        menuScreen.title("El Aziz")
        menuScreen.geometry("600x600")

        #Back button to improve navigation
        tk.Button(menuScreen, text="Back", command=menuScreen.destroy).pack(anchor="w", padx=10, pady=5)

        tk.Label(
            menuScreen,
            text="Welcome to El Aziz's Menu",
            bg="darkgrey",
            font=("Arial", 16, "bold"),
            height=3
        ).pack(fill="x", pady=10)

        #Scrollbar to view all itmes, does not fit in normal sized window
        scroll_bar = tk.Scrollbar(menuScreen)
        scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
        
        #Listbox to hold the menu items data, connected to scrollbar
        mylist = tk.Listbox(menuScreen, yscrollcommand=scroll_bar, width=80)
        mylist.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_bar.config(command=mylist.yview)

        search_var = tk.StringVar()
        tk.Label(menuScreen, text="Search for an item:").pack()
        tk.Entry(menuScreen, textvariable=search_var).pack() 

        #Retrieve all menu items with no ordering - bubble sort handles ordering
        connection = sqlite3.connect("ElAziz.db")
        cursor = connection.cursor()
        cursor.execute("SELECT itemCategory, itemName, itemPrice, itemDescription FROM tblMenu")
        all_items = list(cursor.fetchall())
        connection.close()

        #Bubble sort by itemPrice, ascending order
        n = len(all_items)
        swapped = True
        while n > 0 and swapped == True:
            swapped = False
            n = n - 1
            for index in range(0, n):   #Index 2 = itemPrice
                if all_items[index][2] > all_items[index + 1][2]:
                    temp = all_items[index]
                    all_items[index] = all_items[index + 1]
                    all_items[index + 1] = temp
                    swapped = True

        #Binary search by itemName
        def binary_search_menu():
            target = search_var.get()
            low = 0
            high = len(all_items) - 1
            found = None
            while low <= high:
                mid = (low + high) // 2
                if all_items[mid][1] == target:
                    found = all_items[mid]
                    #Stop the loop
                    low = high + 1
                elif all_items[mid][1] < target:
                    #Search right half
                    low = mid + 1
                else:
                    #Search left half
                    high = mid - 1

            #Display result in the GUI
            if found:
                result_label.config(text=f"Found: {found[1]} - ${found[2]:.2f} ({found[0]})")
            else:
                result_label.config(text="Item not found")
                    
        tk.Button(menuScreen, text="Search", command= binary_search_menu).pack(pady=5)
        result_label = tk.Label(menuScreen, text="", fg="black")
        result_label.pack()

        #Display sorted items
        current_category = None
        for category, name, price, desc in all_items:
            if category != current_category:
                current_category = category
                mylist.insert(tk.END, f" {category}")
            mylist.insert(tk.END, f"{name} - ${price:.2f}")
            mylist.insert(tk.END, f"{desc}")
            mylist.insert(tk.END, "")  #spacing
            
    def create_order():
        #Allows customers to select items and quantities, calculates total, stores order in database
        orderScreen = tk.Toplevel(dashboardScreen)
        orderScreen.title("El Aziz")
        orderScreen.geometry("500x900")

        #Back button to improve navigation
        tk.Button(orderScreen, text="Back", command=orderScreen.destroy).pack(anchor="w", padx=10, pady=5)

        tk.Label(
            orderScreen,
            text="Create Order",
            bg="darkgrey",
            font=("Arial", 16, "bold"),
            height=3
        ).pack(fill="x", pady=10)

        #Retrieve menu items from database
        connection = sqlite3.connect("ElAziz.db")
        cursor = connection.cursor()
        cursor.execute("SELECT menuItemID, itemName, itemPrice FROM tblMenu")
        menu_items = cursor.fetchall()
        connection.close()

        #Track the users choices/selections and the quantities specified
        selections = {}
        quantities = {}
        total_var = tk.DoubleVar(value=0.0)

        #Function to calculate the total price whenever an item or quantity changes
        def update_total():
            total = 0
            for item in menu_items:
                item_id = item[0]
                if selections[item_id].get() == 1:  #Check if item is selected
                    try:
                        quantity = int(quantities[item_id].get())  #Get the quantity specified
                        if quantity < 1 or quantity > 5:  #Range check
                            quantity = 0
                    except:
                        quantity = 0
                    total += quantity * item[2]  #Multiply by item price
            total_var.set(total)  #Update total displayed in the GUI

        #Submit the order to the database
        def submit_order():
             errors = []
             for item in menu_items:
                 item_id = item[0]
                 if selections[item_id].get() == 1:
                     raw = quantities[item_id].get()
                     try:
                         quantity = int(raw)
                     except:
                         errors.append(f"'{item[1]}': quantity must be a number.")
                     if quantity == 0:
                        errors.append(f"'{item[1]}' is selected but quantity is 0. Enter 1–5.")
                     elif quantity < 1 or quantity > 5:
                        errors.append(f"'{item[1]}': quantity must be between 1 and 5.")
             if errors:
                tk.Label(orderScreen, text="Invalid Order", fg="red").pack()

             order_items = []
             for item in menu_items:
                 item_id = item[0]
                 if selections[item_id].get() == 1:
                    try:
                        quantity = int(quantities[item_id].get())
                    except:
                        quantity = 0
                    if quantity > 0:
                        order_items.append(f"{item[1]} x {quantity}")

             #Insert the order into the Orders table
             connection = sqlite3.connect("ElAziz.db")
             cursor = connection.cursor()
             cursor.execute(
                "INSERT INTO tblOrders (customerID, menuItem, totalPrice) VALUES (?,?,?)",
                (roleID, ", ".join(order_items), total_var.get())
             )
             connection.commit()
             connection.close()
             orderScreen.destroy()
             print(f"Order placed! Total: ${total_var.get()}")

        #Create checkboxes and quantity entries for each menu item
        for item in menu_items:
            selections[item[0]] = tk.IntVar()
            quantities[item[0]] = tk.StringVar(value="0")
            tk.Checkbutton(orderScreen, text=f"{item[1]} - ${item[2]}", variable=selections[item[0]], command=update_total).pack(anchor="w")
            tk.Entry(orderScreen, textvariable=quantities[item[0]], width=5).pack(anchor="w")

        #Display the dynamic total and submit button
        tk.Label(orderScreen, textvariable=total_var, font=("Arial", 14, "bold")).pack(pady=10)
        tk.Button(orderScreen, text="Submit Order", command=submit_order).pack(pady=5)

    def create_reservation():
        #Allows customers to book tables, specifying date, time, and special requests
        reservationScreen = tk.Toplevel(dashboardScreen)
        reservationScreen.title("El Aziz")
        reservationScreen.geometry("500x500")

        #Back button to improve navigation
        tk.Button(reservationScreen, text="Back", command=reservationScreen.destroy).pack(anchor="w", padx=10, pady=5)

        tk.Label(
            reservationScreen,
            text="Create Reservation",
            bg="darkgrey",
            font=("Arial", 16, "bold"),
            height=3
        ).pack(fill="x", pady=10)

        #Tkinter variables to store inputs
        date_var = tk.StringVar()
        time_var = tk.StringVar()
        guests_var = tk.StringVar()
        special_var = tk.StringVar()

        #Create fields of entry for each field
        tk.Label(reservationScreen, text="Date (DD/MM/YYYY)").pack()
        tk.Entry(reservationScreen, textvariable=date_var).pack()
        tk.Label(reservationScreen, text="Time (HH:MM)").pack()
        tk.Entry(reservationScreen, textvariable=time_var).pack()
        tk.Label(reservationScreen, text="Number of Guests").pack()
        tk.Entry(reservationScreen, textvariable=guests_var).pack()
        tk.Label(reservationScreen, text="Special Requests").pack()
        tk.Entry(reservationScreen, textvariable=special_var).pack()

        #Function to insert the reservation into the database
        def submit_reservation():
            #Presence checks: ensure no fields are left empty
            if date_var.get() == "" or time_var.get() == "" or guests_var.get() == "":
                tk.Label(reservationScreen, text="Date, time and guests must be filled in", fg="red").pack()
                return

            #Format check: date must follow DD/MM/YYYY
            if len(date_var.get()) != 10 or date_var.get()[2] != "/" or date_var.get()[5] != "/":
                tk.Label(reservationScreen, text="Date must be in format DD/MM/YYYY", fg="red").pack()
                return

            #Format check: time must follow HH:MM
            if len(time_var.get()) != 5 or time_var.get()[2] != ":":
                tk.Label(reservationScreen, text="Time must be in format HH:MM", fg="red").pack()
                return

            #Type check: guests must be a number
            if guests_var.get().isdigit() == False:
                tk.Label(reservationScreen, text="Number of guests must be a number", fg="red").pack()
                return

            #Range check: guests must be between 1 and 20
            if int(guests_var.get()) < 1 or int(guests_var.get()) > 20:
                tk.Label(reservationScreen, text="Number of guests must be between 1 and 20", fg="red").pack()
                return

            #After all checks, insert into database
            connection = sqlite3.connect("ElAziz.db")
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO tblReservations (customerID, reservationDate, reservationTime, numOfGuests, specialRequest)
                VALUES (?,?,?,?,?)
            """, (roleID, date_var.get(), time_var.get(), guests_var.get(), special_var.get()))

            connection.commit()
            connection.close()
            reservationScreen.destroy()
            tk.Label(reservationScreen, text="Reservation Made!", fg="red").pack()

        tk.Button(reservationScreen, text="Submit Reservation", command=submit_reservation).pack(pady=10)

    def view_orders_reservations():
        viewScreen = tk.Toplevel(dashboardScreen)
        viewScreen.title("El Aziz")
        viewScreen.geometry("600x500")

        #Back button to improve navigation
        tk.Button(viewScreen, text="Back", command=viewScreen.destroy).pack(anchor="w", padx=10, pady=5)

        tk.Label(
        viewScreen,
        text="View Orders & Reservations",
        bg="darkgrey",
        font=("Arial", 16, "bold"),
        height=3
        ).pack(fill="x", pady=10)

        #Scrollbar and box to see all results, scroll to see all data
        frame = tk.Frame(viewScreen)
        frame.pack(fill="both", expand=True)
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")
        listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, width=100, font=("Arial", 10))
        listbox.pack(fill="both", expand=True)
        scrollbar.config(command=listbox.yview)

        connection = sqlite3.connect("ElAziz.db")
        cursor = connection.cursor()

        #Retrieve all orders
        cursor.execute("SELECT orderID, menuItem, totalPrice, customerID FROM tblOrders")
        all_orders = cursor.fetchall()

        #Retrieve all reservations
        cursor.execute("SELECT reservationID, reservationDate, reservationTime, numOfGuests, specialRequest, customerID FROM tblReservations")
        all_reservations = cursor.fetchall()

        connection.close()

        #Linear search: find orders belonging to this customer 
        orders = []
        for row in all_orders: #index 3 = customerID)
            if str(row[3]) == str(roleID):
                orders.append(row)

        #Insertion sort: sort orders by totalPrice (index 2)
        n = len(orders)
        for index in range(1, n):
            current = orders[index]
            index2 = index
            while index2 > 0 and orders[index2 - 1][2] > current[2]:  #[2] = totalPrice
                orders[index2] = orders[index2 - 1]
                index2 = index2 - 1
                orders[index2] = current

        search_var = tk.StringVar()
        tk.Label(viewScreen, text="Search Reservation by ID:").pack()
        tk.Entry(viewScreen, textvariable=search_var).pack()

        #Linear search: find reservations belonging to this customer
        reservations = []
        for row in all_reservations: #index 5 = customerID
            if str(row[5]) == str(roleID):
                reservations.append(row)

        #Bubble sort: sort reservations by reservationDate
        n = len(reservations)
        swapped = True
        while n > 0 and swapped == True:
            swapped = False
            n = n - 1
            for index in range(0, n):
                if reservations[index][1] > reservations[index + 1][1]:  #index 1 = reservationDate
                    temp = reservations[index]
                    reservations[index] = reservations[index + 1]
                    reservations[index + 1] = temp
                    swapped = True

        #Search bar: linear search orders by orderID
        search_var = tk.StringVar()
        tk.Label(viewScreen, text="Search Order by ID:").pack()
        tk.Entry(viewScreen, textvariable=search_var).pack()

        #Linear Search active/complete orders, search one at a time
        def linear_search_orders_res():
            target = search_var.get()

            #Search orders by orderID
            index = 0
            found_order = False
            while index < len(orders):
                if str(orders[index][0]) == str(target):  #[0]= orderID
                    found_order = True
                    break
                index = index + 1
                
            #Search reservations by reservationID
            index = 0
            found_reservation = False
            while index < len(reservations):
                if str(reservations[index][0]) == str(target):  #[0]= orderID
                    found_reservation = True
                    break
                index = index + 1

            #Display messages for search results
            if found_order:
                result_label.config(text=f"Found Order - ID: {found_order[index][0]}, Items: {found_order[index][1]}, Total: ${found_order[index][2]:.2f}")
            elif found_reservation:
                result_label.config(text=f"Found Reservation - ID: {found_reservation[0]}, Date: {found_reservation[1]}, Time: {found_reservation[2]}, Guests: {found_reservation[3]}")
            else:
                result_label.config(text="Order/Reservation not found")

        tk.Button(viewScreen, text="Search", command=linear_search_orders_res).pack(pady=5)
        result_label = tk.Label(viewScreen, text="", fg="green")
        result_label.pack()

        #Display orders
        listbox.insert("end", "* Orders ")
        if orders:
            for order in orders:
                listbox.insert("end", f"Order ID: {order[0]}")
                listbox.insert("end", f"  Items: {order[1]}")
                listbox.insert("end", f"  Total: ${order[2]:.2f}")
                listbox.insert("end", "")

        else:
            listbox.insert("end", "No orders found")
            listbox.insert("end", "")

        #Display reservations
        listbox.insert("end", "* Reservations ")
        if reservations:
            for reservation in reservations:
                listbox.insert("end", f"Reservation ID: {reservation[0]}")
                listbox.insert("end", f"  Date: {reservation[1]}, Time: {reservation[2]}")
                listbox.insert("end", f"  Guests: {reservation[3]}")
                listbox.insert("end", f"  Special Request: {reservation[4]}")
                listbox.insert("end", "")
        else:
            listbox.insert("end", "No reservations found")

    def manage_account():
        #Displays the account details for the logged in user
        connection = sqlite3.connect("ElAziz.db")
        cursor = connection.cursor()

        #Retrieve all records: linear search finds the matching one
        if role == "Customer":
            cursor.execute("SELECT * FROM tblCustomers")
        elif role == "Staff":
            cursor.execute("SELECT * FROM tblStaff")
        elif role == "Admin":
            cursor.execute("SELECT * FROM tblAdmin")

        all_data = cursor.fetchall()
        connection.close()

        #Linear search by ID
        data = None
        index = 0
        while index < len(all_data):
            if str(all_data[index][0]) == str(roleID):  #[0] = ID
                data = all_data[index]
                index = len(all_data)  #Stop the loop once found
            index = index + 1

        accountScreen = tk.Toplevel(dashboardScreen)
        accountScreen.title("El Aziz")
        accountScreen.geometry("400x350")

        #Back button to improve navigation
        tk.Button(accountScreen, text="Back", command=accountScreen.destroy).pack(anchor="w", padx=10, pady=5)

        tk.Label(
            accountScreen,
            text="My Account",
            bg="darkgrey",
            font=("Arial", 16, "bold"),
            height=3
        ).pack(fill="x", pady=10)

        if data:
            tk.Label(accountScreen, text="ID: " + str(data[0])).pack(anchor="w", padx=10, pady=2)
            tk.Label(accountScreen, text="First Name: " + str(data[1])).pack(anchor="w", padx=10, pady=2)
            tk.Label(accountScreen, text="Surname: " + str(data[2])).pack(anchor="w", padx=10, pady=2)
            tk.Label(accountScreen, text="Email: " + str(data[3])).pack(anchor="w", padx=10, pady=2)
            tk.Label(accountScreen, text="Phone: " + str(data[4])).pack(anchor="w", padx=10, pady=2)
            tk.Label(accountScreen, text="Username: " + str(data[5])).pack(anchor="w", padx=10, pady=2)
        else:
            tk.Label(accountScreen, text="No account data found").pack(pady=20)

    #STAFF TASKS

    def view_shifts():
        #Opens a window showing all shifts for the logged in staff member
        shiftsScreen = tk.Toplevel(dashboardScreen)
        shiftsScreen.title("El Aziz")
        shiftsScreen.geometry("600x400")

        #Back button to improve navigation
        tk.Button(shiftsScreen, text="Back", command=shiftsScreen.destroy).pack(anchor="w", padx=10, pady=5)

        tk.Label(
            shiftsScreen,
            text="My Shifts",
            bg="darkgrey",
            font=("Arial", 16, "bold"),
            height=3
        ).pack(fill="x", pady=10)

        connection = sqlite3.connect("ElAziz.db")
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM tblShifts WHERE staffID=?", (roleID,))
        #Insert test data to demonstrate its representation
        if cursor.fetchone() is None:
            cursor.execute("""
            INSERT INTO tblShifts (staffID, shiftDate, startTime, endTime, hours)
            VALUES (?, '02/04/2026', '09:00', '17:00', 8) 
            """, (roleID,))
            connection.commit()
        
        #Retrieve all shifts with no filter, linear search handles sorting
        cursor.execute("SELECT shiftID, staffID, shiftDate, startTime, endTime, hours FROM tblShifts")
        all_shifts = cursor.fetchall()
        connection.close()

        #Linear search to find shifts belonging to this staff member 
        found_shifts = []
        index = 0
        found = False
        while index < len(all_shifts):
            if str(all_shifts[index][1]) == str(roleID):  #[1] = staffID
                found_shifts.append(all_shifts[index])
                found = True
            index = index + 1

        if found:
            for shift in found_shifts:
                tk.Label(shiftsScreen, text=f"Shift ID: {shift[0]}").pack(anchor="w", padx=10)
                tk.Label(shiftsScreen, text=f"Date: {shift[2]}").pack(anchor="w", padx=20)
                tk.Label(shiftsScreen, text=f"Start: {shift[3]}  End: {shift[4]}").pack(anchor="w", padx=20)
                tk.Label(shiftsScreen, text=f"Hours: {shift[5]}").pack(anchor="w", padx=20)
                tk.Label(shiftsScreen, text="").pack()
        else:
            tk.Label(shiftsScreen, text="No shifts found").pack(pady=10)

    def view_databases():
        #Opens a window showing key database tables for staff
        databaseScreen = tk.Toplevel(dashboardScreen)
        databaseScreen.title("El Aziz")
        databaseScreen.geometry("700x500")

        #Back button to improve navigation
        tk.Button(databaseScreen, text="Back", command=databaseScreen.destroy).pack(anchor="w", padx=10, pady=5)

        tk.Label(
            databaseScreen,
            text="View Databases",
            bg="darkgrey",
            font=("Arial", 16, "bold"),
            height=3
        ).pack(fill="x", pady=10)

        #Scrollbar and scrollable box so all data is visible
        frame = tk.Frame(databaseScreen)
        frame.pack(fill="both", expand=True)
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")
        listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, width=100)
        listbox.pack(fill="both", expand=True)
        scrollbar.config(command=listbox.yview)

        connection = sqlite3.connect("ElAziz.db")
        cursor = connection.cursor()

        #Retrieve and display each table separately
        for table in ["tblOrders", "tblReservations", "tblMenu", "tblShifts", "tblStock"]:
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            listbox.insert("end", f"{table}")
            for row in rows:
                listbox.insert("end", str(row))
            listbox.insert("end", "")

        connection.close()

    def view_active_orders():
        #Opens a window showing all orders and reservations, sorted by date
        activeOrdersScreen = tk.Toplevel(dashboardScreen)
        activeOrdersScreen.title("El Aziz")
        activeOrdersScreen.geometry("600x500")

        #Back button to improve navigation
        tk.Button(activeOrdersScreen, text="Back", command=activeOrdersScreen.destroy).pack(anchor="w", padx=10, pady=5)

        tk.Label(
            activeOrdersScreen,
            text="Active Orders & Reservations",
            bg="darkgrey",
            font=("Arial", 16, "bold"),
            height=3
        ).pack(fill="x", pady=10)

        connection = sqlite3.connect("ElAziz.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM tblOrders")
        all_orders = list(cursor.fetchall())
        cursor.execute("SELECT * FROM tblReservations")
        all_reservations = list(cursor.fetchall())
        connection.close()

        #Bubble sort orders by orderDate 
        n = len(all_orders)
        swapped = True
        while n > 0 and swapped == True:
            swapped = False
            n = n - 1
            for index in range(0, n):
                if all_orders[index][2] is not None and all_orders[index + 1][2] is not None:  #[2] = orderDate
                    temp = all_orders[index]
                    all_orders[index] = all_orders[index + 1]
                    all_orders[index + 1] = temp
                    swapped = True

        tk.Label(activeOrdersScreen, text="Orders", font=("Arial", 12, "bold")).pack(pady=5)
        if all_orders:
            for order in all_orders:
                tk.Label(activeOrdersScreen, text=f"Order ID: {order[0]}  Customer: {order[1]}  Items: {order[4]}  Total: ${order[6]}").pack(anchor="w", padx=10)
        else:
            tk.Label(activeOrdersScreen, text="No orders found").pack(pady=5)

        tk.Label(activeOrdersScreen, text="Reservations", font=("Arial", 12, "bold")).pack(pady=5)
        if all_reservations:
            for reservation in all_reservations:
                tk.Label(activeOrdersScreen, text=f"Reservation ID: {reservation[0]}  Customer: {reservation[1]}  Date: {reservation[2]}  Time: {reservation[3]}  Guests: {reservation[5]}").pack(anchor="w", padx=10)
        else:
            tk.Label(activeOrdersScreen, text="No reservations found").pack(pady=5)

    #ADMIN TASKS 

    def view_all_shifts():
        #Opens a window showing all shifts for all staff
        shiftsScreen = tk.Toplevel(dashboardScreen)
        shiftsScreen.title("El Aziz")
        shiftsScreen.geometry("600x400")

        #Back button to improve navigation
        tk.Button(shiftsScreen, text="Back", command=shiftsScreen.destroy).pack(anchor="w", padx=10, pady=5)

        tk.Label(
            shiftsScreen,
            text="All Staff Shifts",
            bg="darkgrey",
            font=("Arial", 16, "bold"),
            height=3
        ).pack(fill="x", pady=10)

        connection = sqlite3.connect("ElAziz.db")
        cursor = connection.cursor()
        cursor.execute("SELECT shiftID, staffID, shiftDate, startTime, endTime, hours FROM tblShifts")
        all_shifts = cursor.fetchall()
        connection.close()

        if all_shifts:
            for shift in all_shifts:
                tk.Label(shiftsScreen, text=f"Shift ID: {shift[0]}  Staff: {shift[1]}").pack(anchor="w", padx=10)
                tk.Label(shiftsScreen, text=f"Date: {shift[2]}  Start: {shift[3]}  End: {shift[4]}  Hours: {shift[5]}").pack(anchor="w", padx=20)
                tk.Label(shiftsScreen, text="").pack()
        else:
            tk.Label(shiftsScreen, text="No shifts found").pack(pady=10)

    def view_all_databases():
        #Opens a window showing all database tables for admin
        databasesScreen = tk.Toplevel(dashboardScreen)
        databasesScreen.title("El Aziz")
        databasesScreen.geometry("700x500")

        #Back button to improve navigation
        tk.Button(databasesScreen, text="Back", command=databasesScreen.destroy).pack(anchor="w", padx=10, pady=5)

        tk.Label(
            databasesScreen,
            text="All Databases",
            bg="darkgrey",
            font=("Arial", 16, "bold"),
            height=3
        ).pack(fill="x", pady=10)

        frame = tk.Frame(databasesScreen)
        frame.pack(fill="both", expand=True)
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")
        listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, width=100)
        listbox.pack(fill="both", expand=True)
        scrollbar.config(command=listbox.yview)

        connection = sqlite3.connect("ElAziz.db")
        cursor = connection.cursor()

        #Display every table for admin
        for table in ["tblCustomers", "tblStaff", "tblAdmin", "tblOrders", "tblReservations", "tblMenu", "tblShifts", "tblStock", "tblPayments", "tblReports", "tblLoginLogs"]:
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            listbox.insert("end", f" {table} ")
            for row in rows:
                listbox.insert("end", str(row))
            listbox.insert("end", "")

        connection.close()

    def order_new_stock():
        stockScreen = tk.Toplevel(dashboardScreen)
        stockScreen.title("El Aziz")
        stockScreen.geometry("400x300")
        tk.Button(stockScreen, text="Back", command=stockScreen.destroy).pack(anchor="w", padx=10, pady=5)
        tk.Label(stockScreen, text="Order New Stock", bg="darkgrey", font=("Arial", 16, "bold"), height=3).pack(fill="x", pady=10)
        tk.Label(stockScreen, text="Feature coming soon").pack(pady=20)
 
    def view_reports_analytics():
        reportsScreen = tk.Toplevel(dashboardScreen)
        reportsScreen.title("El Aziz")
        reportsScreen.geometry("400x300")
        tk.Button(reportsScreen, text="Back", command=reportsScreen.destroy).pack(anchor="w", padx=10, pady=5)
        tk.Label(reportsScreen, text="Reports & Analytics", bg="darkgrey", font=("Arial", 16, "bold"), height=3).pack(fill="x", pady=10)
        tk.Label(reportsScreen, text="Feature coming soon").pack(pady=20)

    def manage_accounts():
        #Opens a window showing all customer, staff and admin accounts
        manageScreen = tk.Toplevel(dashboardScreen)
        manageScreen.title("El Aziz")
        manageScreen.geometry("700x500")

        #Back button to improve navigation
        tk.Button(manageScreen, text="Back", command=manageScreen.destroy).pack(anchor="w", padx=10, pady=5)

        tk.Label(
            manageScreen,
            text="Manage Accounts",
            bg="darkgrey",
            font=("Arial", 16, "bold"),
            height=3
        ).pack(fill="x", pady=10)

        #Scrollbar and scrollable box so all accounts are visible
        frame = tk.Frame(manageScreen)
        frame.pack(fill="both", expand=True)
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")
        listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, width=100)
        listbox.pack(fill="both", expand=True)
        scrollbar.config(command=listbox.yview)

        connection = sqlite3.connect("ElAziz.db")
        cursor = connection.cursor()

        #Retrieve all customers and display
        cursor.execute("SELECT * FROM tblCustomers")
        all_customers = cursor.fetchall()
        listbox.insert("end", " * Customers ")
        for row in all_customers:
            listbox.insert("end", f"ID: {row[0]}  Name: {row[1]} {row[2]}  Email: {row[3]}  Phone: {row[4]}  Username: {row[5]}")
        listbox.insert("end", "")

        #Retrieve all staff and display
        cursor.execute("SELECT * FROM tblStaff")
        all_staff = cursor.fetchall()
        listbox.insert("end", " * Staff")
        for row in all_staff:
            listbox.insert("end", f"ID: {row[0]}  Name: {row[1]} {row[2]}  Email: {row[3]}  Phone: {row[4]}  Username: {row[5]}")
        listbox.insert("end", "")

        #Retrieve all admins and display
        cursor.execute("SELECT * FROM tblAdmin")
        all_admins = cursor.fetchall()
        listbox.insert("end", " * Admins")
        for row in all_admins:
            listbox.insert("end", f"ID: {row[0]}  Name: {row[1]} {row[2]}  Email: {row[3]}  Phone: {row[4]}  Username: {row[5]}")

        connection.close()

    if role == "Customer":
        tk.Button(dashboardScreen, text='Browse Menu', width=25, height=2, command=browse_menu).pack(pady=5)
        tk.Button(dashboardScreen, text='Create Order', width=25, height=2, command=create_order).pack(pady=5)
        tk.Button(dashboardScreen, text='Create Reservation', width=25, height=2, command=create_reservation).pack(pady=5)
        tk.Button(dashboardScreen, text='View Orders/Reservations', width=25, height=2, command=view_orders_reservations).pack(pady=5)
        tk.Button(dashboardScreen, text='Manage Account', width=25, height=2, command=manage_account).pack(pady=5)

    elif role == "Staff":
        tk.Button(dashboardScreen, text='View Shifts', width=25, height=2, command=view_shifts).pack(pady=5)
        tk.Button(dashboardScreen, text='View Databases', width=25, height=2, command=view_databases).pack(pady=5)
        tk.Button(dashboardScreen, text='View Orders/Reservations', width=25, height=2, command=view_active_orders).pack(pady=5)
        tk.Button(dashboardScreen, text='Manage Account', width=25, height=2, command=manage_account).pack(pady=5)

    elif role == "Admin":
        tk.Button(dashboardScreen, text='View All Shifts', width=25, height=2, command=view_all_shifts).pack(pady=5)
        tk.Button(dashboardScreen, text='View Databases', width=25, height=2, command=view_all_databases).pack(pady=5)
        tk.Button(dashboardScreen, text='Order New Stock', width=25, height=2, command=order_new_stock).pack(pady=5)
        tk.Button(dashboardScreen, text='Reports & Analytics', width=25, height=2, command=view_reports_analytics).pack(pady=5)
        tk.Button(dashboardScreen, text='Manage Accounts', width=25, height=2, command=manage_accounts).pack(pady=5)

#Home Screen
homeScreen = tk.Tk()
homeScreen.title("El Aziz")
homeScreen.geometry('600x400')

#Header Label
textVarHeader = tk.StringVar(value="Welcome to El Aziz!")

header = tk.Label(
    homeScreen,
    textvariable=textVarHeader,
    anchor=tk.CENTER,
    bg="darkgrey",
    height=3,
    width=30,
    bd=3,
    font=("Arial", 16, "bold"),
    fg="black",
    padx=15,
    pady=15,
    justify=tk.CENTER,
    relief=tk.RAISED,
    wraplength=250
)
header.pack(pady=20)

#Contact Information
textVarContact = tk.StringVar(value=
    "Contact Us:\n"
    "elazizservices@gmail.com\n"
    "+998 93-945-86-91"
)

contact = tk.Label(
    homeScreen,
    textvariable=textVarContact,
    anchor=tk.CENTER,
    bd=3,
    font=("Arial", 8),
    fg="black",
    padx=15,
    pady=15,
    justify=tk.CENTER,
    relief=tk.RAISED,
    wraplength=300
)
contact.pack(pady=10)

#Home Screen Buttons
btn_create = ttk.Button(homeScreen, text='Create an Account', command=account_creation)
btn_create.pack(pady=10)

btn_login = ttk.Button(homeScreen, text='Login', command=login)
btn_login.pack(pady=10)


#Start Program
create_database()
insert_menu_items()
homeScreen.mainloop()
