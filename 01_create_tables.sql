-- Courses Table
CREATE TABLE courses (
    course_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    course_name VARCHAR2(100) NOT NULL,
    description VARCHAR2(400),
    credit_hours NUMBER(2)
);

-- Instructors Table
CREATE TABLE instructors (
    instructor_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    first_name VARCHAR2(50) NOT NULL,
    last_name VARCHAR2(50) NOT NULL,
    email VARCHAR2(100),
    department VARCHAR2(50)
);

-- Schedules Table
CREATE TABLE schedules (
    schedule_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    course_id NUMBER REFERENCES courses(course_id) ON DELETE CASCADE,
    instructor_id NUMBER REFERENCES instructors(instructor_id),
    day_of_week VARCHAR2(10) CHECK (day_of_week IN ('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday')),
    start_time VARCHAR2(5),
    end_time VARCHAR2(5),
    room_number VARCHAR2(20),
    semester VARCHAR2(20)
);

-- Enrollments Table
CREATE TABLE enrollments (
    enrollment_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    student_id VARCHAR2(20) NOT NULL,
    student_name VARCHAR2(100) NOT NULL,
    course_id NUMBER REFERENCES courses(course_id) ON DELETE CASCADE,
    enrollment_date DATE DEFAULT SYSDATE,
    status VARCHAR2(20) DEFAULT 'Active'
);