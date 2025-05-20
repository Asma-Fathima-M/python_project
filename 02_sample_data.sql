-- COURSES
INSERT INTO courses (course_name, description, credit_hours) VALUES 
('CS101', 'Introduction to Computer Science', 3);

INSERT INTO courses (course_name, description, credit_hours) VALUES 
('MATH201', 'Calculus I', 4);

INSERT INTO courses (course_name, description, credit_hours) VALUES 
('ENG105', 'Academic Writing', 3);

-- INSTRUCTORS
INSERT INTO instructors (first_name, last_name, email, department) VALUES 
('John', 'Smith', 'jsmith@university.edu', 'Computer Science');

INSERT INTO instructors (first_name, last_name, email, department) VALUES 
('Sarah', 'Johnson', 'sjohnson@university.edu', 'Mathematics');

INSERT INTO instructors (first_name, last_name, email, department) VALUES 
('Robert', 'Lee', 'rlee@university.edu', 'English');

-- SCHEDULES (must run after courses and instructors)
INSERT INTO schedules (course_id, instructor_id, day_of_week, start_time, end_time, room_number, semester) VALUES 
(1, 1, 'Monday', '09:00', '10:30', 'Room 101', 'Fall 2023');

INSERT INTO schedules (course_id, instructor_id, day_of_week, start_time, end_time, room_number, semester) VALUES 
(2, 2, 'Tuesday', '13:00', '14:30', 'Room 205', 'Fall 2023');

-- ENROLLMENTS
INSERT INTO enrollments (student_id, student_name, course_id) VALUES 
('S1001', 'Alice Johnson', 1);

INSERT INTO enrollments (student_id, student_name, course_id) VALUES 
('S1002', 'Bob Williams', 2);

COMMIT;