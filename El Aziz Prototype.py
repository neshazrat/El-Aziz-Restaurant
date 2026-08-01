import tkinter as tk
from tkinter import ttk
import sqlite3

# --- DATABASES ---
# Create all databases in DBrowser

def create_database():
    conn = sqlite3.connect("ElAziz.db")
    cur = conn.cursor()

    # Customer table - store user credentials and personal info
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Customers (
    customerID TEXT PRIMARY KEY,
    firstName TEXT,
    surname TEXT,
    email TEXT,
    phone TEXT,
    username TEXT,
    password TEXT
    );
    """)

    # Staff table - store user credentials and personal info
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Staff (
    staffID TEXT PRIMARY KEY,
    firstName TEXT,
    surname TEXT,
    email TEXT,
    phone TEXT,
    username TEXT,
    password TEXT
    );
    """)

    # Admin table - store user credentials and personal info
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Admin (
    adminID TEXT PRIMARY KEY,
    firstName TEXT,
    surname TEXT,
    email TEXT,
    phone TEXT,
    username TEXT,
    password TEXT
    );
    """)

    # Menu table - contains menu items, prices, categories, descriptions, availability
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Menu(
        menuItemID INTEGER PRIMARY KEY ,
        itemName TEXT NOT NULL,
        itemCategory TEXT NOT NULL,
        itemPrice REAL NOT NULL,
        itemDescription TEXT,
        itemAvailability TEXT DEFAULT 'Available',
        preparationTime INTEGER
    );
    """)

    # Orders table - stores customer orders, including items, quantities, total price
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Orders(
        orderID INTEGER PRIMARY KEY,
        customerID TEXT,
        orderDate TEXT,
        orderTime TEXT,
        menuItem TEXT,
        quantity INTEGER,
        totalPrice REAL,
        orderStatus TEXT DEFAULT 'Pending',
        dietaryRequirement TEXT,
        FOREIGN KEY (customerID) REFERENCES Customer(customerID)
    );
    """)

    # Reservations table - store booking information for tables
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Reservations(
        reservationID INTEGER PRIMARY KEY,
        customerID TEXT,
        reservationDate TEXT NOT NULL,
        reservationTime TEXT NOT NULL,
        tableNumber INTEGER,
        numOfGuests INTEGER NOT NULL,
        specialRequest TEXT,
        status TEXT DEFAULT 'Confirmed',
        FOREIGN KEY (customerID) REFERENCES Customers(customerID)
    );
    """)

    # Shifts table - monitor working hours 
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Shifts(
        shiftID INTEGER PRIMARY KEY,
        staffID TEXT,
        day TEXT,
        startTime TEXT,
        endTime TEXT,
        hours INTEGER,
        FOREIGN KEY (staffID) REFERENCES Staff(staffID)
    );
    """)

    # Stock table - track ingredients and their levels of amount
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Stock(
        stockID INTEGER PRIMARY KEY,
        itemName TEXT NOT NULL,
        quantityAvailable INTEGER DEFAULT 0,
        reorderLevel INTEGER DEFAULT 5,
        unitPrice REAL,
        supplierName TEXT
    );
    """)

    # Payments table - logs payments for orders
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Payments(
        paymentID INTEGER PRIMARY KEY,
        orderID INTEGER,
        customerID TEXT,
        paymentDate TEXT,
        amountPaid REAL,
        paymentMethod TEXT,
        paymentStatus TEXT DEFAULT 'Pending',
        FOREIGN KEY (orderID) REFERENCES Orders(orderID),
        FOREIGN KEY (customerID) REFERENCES Customers(customerID)
    );
    """)

    # Analytics & Reports table - stores analytics on sales, orders, and popular items
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Reports(
        reportID INTEGER PRIMARY KEY ,
        reportType TEXT,
        dateGenerated TEXT,
        totalSales REAL DEFAULT 0.00,
        totalOrders INTEGER DEFAULT 0,
        mostPopularItem TEXT,
        startDate TEXT,
        endDate TEXT
    );
    """)

    # Login Logs table - records login history for security and tracking
    cur.execute("""
    CREATE TABLE IF NOT EXISTS LoginLogs(
        logID INTEGER PRIMARY KEY ,
        time TEXT,
        date TEXT,
        username TEXT,
        roleID TEXT
    );
    """)

    conn.commit()
    conn.close()

    
