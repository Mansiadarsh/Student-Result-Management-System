import streamlit as st
import requests
import pandas as pd

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Student Result Management",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Student Result Management System")

menu = st.sidebar.selectbox(
    "Select Option",
    [
        "Add Student",
        "View Students",
        "Search Student",
        "Topper",
        "Status"
    ]
)

# -------------------------
# ADD STUDENT
# -------------------------

if menu == "Add Student":

    st.header("Add Student")

    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1)

    roll_no = st.number_input("Roll No", min_value=1)

    math_marks = st.number_input("Math Marks", 0, 100)
    science_marks = st.number_input("Science Marks", 0, 100)
    english_marks = st.number_input("English Marks", 0, 100)
    computer_marks = st.number_input("Computer Marks", 0, 100)
    physics_marks = st.number_input("Physics Marks", 0, 100)

    if st.button("Add Student"):

        payload = {
            "name": name,
            "age": age,
            "roll_no": roll_no,
            "math_marks": math_marks,
            "science_marks": science_marks,
            "english_marks": english_marks,
            "computer_marks": computer_marks,
            "physics_marks": physics_marks
        }

        response = requests.post(
            f"{BASE_URL}/add_student",
            json=payload
        )

        if response.status_code == 200:
            st.success("Student Added Successfully")
        else:
            st.error(response.text)

# -------------------------
# VIEW STUDENTS
# -------------------------

elif menu == "View Students":

    st.header("All Students")

    response = requests.get(
        f"{BASE_URL}/students"
    )

    if response.status_code == 200:

        data = response.json()

        if data:
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No Students Found")

# -------------------------
# SEARCH STUDENT
# -------------------------

elif menu == "Search Student":

    st.header("Search Student")

    roll = st.number_input(
        "Enter Roll Number",
        min_value=1
    )

    if st.button("Search"):

        response = requests.get(
            f"{BASE_URL}/students/{roll}"
        )

        if response.status_code == 200:

            student = response.json()

            st.json(student)

        else:
            st.error("Student Not Found")

# -------------------------
# TOPPER
# -------------------------

elif menu == "Topper":

    st.header("🏆 Topper")

    response = requests.get(
        f"{BASE_URL}/topper"
    )

    if response.status_code == 200:

        topper = response.json()

        st.success(
            f"Topper: {topper['name']}"
        )

        st.json(topper)

# -------------------------
# STATUS
# -------------------------

elif menu == "Status":

    st.header("Pass / Fail Summary")

    response = requests.get(
        f"{BASE_URL}/status"
    )

    if response.status_code == 200:

        status = response.json()

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Pass",
                status["Pass"]
            )

        with col2:
            st.metric(
                "Fail",
                status["Fail"]
            )