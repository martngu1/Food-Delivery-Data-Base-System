# users.py
import streamlit as st
import sqlite3

# Page setup
st.set_page_config(page_title="Manage Users", page_icon="➕", layout="centered")
st.title("➕ User Management")

# Connect to SQLite database
conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

# CREATE
with st.expander("➕ Add New User"):
    with st.form("create_user_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        phone = st.text_input("Phone")
        submitted = st.form_submit_button("Add User")
        if submitted:
            try:
                cursor.execute("INSERT INTO Users (name, email, password, phone) VALUES (?, ?, ?, ?)",
                               (name, email, password, phone))
                conn.commit()
                st.success("User added successfully!")
            except sqlite3.IntegrityError:
                st.error("Email is already in use!")

# READ
with st.expander(" View All Users"):
    cursor.execute("SELECT * FROM Users")
    users = cursor.fetchall()
    if users:
        st.dataframe(users, use_container_width=True)
    else:
        st.info("No users found.")

# UPDATE
with st.expander(" Update User"):
    cursor.execute("SELECT user_id, name FROM Users")
    user_options = cursor.fetchall()
    if user_options:
        user_dict = {f"{name} (ID {uid})": uid for uid, name in user_options}
        selected_user = st.selectbox("Select user", list(user_dict.keys()), key="user_update")
        new_name = st.text_input("New Name", key="user_name_update")
        if st.button("Update User"):
            user_id = user_dict[selected_user]
            cursor.execute("UPDATE Users SET name = ? WHERE user_id = ?", (new_name, user_id))
            conn.commit()
            st.success("User updated successfully!")
    else:
        st.warning("No users to update.")

# DELETE
with st.expander("🗑️ Delete User"):
    if user_options:
        selected_del = st.selectbox("Select user to delete", list(user_dict.keys()), key="user_delete")
        if st.button("Delete User"):
            user_id = user_dict[selected_del]
            cursor.execute("DELETE FROM Users WHERE user_id = ?", (user_id,))
            conn.commit()
            st.warning("User deleted!")
    else:
        st.warning("No users to delete.")

conn.close()
