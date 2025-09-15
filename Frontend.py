import streamlit as st
import requests
import json

# Set wide layout
st.set_page_config(page_title="Patient Management System", layout="wide")

BASE_URL = "http://localhost:8000"  # Change if your FastAPI backend runs elsewhere

# Sidebar - navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "View Patients", "Add Patient", "Update Patient", "Patient Details", "Sort Patients", "About"])

st.sidebar.markdown("---")
st.sidebar.markdown("API powered by FastAPI | Frontend with Streamlit")
st.sidebar.markdown("")

# Helper to show message alerts
def alert_msg(msg, success=True):
    if success:
        st.success(msg)
    else:
        st.error(msg)

# Home page
if page == "Home":
    st.title("Patient Management System")
    st.markdown("Welcome to the Patient Management System frontend interface using Streamlit.")
    st.markdown(
        """
        - Use the sidebar to navigate between pages.
        - Add, update, view, and sort patient data powered by a FastAPI backend.
        - All data is fetched and updated via REST API calls.
        """
    )

# About page
elif page == "About":
    st.title("About this Application")
    st.markdown("""
    ### Overview
    This frontend interfaces with a FastAPI backend that manages patient records.
    
    Features:
    - Add new patients with validation.
    - Update patient records.
    - View patient details.
    - Sort patients by height, weight, or BMI.
    - Clean, responsive UI designed with Streamlit.
    
    ### Technologies Used
    - FastAPI for backend API server.
    - Streamlit for frontend web interface.
    - JSON file storage for demonstration.
    
    """)

# View all patients
elif page == "View Patients":
    st.title("All Patients")
    try:
        response = requests.get(f"{BASE_URL}/view")
        response.raise_for_status()
        patients = response.json()
        if not patients:
            st.info("No patients found.")
        else:
            # Convert dict to list for table
            patient_list = []
            for pid, pdata in patients.items():
                patient_list.append({"ID": pid, **pdata})
            st.dataframe(patient_list, use_container_width=True)
    except Exception as e:
        alert_msg(f"Error loading patients: {e}", success=False)

# Add new patient form
elif page == "Add Patient":
    st.title("Add New Patient")
    with st.form("add_patient_form"):
        st.markdown("Enter patient details:")
        pid = st.text_input("Patient ID", max_chars=10, help="Unique ID, e.g. P001")
        name = st.text_input("Name", help="Patient full name")
        city = st.text_input("City", help="City of residence")
        age = st.number_input("Age", min_value=1, max_value=119, step=1, help="Age (1-119)")
        gender = st.selectbox("Gender", options=["male", "female", "others"], help="Gender")
        height = st.number_input("Height (meters)", min_value=0.1, format="%.2f", help="Height in meters")
        weight = st.number_input("Weight (kg)", min_value=0.1, format="%.1f", help="Weight in kilograms")

        submit = st.form_submit_button("Add Patient")
    
    if submit:
        if not pid.strip():
            alert_msg("Patient ID is required.", success=False)
        else:
            new_patient = {
                "id": pid.strip(),
                "name": name.strip(),
                "city": city.strip(),
                "age": age,
                "gender": gender,
                "height": height,
                "weight": weight
            }
            try:
                res = requests.post(f"{BASE_URL}/add_patient", json=new_patient)
                if res.status_code == 201:
                    alert_msg(f"Patient {pid} added successfully!")
                else:
                    err = res.json().get("detail") if res.headers.get('content-type', '').startswith('application/json') else res.text
                    alert_msg(f"Failed to add patient: {err}", success=False)
            except Exception as e:
                alert_msg(f"API call failed: {e}", success=False)

