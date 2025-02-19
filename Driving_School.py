import streamlit as st
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io
from google.oauth2.service_account import Credentials
import os

private_key_sheets = os.getenv('PRIVATE_KEY_SHEETS')
private_key_drive = os.getenv('PRIVATE_KEY_DRIVE')


st.set_page_config(page_title="Maharashtra Motor Driving School", layout="wide")

# Google Drive and Google Sheets API setup
SERVICE_ACCOUNT_FILE_D = {
    "type": "service_account",
    "project_id": "driving-school-451318",
    "private_key_id": "0162ff551fbe9981d838f34aed1683da978da24a",
    "private_key": private_key_drive,
    "client_email": "drive-school@driving-school-451318.iam.gserviceaccount.com",
    "client_id": "106944027333027449191",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/drive-school%40driving-school-451318.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}

SERVICE_ACCOUNT_FILE_S = {
    "type": "service_account",
    "project_id": "driving-school-451318",
    "private_key_id": "2420c9bc8bbe005528f269ccd4c306102fed04be",
    "private_key": private_key_sheets,
    "client_email": "driving-sheets@driving-school-451318.iam.gserviceaccount.com",
    "client_id": "110903778401150039669",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/driving-sheets%40driving-school-451318.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}

# Create credentials object
credentials_S = Credentials.from_service_account_info(SERVICE_ACCOUNT_FILE_S)
credentials_D = Credentials.from_service_account_info(SERVICE_ACCOUNT_FILE_D)

SCOPES_D = ['https://www.googleapis.com/auth/drive']
SCOPES_S = ['https://www.googleapis.com/auth/spreadsheets']

# credentials_d = service_account.Credentials.from_service_account_file(
#     SERVICE_ACCOUNT_FILE_D, scopes=SCOPES_D
# )
# credentials_s = service_account.Credentials.from_service_account_file(
#     SERVICE_ACCOUNT_FILE_S, scopes=SCOPES_S
# )
drive_service = build('drive', 'v3', credentials=credentials_D)
sheets_service = build('sheets', 'v4', credentials=credentials_S)

LICENSE_SHEET_ID = os.getenv("SHEET_ID")
COURSE_SHEET_ID = os.getenv("COURSE_SHEET_ID")
DRIVE_FOLDER_ID = os.getenv("DRIVE_FOLDER_ID")

# Upload file to Google Drive
def upload_to_drive(file, filename):
    file_metadata = {'name': filename, 'parents': [DRIVE_FOLDER_ID]}
    media = MediaIoBaseUpload(io.BytesIO(file.getvalue()), mimetype=file.type)
    uploaded_file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return f"https://drive.google.com/file/d/{uploaded_file['id']}"  # File URL

# Append data to Google Sheet
def append_to_sheet(sheet_id, data):
    sheets_service.spreadsheets().values().append(
        spreadsheetId=sheet_id,
        range='Sheet1!A1',
        valueInputOption='RAW',
        insertDataOption='INSERT_ROWS',
        body={'values': [data]}
    ).execute()

