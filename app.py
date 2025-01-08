from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import datetime

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Antares@123'
app.config['MYSQL_DB'] = 'ProjectManagement'
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

from flask import request, redirect, url_for

@app.route('/manager_dashboard')
def manager_dashboard():
    return render_template('manager_dashboard.html')


@app.route('/update-status', methods=['POST'])
def update_project_status():
    project_id = request.form['project_id']  # Get project ID from form data

    try:
        # Create a database cursor
        cursor = mysql.connection.cursor()

        # Update query to mark project status as 'Done'
        update_query = """
            UPDATE Project 
            SET Project_Status = 'Done' 
            WHERE Project_ID = %s
        """
        cursor.execute(update_query, (project_id,))  # Execute query with parameterized input

        # Commit changes to the database
        mysql.connection.commit()

        # Close the cursor
        cursor.close()
    except Exception as e:
        print(f"Error: {e}")
        return "Failed to update project status", 500

    # Redirect back to a projects page or another route
    return redirect(url_for('view_employee_projects')) 

@app.route('/manager', methods=['GET', 'POST'])
def manager():
    if request.method == 'GET':
            cur = mysql.connection.cursor()
            cur.execute("SELECT Project_ID, Project_Name FROM Project")
            projects = cur.fetchall()  # Fetch all projects
            cur.close()
            return render_template('manager.html', projects=projects)
        
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add_manager':
            # Insert manager details into the Manager table
            manager_name = request.form['manager_name']
            manager_email = request.form['manager_email']
            manager_department = request.form['manager_department']

            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO Manager (Manager_Name, Manager_Email, Department)
                VALUES (%s, %s, %s)
            """, (manager_name, manager_email, manager_department))
            mysql.connection.commit()
            cur.close()
            return redirect('/manager')

        elif action == 'add_employee':
            # Insert employee details into the Employee table
            employee_name = request.form['employee_name']
            employee_email = request.form['employee_email']
            department = request.form['department']
            role = request.form['role']

            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO Employee (Employee_Name, Employee_Email, Department, Role)
                VALUES (%s, %s, %s, %s)
            """, (employee_name, employee_email, department, role))
            mysql.connection.commit()
            cur.close()
            return redirect('/manager')
        
        
        elif 'create_project' in request.form:
            # Gather project data
            name = request.form['name']
            desc = request.form['desc']
            start_date = request.form['start_date']
            end_date = request.form['end_date']
            budget = request.form['budget']
            manager_id = request.form['manager_id']
            status = request.form['status']

            # Gather milestone data
            milestone_name = request.form['milestone_name']
            milestone_deadline = request.form['milestone_deadline']

            # Gather resource data
            resource_type = request.form['resource_type']
            resource_desc = request.form['resource_desc']
            resource_cost = request.form['resource_cost']

            # Gather documentation data
            doc_title = request.form['doc_title']
            doc_type = request.form['doc_type']
            file_link = request.form['file_link']

            # Insert into Project table
            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO Project (Project_Name, Project_Description, Start_Date, End_Date, Project_Budget, Manager_ID, Project_Status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (name, desc, start_date, end_date, budget, manager_id, status))
            project_id = cur.lastrowid  # Get the Project_ID of the inserted project

            # Insert into Milestone table
            if milestone_name:
                cur.execute("""
                    INSERT INTO Milestone (Milestone_Name, Milestone_Deadline, Project_ID)
                    VALUES (%s, %s, %s)
                """, (milestone_name, milestone_deadline, project_id))

            # Insert into Resource table
            if resource_type:
                cur.execute("""
                    INSERT INTO Resource (Resource_Type, Resource_Description, Project_ID, Resource_Cost)
                    VALUES (%s, %s, %s, %s)
                """, (resource_type, resource_desc, project_id, resource_cost))

            # Insert into Documentation table
            if doc_title:
                cur.execute("""
                    INSERT INTO Documentation (Document_Title, Document_Type, File_Link, Project_ID)
                    VALUES (%s, %s, %s, %s)
                """, (doc_title, doc_type, file_link, project_id))

            # Commit and close connection
            mysql.connection.commit()
            cur.close()
            return redirect('/manager')
        
        elif 'create_task' in request.form:
            # Gather task data
            task_desc = request.form['task_desc']
            task_status = request.form['task_status']
            task_priority = request.form['task_priority']
            task_assignee = request.form['task_assignee']
            estimated_time = request.form['estimated_time']
            task_deadline = request.form['task_deadline']
            project_id = request.form['project_id']

            cur = mysql.connection.cursor()

            # Validate Project_ID
            cur.execute("SELECT COUNT(*) FROM Project WHERE Project_ID = %s", (project_id,))
            project_exists = cur.fetchone()[0]

            if not project_exists:
                # Handle case where Project_ID doesn't exist
                return "Error: Project_ID does not exist. Please link the task to an existing project.", 400

            # Insert task into the Task table
            cur.execute("""
                INSERT INTO Task (Task_Description, Task_Status, Task_Priority, Task_Assignee, Project_ID, Estimated_Completion_Time, Deadline)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (task_desc, task_status, task_priority, task_assignee, project_id, estimated_time, task_deadline))

            mysql.connection.commit()
            cur.close()
            return redirect('/manager')

        
        elif 'assign_employee' in request.form:
            cur = mysql.connection.cursor()
            emp_id = request.form['employee_id']
            proj_id = request.form['project_id']
            role = request.form['role']
            hours = request.form['hours']
            start_date = request.form['start_date']
            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO Employee_Project (Employee_ID, Project_ID, Role_in_Project, Hours_Allocated, Start_Date) 
                VALUES (%s, %s, %s, %s, %s)
            """, (emp_id, proj_id, role, hours, start_date))
            mysql.connection.commit()
            cur.close()
            return redirect('/manager')
    return render_template('manager.html')

