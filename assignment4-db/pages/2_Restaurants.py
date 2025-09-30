# pages/2_Restaurants.py
import streamlit as st
import sqlite3


st.set_page_config(page_title="Manage Restaurants", page_icon="🍽️", layout="centered")

# Sideoverskrift
st.title("🥪 Restaurant Administration")

# Tilkobling til database
conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

# --- CREATE ---
with st.expander("➕ Add New Restaurant"):
    with st.form("create_restaurant"):
        r_name = st.text_input("Restaurant Name 🍽️")
        r_address = st.text_input("Address 📍")
        r_phone = st.text_input("Phone 📞")
        r_submit = st.form_submit_button("Add Restaurant")
        if r_submit:
            cursor.execute(
                "INSERT INTO Restaurants (name, address, phone) VALUES (?, ?, ?)",
                (r_name, r_address, r_phone)
            )
            conn.commit()
            st.success(" Restaurant added!")

# --- READ ---
with st.expander(" View Existing Restaurants"):
    cursor.execute("SELECT * FROM Restaurants")
    restaurants = cursor.fetchall()
    if restaurants:
        st.dataframe(restaurants, use_container_width=True)
    else:
        st.info("No restaurants found.")

# --- UPDATE ---
with st.expander(" Update Restaurant"):
    if restaurants:
        r_ids = [str(row[0]) for row in restaurants]
        selected_rid = st.selectbox("Select Restaurant ID", r_ids, key="restaurant_update_select")
        new_rname = st.text_input("New Name", key="restaurant_name_update")
        new_raddress = st.text_input("New Address", key="restaurant_address_update")
        if st.button("Update Restaurant"):
            cursor.execute(
                "UPDATE Restaurants SET name = ?, address = ? WHERE restaurant_id = ?",
                (new_rname, new_raddress, selected_rid)
            )
            conn.commit()
            st.success(" Restaurant updated!")
    else:
        st.warning("No restaurants available to update.")

# --- DELETE ---
with st.expander("🗑️ Delete Restaurant"):
    if restaurants:
        del_rid = st.selectbox("Select Restaurant ID to delete", r_ids, key="delete_restaurant")
        if st.button("Delete Restaurant"):
            cursor.execute("DELETE FROM Restaurants WHERE restaurant_id = ?", (del_rid,))
            conn.commit()
            st.warning("🗑️ Restaurant deleted!")
    else:
        st.warning("No restaurants available to delete.")

# Lukk databasetilkoblingen
conn.close()
