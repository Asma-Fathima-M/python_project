from flask import Blueprint, render_template, request, redirect, url_for, flash
from backend.db import OracleDB

bp = Blueprint('enrollments', __name__)

@bp.route('/')
def list_enrollments():
    try:
        conn = OracleDB.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT e.enrollment_id, e.student_name, c.course_name
            FROM enrollments e
            JOIN courses c ON e.course_id = c.course_id
        """)
        enrollments = cursor.fetchall()
        
        cursor.execute("SELECT course_id, course_name FROM courses")
        courses = cursor.fetchall()
        
        return render_template('enrollments/list.html',
                           enrollments=enrollments,
                           courses=courses)
    except Exception as e:
        flash('Error loading enrollments', 'danger')
        print(f"Error: {e}")
        return render_template('error.html'), 500
    finally:
        if 'conn' in locals():
            conn.close()

@bp.route('/add', methods=['POST'])
def add_enrollment():
    try:
        student_name = request.form['student_name']
        course_id = request.form['course_id']
        
        conn = OracleDB.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO enrollments (student_name, course_id)
            VALUES (:1, :2)
        """, (student_name, int(course_id)))
        
        conn.commit()
        flash('Student enrolled!', 'success')
    except Exception as e:
        flash('Failed to enroll student', 'danger')
        print(f"Error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()
    return redirect(url_for('enrollments.list_enrollments'))

@bp.route('/delete/<int:enrollment_id>', methods=['POST'])
def delete_enrollment(enrollment_id):
    try:
        conn = OracleDB.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM enrollments WHERE enrollment_id = :1",
            (enrollment_id,))
        conn.commit()
        flash('Enrollment removed!', 'success')
    except Exception as e:
        flash('Failed to remove enrollment', 'danger')
        print(f"Error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()
    return redirect(url_for('enrollments.list_enrollments'))