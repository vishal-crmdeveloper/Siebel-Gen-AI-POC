import streamlit as st
import requests

# Configure the Streamlit page
st.set_page_config(page_title="Oracle Siebel x Gen AI", page_icon="⚡", layout="wide")

st.title("⚡ Oracle Siebel × Gen AI")
st.subheader("Order Summarization POC")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Order Details")
    order_id = st.text_input("Order ID", value="SBL-ORD-2026-0847")
    customer_name = st.text_input("Customer Name", value="Acme Corporation")
    order_date = st.date_input("Order Date")
    
    col_s, col_p, col_c = st.columns(3)
    with col_s:
        status = st.selectbox("Status", ["Open", "In Progress", "Complete", "Cancelled"], index=1)
    with col_p:
        priority = st.selectbox("Priority", ["Low", "Normal", "High", "Critical"], index=2)
    with col_c:
        currency = st.selectbox("Currency", ["USD", "EUR", "GBP", "INR"])
        
    st.markdown("### Line Items")
    items_data = []
    
    # Row 1
    row1_c1, row1_c2, row1_c3 = st.columns([3, 1, 1])
    p1 = row1_c1.text_input("Product 1", value="Enterprise CRM License")
    q1 = row1_c2.number_input("Qty 1", value=10, min_value=1)
    u1 = row1_c3.number_input("Unit Price 1", value=1200.0, min_value=0.0)
    if p1:
        items_data.append({"product_name": p1, "quantity": q1, "unit_price": u1, "total_price": q1 * u1})
        
    # Row 2
    row2_c1, row2_c2, row2_c3 = st.columns([3, 1, 1])
    p2 = row2_c1.text_input("Product 2", value="Premium Support Package")
    q2 = row2_c2.number_input("Qty 2", value=1, min_value=1)
    u2 = row2_c3.number_input("Unit Price 2", value=5000.0, min_value=0.0)
    if p2:
        items_data.append({"product_name": p2, "quantity": q2, "unit_price": u2, "total_price": q2 * u2})
        
    total_amount = sum(item["total_price"] for item in items_data)
    st.info(f"**Order Total: {currency} {total_amount:,.2f}**")
    
    st.markdown("### Additional Info")
    notes = st.text_area("Notes", value="Key account - customer requested expedited processing. Q3 renewal coming up.")
    user_question = st.text_input("Ask a specific question (Optional)", placeholder="e.g. What risks do you see?")
    
    submit_btn = st.button("✨ Generate AI Summary", type="primary", use_container_width=True)

with col2:
    st.markdown("### AI Response")
    if submit_btn:
        if not items_data:
            st.error("Please add at least one line item.")
        else:
            payload = {
                "order_id": order_id,
                "customer_name": customer_name,
                "order_date": str(order_date),
                "status": status,
                "priority": priority,
                "line_items": items_data,
                "total_amount": total_amount,
                "currency": currency,
                "notes": notes,
                "user_question": user_question if user_question.strip() else None
            }
            
            with st.spinner("Analyzing order with AI... This may take 1-2 minutes on a local CPU model."):
                try:
                    # Send request to our FastAPI backend
                    response = requests.post("http://localhost:8000/api/v1/summarize-order", json=payload)
                    response.raise_for_status()
                    data = response.json()
                    
                    st.success(f"Generated successfully by {data.get('provider')} • {data.get('model')}")
                    st.markdown("---")
                    st.markdown(data.get("summary"))
                    
                except requests.exceptions.RequestException as e:
                    st.error("Failed to connect to the FastAPI server. Make sure it is running on port 8000!")
                    st.write("Error details:", e)
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")
    else:
        st.info("Submit an order on the left to see the AI summary here.")
