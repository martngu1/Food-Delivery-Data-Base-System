import streamlit as st
import sqlite3
import pandas as pd  # ✅ Make sure pandas is imported

st.set_page_config(page_title="Orders", page_icon="🧾")
st.title("🧾 Orders Management")

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

# --- CREATE ---
with st.expander(" ➕ Create New Order"):
    # Fetch users and restaurants
    cursor.execute("SELECT user_id, name FROM Users")
    users = {f"{name} (ID {uid})": uid for uid, name in cursor.fetchall()}
    selected_user = st.selectbox("Select User", list(users.keys()), key="order_user")

    cursor.execute("SELECT restaurant_id, name FROM Restaurants")
    restaurants = {f"{name} (ID {rid})": rid for rid, name in cursor.fetchall()}
    selected_restaurant = st.selectbox("Select Restaurant", list(restaurants.keys()), key="order_rest")

    # Fetch menu items for the selected restaurant
    rest_id = restaurants[selected_restaurant]
    cursor.execute("SELECT menu_id, item_name, price FROM Menu WHERE restaurant_id = ?", (rest_id,))
    menu_items = cursor.fetchall()

    with st.form("create_new_order"):
        st.write("### Select Items and Quantity")
        order_items = []
        total_amount = 0

        for menu_id, item_name, price in menu_items:
            qty = st.number_input(
                f"{item_name} ({price:.2f} kr)", min_value=0, step=1, key=f"qty_{menu_id}"
            )
            if qty > 0:
                order_items.append((menu_id, qty, price))
                total_amount += qty * price

        st.markdown(f"**Total Order Amount: {total_amount:.2f} kr**")
        submit_button = st.form_submit_button("Place Order")

        if submit_button:
            if len(order_items) == 0:
                st.warning("Please select at least one item to place an order.")
            else:
                user_id = users[selected_user]
                cursor.execute(
                    "INSERT INTO Orders (user_id, restaurant_id, order_total, delivery_status) VALUES (?, ?, ?, ?)",
                    (user_id, rest_id, total_amount, "Processing")
                )
                order_id = cursor.lastrowid

                for menu_id, qty, _ in order_items:
                    cursor.execute(
                        "INSERT INTO Order_Items (order_id, menu_id, quantity) VALUES (?, ?, ?)",
                        (order_id, menu_id, qty)
                    )
                conn.commit()
                st.success(f"✅ Order placed successfully! Total: {total_amount:.2f} kr")

# --- READ ---
with st.expander("View All Orders"):
    cursor.execute("""
        SELECT 
            Orders.order_id, 
            Users.name AS user_name, 
            Restaurants.name AS restaurant_name, 
            Orders.order_total, 
            Orders.delivery_status
        FROM Orders
        JOIN Users ON Orders.user_id = Users.user_id
        JOIN Restaurants ON Orders.restaurant_id = Restaurants.restaurant_id
    """)    
    orders = cursor.fetchall()

    if orders:
        df_orders = pd.DataFrame(orders, columns=["Order ID", "User", "Restaurant", "Total (kr)", "Status"])
        st.dataframe(df_orders, use_container_width=True)
    else:
        st.info("No orders found.")

# --- UPDATE ---
with st.expander("Update Order Status"):
    cursor.execute("SELECT order_id, delivery_status FROM Orders")
    orders = cursor.fetchall()

    if orders:
        order_options = {f"Order ID {oid} - {status}": oid for oid, status in orders}
        selected_order = st.selectbox("Select Order to Update", list(order_options.keys()), key="update_order")

        new_status = st.selectbox("Select New Status", ["Processing", "On the way", "Delivered", "Cancelled"], key="new_status")

        if st.button("Update Status"):
            order_id = order_options[selected_order]
            cursor.execute(
                "UPDATE Orders SET delivery_status = ? WHERE order_id = ?",
                (new_status, order_id)
            )
            conn.commit()
            st.success(f"✅ Order {order_id} status updated to {new_status}!")

    else:
        st.info("No orders to update.")

# --- DELETE ---
with st.expander("🗑️ Delete Order"):
    cursor.execute("SELECT order_id FROM Orders")
    orders = cursor.fetchall()

    if orders:
        order_options = {f"Order ID {oid}": oid for oid, in orders}
        selected_order = st.selectbox("Select Order to Delete", list(order_options.keys()), key="delete_order")

        if st.button("Delete Order"):
            order_id = order_options[selected_order]
            cursor.execute("DELETE FROM Order_Items WHERE order_id = ?", (order_id,))
            cursor.execute("DELETE FROM Orders WHERE order_id = ?", (order_id,))
            conn.commit()
            st.success(f"🗑️ Order {order_id} deleted successfully!")

    else:
        st.info("No orders to delete.")