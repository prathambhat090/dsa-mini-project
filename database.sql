
CREATE DATABASE IF NOT EXISTS student_db;

USE student_db;

CREATE TABLE IF NOT EXISTS students (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    course VARCHAR(100) NOT NULL,
    semester INT NOT NULL
);

-- Sample student records
INSERT IGNORE INTO students
(name, email, course, semester)
VALUES
('Rahul Sharma', 'rahul@example.com', 'BCA', 3),
('Priya Kumar', 'priya@example.com', 'BSc CS', 2);

-- Display all student records
SELECT * FROM students;
