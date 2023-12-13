import streamlit as st
from datetime import datetime, date
import pytz
from SQL_connection import create_server_connection, execute_query
from utils import *
from secret.credentials import *
import datetime as dt
from streamlit_extras.switch_page_button import switch_page

st.title('Doctor Appointment Booking')

db_connection = create_server_connection(host, username, password, database)

doctor_name = st.selectbox(
    'Select a Doctor', ["", "Dr. Nirvi Shenoy", "Dr. Elakshi Lalaa", "Dr. Shalv Grover", "Dr. Veer Dhawan", "Dr. Vanya Singhal", "Dr. Anvi Ramakrishnan", "Dr. Seher Mand",
                        "Dr. Shlok Bhargava", "Dr. Damini Doctor", "Dr. Renee Malhotra", "Dr. Emir Khare", "Dr. Madhav Mand", "Dr. Nitya Krishnan", "Dr. Tarini Sant", "Dr. Veer Amble", "Dr. Navya Biswas", "Dr. Gatik Shan", "Dr. Vihaan Raval", "Dr. Aniruddh Sahota", "Dr. Farhan Chadha", "Dr. Neelofar Amble", "Dr. Nirvi Babu",
                        "Dr. Seher Ratta", "Dr. Eva Madan", "Dr. Mannat Chaudhary", "Dr. Ojas Wali", "Dr. Reyansh Jain", "Dr. Shaan Venkatesh", "Dr. Ishita Sule", "Dr. Anika Tripathi", "Dr. Priyansh Sarin", "Dr. Taran Kapoor", "Dr. Rania Shetty", "Dr. Ahana  Deep", "Dr. Mamooty Soni", "Dr. Purab Sangha", "Dr. Pihu Joshi",
                        "Dr. Neysa Koshy", "Dr. Biju Sem", "Dr. Hunar Vasa"]
)

appointment_date = st.date_input(
    'Select a Date', min_value=date.today())

current_date = date.today()
local_tz = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(local_tz).time()
st.header(current_time)

if doctor_name and appointment_date:
    doctor_id = get_doctors_id(db_connection, doctor_name)
    time_condition = ""
    if appointment_date == current_date:
        current_time_str = current_time.strftime('%H:%M:%S')
        time_condition = f" AND ADDTIME('10:00:00', SEC_TO_TIME(slot * 1800)) > '{current_time_str}'"

    available_slots_query = f"""
    SELECT 
        ADDTIME('10:00:00', SEC_TO_TIME(slot * 1800)) AS AvailableSlot
    FROM 
        (SELECT 0 AS slot UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 
         UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 
         UNION SELECT 10 UNION SELECT 11 UNION SELECT 12 UNION SELECT 13 ) slots
    WHERE 
        (ADDTIME('10:00:00', SEC_TO_TIME(slot * 1800)) < '12:30:00' OR 
         ADDTIME('10:00:00', SEC_TO_TIME(slot * 1800)) > '13:59:00')
        AND ADDTIME('10:00:00', SEC_TO_TIME(slot * 1800)) < '16:30:00'
        {time_condition}
        AND NOT EXISTS (
            SELECT 1 
            FROM Appointment 
            WHERE DoctorID = %s 
            AND AppointmentDate = %s 
            AND AppointmentStartTime = ADDTIME('10:00:00', SEC_TO_TIME(slot * 1800))
            AND AppointmentStatus IN ('Scheduled', 'Rescheduled')
        );
    """

    formatted_date = appointment_date.strftime('%Y-%m-%d')
    available_slots = execute_read_query(
        db_connection, available_slots_query, (doctor_id, formatted_date))

    if available_slots:
        available_slots = [slot[0] for slot in available_slots]
        available_slots = ['']+available_slots
        selected_slot = st.selectbox("Available Time Slots", available_slots)
    else:
        st.write("No available slots for the selected date.")

patient_id = st.number_input("Enter your Patient ID", min_value=1)
reason_for_visit = st.text_input('Reason For Visit', "").strip()

if st.button('Book Appointment') and selected_slot:
    book_appointment(db_connection, patient_id, doctor_name,
                     appointment_date, selected_slot, reason_for_visit)
    st.success(
        f"Appointment booked successfully for {selected_slot} on {appointment_date}.")


st.title(" ")
st.header(" ")

col1, spacer1, col2 = st.columns(
    [1, 1.5, 1])

with col2:
    appointment_back_button = st.button(label='Go Back to Patient Page')

    if appointment_back_button:
        switch_page("Patient")
