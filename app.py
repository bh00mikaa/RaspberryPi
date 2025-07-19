from flask import Flask, render_template, request, send_file
import pandas as pd
import io

app = Flask(__name__)

df = pd.read_csv('Daily Report (Authentic Engineers)_DAILY REPORT_Table.csv')

@app.route('/', methods=['GET', 'POST'])
def index():
    report = None
    error = None
    selected_number = None

    # Get all unique project numbers for dropdown
    all_project_numbers = sorted(df['Project Number'].dropna().unique())

    if request.method == 'POST':
        project_number = request.form['project_number'].strip()
        selected_number = project_number
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

    return render_template('index.html', report=report, error=error,
                           all_project_numbers=all_project_numbers, selected_number=selected_number)

@app.route('/download', methods=['POST'])
def download():
    project_number = request.form['project_number'].strip()
    filtered_df = df[df['Project Number'] == project_number]

    if filtered_df.empty:
        return "No data found.", 404

    buffer = io.StringIO()
    project_name = filtered_df['Project Name'].iloc[0]
    buffer.write(f"Project Number: {project_number}\n")
    buffer.write(f"Project Name: {project_name}\n\n")

    total_hours = filtered_df['Hours'].sum()
    buffer.write(f"Total Hours: {total_hours:.2f}\n")
    buffer.write(f"Departments Involved: {filtered_df['DEPARTMENT'].nunique()}\n\n")

    for dept_name, dept_df in filtered_df.groupby('DEPARTMENT'):
        buffer.write(f"Department: {dept_name}\n")
        buffer.write(f"  - Employees: {dept_df['Enter Your Name'].nunique()}\n")
        buffer.write(f"  - Hours: {dept_df['Hours'].sum():.2f}\n")

        for name in dept_df['Enter Your Name'].unique():
            person_data = dept_df[dept_df['Enter Your Name'] == name]
            person_hours = person_data['Hours'].sum()
            buffer.write(f"    👤 {name} - {person_hours:.2f} hrs\n")
            daily = person_data.groupby('Date')['Hours'].sum().reset_index()
            for _, row in daily.iterrows():
                buffer.write(f"      • {row['Date']}: {row['Hours']} hrs\n")
        buffer.write("\n")

    buffer.seek(0)
    return send_file(
        io.BytesIO(buffer.getvalue().encode()),
        as_attachment=True,
        download_name=f'report_{project_number}.txt',
        mimetype='text/plain'
    )
from flask import Flask, render_template, request, send_file
import pandas as pd
import io

app = Flask(__name__)

df = pd.read_csv('Daily Report (Authentic Engineers)_DAILY REPORT_Table.csv')

@app.route('/', methods=['GET', 'POST'])
def index():
    report = None
    error = None
    selected_number = None

    # Get all unique project numbers for dropdown
    all_project_numbers = sorted(df['Project Number'].dropna().unique())

    if request.method == 'POST':
        project_number = request.form['project_number'].strip()
        selected_number = project_number
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

    return render_template('index.html', report=report, error=error,
                           all_project_numbers=all_project_numbers, selected_number=selected_number)

@app.route('/download', methods=['POST'])
def download():
    project_number = request.form['project_number'].strip()
    filtered_df = df[df['Project Number'] == project_number]

    if filtered_df.empty:
        return "No data found.", 404

    buffer = io.StringIO()
    project_name = filtered_df['Project Name'].iloc[0]
    buffer.write(f"Project Number: {project_number}\n")
    buffer.write(f"Project Name: {project_name}\n\n")

    total_hours = filtered_df['Hours'].sum()
    buffer.write(f"Total Hours: {total_hours:.2f}\n")
    buffer.write(f"Departments Involved: {filtered_df['DEPARTMENT'].nunique()}\n\n")

    for dept_name, dept_df in filtered_df.groupby('DEPARTMENT'):
        buffer.write(f"Department: {dept_name}\n")
        buffer.write(f"  - Employees: {dept_df['Enter Your Name'].nunique()}\n")
        buffer.write(f"  - Hours: {dept_df['Hours'].sum():.2f}\n")

        for name in dept_df['Enter Your Name'].unique():
            person_data = dept_df[dept_df['Enter Your Name'] == name]
            person_hours = person_data['Hours'].sum()
            buffer.write(f"    👤 {name} - {person_hours:.2f} hrs\n")
            daily = person_data.groupby('Date')['Hours'].sum().reset_index()
            for _, row in daily.iterrows():
                buffer.write(f"      • {row['Date']}: {row['Hours']} hrs\n")
        buffer.write("\n")

    buffer.seek(0)
    return send_file(
        io.BytesIO(buffer.getvalue().encode()),
        as_attachment=True,
        download_name=f'report_{project_number}.txt',
        mimetype='text/plain'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
