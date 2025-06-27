import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Aynı Student sınıfı burada (ya da student_model.py'den import edebilirsin)
class Person:
    def __init__(self, name):
        self.name = name

class Student(Person):
    def __init__(self, student_no, name, email, classroom):
        super().__init__(name)
        self.student_no = student_no
        self.email = email
        self.classroom = classroom
        self.records = []

    def add_record(self, subject, teacher, week, grade, attendance):
        self.records.append({
            "subject": subject,
            "teacher": teacher,
            "week": week,
            "grade": grade,
            "attendance": attendance
        })

    def __str__(self):
        return f"{self.name} | No: {self.student_no} | Mail: {self.email} | Kayıt: {len(self.records)}"

def load_students_from_df(df):
    students_dict = {}

    for _, row in df.iterrows():
        student_id = row["student_id"]
        if student_id not in students_dict:
            s = Student(
                student_no=student_id,
                name=row["name"],
                email=row["email"],
                classroom=row["classroom"]
            )
            students_dict[student_id] = s

        students_dict[student_id].add_record(
            subject=row["subject"],
            teacher=row["teacher"],
            week=row["week"],
            grade=row["grade"],
            attendance=row["attendance"]
        )
    
    return list(students_dict.values())

# Streamlit UI
st.title("📊 Öğrenci Performans Raporu")

uploaded_file = st.file_uploader("Lütfen student_data.csv dosyanızı yükleyin", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    students = load_students_from_df(df)

    student_names = [f"{s.name} (#{s.student_no})" for s in students]
    selected_name = st.selectbox("Öğrenci Seçin", student_names)
    selected_student = students[student_names.index(selected_name)]

    st.subheader(f"{selected_student.name} - {selected_student.classroom}")

    for subject in set(r["subject"] for r in selected_student.records):
        subject_records = [r for r in selected_student.records if r["subject"] == subject]
        weeks = [r["week"] for r in subject_records]
        grades = [r["grade"] for r in subject_records]

        plt.plot(weeks, grades, marker="o", label=subject)

    plt.xlabel("Hafta")
    plt.ylabel("Not")
    plt.title("Haftalık Ders Notları")
    plt.legend()
    st.pyplot(plt)

else:
    st.info("Lütfen önce bir CSV dosyası yükleyin.")