#--- NEW WINDOW: CREATE AN ACCOUNT ---
def new():
    # Create a window
    newScreen = tk.Toplevel(root)
    newScreen.title("El Aziz")
    newScreen.geometry("600x400")

    # Add a heading to inform the user of the process
    tk.Label(
        newScreen,
        text="Create Account",
        bg="darkgrey",
        font=("Arial", 16, "bold"),
        height=3
    ).pack(fill="x", pady=10)

    # Role selection 
    role_frame = tk.Frame(newScreen)
    role_frame.pack(pady=10)

    role = tk.IntVar(value=0)

    tk.Radiobutton(role_frame, text="Customer", variable=role, value=1).pack(anchor="w")
    tk.Radiobutton(role_frame, text="Staff", variable=role, value=2).pack(anchor="w")
    tk.Radiobutton(role_frame, text="Admin", variable=role, value=3).pack(anchor="w")

    # Form
    form = tk.Frame(newScreen)
    form.pack(pady=10)

    firstName = tk.StringVar()
    surname = tk.StringVar()
    email = tk.StringVar()
    phone = tk.StringVar()
    username = tk.StringVar()
    password = tk.StringVar()

    # Create bars for entry, for user to input details
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

    # --- Submit function ---
    def submit_user():
        conn = sqlite3.connect("ElAziz.db")
        cur = conn.cursor()

        # Generate a unique ID
        if role.get() == 1:  # Customer
            userID = "CUST" + str(len(firstName.get())*100 + len(surname.get())*10 + ord(firstName.get()[0]))
            cur.execute("""
                INSERT INTO Customers
                (customerID, firstName, surname, email, phone, username, password)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                userID,
                firstName.get(),
                surname.get(),
                email.get(),
                phone.get(),
                username.get(),
                password.get()
            ))

        elif role.get() == 2:  # Staff
            userID = "STAFF" + str(len(firstName.get())*100 + len(surname.get())*10 + ord(firstName.get()[0]))
            cur.execute("""
                INSERT INTO Staff
                (staffID, firstName, surname, email, phone, username, password)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                userID,
                firstName.get(),
                surname.get(),
                email.get(),
                phone.get(),
                username.get(),
                password.get()
            ))

        elif role.get() == 3:  # Admin
            cur.execute("SELECT COUNT(*) FROM Admin")
            count = cur.fetchone()[0]
            userID = "ADMIN" + str(count + 1)

            cur.execute("""
                INSERT INTO Admin
                (adminID, firstName, surname, email, phone, username, password)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    userID,
                    firstName.get(),
                    surname.get(),
                    email.get(),
                    phone.get(),
                    username.get(),
                    password.get()
                ))
            
        conn.commit()
        conn.close()

        # Close window after submission
        newScreen.destroy()

    # --- Submit Button ---
    tk.Button(newScreen, text="Submit", command=submit_user).pack(pady=15)
    

# --- LOGIN WINDOW ---
def new1():
    # Create a new window
    newScreen1 = tk.Toplevel(root)
    newScreen1.title("El Aziz")
    newScreen1.geometry('600x400')

    # Create a heading to infrom user of process
    tk.Label(
        newScreen1,
        text="Login",
        bg="darkgrey",
        font=("Arial", 16, "bold"),
        height=3
    ).pack(fill="x", pady=20)

    form = tk.Frame(newScreen1)
    form.pack(pady=20)

    # Create entry bars for user to input Login
    tk.Label(form, text="Username: ").grid(row=0, column=0, pady=5)
    tk.Label(form, text="Password: ").grid(row=1, column=0, pady=5)

    entry_user = tk.Entry(form)
    entry_pass = tk.Entry(form, show="*")

    entry_user.grid(row=0, column=1, pady=5)
    entry_pass.grid(row=1, column=1, pady=5)

    # Separate subroutine to submit the login details
    def submit_login():
        username = entry_user.get()
        password = entry_pass.get()
        conn = sqlite3.connect("ElAziz.db")
        cur = conn.cursor()
        role = ""
        roleID = ""

        # Check Customers
        cur.execute("SELECT * FROM Customers WHERE username=? AND password=?", (username, password))
        row = cur.fetchone()
        if row:
            role = "Customer"
            roleID = row[0]
        else:
            # Check Staff
            cur.execute("SELECT * FROM Staff WHERE username=? AND password=?", (username, password))
            row = cur.fetchone()
            if row:
                role = "Staff"
                roleID = row[0]
            else:
                # Check Admin
                cur.execute("SELECT * FROM Admin WHERE username=? AND password=?", (username, password))
                row = cur.fetchone()
                if row:
                    role = "Admin"
                    roleID = row[0]

        if role != "":
            # Save login log
            date = "18-01-2026"
            time = "16:22"

            try:
                cur.execute(
                    "INSERT INTO LoginLogs (username, roleID, date, time) VALUES (?,?,?,?)", (username, roleID, date, time))
                conn.commit()
            except:
                pass
            conn.close()
            new2(role, roleID)
            newScreen1.destroy()
        else:
            print("Login failed")
            conn.close()

    tk.Button(newScreen1, text="Login", command= submit_login).pack(pady=20)



# -------- DASHBOARDS --------
def insert_menu_items():
        conn = sqlite3.connect("ElAziz.db")
        cur = conn.cursor()

        # Connect to the database and retrieve all menu items ordered by category and name
        cur.execute("SELECT COUNT(*) FROM Menu")
        if cur.fetchone()[0] == 0:
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

            cur.executemany(
                "INSERT INTO Menu (itemName, itemCategory, itemPrice, itemDescription) VALUES (?,?,?,?)",
                menu_items
            )
            conn.commit()
        conn.close()

# Seperate subroutine to create the dashboard window.
def new2(role, roleID):
    dashboard = tk.Toplevel(root)
    dashboard.title("El Aziz")
    dashboard.geometry("600x400")

    tk.Label(
        dashboard,
        text="Welcome to your dashboard!",
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
    ).pack(pady=20)

# --- CUSTOMER FUNCTIONS ---
    def browse_menu():
    # Opens a new window showing all menu items, grouped by category
        menu_window = tk.Toplevel(dashboard)
        menu_window.title("El Aziz")
        menu_window.geometry("600x600")

        tk.Label(
            menu_window,
            text="Welcome to El Aziz's Menu",
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
        ).pack(pady=20)
         
        # Container to centre everything
        container = tk.Frame(menu_window)
        container.pack(expand=True)

        # Connect to the database and retrieve all menu items ordered by category and name
        conn = sqlite3.connect("ElAziz.db")
        cur = conn.cursor()
        cur.execute("""
        SELECT itemCategory, itemName, itemPrice, itemDescription
        FROM Menu
        ORDER BY itemCategory, itemName
        """)
        all_items = cur.fetchall() # Retrieve all menu records
        conn.close()

        current_category = None

        # Display each menu item in the GUI
        for category, name, price, desc in all_items:
            if category != current_category:
                current_category = category
                tk.Label(container, text=category, font=("Arial", 16, "bold")).pack(pady=(15,5))

            # Display the item name and price
            tk.Label(container, text=f"{name} - ${price:.2f}", font=("Arial", 11, "bold")).pack()
            # Display the item description below the name
            tk.Label(container, text=desc, font=("Arial", 9), fg="gray").pack(pady=(0, 8))

        conn.commit()
        conn.close()
        
        
    def create_order():
    # Allows customers to select items and quantities, calculates total, and stores order in database
    # Opens a new window to allow the customer to select menu items and place an order
        order_window = tk.Toplevel(dashboard)
        order_window.title("El Aziz")
        order_window.geometry("500x500")

        # Heading to display 'Create Order' 
        tk.Label(
            order_window,
            text="Create Order",
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
            ).pack(pady=20)

        # Retrieve menu items from database
        conn = sqlite3.connect("ElAziz.db")
        cur = conn.cursor()
        cur.execute("SELECT menuItemID, itemName, itemPrice FROM Menu")
        menu_items = cur.fetchall()
        conn.close()

        # Track the users chocies/selections and the quantities specified
        selections = {}
        quantities = {}
        total_var = tk.DoubleVar(value=0.0)

        # Function to calculate the total price whenever an item or quantity changes
        def update_total():
            total = 0
            for item_id in selections:
                if selections[item_id].get() == 1: # Check if item is selected
                    try:
                        qty = int(quantities[item_id].get()) # Get the quantity specified
                    except:
                        qty = 0
                    total += qty * menu_items[item_id-1][2] # Multiply by item price
            total_var.set(total) # Update total displayed in the GUI

        # Submit the order to the database
        def submit_order():
            order_items = []
            for item_id in selections:
                if selections[item_id].get() == 1:
                    qty = int(quantities[item_id].get())
                    order_items.append(f"{menu_items[item_id-1][1]} x{qty}")

            # Insert the order into the Orders table
            conn = sqlite3.connect("ElAziz.db")
            cur = conn.cursor()
            cur.execute("INSERT INTO Orders (customerID, menuItem, quantity, totalPrice) VALUES (?,?,?,?)",
                        (roleID, ", ".join(order_items), total, total_var.get()))
            conn.commit()
            conn.close()
            order_window.destroy()  # Close order window after submission
            print(f"Order placed! Total: ${total_var.get()}")

        # Create checkboxes and quantity entries for each menu item
        for item in menu_items:
            selections[item[0]] = tk.IntVar()
            quantities[item[0]] = tk.StringVar(value="0")
            tk.Checkbutton(order_window, text=f"{item[1]} - ${item[2]}", variable=selections[item[0]], command=update_total).pack(anchor="w")
            tk.Entry(order_window, textvariable=quantities[item[0]], width=5).pack(anchor="w")

        # Display the dynamic total and submit button
        tk.Label(order_window, textvariable=total_var, font=("Arial",14,"bold")).pack(pady=10)
        tk.Button(order_window, text="Submit Order", command=submit_order).pack(pady=5)

        

    def create_reservation():
    # Allows customers to book tables, specifying date, time, and special requests
    # Opens a new window for customers to make a table reservation
        reservation_window = tk.Toplevel(dashboard)
        reservation_window.title("El Aziz")
        reservation_window.geometry("500x500")

        # Display heading to say 'Create Reservation' 
        tk.Label(
        reservation_window,
        text="Create Reservation",
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
    ).pack(pady=20)

        # Tkinter variables to store inputs
        customerID_var = tk.StringVar()
        date_var = tk.StringVar()
        time_var = tk.StringVar()
        guests_var = tk.StringVar()
        special_var = tk.StringVar()

        # Create fields of entry for each field. 
        tk.Label(reservation_window, text="Customer ID").pack()
        tk.Entry(reservation_window, textvariable=customerID_var).pack()
        tk.Label(reservation_window, text="Date (DD/MM/YYYY)").pack()
        tk.Entry(reservation_window, textvariable=date_var).pack()
        tk.Label(reservation_window, text="Time (HH:MM)").pack()
        tk.Entry(reservation_window, textvariable=time_var).pack()
        tk.Label(reservation_window, text="Number of Guests").pack()
        tk.Entry(reservation_window, textvariable=guests_var).pack()
        tk.Label(reservation_window, text="Special Requests").pack()
        tk.Entry(reservation_window, textvariable=special_var).pack()


        # Function to insert the reservation into the database
        def submit_reservation():
             # Retrieve menu items from the database
            conn = sqlite3.connect("ElAziz.db")
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO Reservations (customerID, reservationDate, reservationTime, numOfGuests, specialRequest)
                VALUES (?,?,?,?,?)
            """, (customerID_var.get(), date_var.get(), time_var.get(), guests_var.get(), special_var.get()))
            conn.commit()
            conn.close()
            reservation_window.destroy()  # Close Window
            print("Reservation made!")

        tk.Button(reservation_window, text="Submit Reservation", command=submit_reservation).pack(pady=10)

    def view_orders_reservations():
    # Displays all previous orders and reservations for the customer
    # Opens a new window to display all orders and reservations for the customer
        view_window = tk.Toplevel(dashboard)
        view_window.title("El Aziz")
        view_window.geometry("600x400")

         # Heading to dsiplay 'View Orders & Reservations'  
        tk.Label(
        view_window,
        text="View Orders & Reservations",
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
    ).pack(pady=20)

        # Connect to database
        conn = sqlite3.connect("ElAziz.db")
        cur = conn.cursor()

        # Retrieve all orders from the customer
        cur.execute("SELECT orderID, items, total FROM Orders WHERE customerID=?", (roleID,))
        orders = cur.fetchall()

        # Retrieve all reservations from the customer
        cur.execute("SELECT reservationID, reservationDate, reservationTime, numOfGuests, specialRequest FROM Reservations WHERE customerID=?", (roleID,))
        reservations = cur.fetchall()

        conn.close()

        # Display orders section
        tk.Label(view_window, text="Orders", font=("Arial",14,"bold")).pack(pady=5)
        if orders:
            for order in orders:
                    tk.Label(view_window, text=f"Order ID: {order[0]}").pack(anchor="w", padx=10)
                    tk.Label(view_window, text=f"Items: {order[1]}").pack(anchor="w", padx=20)
                    tk.Label(view_window, text=f"Total: ${order[2]:.2f}").pack(anchor="w", padx=20)
                    tk.Label(view_window, text="").pack()
        else:
            tk.Label(view_window, text="No orders found").pack(pady=5)

        # Display reservation section
        tk.Label(view_window, text="Reservations", font=("Arial",14,"bold")).pack(pady=5)
        if reservations:
            for res in reservations:
                tk.Label(view_window, text=f"Reservation ID: {res[0]}").pack(anchor="w", padx=10)
                tk.Label(view_window, text=f"Date: {res[1]}, Time: {res[2]}").pack(anchor="w", padx=20)
                tk.Label(view_window, text=f"Guests: {res[3]}").pack(anchor="w", padx=20)
                tk.Label(view_window, text=f"Special Request: {res[4]}").pack(anchor="w", padx=20)
                tk.Label(view_window, text="").pack()
        else:
            tk.Label(view_window, text="No reservations found").pack(pady=5)

                  
    def manage_account():
    # Displays the customer's account details, retreived from the database
    # Connect to the database and retrieve account info based on user role
      conn = sqlite3.connect("ElAziz.db")
      cur = conn.cursor()

      # Select based on role
      if role == "Customer":
        cur.execute("SELECT * FROM Customers WHERE customerID=?", (roleID,))
      elif role == "Staff":
        cur.execute("SELECT * FROM Staff WHERE staffID=?", (roleID,))
      elif role == "Admin":
        cur.execute("SELECT * FROM Admin WHERE adminID=?", (roleID,))

      data = cur.fetchone() # Retrieve user account data
      conn.close()

      # Open a new window to display account info
      account_window = tk.Toplevel(dashboard)
      account_window.title("El Aziz")
      account_window.geometry("400x300")

      if data:
        # Display each field manually
        tk.Label(account_window, text="ID: " + str(data[0])).pack(anchor="w", padx=10, pady=2)
        tk.Label(account_window, text="First Name: " + str(data[1])).pack(anchor="w", padx=10, pady=2)
        tk.Label(account_window, text="Surname: " + str(data[2])).pack(anchor="w", padx=10, pady=2)
        tk.Label(account_window, text="Email: " + str(data[3])).pack(anchor="w", padx=10, pady=2)
        tk.Label(account_window, text="Phone: " + str(data[4])).pack(anchor="w", padx=10, pady=2)
        tk.Label(account_window, text="Username: " + str(data[5])).pack(anchor="w", padx=10, pady=2)
        tk.Label(account_window, text="Password: " + str(data[6])).pack(anchor="w", padx=10, pady=2)
      else:
        tk.Label(account_window, text="No account data found").pack(pady=20)


    # --- STAFF FUNCTIONS ---
    
    def view_shifts():
    # Placeholder to view staff shifts
        print("View Shifts clicked")

    def view_databases():
    # Placeholder to view database tables and their contents
        print("View Databases clicked")

    def view_active_orders():
    # Placeholder to manage/view customer orders and reservations
        print("View Orders/Reservations clicked")

    # --- ADMIN FUNCTIONS ---
    
    def order_new_stock():
    # Placeholder for admin to order stock for restaurants
        print("Order New Stock clicked")

    def view_reports_analytics():
    # Placeholder to view sales and performance analytics
        print("Reports & Analytics clicked")

    def manage_accounts():
    # Placeholder for admin to manage all user account
        print("Manage Accounts clicked")

    # --- CUSTOMER DASHBOARD ---
    if role == "Customer":
        tk.Button(dashboard, text='Browse Menu', width=25, height=2, command=browse_menu).pack(pady=5)
        tk.Button(dashboard, text='Create Order', width=25, height=2, command=create_order).pack(pady=5)
        tk.Button(dashboard, text='Create Reservation', width=25, height=2, command=create_reservation).pack(pady=5)
        tk.Button(dashboard, text='View Orders/Reservations', width=25, height=2, command=view_orders_reservations).pack(pady=5)
        tk.Button(dashboard, text='Manage Account', width=25, height=2, command=manage_account).pack(pady=5)

    # --- STAFF DASHBOARD ---
    elif role == "Staff":
        tk.Button(dashboard, text='View Shifts', width=25, height=2, command=view_shifts).pack(pady=5)
        tk.Button(dashboard, text='View Databases', width=25, height=2, command=view_databases).pack(pady=5)
        tk.Button(dashboard, text='View Orders/Reservations', width=25, height=2, command=view_active_orders).pack(pady=5)
        tk.Button(dashboard, text='Manage Account', width=25, height=2, command=manage_account).pack(pady=5)

    # --- ADMIN DASHBOARD ---
    elif role == "Admin":
        tk.Button(dashboard, text='View Shifts', width=25, height=2, command=view_shifts).pack(pady=5)
        tk.Button(dashboard, text='View Databases', width=25, height=2, command=view_databases).pack(pady=5)
        tk.Button(dashboard, text='Order New Stock', width=25, height=2, command=order_new_stock).pack(pady=5)
        tk.Button(dashboard, text='Reports & Analytics', width=25, height=2, command=view_reports_analytics).pack(pady=5)
        tk.Button(dashboard, text='Manage Accounts', width=25, height=2, command=manage_accounts).pack(pady=5)



# -------- MAIN WINDOW --------
root = tk.Tk()
root.title("El Aziz")
root.geometry('600x400')

# --- HEADER LABEL ---
textVarHeader = tk.StringVar(value="Welcome to El Aziz!")

label = tk.Label(
    root,
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
label.pack(pady=20)

# --- CONTACT INFORMATION ---
textVarContact = tk.StringVar(value=
    "Contact Us:\n"
    "elazizservices@gmail.com\n"
    "+998 93-945-86-91"
)

label2 = tk.Label(
    root,
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
label2.pack(pady=10)

# --- BUTTONS ---
btn_create = ttk.Button(root, text='Create an Account', command=new)
btn_create.pack(pady=10)

btn_login = ttk.Button(root, text='Login', command=new1)
btn_login.pack(pady=10)



# --- START APPLICATION ---
create_database()
insert_menu_items()
root.mainloop()
