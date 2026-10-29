import streamlit as st
st.set_page_config(page_title="Retail Sales Analytics",page_icon="📊",layout="wide")

import pandas as pd
st.title("Retail Sales Analytics Dashboard")

df = pd.read_csv("retail_sales_dataset (1) - retail_sales_dataset (1).csv")

df["date"] = pd.to_datetime(df["date"],errors="coerce")

st.sidebar.header("Filter Options")
selected_region = st.sidebar.selectbox("Select Region",["All"]+sorted(df["region"].dropna().unique().tolist()))

st.sidebar.subheader("Date Filter")
valid_dates = df["date"].dropna()
if not valid_dates.empty:
    min_date = valid_dates.min().date()
    max_date = valid_dates.max().date()

    start_date = st.sidebar.date_input("Start Date",value=min_date,min_value=min_date,max_value=max_date)
    end_date = st.sidebar.date_input("End Date",value=max_date,min_value=min_date,max_value=max_date)


if selected_region == "All":
    filtered_df = df
else:
    filtered_df = df[df["region"] == selected_region]

if start_date <= end_date:
    filtered_df = filtered_df[(filtered_df["date"].dt.date >= start_date) & (filtered_df["date"].dt.date <= end_date)]
else:
    st.sidebar.error("Start date must be before end date.")
    filtered_df = filtered_df.iloc[0:0]


total_revenue = filtered_df["revenue"].sum()
total_units = filtered_df["units_sold"].sum()

st.subheader("Business Overview")
col1,col2 = st.columns(2)
col1.metric("Total Revenue",f"{total_revenue:,.2f}")
col2.metric("Total Units_Sold",f"{total_units:,.0f}")
st.write(df.columns.tolist())

st.subheader("Top 5 Products by Revenue")
product_revenue = filtered_df.groupby("product")["revenue"].sum()
top_5_products = product_revenue.sort_values(ascending=False).head(5)
st.bar_chart(top_5_products)
st.title("📊 Retail Sales Analytics Dashboard")

st.markdown("Explore sales performance,compare regions," "analyse product revenue,and download filtered data.")

st.subheader("Filtered Sales Dataset")
st.dataframe(filtered_df)
st.subheader("Revenue by Category")
category_revenue = filtered_df.groupby("category")["revenue"].sum()
st.bar_chart(category_revenue)

st.subheader("Download Filtered Data")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(label="Download CSV",data=csv,file_name="filtered_sales_data.csv",mime="text/csv")
