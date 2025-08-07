import streamlit as st
import pandas as pd
import altair as alt

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
    st.subheader('Item Quantities and Prices')
    st.write('**Quantity of Each Item**')
    st.bar_chart(inventory_df.set_index('Item')['Quantity'])
    
    st.write('**Price of Each Item**')
    st.line_chart(inventory_df.set_index('Item')['Price'])

    # --- Pie Chart ---
    st.subheader('Inventory Value Distribution')
    # Calculate the value of each item type
    inventory_df['Total Value'] = inventory_df['Quantity'] * inventory_df['Price']
    # Create the pie chart using Altair since Streamlit doesn't have a native pie chart function
    chart = alt.Chart(inventory_df).mark_arc(outerRadius=120).encode(
        theta=alt.Theta("Total Value", stack=True),
        color=alt.Color("Item"),
        tooltip=["Item", "Total Value"]
    ).properties(
        title='Proportion of Total Inventory Value by Item'
    )
    st.altair_chart(chart, use_container_width=True)
    
    
    

    
else:
    st.info("The inventory is empty. Add some items on the main page to see the dashboard.")