import streamlit as st
import pandas as pd
from secret.credentials import *
from utils import *
from SQL_connection import *
from streamlit_extras.switch_page_button import switch_page


db_connection = create_server_connection(host, username, password, database)


st.title('Welcome to Hospital Pharmacy')
st.header("")

with st.form(key='search_medicine'):
    st.subheader('Search for Medicine')
    search_query = st.text_input('Enter the name of the medicine')
    submit_search = st.form_submit_button('Search')
    if submit_search and search_query:
        stock_info = get_medicine_stock(db_connection, search_query)
        if stock_info:
            df_stock = pd.DataFrame(stock_info, columns=[
                                    'Medicine Name', 'Available Quantity', 'Description', 'Price per Unit'])
            st.table(df_stock)
        else:
            st.error('Medicine not found or no stock available.')

st.header("")

with st.form(key='update_stock'):
    st.subheader('Update Medicine Stock')
    medicine_id_to_update = st.number_input('Enter Medicine ID', min_value=0)
    new_quantity = st.number_input('Enter New Stock Quantity', min_value=0)
    update_stock_button = st.form_submit_button('Update Stock')
    if update_stock_button and medicine_id_to_update > 0:
        update_stock(
            db_connection, medicine_id_to_update, new_quantity)

st.header("")

with st.form(key='add_medicine'):
    st.subheader('Add New Medicine Entry')
    new_medicine_name = st.text_input('Medicine Name')
    new_description = st.text_area('Description')
    new_quantity_in_sheets = st.number_input('Quantity in Sheets', min_value=0)
    new_price = st.number_input('Price', min_value=0.0)
    add_medicine_button = st.form_submit_button('Add Medicine')
    if add_medicine_button and new_medicine_name:
        inserted_rows = add_medicine(
            db_connection, new_medicine_name, new_description, new_quantity_in_sheets, new_price)
        if inserted_rows:
            st.success(f'Medicine {new_medicine_name} added successfully.')
        else:
            st.error('Failed to add the medicine. Please check the details.')


st.title(" ")
st.header(" ")

col1, spacer1, col2 = st.columns(
    [1, 1.5, 1])

with col2:
    pharmacy_back_button = st.button(label='Go Back to Admin Page')

    if pharmacy_back_button:
        switch_page("Admin")
