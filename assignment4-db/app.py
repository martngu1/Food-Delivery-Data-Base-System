# app.py
import streamlit as st
import base64


st.set_page_config(page_title="Food Delivery Admin", page_icon="🍕", layout="centered")
st.markdown("""
    <style>
    .stApp {
        background-image: url('https://images.unsplash.com/photo-1606756797752-1af069bfa925');
        background-size: cover;
        background-position: center;
    }
    .block-container {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 2rem;
        border-radius: 15px;
    }
    </style>
""", unsafe_allow_html=True)

#  Bakgrunnsbilde-funksjon
def set_bg(image_file):
    with open(image_file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        .block-container {{
            background-color: rgba(255, 255, 255, 0.88);
            padding: 2rem;
            border-radius: 1rem;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.2);
        }}
        h1, h2, h3 {{
            color: #d62828;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

#  Bruk et bilde som ligger i mappen
set_bg("bg.jpg")  # sørg for at bg.jpg finnes i samme mappe!

#  App-innhold
st.markdown("""
<h1 style='text-align: center; font-size: 3rem;'>🍕 Food Delivery Admin Panel</h1>
<h4 style='text-align: center; color: #333;'>Delivering deliciousness, one click at a time.</h4>
<hr style="margin-top:2rem;margin-bottom:2rem;">
""", unsafe_allow_html=True)

st.markdown("""
### 👇 What can you manage?

- **Users** – register new customers, update their details, or remove them.
- **Restaurants** – manage restaurants and their contact details.
- **Menu** – add menu items and update prices.

---

🍴 This app is built using **Streamlit** and **SQLite**, with secure best practices such as parameterized SQL queries to prevent injection attacks.
""")