@app.route('/employee', methods=['GET', 'POST'])
def employee():
    if request.method == 'POST':
        emp_id = request.form['employee_id']
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT * FROM Project 
            JOIN Employee_Project ON Project.Project_ID = Employee_Project.Project_ID 
            WHERE Employee_Project.Employee_ID = %s
        """, [emp_id])
        projects = cur.fetchall()
        cur.close()
        return render_template('view_project.html', projects=projects)
    return render_template('employee.html')

@app.route('/view_projects')
def view_projects():
    cur = mysql.connection.cursor()
    # Fetch all projects with details
    cur.execute("""
        SELECT * FROM Project
    """)
    projects = cur.fetchall()

    project_details = []
    for project in projects:
        project_id = project[0]

        # Fetch associated tasks
        cur.execute("""
            SELECT * FROM Task WHERE Project_ID = %s
        """, [project_id])
        tasks = cur.fetchall()

        # Fetch associated milestones
        cur.execute("""
            SELECT * FROM Milestone WHERE Project_ID = %s
        """, [project_id])
        milestones = cur.fetchall()

        # Fetch associated resources
        cur.execute("""
            SELECT * FROM Resource WHERE Project_ID = %s
        """, [project_id])
        resources = cur.fetchall()

        # Fetch associated documentation
        cur.execute("""
            SELECT * FROM Documentation WHERE Project_ID = %s
        """, [project_id])
        documentation = cur.fetchall()

        project_details.append({
            'project': project,
            'tasks': tasks,
            'milestones': milestones,
            'resources': resources,
            'documentation': documentation
        })

    cur.close()
    return render_template('view_projects.html', project_details=project_details)

@app.route('/view_employee_projects', methods=['GET', 'POST'])
def view_employee_projects():
    if request.method == 'POST':
        emp_id = request.form['employee_id']

        cur = mysql.connection.cursor()
        # Fetch projects assigned to the employee
        cur.execute("""
            SELECT Project.* FROM Project 
            JOIN Employee_Project ON Project.Project_ID = Employee_Project.Project_ID 
            WHERE Employee_Project.Employee_ID = %s
        """, [emp_id])
        projects = cur.fetchall()

        project_details = []
        for project in projects:
            project_id = project[0]

            # Fetch associated tasks
            cur.execute("""
                SELECT * FROM Task WHERE Project_ID = %s
            """, [project_id])
            tasks = cur.fetchall()

            # Fetch associated milestones
            cur.execute("""
                SELECT * FROM Milestone WHERE Project_ID = %s
            """, [project_id])
            milestones = cur.fetchall()

            # Fetch associated resources
            cur.execute("""
                SELECT * FROM Resource WHERE Project_ID = %s
            """, [project_id])
            resources = cur.fetchall()

            # Fetch associated documentation
            cur.execute("""
                SELECT * FROM Documentation WHERE Project_ID = %s
            """, [project_id])
            documentation = cur.fetchall()

            project_details.append({
                'project': project,
                'tasks': tasks,
                'milestones': milestones,
                'resources': resources,
                'documentation': documentation
            })

        cur.close()
        return render_template('view_employee_projects.html', project_details=project_details)
    return render_template('employee.html')  # Display employee login


if __name__ == '__main__':
    app.run(debug=True)