# Streamlit App
def chatbot():
    st.title("Maharashtra Motor Driving School")
    st.write("Welcome to Maharashtra Motor Driving School! We are dedicated to providing high-quality driving training to ensure road safety and confidence for our learners. Our experienced instructors and well-structured courses cater to both beginners and experienced drivers looking to refresh their skills.")

    with st.sidebar:
        action = st.selectbox("What would you like to do?", ("About Us", "Enroll in Learning Driving Course", "Work with License"))

    if action == "Work with License":
        action2 = st.radio("What would you like to Know about License?", ("Apply", "Enquire"))

        if action2 == "Apply":
            name = st.text_input("Your Name")
            contact = st.text_input("Contact Number")

            license_type = st.selectbox("Select License Type:", ("Old License", "Fresh License"))
            address_proof_1 = st.selectbox("Select first address proof:", ("Aadhar Card", "Passport", "Voter ID", "Light Bill & Index 2", "Registered Rent Agreement & Index 2"))
            address_proof_1_file = st.file_uploader(f"Upload your {address_proof_1}")

            address_proof_2 = st.selectbox("Select second address proof:", ("Passport", "Voter ID", "Light Bill & Index 2", "Registered Rent Agreement & Index 2", "Aadhar Card"))
            address_proof_2_file = st.file_uploader(f"Upload your {address_proof_2}")

            age_proof = st.selectbox("Select age proof:", ("PAN Card", "Passport", "Leaving Certificate", "Birth Certificate"))
            age_proof_file = st.file_uploader(f"Upload your {age_proof}")

            if st.button("Submit"):
                if name and contact and address_proof_1_file and address_proof_2_file and age_proof_file:
                    address_proof_1_url = upload_to_drive(address_proof_1_file, address_proof_1_file.name)
                    address_proof_2_url = upload_to_drive(address_proof_2_file, address_proof_2_file.name)
                    age_proof_url = upload_to_drive(age_proof_file, age_proof_file.name)

                    append_to_sheet(LICENSE_SHEET_ID, [name ,contact,license_type, address_proof_1, address_proof_1_url, address_proof_2, address_proof_2_url, age_proof, age_proof_url])
                    st.success("Application Submitted Successfully!")
                else:
                    st.error("Please upload all required files")
        else:   
            # Step 1: Select License Inquiry Type
            inquiry_type = st.selectbox("What would you like to do?", 
                                ["Apply for a New License", "Renew an Old License"])

            if inquiry_type == "Apply for a New License":
                # Step 2: License Type Selection for New License
                license_type = st.selectbox("Which type of license do you want to apply for?", 
                                            ["Learner's License", "Permanent Driving License"])

                if license_type == "Learner's License":
                    st.subheader("Steps to Apply for a Learner's License:")
                    st.write("""
                    1. **Eligibility**: You must be at least 18 years old.
                    2. **Documents Required**: 
                        - Age Proof (PAN Card, Passport, Birth Certificate, etc.)
                        - Address Proof (Aadhar Card, Passport, Utility Bill, Rent Agreement, etc.)
                    3. **Application Process**:
                        - Visit the official RTO website or the nearest RTO office.
                        - Fill out the learner's license application form (Form 2).
                        - Upload the required documents and passport-sized photographs.
                        - Book a slot for the learner's test.
                    4. **Learner's Test**: 
                        - Appear for a simple theory test covering traffic rules and regulations.
                        - Upon passing, you will receive the learner's license.
                    """)

                elif license_type == "Permanent Driving License":
                    st.subheader("Steps to Apply for a Permanent Driving License:")
                    st.write("""
                    1. **Eligibility**: 
                        - You must hold a valid learner's license for at least 30 days.
                        - You must apply for a permanent license within 180 days of getting the learner's license.
                    2. **Documents Required**: 
                        - Learner's License
                        - Address Proof (Aadhar Card, Passport, Utility Bill, Rent Agreement, etc.)
                        - Age Proof (PAN Card, Passport, Birth Certificate, etc.)
                    3. **Application Process**:
                        - Visit the RTO office or use the online portal.
                        - Fill out the driving license application form (Form 4).
                        - Upload required documents and photographs.
                        - Book a driving test slot.
                    4. **Driving Test**: 
                        - You will need to pass a practical driving test at the RTO.
                        - If you pass, the RTO will issue your permanent driving license.
                    """)

            elif inquiry_type == "Renew an Old License":
                st.subheader("Steps to Renew an Old Driving License:")
                st.write("""
                1. **Eligibility**: You can renew your license 30 days before its expiration date.
                2. **Documents Required**:
                    - Expired or expiring Driving License
                    - Address Proof (Aadhar Card, Passport, Utility Bill, Rent Agreement, etc.)
                    - Age Proof (PAN Card, Passport, Birth Certificate, etc.)
                3. **Application Process**:
                    - Visit the official RTO website or the nearest RTO office.
                    - Fill out the renewal application form (Form 9).
                    - Submit the required documents and pay the renewal fee.
                    - If your license has expired for more than 5 years, you may be asked to take a retest.
                4. **Issue of Renewed License**: Once your documents are verified, the RTO will issue the renewed license.
                """)

    elif action == "Enroll in Learning Driving Course":
        st.subheader("Enroll in a Driving Course")
        st.write("Follow the steps below to enroll in a driving course that suits your needs.")

        st.markdown("### Step 1: Select a Location")
        location = st.selectbox("Choose your preferred training location:", 
                                ["Phase 3 - (Basic & Refresh Courses)", "Sus Gaon - (Basic & Refresh Courses)"])
        
        # Step 3: User selects course type based on the location
        st.markdown("### Step 2: Select a Course Type")
        if location == "Phase 3 - (Basic & Refresh Courses)":
            course_type = st.selectbox("Choose the course that fits your needs:", 
                                       ["Basic Course (₹3500 for 25 Days)", 
                                        "Refresh Course (₹3000 for 10 Days)"])
        elif location == "Sus Gaon - (Basic & Refresh Courses)":
            course_type = st.selectbox("Choose the course that fits your needs:", 
                                       ["Basic Course (₹4500 for 30 Days)", 
                                        "Refresh Course (₹3000 for 10 Days)"])

        # Step 4: Display course details based on selection
        st.markdown("### Step 3: Course Details")
        if course_type == "Basic Course (₹3500 for 25 Days)" or course_type == "Basic Course (₹4500 for 30 Days)":
            st.write("""
            **Basic Course Overview:**
            - **Duration**: 25/30 Days (depending on the location)
            - **Fees**: ₹3500 (Phase 3) / ₹4500 (Sus Gaon)
            - **Daily Driving Distance**: 5 km
            - **Total Driving Distance**: 125 km (Phase 3) / 150 km (Sus Gaon)
            - **Daily Sessions**: 1 Hour each day
            """)
        elif course_type == "Refresh Course (₹3000 for 10 Days)":
            st.write("""
            **Refresh Course Overview:**
            - **Duration**: 10 Days
            - **Fees**: ₹3000
            - **Daily Driving Distance**: 10 km
            - **Total Driving Distance**: 100 km
            - **Daily Sessions**: 1 Hour each day
            """)

        # Final enrollment step
        name = st.text_input("Your Name")
        contact = st.text_input("Contact Number")

        if st.button("Enroll Now"):
            if name and contact:
                append_to_sheet(COURSE_SHEET_ID, [name, contact, location, course_type])
                st.success(f"You have successfully enrolled in the {course_type} at {location}!")
            else:
                st.error("Please provide your Name and Contact Number")

    elif action == "About Us":
        st.title("Welcome to Maharashtra Motor Driving School")
        st.write("""
        🚗 **Your Journey to Safe and Confident Driving Starts Here!**
    
        Maharashtra Motor Driving School is a leading institution committed to providing top-quality driving education. With over a decade of experience, we have trained thousands of confident drivers across the state. Our mission is to ensure that every student masters the art of driving while prioritizing road safety and traffic regulations.
        """)

        st.image("https://images.unsplash.com/photo-1570125909232-8b5b5eb702c7", caption="Driving Lessons in Progress", use_container_width=True)
    
        st.subheader("Why Choose Us?")
        st.write("""
        - 🏆 Experienced and Certified Instructors
        - 🚦 Comprehensive and Personalized Driving Courses
        - 🏎️ Training on Modern Vehicles
        - 🛣️ Focus on Road Safety and Defensive Driving
        - ✅ Flexible Scheduling to Suit Your Needs
        - 📋 Assistance with Learner’s and Permanent Driving License
        """)
    
        st.image("https://images.unsplash.com/photo-1517686469429-8bdb88b9e0c4", caption="Our Experienced Instructors", use_container_width=True)
    
        st.subheader("Our Services")
        st.write("""
        - **Basic Driving Lessons**: Learn the fundamentals of driving.
        - **Advanced Driving Techniques**: For experienced drivers to enhance their skills.
        - **Traffic Rules and Road Safety Education**: Stay updated on all traffic laws.
        - **Practical On-Road Training**: Real-time practice on busy roads.
        - **License Assistance**: Complete support for obtaining your driving license.
        """)
    
        st.image("https://images.unsplash.com/photo-1552642986-ccb41e7059a4", caption="Practical Training Session", use_container_width=True)
    
        st.subheader("Our Commitment to Safety")
        st.write("""
        We prioritize safety above all else. Our curriculum is designed to educate learners on defensive driving techniques, emergency handling, and responsible driving behavior.
    
        Our vehicles are equipped with dual control systems to ensure that our instructors can take charge whenever necessary, giving you peace of mind as you learn.
        """)
    
        st.image("https://images.unsplash.com/photo-1527245386021-5c0f27ebc61a", caption="Safety-First Approach", use_container_width=True)
    
        st.subheader("Join Us Today")
        st.write("""
        Ready to start your driving journey? Contact us now and take the first step towards becoming a confident and responsible driver!
        
        📞 **Call Us:** +91 98765 43210  
        📧 **Email:** info@maharashtramotor.com
        🌐 **Website:** www.maharashtramotordrivingschool.com
        """)


if __name__ == "__main__":
    chatbot()
