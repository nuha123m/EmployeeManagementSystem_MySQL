

CREATE DATABASE ProjectManagement;

USE ProjectManagement;

CREATE TABLE Employee (
    Employee_ID INT AUTO_INCREMENT PRIMARY KEY,
    Employee_Name VARCHAR(255),
    Employee_Email VARCHAR(255),
    Department VARCHAR(255),
    Role VARCHAR(255)
);

CREATE TABLE Manager (
    Manager_ID INT AUTO_INCREMENT PRIMARY KEY,
    Manager_Name VARCHAR(255),
    Manager_Email VARCHAR(255),
    Department VARCHAR(255)
);

CREATE TABLE Project (
    Project_ID INT AUTO_INCREMENT PRIMARY KEY,
    Project_Name VARCHAR(255),
    Project_Description TEXT,
    Start_Date DATE,
    End_Date DATE,
    Project_Budget DECIMAL(10, 2),
    Manager_ID INT,
    Project_Status VARCHAR(50),
    FOREIGN KEY (Manager_ID) REFERENCES Manager(Manager_ID)
);

CREATE TABLE Employee_Project (
    Employee_Project_ID INT AUTO_INCREMENT PRIMARY KEY,
    Employee_ID INT,
    Project_ID INT,
    Role_in_Project VARCHAR(255),
    Hours_Allocated INT,
    Start_Date DATE,
    FOREIGN KEY (Employee_ID) REFERENCES Employee(Employee_ID),
    FOREIGN KEY (Project_ID) REFERENCES Project(Project_ID)
);

CREATE TABLE Task (
    Task_ID INT AUTO_INCREMENT PRIMARY KEY,
    Task_Description TEXT,
    Task_Status VARCHAR(50),
    Task_Priority INT,
    Task_Assignee INT,
    Project_ID INT,
    Estimated_Completion_Time INT,
    Deadline DATE,
    FOREIGN KEY (Task_Assignee) REFERENCES Employee(Employee_ID),
    FOREIGN KEY (Project_ID) REFERENCES Project(Project_ID)
);

CREATE TABLE Milestone (
    Milestone_ID INT AUTO_INCREMENT PRIMARY KEY,
    Milestone_Name VARCHAR(255),
    Milestone_Deadline DATE,
    Project_ID INT,
    FOREIGN KEY (Project_ID) REFERENCES Project(Project_ID)
);

CREATE TABLE Resource (
    Resource_ID INT AUTO_INCREMENT PRIMARY KEY,
    Resource_Type VARCHAR(255),
    Resource_Description TEXT,
    Project_ID INT,
    Resource_Cost DECIMAL(10, 2),
    FOREIGN KEY (Project_ID) REFERENCES Project(Project_ID)
);

CREATE TABLE Documentation (
    Document_ID INT AUTO_INCREMENT PRIMARY KEY,
    Document_Title VARCHAR(255),
    Document_Type VARCHAR(255),
    File_Link TEXT,
    Project_ID INT,
    FOREIGN KEY (Project_ID) REFERENCES Project(Project_ID)
);

