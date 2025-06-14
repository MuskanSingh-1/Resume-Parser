# 📄 Resume Parser Web Application

A web-based application built using **Streamlit** that allows users to securely **upload resumes (PDF or DOCX)** and extract important details such as **Name, Email, Phone, Skills, Education, Experience, LinkedIn, and GitHub links**. The parsed data can be downloaded in **JSON** format, and users can also view or clear their parsing history.

---

## 🌟 Features

- 🔐 **User Authentication** (Sign-up/Sign-in)
- 📤 **Upload Resumes** in `.pdf` or `.docx` formats
- 🧠 **AI-powered Parsing** using spaCy and regex
- 🛠️ Extracts:
  - Name
  - Email
  - Phone Number
  - Skills (from a custom skill database)
  - Education
  - Experience
  - LinkedIn URL
  - GitHub URL
- 💾 **Download parsed data** in JSON format
- 🕘 **View & clear parsing history**
- 🎨 **Custom-styled UI** using embedded CSS
- 🗂️ **Modular codebase** with clean separation of frontend, backend, and logic

---

## 🛠️ Tech Stack

- **Frontend:** [Streamlit](https://streamlit.io/)
- **Backend Logic:** Python
- **NLP Engine:** spaCy (`en_core_web_sm`)
- **PDF Parsing:** `pdfplumber`
- **DOCX Parsing:** `docx2txt`
- **Authentication:** SHA256 hashing + validation
- **Database:** Assumed to be JSON or SQLite (defined in `db.py`)

---

## 📁 Project Structure

```plaintext
resume-parser/
├── app.py           # Main Streamlit UI and routing
├── auth.py          # Handles user signup/signin and validation
├── parser.py        # Resume text extraction and field parsing
├── db.py            # Database operations (create, insert, retrieve, delete)
├── reusme_parser.db # File to store user login information and user parsed history (creadted automatically on running the files)
└── README.md        # Project documentation (this file)
```

---

# ⚙️ Project Setup & Requirements

This document lists all necessary downloads and installation steps to set up and run the **Resume Parser Web Application**.

---

## ✅ System Requirements

- **Python Version:** 3.8 or higher
- **Internet Connection:** Required (for downloading dependencies and models)
- **Operating System:** Windows, macOS, or Linux

---

## 📦 Required Python Packages

Install all required libraries using the following commands:
- pip install pdfplumber docx2txt spacy
- pip install streamlit pandas

---

## 🧠 NLP Model Setup

Download the required English language model for spaCy:
- python -m spacy download en_core_web_sm

## 🚀 Hpw to run
### Method 1:
```bash
- Go to the folder in which all the files are saved
- Click on the address bar and type cmd
- Command prompt for the folder will open
- On the command prompt type:
     python -m streamlit run app.py
```
### Method 2:

- Goto the command prompt and type:
      python -m streamlit run **full address of the app.py file**
