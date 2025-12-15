from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'

# Database configuration: Use /tmp on Vercel (serverless), instance/ locally
# Vercel's filesystem is read-only except /tmp, so SQLite must be stored there
if os.environ.get('VERCEL'):
    db_path = '/tmp/studytrackr.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
else:
    # Local development: use instance/ directory (Flask convention)
    os.makedirs('instance', exist_ok=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/studytrackr.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Initialize database tables (works for both local and Vercel)
# This ensures tables exist when the app starts
with app.app_context():
    db.create_all()

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    courses = db.relationship('Course', backref='user', lazy=True, cascade='all, delete-orphan')

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    estimated_grade = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sessions = db.relationship('StudySession', backref='course', lazy=True, cascade='all, delete-orphan')

class StudySession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    hours = db.Column(db.Float, nullable=False)
    note = db.Column(db.Text, nullable=True)

def grade_to_gpa(grade):
    """Convert 0-100 grade to 4.0 GPA scale"""
    if grade >= 93:
        return 4.0
    elif grade >= 90:
        return 3.7
    elif grade >= 87:
        return 3.3
    elif grade >= 83:
        return 3.0
    elif grade >= 80:
        return 2.7
    elif grade >= 77:
        return 2.3
    elif grade >= 73:
        return 2.0
    elif grade >= 70:
        return 1.7
    elif grade >= 67:
        return 1.3
    elif grade >= 65:
        return 1.0
    else:
        return 0.0

# Auth routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'error')
            return redirect(url_for('register'))
        
        password_hash = generate_password_hash(password)
        user = User(username=username, email=email, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    courses = Course.query.filter_by(user_id=user.id).all()
    
    # Calculate GPA
    total_credits = 0
    total_points = 0.0
    
    for course in courses:
        gpa_points = grade_to_gpa(course.estimated_grade)
        total_points += gpa_points
        total_credits += 1
    
    gpa = total_points / total_credits if total_credits > 0 else 0.0
    
    # Prepare chart data
    chart_labels = []
    chart_data = []
    
    for course in courses:
        total_hours = sum(session.hours for session in course.sessions)
        chart_labels.append(course.name)
        chart_data.append(total_hours)
    
    return render_template('dashboard.html', 
                         courses=courses, 
                         gpa=round(gpa, 2), 
                         chart_labels=chart_labels,
                         chart_data=chart_data)

@app.route('/courses', methods=['GET', 'POST'])
def courses():
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        estimated_grade = int(request.form.get('estimated_grade'))
        
        course = Course(name=name, estimated_grade=estimated_grade, user_id=session['user_id'])
        db.session.add(course)
        db.session.commit()
        
        flash('Course added successfully!', 'success')
        return redirect(url_for('courses'))
    
    user = User.query.get(session['user_id'])
    courses_list = Course.query.filter_by(user_id=user.id).all()
    return render_template('courses.html', courses=courses_list)

@app.route('/courses/<int:id>/delete', methods=['POST'])
def delete_course(id):
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))
    
    course = Course.query.get_or_404(id)
    if course.user_id != session['user_id']:
        flash('Unauthorized access', 'error')
        return redirect(url_for('courses'))
    
    db.session.delete(course)
    db.session.commit()
    flash('Course deleted successfully!', 'success')
    return redirect(url_for('courses'))

@app.route('/sessions', methods=['GET', 'POST'])
def sessions():
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        course_id = int(request.form.get('course_id'))
        date_str = request.form.get('date')
        hours = float(request.form.get('hours'))
        note = request.form.get('note', '')
        
        # Verify course belongs to user
        course = Course.query.get(course_id)
        if not course or course.user_id != session['user_id']:
            flash('Invalid course', 'error')
            return redirect(url_for('sessions'))
        
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        session_obj = StudySession(course_id=course_id, date=date, hours=hours, note=note)
        db.session.add(session_obj)
        db.session.commit()
        
        flash('Study session added successfully!', 'success')
        return redirect(url_for('sessions'))
    
    user = User.query.get(session['user_id'])
    courses_list = Course.query.filter_by(user_id=user.id).all()
    sessions_list = StudySession.query.join(Course).filter(Course.user_id == user.id).order_by(StudySession.date.desc()).all()
    return render_template('sessions.html', courses=courses_list, sessions=sessions_list)

@app.route('/sessions/<int:id>/delete', methods=['POST'])
def delete_session(id):
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))
    
    session_obj = StudySession.query.get_or_404(id)
    if session_obj.course.user_id != session['user_id']:
        flash('Unauthorized access', 'error')
        return redirect(url_for('sessions'))
    
    db.session.delete(session_obj)
    db.session.commit()
    flash('Study session deleted successfully!', 'success')
    return redirect(url_for('sessions'))

# Local development entry point
# Database tables are already initialized above, so we can just run the app
if __name__ == '__main__':
    app.run(debug=True)

