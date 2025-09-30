##  Logical Model (Relational Schema)

```sql
Users(
    user_id INT PK,
    name VARCHAR(255),
    email VARCHAR(255),
    password VARCHAR(255),
    phone VARCHAR(20)
)

Address(
    address_id INT PK,
    user_id INT FK REFERENCES Users(user_id),
    state VARCHAR(255),
    city VARCHAR(255),
    street VARCHAR(255),
    pincode INT
)

Restaurants(
    restaurant_id INT PK,
    name VARCHAR(255),
    address VARCHAR(255),
    phone VARCHAR(20)
)

Menu(
    menu_id INT PK,
    restaurant_id INT FK REFERENCES Restaurants(restaurant_id),
    item_name VARCHAR(255),
    price DECIMAL(10,2)
)

Orders(
    order_id INT PK,
    user_id INT FK REFERENCES Users(user_id),
    restaurant_id INT FK REFERENCES Restaurants(restaurant_id),
    order_total DECIMAL(10,2),
    delivery_status VARCHAR(20),
    driver_id INT FK REFERENCES Drivers(driver_id)
)

Order_Items(
    order_item_id INT PK,
    order_id INT FK REFERENCES Orders(order_id),
    menu_id INT FK REFERENCES Menu(menu_id),
    quantity INT
)

Drivers(
    driver_id INT PK,
    name VARCHAR(255),
    phone VARCHAR(20),
    location VARCHAR(255),
    email VARCHAR(255)
)

Payment(
    payment_id INT PK,
    order_id INT FK REFERENCES Orders(order_id),
    payment_method VARCHAR(20),
    amount DECIMAL(10,2),
    status VARCHAR(20)
)

Rating(
    rating_id INT PK,
    user_id INT FK REFERENCES Users(user_id),
    restaurant_id INT FK REFERENCES Restaurants(restaurant_id),
    rating INT
)
