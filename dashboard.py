import streamlit as st
import pandas as pd
import plotly.express as px
from database_setup import SalesRecord, Session

def admin_dashboard():
    st.title("Admin Dashboard")

    # Submit Sales Data
    with st.form("sales_form"):
        date = st.date_input("Date")
        outlet_name = st.text_input("Outlet Name")
        address = st.text_input("Address")
        owner_name = st.text_input("Owner Name")
        contact_number = st.text_input("Contact Number")
        gstin_un = st.text_input("GSTIN/UN")
        products_ordered = st.text_input("Products Ordered")
        quantity = st.number_input("Quantity", min_value=1)
        order_value = st.number_input("Order Value", min_value=0.0)
        distributor_id = st.number_input("Distributor ID", min_value=1)
        submitted = st.form_submit_button("Submit")

        if submitted:
            session = Session()
            new_sale = SalesRecord(
                date=date, outlet_name=outlet_name, address=address,
                owner_name=owner_name, contact_number=contact_number,
                gstin_un=gstin_un, products_ordered=products_ordered,
                quantity=quantity, order_value=order_value,
                distributor_id=distributor_id
            )
            session.add(new_sale)
            session.commit()
            session.close()
            st.success("Sales record added!")

    # View Sales Insights
    st.header("Sales Insights")
    session = Session()
    sales_data = pd.read_sql(session.query(SalesRecord).statement, session.bind)
    session.close()

    if not sales_data.empty:
        st.write(sales_data)

        # Total Sales
        total_sales = sales_data['order_value'].sum()
        st.metric("Total Sales", f"₹{total_sales:,.2f}")

        # Sales by Date Range
        date_range = st.date_input("Select Date Range", [])
        if len(date_range) == 2:
            filtered_data = sales_data[(sales_data['date'] >= date_range[0]) & (sales_data['date'] <= date_range[1])]
            st.write(filtered_data)

        # Product Performance
        product_performance = sales_data.groupby('products_ordered')['quantity'].sum().reset_index()
        fig = px.bar(product_performance, x='products_ordered', y='quantity', title="Product Performance")
        st.plotly_chart(fig)
