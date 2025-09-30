##  Data Dictionary for Food Delivery App

---

###  Table: `Users`

| Column Name | Data Type     | Description                  |
|-------------|---------------|------------------------------|
| user_id     | INT (PK)      | Unique ID for the user       |
| name        | VARCHAR(255)  | User's full name             |
| email       | VARCHAR(255)  | User's email address         |
| password    | VARCHAR(255)  | User's hashed password       |
| phone       | VARCHAR(20)   | User's phone number          |

---

###  Table: `Address`

| Column Name | Data Type     | Description                  |
|-------------|---------------|------------------------------|
| address_id  | INT (PK)      | Unique ID for the address    |
| user_id     | INT (FK)      | Reference to the user        |
| state       | VARCHAR(255)  | State                        |
| city        | VARCHAR(255)  | City                         |
| street      | VARCHAR(255)  | Street address               |
| pincode     | INT           | Postal code                  |

---

###  Table: `Restaurants`

| Column Name   | Data Type     | Description                    |
|---------------|---------------|--------------------------------|
| restaurant_id | INT (PK)      | Unique ID for the restaurant   |
| name          | VARCHAR(255)  | Restaurant name                |
| address       | VARCHAR(255)  | Restaurant address             |
| phone         | VARCHAR(20)   | Restaurant phone number        |

---

###  Table: `Menu`

| Column Name   | Data Type     | Description                     |
|---------------|---------------|---------------------------------|
| menu_id       | INT (PK)      | Unique ID for the menu item     |
| restaurant_id | INT (FK)      | Reference to the restaurant     |
| item_name     | VARCHAR(255)  | Name of the menu item           |
| price         | DECIMAL(10,2) | Price of the menu item          |

---

###  Table: `Orders`

| Column Name     | Data Type     | Description                            |
|------------------|---------------|----------------------------------------|
| order_id         | INT (PK)      | Unique ID for the order                |
| user_id          | INT (FK)      | Reference to the user who ordered      |
| restaurant_id    | INT (FK)      | Reference to the restaurant            |
| order_total      | DECIMAL(10,2) | Total price of the order               |
| delivery_status  | VARCHAR(20)   | Delivery status (pending, delivered)   |
| driver_id        | INT (FK)      | Reference to the driver                |

---

###  Table: `Order_Items`

| Column Name   | Data Type | Description                           |
|---------------|-----------|---------------------------------------|
| order_item_id | INT (PK)  | Unique ID for the order item          |
| order_id      | INT (FK)  | Reference to the order                |
| menu_id       | INT (FK)  | Reference to the menu item            |
| quantity      | INT       | Quantity of the item ordered          |

---

###  Table: `Drivers`

| Column Name | Data Type     | Description                |
|-------------|---------------|----------------------------|
| driver_id   | INT (PK)      | Unique ID for the driver   |
| name        | VARCHAR(255)  | Driver’s full name         |
| phone       | VARCHAR(20)   | Driver’s phone number      |
| location    | VARCHAR(255)  | Current location           |
| email       | VARCHAR(255)  | Driver’s email address     |

---

###  Table: `Payment`

| Column Name     | Data Type     | Description                         |
|------------------|---------------|-------------------------------------|
| payment_id       | INT (PK)      | Unique ID for the payment           |
| order_id         | INT (FK)      | Reference to the order              |
| payment_method   | VARCHAR(20)   | Method used (card, cash, etc.)      |
| amount           | DECIMAL(10,2) | Payment amount                      |
| status           | VARCHAR(20)   | Payment status (paid, pending, etc.)|

---

###  Table: `Rating`

| Column Name   | Data Type | Description                          |
|---------------|-----------|--------------------------------------|
| rating_id     | INT (PK)  | Unique ID for the rating             |
| user_id       | INT (FK)  | Reference to the user who rated      |
| restaurant_id | INT (FK)  | Reference to the rated restaurant    |
| rating        | INT       | Rating value (1–5 stars)             |
