from flask import Blueprint, render_template, request, redirect, url_for, flash
from backend.db import OracleDB

bp = Blueprint('courses', __name__)

# List all courses (READ)
@bp.route('/')
def list_courses():
    try:
        conn = OracleDB.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.course_id, c.course_name, c.description, c.credit_hours,
                   COUNT(e.enrollment_id) as student_count
            FROM courses c
            LEFT JOIN enrollments e ON c.course_id = e.course_id
            GROUP BY c.course_id, c.course_name, c.description, c.credit_hours
            ORDER BY c.course_id
        """)
        courses = cursor.fetchall()
        return render_template('courses/list.html', courses=courses)
    except Exception as e:
        flash('Error loading courses', 'danger')
        print(f"Database error: {e}")
        return render_template('error.html', message="Failed to load courses"), 500
    finally:
        if 'conn' in locals():
            conn.close()

# Add new course (CREATE)
@bp.route('/add', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        try:
            name = request.form['name']
            desc = request.form['description']
            credits = request.form['credits']
            
            if not name or not credits:
                flash('Course name and credits are required', 'warning')
                return redirect(url_for('courses.add_course'))
            
            conn = OracleDB.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO courses (course_name, description, credit_hours) VALUES (:1, :2, :3)",
                (name, desc, int(credits))
            )
            conn.commit()
            flash('Course added successfully!', 'success')
            return redirect(url_for('courses.list_courses'))
        except Exception as e:
            flash('Failed to add course', 'danger')
            print(f"Database error: {e}")
            return render_template('error.html', message="Failed to add course"), 500
        finally:
            if 'conn' in locals():
                conn.close()
    return render_template('courses/add.html')

# Edit existing course (UPDATE)
@bp.route('/edit/<int:course_id>', methods=['GET', 'POST'])
def edit_course(course_id):
    if request.method == 'POST':
        try:
            name = request.form['name']
            desc = request.form['description']
            credits = request.form['credits']
            
            conn = OracleDB.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE courses 
                SET course_name = :1, 
                    description = :2, 
                    credit_hours = :3 
                WHERE course_id = :4""",
                (name, desc, int(credits), course_id)
            )
            conn.commit()
            flash('Course updated successfully!', 'success')
            return redirect(url_for('courses.list_courses'))
        except Exception as e:
            flash('Failed to update course', 'danger')
            print(f"Database error: {e}")
            return render_template('error.html', message="Failed to update course"), 500
        finally:
            if 'conn' in locals():
                conn.close()
    else:
        try:
            conn = OracleDB.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT course_id, course_name, description, credit_hours FROM courses WHERE course_id = :1",
                (course_id,)
            )
            course = cursor.fetchone()
            return render_template('courses/edit.html', course=course)
        except Exception as e:
            flash('Error loading course for editing', 'danger')
            print(f"Database error: {e}")
            return redirect(url_for('courses.list_courses'))
        finally:
            if 'conn' in locals():
                conn.close()

# Delete course (DELETE)
@bp.route('/delete/<int:course_id>', methods=['POST'])
def delete_course(course_id):
    try:
        conn = OracleDB.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM courses WHERE course_id = :1",
            (course_id,)
        )
        conn.commit()
        flash('Course deleted successfully!', 'success')
    except Exception as e:
        flash('Failed to delete course', 'danger')
        print(f"Database error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()
    return redirect(url_for('courses.list_courses'))