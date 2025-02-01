import streamlit as st
from database_setup import SalesRecord, Session

def distributor_view(distributor_id: int):
    st.title("Distributor Dashboard")

    session = Session()
    orders = session.query(SalesRecord).filter(SalesRecord.distributor_id == distributor_id).all()
    session.close()

    for order in orders:
        with st.expander(f"Order ID: {order.id} - {order.outlet_name}"):
            st.write(f"Products: {order.products_ordered}")
            st.write(f"Quantity: {order.quantity}")
            st.write(f"Order Value: ₹{order.order_value:,.2f}")

            payment_status = st.selectbox("Payment Status", ["Pending", "Done"], key=f"pay_{order.id}")
            delivery_status = st.selectbox("Delivery Status", ["Pending", "Done"], key=f"del_{order.id}")
            remarks = st.text_input("Remarks", key=f"rem_{order.id}")

            if st.button("Update", key=f"btn_{order.id}"):
                session = Session()
                order.payment_status = payment_status
                order.delivery_status = delivery_status
                order.remarks = remarks
                session.commit()
                session.close()
                st.success("Order updated!")
