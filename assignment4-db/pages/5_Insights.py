# pages/4_Insights.py
import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Insights", page_icon="📈", layout="centered")

# Sideoverskrift
st.title("Insights")

# Tilkobling til database
conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

query = """
SELECT R.name AS restaurant_name,
       COUNT(O.order_id) AS total_orders,
       AVG(O.order_total) AS avg_order_price
FROM Orders O
JOIN Restaurants R ON O.restaurant_id = R.restaurant_id
GROUP BY R.restaurant_id
"""
df = pd.read_sql_query(query, conn)

if df.empty:
    st.warning("No orders available in the database.")
else:
    # Total orders per restaurant
    fig1 = px.bar(df, x="restaurant_name", y="total_orders",
                title="Total Orders per Restaurant",
                labels={"restaurant_name": "Restaurant", "total_orders": "Total Orders"},
                color="total_orders", color_continuous_scale="Blues")
    st.plotly_chart(fig1, use_container_width=True)
    st.caption("This chart shows the total number of orders placed at each restaurant.")

    # Average order price per restaurant
    fig2 = px.bar(df, x="restaurant_name", y="avg_order_price",
                title="Average Order Price per Restaurant",
                labels={"restaurant_name": "Restaurant", "avg_order_price": "Avg Price (kr)"},
                color="avg_order_price", color_continuous_scale="Greens")
    st.plotly_chart(fig2, use_container_width=True)
    st.caption("This chart shows the average value of orders made at each restaurant.")

conn.close()