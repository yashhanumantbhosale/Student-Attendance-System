from flask import Flask, render_template, request, redirect
import pandas as pd
import os

if not os.path.exists('students.xlsx'):
    import pandas as pd
    data = {
        'Student ID': ['S001', 'S002', 'S003', 'S004'],
        'Name': ['Sameer', 'Abhii', 'Yash','Mayur'],
        'Attendance': [0, 0, 0, 0],
        'Total Classes': [0, 0, 0 ,0],
    }
    df = pd.DataFrame(data)
    df.to_excel('students.xlsx', index=False)

app = Flask(__name__)
EXCEL_FILE = 'students.xlsx'

# Home Page
@app.route('/')
def home():
    df = pd.read_excel(EXCEL_FILE)
    df['Percentage'] = (df['Attendance'] / df['Total Classes'].replace(0, 1)) * 100
    return render_template('home.html', students=df.to_dict(orient='records'))

# Mark Attendance
@app.route('/mark', methods=['GET', 'POST'])
def mark():
    df = pd.read_excel(EXCEL_FILE)

    if request.method == 'POST':
        present_ids = request.form.getlist('present')
        df['Total Classes'] += 1
        df.loc[df['Student ID'].isin(present_ids), 'Attendance'] += 1
        df.to_excel(EXCEL_FILE, index=False)
        return redirect('/')

    return render_template('mark.html', students=df.to_dict(orient='records'))

# Attendance Report
@app.route('/report')
def report():
    df = pd.read_excel(EXCEL_FILE)
    df['Percentage'] = (df['Attendance'] / df['Total Classes'].replace(0, 1)) * 100
    return render_template('report.html', students=df.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)