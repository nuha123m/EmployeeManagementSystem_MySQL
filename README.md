# Project Management System  

A web application to manage employees, projects, tasks, milestones, and resources efficiently. Built using Flask and MySQL, this tool helps streamline project workflows and resource allocation for organizations.

---

## Features  
- **User Management**: Secure signup/login with password hashing.  
- **Employee Management**: Add, view, and assign employees to projects.  
- **Project Management**: Manage projects with budgets, timelines, and status tracking.  
- **Task Management**: Add and assign tasks with priorities and deadlines.  
- **Milestone Tracking**: Define and monitor key project milestones.  
- **Resource Allocation**: Manage resources for each project.  
- **Dashboard**: Centralized view of employees, projects, and assignments.  

---

## Tools & Technologies  
- **Backend**: Flask (Python)  
- **Database**: MySQL with SQLAlchemy ORM  
- **Frontend**: HTML, CSS, Bootstrap  
- **Migrations**: Flask-Migrate  
- **Libraries**: PyMySQL, Werkzeug  

---

### Steps to Run the Project

1. **Clone the repository**:
    ```bash
    git clone https://github.com/username/project-management-system.git
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Update `db_config.py` with your MySQL credentials.**

4. **Apply database migrations**:
    ```bash
    flask db upgrade
    ```

5. **Run the application**:
    ```bash
    python app.py
    ```

6. **Open `http://127.0.0.1:5000` in your browser.**
---