# Update patient form
elif page == "Update Patient":
    st.title("Update Patient Details")

    patient_id = st.text_input("Enter Patient ID to update", key="update_pid", help="e.g. P001")
    if patient_id:
        try:
            patient_res = requests.get(f"{BASE_URL}/patient/{patient_id.strip()}")
            if patient_res.status_code == 200:
                patient_data = patient_res.json()
                with st.form("update_patient_form"):
                    st.markdown("Update patient fields (leave blank to keep unchanged):")
                    name = st.text_input("Name", value=patient_data.get("name", ""), help="Patient full name")
                    city = st.text_input("City", value=patient_data.get("city", ""), help="City of residence")
                    age = st.number_input("Age", min_value=1, max_value=119, value=patient_data.get("age", 30), step=1)
                    gender = st.selectbox("Gender", options=["male", "female"], index=["male","female"].index(patient_data.get("gender","male")))
                    height = st.number_input("Height (meters)", min_value=0.1, value=patient_data.get("height", 1.75), format="%.2f")
                    weight = st.number_input("Weight (kg)", min_value=0.1, value=patient_data.get("weight",70.0), format="%.1f")

                    submit_update = st.form_submit_button("Update Patient")

                if submit_update:
                    updated_fields = {
                        "name": name,
                        "city": city,
                        "age": age,
                        "gender": gender,
                        "height": height,
                        "weight": weight
                    }
                    # Remove unchanged fields or blanks if needed
                    updated_data = {k:v for k,v in updated_fields.items() if v not in [None, "", 0]}
                    try:
                        res = requests.put(f"{BASE_URL}/update/{patient_id.strip()}", json=updated_data)
                        if res.status_code == 200:
                            alert_msg(f"Patient {patient_id} updated successfully!")
                        else:
                            err = res.json().get("detail") if res.headers.get('content-type', '').startswith('application/json') else res.text
                            alert_msg(f"Failed to update patient: {err}", success=False)
                    except Exception as e:
                        alert_msg(f"API call failed: {e}", success=False)
            else:
                st.warning("Patient not found or invalid ID.")
        except Exception as e:
            alert_msg(f"Failed to fetch patient details: {e}", success=False)

# Patient details by ID view
elif page == "Patient Details":
    st.title("View Patient Details")
    pid = st.text_input("Enter Patient ID", help="e.g. P001")
    if pid:
        try:
            res = requests.get(f"{BASE_URL}/patient/{pid.strip()}")
            if res.status_code == 200:
                patient = res.json()
                st.markdown(f"### Patient ID: {pid.strip()}")
                st.markdown(f"**Name:** {patient.get('name')}")
                st.markdown(f"**City:** {patient.get('city')}")
                st.markdown(f"**Age:** {patient.get('age')}")
                st.markdown(f"**Gender:** {patient.get('gender')}")
                st.markdown(f"**Height (m):** {patient.get('height')}")
                st.markdown(f"**Weight (kg):** {patient.get('weight')}")
                st.markdown(f"**BMI:** {patient.get('bmi')}")
                st.markdown(f"**Verdict:** {patient.get('verdict')}")
            else:
                st.warning("Patient not found.")
        except Exception as e:
            alert_msg(f"Error fetching patient: {e}", success=False)

# Sort and display patients
elif page == "Sort Patients":
    st.title("Sort Patients")
    sort_by = st.selectbox("Sort by", ["height", "weight", "bmi"], help="Choose field to sort on")
    order = st.selectbox("Order", ["asc", "desc"], help="Ascending or descending order")

    if st.button("Sort"):
        try:
            res = requests.get(f"{BASE_URL}/sort", params={"sort_by": sort_by, "order": order})
            if res.status_code == 200:
                sorted_patients = res.json()
                if not sorted_patients:
                    st.info("No patients found.")
                else:
                    patient_list = []
                    for pdata in sorted_patients:
                        # ID is not included, add placeholder or fetch again if needed
                        patient_list.append({
                            "Name": pdata.get("name"),
                            "City": pdata.get("city"),
                            "Age": pdata.get("age"),
                            "Gender": pdata.get("gender"),
                            "Height": pdata.get("height"),
                            "Weight": pdata.get("weight"),
                            "BMI": pdata.get("bmi"),
                            "Verdict": pdata.get("verdict"),
                        })
                    st.dataframe(patient_list, use_container_width=True)
            else:
                err = res.json().get("detail") if res.headers.get('content-type', '').startswith('application/json') else res.text
                alert_msg(f"Failed to sort patients: {err}", success=False)
        except Exception as e:
            alert_msg(f"API call failed: {e}", success=False)
