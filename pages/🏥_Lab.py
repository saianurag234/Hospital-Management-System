import streamlit as st
from datetime import datetime
from SQL_connection import create_server_connection, execute_query
from utils import get_test_id
from secret.credentials import *
from streamlit_extras.switch_page_button import switch_page

st.subheader('Lab Test Record')

# Inputs for Lab Test Record
patient_id = int(st.text_input('Patient ID', '0'))
referred_doctor_id = int(st.text_input('Referred Doctor ID', '0'))
test_date = st.date_input('Test Date', value=datetime.now().date())
test_time = st.time_input('Test Time', value=datetime.now().time())
test_datetime = datetime.combine(test_date, test_time)

# Assuming get_test_id function fetches the TestID based on the test name
test_names = ['Complete Blood Count', 'Lipid Profile', 'Liver Function Test', 'Thyroid Function Test',
              'Hemoglobin A1C', 'Basic Metabolic Panel', 'Comprehensive Metabolic Panel', 'Electrolyte Panel',
              'Urinalysis', 'C-Reactive Protein', 'Blood Pressure Monitoring', 'Blood Sugar Test',
              'Routine Urine Analysis', 'Chest X-ray', 'Abdominal X-ray', 'Bone Density Scan',
              'CT Scan - Head', 'MRI - Lumbar Spine', 'Ultrasound - Abdomen', 'Echocardiogram']

selected_test_name = st.selectbox('Test Taken', [''] + test_names)

submit_button = st.button('Submit')

if submit_button:
    if not all([patient_id, referred_doctor_id, selected_test_name]) or selected_test_name == '':
        st.error('Please fill out all fields.')
    else:
        db_connection = create_server_connection(
            host, username, password, database)
        test_id = get_test_id(db_connection, selected_test_name)

        if test_id is not None:
            st.header(test_datetime)
            insert_lab_record_query = f"""
                INSERT INTO Lab (PatientID, ReferredDoctorID, TestID)
                VALUES ('{patient_id}', '{referred_doctor_id}', '{test_id}');
            """

            execute_query(db_connection, insert_lab_record_query)
        else:
            st.error('Selected test is not valid.')

st.title(" ")
st.header(" ")

col1, spacer1, col2 = st.columns(
    [1, 1.5, 1])

with col2:
    lab_back_button = st.button(label='Go Back to Admin Page')

    if lab_back_button:
        switch_page("Admin")
