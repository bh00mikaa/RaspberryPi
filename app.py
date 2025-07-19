from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load the CSV file
df = pd.read_csv('Daily Report (Authentic Engineers)_DAILY REPORT_Table.csv')

@app.route('/', methods=['GET', 'POST'])
def index():
    report = None
    error = None

    if request.method == 'POST':
        project_number = request.form['project_number'].strip()
        filtered_df = df[df['Project Number'] == project_number]

        if filtered_df.empty:
            error = f"No data found for Project Number: {project_number}"
        else:
            project_name = filtered_df['Project Name'].iloc[0]
            unique_employee = filtered_df['Enter Your Name'].nunique()
            total_project_hours = filtered_df['Hours'].sum()
            project_dates = pd.to_datetime(filtered_df['Date'], errors='coerce').dropna()
            start_date = project_dates.min().strftime('%b %d, %Y')
            end_date = project_dates.max().strftime('%b %d, %Y')
            total_days = (project_dates.max() - project_dates.min()).days + 1
            total_departments = filtered_df['DEPARTMENT'].nunique()

            departments = []
            for dept_name, dept_df in filtered_df.groupby('DEPARTMENT'):
                members = []
                for name in dept_df['Enter Your Name'].unique():
                    person_data = dept_df[dept_df['Enter Your Name'] == name]
                    person_hours = person_data['Hours'].sum()
                    daily = person_data.groupby('Date')['Hours'].sum().reset_index()
                    daily = daily.to_dict(orient='records')
                    members.append({
                        'name': name,
                        'total_hours': round(person_hours, 2),
                        'daily': daily
                    })

                departments.append({
                    'name': dept_name,
                    'employees': len(dept_df['Enter Your Name'].unique()),
                    'hours': round(dept_df['Hours'].sum(), 2),
                    'members': members
                })

            report = {
                'project_number': project_number,
                'project_name': project_name,
                'employees': unique_employee,
                'total_hours': round(total_project_hours, 2),
                'start_date': start_date,
                'end_date': end_date,
                'duration': total_days,
                'departments_count': total_departments,
                'departments': departments
            }

    return render_template('index.html', report=report, error=error)
