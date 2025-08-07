import streamlit as st
import pandas as pd

# This function must be available on this page to load the data
def load_data():
    try:
        df = pd.read_csv('inventory.csv')
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Item', 'Quantity', 'Price'])
    return df

st.title('Inventory Dashboard 📊')

inventory_df = load_data()

if not inventory_df.empty:
    # --- Calculate KPIs ---
    total_items = len(inventory_df['Item'].unique())
    total_value = (inventory_df['Quantity'] * inventory_df['Price']).sum()

    # --- Display KPIs in columns ---
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Total Unique Items", value=total_items)

    with col2:
        st.metric(label="Total Inventory Value", value=f"₹{total_value:,.2f}")

    # --- Low Stock Alerts ---
    st.markdown("---")
    st.subheader("Low Stock Alerts")
    
    # You can set a minimum threshold for low stock.
    # For this example, let's use a threshold of 10.
    low_stock_threshold = 10 
    low_stock_items = inventory_df[inventory_df['Quantity'] <= low_stock_threshold]

    if not low_stock_items.empty:
        st.warning(f"There are **{len(low_stock_items)}** items with low stock!")
        st.dataframe(low_stock_items, use_container_width=True, hide_index=True)
    else:
        st.success("All items are well-stocked! 👍")

    # --- Charts ---
    st.markdown("---")
    st.subheader('Inventory Charts')
    st.write('**Quantity of Each Item**')
    st.bar_chart(inventory_df.set_index('Item')['Quantity'])

    st.write('**Price of Each Item**')
    st.line_chart(inventory_df.set_index('Item')['Price'])

else:
    st.info("The inventory is empty. Add some items on the main page to see the dashboard.")