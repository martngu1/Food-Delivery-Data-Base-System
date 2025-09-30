# pages/3_Menu.py
import streamlit as st
import sqlite3

# Må være først
st.set_page_config(page_title="Manage Menu", page_icon="🌮", layout="centered")

st.title("🌮 Menu Administration")

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

# --- CREATE ---
with st.expander(" ➕ Add New Menu Item"):
    with st.form("create_menu_item"):
        cursor.execute("SELECT restaurant_id, name FROM Restaurants")
        restaurant_options = cursor.fetchall()

        rest_dict = {f"{name} (ID {rid})": rid for rid, name in restaurant_options}
        selected_restaurant = st.selectbox("Select Restaurant", list(rest_dict.keys()), key="menu_create_rest")

        item_name = st.text_input("Menu Item Name", key="menu_item_name_create")
        price = st.number_input("Price (kr)", min_value=0.0, format="%.2f", key="menu_item_price_create")

        submitted = st.form_submit_button("Add Menu Item")
        if submitted:
            rest_id = rest_dict[selected_restaurant]
            cursor.execute(
                "INSERT INTO Menu (restaurant_id, item_name, price) VALUES (?, ?, ?)",
                (rest_id, item_name, price)
            )
            conn.commit()
            st.success(" Menu item added!")

# --- READ ---
with st.expander(" View All Menu Items"):
    cursor.execute("""
        SELECT Menu.menu_id, Restaurants.name, Menu.item_name, Menu.price
        FROM Menu
        JOIN Restaurants ON Menu.restaurant_id = Restaurants.restaurant_id
    """)
    menu_items = cursor.fetchall()
    if menu_items:
        st.dataframe(menu_items, use_container_width=True)
    else:
        st.info("No menu items found.")

# --- UPDATE ---
with st.expander(" Update Menu Item"):
    cursor.execute("SELECT menu_id, item_name FROM Menu")
    menu_options = cursor.fetchall()

    if menu_options:
        menu_dict = {f"{name} (ID {mid})": mid for mid, name in menu_options}
        selected_menu = st.selectbox("Select Menu Item", list(menu_dict.keys()), key="menu_update_select")

        new_name = st.text_input("New Item Name", key="menu_item_name_update")
        new_price = st.number_input("New Price (kr)", min_value=0.0, format="%.2f", key="menu_item_price_update")

        if st.button("Update Menu Item"):
            menu_id = menu_dict[selected_menu]
            cursor.execute(
                "UPDATE Menu SET item_name = ?, price = ? WHERE menu_id = ?",
                (new_name, new_price, menu_id)
            )
            conn.commit()
            st.success(" Menu item updated!")
    else:
        st.warning("No menu items available to update.")

# --- DELETE ---
with st.expander("🗑️ Delete Menu Item"):
    if menu_options:
        selected_del = st.selectbox("Select Menu Item to delete", list(menu_dict.keys()), key="menu_delete_select")
        if st.button("Delete Menu Item"):
            menu_id = menu_dict[selected_del]
            cursor.execute("DELETE FROM Menu WHERE menu_id = ?", (menu_id,))
            conn.commit()
            st.warning("🗑️ Menu item deleted!")
    else:
        st.warning("No menu items available to delete.")

# Lukk tilkobling til database
conn.close()
