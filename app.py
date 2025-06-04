from flask import Flask, render_template, request, send_file
from fpdf import FPDF
import os
from datetime import datetime

app = Flask(__name__)
REPORTS_DIR = "reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

def sanitize_text(text):
    return text.encode('latin-1', 'replace').decode('latin-1')

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        student = request.form["student"]
        teacher = request.form["teacher"]
        date_str = request.form["date"]
        subject = request.form["subject"]
        course = request.form["course"]
        objective = request.form["objective"]
        coursework = request.form.getlist("coursework")
        progress = request.form["progress"]
        improvement = request.form["improvement"]

        # PDF generation
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "Student Progress Report", ln=True, align='C')

        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 10, f"Student: {sanitize_text(student)}", ln=True)
        pdf.cell(0, 10, f"Teacher: {sanitize_text(teacher)}", ln=True)
        pdf.cell(0, 10, f"Date: {date_str}", ln=True)
        pdf.cell(0, 10, f"Subject: {sanitize_text(subject)}", ln=True)
        pdf.cell(0, 10, f"Course: {sanitize_text(course)}", ln=True)

        pdf.multi_cell(0, 10, f"Objective: {sanitize_text(objective)}")
        pdf.multi_cell(0, 10, f"Coursework Covered:\n- " + "\n- ".join([sanitize_text(c) for c in coursework]))
        pdf.multi_cell(0, 10, f"Progress:\n{sanitize_text(progress)}")
        pdf.multi_cell(0, 10, f"Improvement:\n{sanitize_text(improvement)}")

        filename = f"{student.replace(' ', '_')}_Report.pdf"
        filepath = os.path.join(REPORTS_DIR, filename)
        pdf.output(filepath)

        return send_file(filepath, as_attachment=True)

    return render_template("index.html")


if __name__ == "__main__":
    app.run()
