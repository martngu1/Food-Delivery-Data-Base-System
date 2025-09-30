import sqlite3

# Opprett tilkobling til SQLite-database
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Slett gamle tabeller hvis de finnes (for testing)
tables = [
    "Rating", "Payment", "Order_Items", "Orders", "Menu", 
    "Restaurants", "Drivers", "Address", "Users"
]
for table in tables:
    cursor.execute(f"DROP TABLE IF EXISTS {table}")

# Opprett tabeller
cursor.execute("""
CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    phone TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE Address (
    address_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    state TEXT,
    city TEXT,
    street TEXT,
    pincode INTEGER,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
)
""")

cursor.execute("""
CREATE TABLE Restaurants (
    restaurant_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    phone TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE Menu (
    menu_id INTEGER PRIMARY KEY AUTOINCREMENT,
    restaurant_id INTEGER,
    item_name TEXT,
    price REAL,
    FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id)
)
""")

cursor.execute("""
CREATE TABLE Drivers (
    driver_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT,
    location TEXT,
    email TEXT
)
""")

cursor.execute("""
CREATE TABLE Orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    restaurant_id INTEGER,
    order_total REAL,
    delivery_status TEXT,
    driver_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id),
    FOREIGN KEY (driver_id) REFERENCES Drivers(driver_id)
)
""")

cursor.execute("""
CREATE TABLE Order_Items (
    order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    menu_id INTEGER,
    quantity INTEGER,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (menu_id) REFERENCES Menu(menu_id)
)
""")

cursor.execute("""
CREATE TABLE Payment (
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    payment_method TEXT,
    amount REAL,
    status TEXT,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id)
)
""")

cursor.execute("""
CREATE TABLE Rating (
    rating_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    restaurant_id INTEGER,
    rating INTEGER,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id)
)
""")

# Eksempeldata – brukere, restauranter, meny
cursor.execute("INSERT INTO Users (name, email, password, phone) VALUES ('Ali Hasan', 'ali@example.com', 'pass123', '12345678')")
cursor.execute("INSERT INTO Users (name, email, password, phone) VALUES ('Sara Noor', 'sara@example.com', 'pass456', '87654321')")

cursor.execute("INSERT INTO Restaurants (name, address, phone) VALUES ('Pasta Palace', 'Main Street 1', '11111111')")
cursor.execute("INSERT INTO Restaurants (name, address, phone) VALUES ('Burger Bros', 'Side Avenue 5', '22222222')")

cursor.execute("INSERT INTO Menu (restaurant_id, item_name, price) VALUES (1, 'Spaghetti Bolognese', 129.90)")
cursor.execute("INSERT INTO Menu (restaurant_id, item_name, price) VALUES (2, 'Cheeseburger', 89.50)")

cursor.execute("INSERT INTO Drivers (name, phone, location, email) VALUES ('Ola Nordmann', '99999999', 'Trondheim', 'ola@driver.com')")

cursor.execute("INSERT INTO Orders (user_id, restaurant_id, order_total, delivery_status, driver_id) VALUES (1, 1, 129.90, 'Delivered', 1)")
cursor.execute("INSERT INTO Order_Items (order_id, menu_id, quantity) VALUES (1, 1, 1)")

cursor.execute("INSERT INTO Payment (order_id, payment_method, amount, status) VALUES (1, 'Card', 129.90, 'Paid')")
cursor.execute("INSERT INTO Rating (user_id, restaurant_id, rating) VALUES (1, 1, 5)")

# Lagre og lukk
conn.commit()
conn.close()

print(" Databaseoppsett fullført og fylt med eksempeldata!")
