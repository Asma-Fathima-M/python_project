from flask import Blueprint, render_template, request, redirect, url_for, flash
from backend.db import OracleDB

bp = Blueprint('schedules', __name__)

@bp.route('/')
def list_schedules():
    try:
        conn = OracleDB.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT s.schedule_id, c.course_name, s.day_of_week, 
                   TO_CHAR(s.start_time, 'HH24:MI'), TO_CHAR(s.end_time, 'HH24:MI'),
                   s.room_number, s.semester
            FROM schedules s
            JOIN courses c ON s.course_id = c.course_id
            ORDER BY s.day_of_week, s.start_time
        """)
        schedules = cursor.fetchall()
        
        cursor.execute("SELECT course_id, course_name FROM courses")
        courses = cursor.fetchall()
        
        return render_template('schedules/list.html',
                           schedules=schedules,
                           courses=courses)
    except Exception as e:
        flash('Error loading schedules', 'danger')
        print(f"Error: {e}")
        return render_template('error.html'), 500
    finally:
        if 'conn' in locals():
            conn.close()

@bp.route('/add', methods=['POST'])
def add_schedule():
    try:
        data = request.form
        conn = OracleDB.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO schedules (
                course_id, day_of_week, start_time, end_time, 
                room_number, semester
            ) VALUES (
                :1, :2, TO_TIMESTAMP(:3, 'HH24:MI'), 
                TO_TIMESTAMP(:4, 'HH24:MI'), :5, :6
            )
        """, (
            int(data['course_id']),
            data['day_of_week'],
            data['start_time'],
            data['end_time'],
            data['room_number'],
            data['semester']
        ))
        conn.commit()
        flash('Schedule added!', 'success')
    except Exception as e:
        flash('Failed to add schedule', 'danger')
        print(f"Error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()
    return redirect(url_for('schedules.list_schedules'))

@bp.route('/delete/<int:schedule_id>', methods=['POST'])
def delete_schedule(schedule_id):
    try:
        conn = OracleDB.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM schedules WHERE schedule_id = :1",
            (schedule_id,))
        conn.commit()
        flash('Schedule deleted!', 'success')
    except Exception as e:
        flash('Failed to delete schedule', 'danger')
        print(f"Error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()
    return redirect(url_for('schedules.list_schedules'))