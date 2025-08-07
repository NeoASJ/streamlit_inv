import streamlit as st
import pandas as pd

# This is the main function to load and save data
def load_data():
    try:
        df = pd.read_csv('inventory.csv')
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Item', 'Quantity', 'Price'])
    return df

def save_data(df):
    df.to_csv('inventory.csv', index=False)

# Main app title
st.title('Inventory Management System 📦')
st.write("Welcome! Use the sidebar to navigate.")

# Load the current inventory
inventory_df = load_data()

st.subheader('Current Inventory')
st.dataframe(inventory_df, use_container_width=True, hide_index=True)

# Sidebar for actions
with st.sidebar:
    st.header('Inventory Actions')

    st.subheader('Add New Item')
    with st.form('add_item_form'):
        item_name = st.text_input('Item Name')
        quantity = st.number_input('Quantity', min_value=0, step=1)
        price = st.number_input('Price', min_value=0.0, format='%f')
        add_button = st.form_submit_button('Add Item')

        if add_button:
            if item_name and quantity is not None and price is not None:
                if item_name in inventory_df['Item'].values:
                    st.warning(f'An item named "{item_name}" already exists.')
                else:
                    new_item = pd.DataFrame([{'Item': item_name, 'Quantity': quantity, 'Price': price}])
                    updated_df = pd.concat([inventory_df, new_item], ignore_index=True)
                    save_data(updated_df)
                    st.success(f'Successfully added "{item_name}"!')
                    st.rerun()
            else:
                st.error('Please fill in all fields.')
    
    st.subheader('Update or Remove an Item')
    if not inventory_df.empty:
        item_to_modify = st.selectbox('Select an Item', inventory_df['Item'].tolist())
        
        if item_to_modify:
            current_data = inventory_df[inventory_df['Item'] == item_to_modify].iloc[0]

            with st.form('update_item_form'):
                new_quantity = st.number_input('New Quantity', min_value=0, step=1, value=int(current_data['Quantity']))
                new_price = st.number_input('New Price', min_value=0.0, format='%f', value=current_data['Price'])
                
                col1, col2 = st.columns(2)
                with col1:
                    update_button = st.form_submit_button('Update Item')
                with col2:
                    remove_button = st.form_submit_button('Remove Item')

                if update_button:
                    inventory_df.loc[inventory_df['Item'] == item_to_modify, 'Quantity'] = new_quantity
                    inventory_df.loc[inventory_df['Item'] == item_to_modify, 'Price'] = new_price
                    save_data(inventory_df)
                    st.success(f'Successfully updated "{item_to_modify}"!')
                    st.rerun()

                if remove_button:
                    updated_df = inventory_df[inventory_df['Item'] != item_to_modify]
                    save_data(updated_df)
                    st.success(f'Successfully removed "{item_to_modify}"!')
                    st.rerun()
    else:
        st.info("The inventory is empty. Add a new item to get started.")