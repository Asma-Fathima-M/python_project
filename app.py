from flask import Flask, g, redirect, url_for, render_template
from dotenv import load_dotenv
import os
import cx_Oracle
from functools import wraps

# 1. Load environment variables FIRST
load_dotenv()

# 2. Create Flask app instance
app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.getenv('SECRET_KEY', 'dev-secret-key'),
    DEBUG=os.getenv('DEBUG', 'False').lower() == 'true',
    TEMPLATES_AUTO_RELOAD=True
)

# 3. Database configuration with validation
required_env_vars = ['DB_USER', 'DB_PASS', 'DB_HOST', 'DB_SERVICE']
missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    raise RuntimeError(f"Missing required environment variables: {', '.join(missing_vars)}")

DB_CONFIG = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'host': os.getenv('DB_HOST'),
    'service': os.getenv('DB_SERVICE'),
    'port': os.getenv('DB_PORT', '1521')
}

# 4. Database connection with enhanced error handling
def get_db():
    """Get a database connection with automatic reconnection"""
    if 'db' not in g:
        try:
            dsn = cx_Oracle.makedsn(
                DB_CONFIG['host'],
                int(DB_CONFIG['port']),
                service_name=DB_CONFIG['service']
            )
            g.db = cx_Oracle.connect(
                user=DB_CONFIG['user'],
                password=DB_CONFIG['password'],
                dsn=dsn,
                encoding='UTF-8',
                threaded=True
            )
            print("Database connection established")
        except cx_Oracle.Error as e:
            error, = e.args
            app.logger.error(f"Database connection failed: Code={error.code}, Message={error.message}")
            raise
    return g.db

# 5. Database cleanup
@app.teardown_appcontext
def close_db(e=None):
    """Ensure connections are closed properly"""
    db = g.pop('db', None)
    if db is not None:
        try:
            db.close()
            print("Database connection closed")
        except Exception as e:
            app.logger.error(f"Error closing database: {str(e)}")

# 6. Blueprint registration with validation
try:
    from .routes.courses import bp as courses_bp
from .routes.schedules import bp as schedules_bp
from .routes.enrollments import bp as enrollments_bp
    
    app.register_blueprint(courses_bp, url_prefix='/courses')
    app.register_blueprint(schedules_bp, url_prefix='/schedules')
    app.register_blueprint(enrollments_bp, url_prefix='/enrollments')
    
    print("Blueprints registered successfully")
except ImportError as e:
    app.logger.critical(f"Failed to register blueprints: {str(e)}")
    raise

# 7. Core routes with error handling
@app.route('/')
def home():
    """Main entry point redirecting to courses"""
    try:
        return redirect(url_for('courses.list_courses'))
    except Exception as e:
        app.logger.error(f"Home redirect failed: {str(e)}")
        return render_template('error.html', message="Service temporarily unavailable"), 503

@app.route('/health')
def health_check():
    """Endpoint for health monitoring"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM DUAL")
        return {'status': 'healthy', 'database': 'connected'}
    except Exception as e:
        return {'status': 'unhealthy', 'error': str(e)}, 500

# 8. Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', message="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', message="Internal server error"), 500

# 9. Main execution
if __name__ == '__main__':
    try:
        # Test database connection before starting
        with app.app_context():
            conn = get_db()
            conn.close()
        
        app.run(
            host=os.getenv('FLASK_HOST', '0.0.0.0'),
            port=int(os.getenv('FLASK_PORT', '5000')),
            debug=app.config['DEBUG'],
            use_reloader=False
        )
    except Exception as e:
        app.logger.critical(f"Failed to start application: {str(e)}")
        raise