import streamlit as st
import time
import json
from auth import handle_signup, handle_signin
from parser import extract_text_from_pdf, extract_text_from_docx, extract_fields
from db import save_parsed_data, initialize_database, get_user_history, clear_user_history
import pandas as pd

# ----------- Custom CSS -----------
def local_css():
    st.markdown(
        """
        <style>
        .main {
            background-color: #f5f0e6;
            color: #5d4037;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .css-18e3th9 {
            color: #4e342e;
            font-weight: 700;
            font-size: 2.4rem;
            margin-bottom: 0.5rem;
        }
        .stFileUploader > div > label > div {
            background-color: #d7ccc8;
            border-radius: 8px;
            padding: 0.75rem;
            color: #4e342e;
            font-weight: 600;
            font-size: 1rem;
        }
        div.stButton > button:first-child {
            background-color: #6d4c41;
            color: #f5f0e6;
            font-weight: 600;
            padding: 0.5rem 1.25rem;
            border-radius: 8px;
            transition: background-color 0.3s ease;
            width: 100%;
        }
        div.stButton > button:first-child:hover {
            background-color: #5d4037;
            color: #fff;
        }
        button[title="Download file"] {
            background-color: #a1887f !important;
            color: #3e2723 !important;
            font-weight: 600;
            border-radius: 8px !important;
            padding: 0.5rem 1rem !important;
            transition: background-color 0.3s ease;
        }
        button[title="Download file"]:hover {
            background-color: #6d4c41 !important;
            color: #f5f0e6 !important;
        }
        h2, h3 {
            color: #4e342e;
        }
        .center-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-top: 20px;
            gap: 12px;
            max-width: 300px;
            margin-left: auto;
            margin-right: auto;
        }
        .extracted-data {
            border: 2px solid #a9746e;
            border-radius: 10px;
            padding: 20px;
            background-color: #fff7e6;
            margin-top: 20px;
        }
        footer {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True,
    )

# ----------- Setup -----------
st.set_page_config(page_title="Resume Parser", layout="centered")
initialize_database()
local_css()

# ----------- Session State -----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_info = None
if "show_history" not in st.session_state:
    st.session_state.show_history = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"
if "parse_result" not in st.session_state:
    st.session_state.parse_result = None

# ----------- Navigation Helper -----------
def navigate_to(page_name):
    st.session_state.current_page = page_name
    if page_name == "home":
        st.session_state.show_history = False
        st.session_state.parse_result = None

# ----------- Main -----------
def main():
    st.title("📄 Resume Parser")

    if st.session_state.logged_in:
        show_logged_in_home()
    else:
        if st.session_state.current_page == "home":
            show_guest_home()
        elif st.session_state.current_page == "signup":
            show_signup()
        elif st.session_state.current_page == "signin":
            show_signin()
        elif st.session_state.current_page == "about":
            show_about()

# ----------- Pages for Guest -----------
def show_guest_home():
    st.subheader("Welcome to the Resume Parser App!")
    st.write("Please choose an option below to continue:")

    st.markdown('<div class="center-container">', unsafe_allow_html=True)
    if st.button("📝 Sign Up"):
        navigate_to("signup")
    if st.button("🔑 Sign In"):
        navigate_to("signin")
    if st.button("ℹ️ About"):
        navigate_to("about")
    st.markdown("</div>", unsafe_allow_html=True)

def show_signup():
    st.subheader("Create a New Account")
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        success, message = handle_signup(name, email, password)
        if success:
            st.success(message)
            time.sleep(1.5)
            st.success("Redirecting to Resume Parser...")
            time.sleep(2)
            st.session_state.logged_in = True
            st.session_state.user_info = (None, name, email)
            navigate_to("home")
            st.experimental_rerun()
        else:
            st.error(message)

    if st.button("⬅️ Back to Home"):
        navigate_to("home")

def show_signin():
    st.subheader("Log In to Your Account")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Sign In"):
        success, result = handle_signin(email, password)
        if success:
            st.success("Login successful! Redirecting...")
            time.sleep(3)
            st.session_state.logged_in = True
            st.session_state.user_info = result
            navigate_to("home")
            st.experimental_rerun()
        else:
            st.error(result)

    if st.button("⬅️ Back to Home"):
        navigate_to("home")

def show_about():
    st.subheader("About This App")
    st.markdown(
        """
        This web application allows you to upload a resume (PDF or DOCX), 
        extract important details like Name, Email, Skills, etc., 
        and download the parsed data as a CSV or JSON file.

        Features:
        - Secure user authentication
        - Resume parsing
        - CSV/JSON export
        - View and clear resume parsing history
        """
    )

    if st.button("⬅️ Back to Home"):
        navigate_to("home")

# ----------- Pages for Logged-In User -----------
def show_logged_in_home():
    user_name = st.session_state.user_info[1]
    st.success(f"Logged in as: **{user_name}**")

    st.markdown(
        '<div style="max-width: 400px; margin: auto; display: flex; flex-direction: column; gap: 12px;">',
        unsafe_allow_html=True,
    )

    if st.button("🚪 Log Out"):
        st.session_state.logged_in = False
        st.session_state.user_info = None
        st.session_state.current_page = "home"
        st.session_state.show_history = False
        st.session_state.parse_result = None
        st.experimental_rerun()

    if st.button("📜 History"):
        st.session_state.show_history = not st.session_state.show_history

    if st.session_state.show_history:
        if st.button("🗑️ Clear History"):
            clear_user_history(st.session_state.user_info[0])
            st.success("Your history has been cleared.")
        show_history()
        st.markdown("<br>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Drag and drop file here or click to upload (.pdf or .docx)",
        type=["pdf", "docx"],
        key="file_uploader",
        help="Upload your resume file",
    )

    st.markdown("</div>", unsafe_allow_html=True)

    if uploaded_file:
        st.success(f"File uploaded: {uploaded_file.name}")

        if st.button("Parse Resume"):
            with st.spinner("Parsing your resume..."):
                file_type = uploaded_file.type
                if file_type == "application/pdf":
                    text = extract_text_from_pdf(uploaded_file)
                elif file_type in [
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    "application/octet-stream",
                ]:
                    text = extract_text_from_docx(uploaded_file)
                else:
                    st.error("Unsupported file format.")
                    return

                data = extract_fields(text)
                st.session_state.parse_result = (data, text)
                user_id = st.session_state.user_info[0]
                save_parsed_data(user_id, data)

    if st.session_state.parse_result:
        display_parsed_results(*st.session_state.parse_result)

# ----------- Resume Parser Area -----------
def display_parsed_results(data, full_text):
    st.markdown("---")
    st.subheader("Extracted Details")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"**Name:**  {data.get('name','')}")
        st.markdown(f"**Email:**  {data.get('email','')}")
        st.markdown(f"**Phone:**  {data.get('phone','')}")
        st.markdown(f"**LinkedIn:**  {data.get('linkedin_url','')}")
        st.markdown(f"**GitHub:**  {data.get('github_url','')}")

    with col2:
        st.markdown("**Skills:**")
        skills = data.get("skills", [])
        if isinstance(skills, str):
            skills = skills.split(",") if "," in skills else [skills]
        for skill in skills:
            skill_cleaned = skill.strip().title()
            if skill_cleaned and skill_cleaned.lower() != "n/a":
                st.markdown(f"- {skill_cleaned}")

    st.markdown("---")
    st.subheader("Education")
    st.text(data.get("education", ""))

    st.markdown("---")
    st.subheader("Experience")
    st.text(data.get("experience", ""))

    with st.expander("Show full extracted text"):
        st.text(full_text)

    json_data = json.dumps(data, indent=4)
    st.download_button(
        label="📥 Download Extracted Data as JSON",
        data=json_data,
        file_name="parsed_resume.json",
        mime="application/json",
    )

# ----------- Show History -----------
def show_history():
    st.markdown("---")
    st.subheader("🕘 Your Past Parsed Resumes")
    user_id = st.session_state.user_info[0]
    history = get_user_history(user_id)

    if not history:
        st.info("No past parsed resumes found.")
        return

    for i, record in enumerate(history, 1):
        st.markdown(f"### Resume #{i}")
        st.markdown(f"**Parsed On:** {record['parsed_on']}")
        st.markdown("**Details:**")
        for key in [
            "name",
            "email",
            "phone",
            "skills",
            "education",
            "experience",
            "linkedin_url",
            "github_url",
        ]:
            st.markdown(f"- **{key.capitalize()}**: {record[key]}")
        st.markdown("---")

if __name__ == "__main__":
    main()