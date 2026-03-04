from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from datetime import datetime, timedelta
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'  # Change this in production!

DATABASE = 'database/university.db'

def get_db_connection():
    """Create a database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    return conn

def init_db():
    """Initialize the database with tables and sample data"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create Users table (for both students and faculty)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            user_type TEXT NOT NULL,
            full_name TEXT NOT NULL,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create Students table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            student_id TEXT UNIQUE NOT NULL,
            program TEXT NOT NULL,
            semester INTEGER NOT NULL,
            cgpa REAL DEFAULT 0.0,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Create Subjects table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_code TEXT UNIQUE NOT NULL,
            subject_name TEXT NOT NULL,
            credits INTEGER NOT NULL
        )
    ''')
    
    # Create Attendance table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            subject_id INTEGER,
            total_classes INTEGER DEFAULT 0,
            attended_classes INTEGER DEFAULT 0,
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (subject_id) REFERENCES subjects(id)
        )
    ''')
    
    # Create Assignments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_id INTEGER,
            title TEXT NOT NULL,
            description TEXT,
            due_date DATE NOT NULL,
            status TEXT DEFAULT 'pending',
            FOREIGN KEY (subject_id) REFERENCES subjects(id)
        )
    ''')
    
    # Create Companies table (for placements)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            visit_date DATE NOT NULL,
            position TEXT NOT NULL,
            package TEXT NOT NULL,
            description TEXT
        )
    ''')
    
    # Create Placement Drives table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS placement_drives (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            position TEXT NOT NULL,
            eligibility_criteria TEXT NOT NULL,
            drive_date DATE NOT NULL,
            status TEXT DEFAULT 'Open',
            min_cgpa REAL DEFAULT 0.0,
            description TEXT
        )
    ''')
    
    # Create Drive Registrations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS drive_registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            drive_id INTEGER,
            registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'Registered',
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (drive_id) REFERENCES placement_drives(id),
            UNIQUE(student_id, drive_id)
        )
    ''')
    

    # Create Event Registrations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS event_registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            event_id INTEGER,
            registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'Registered',
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (event_id) REFERENCES events(id),
            UNIQUE(user_id, event_id)
        )
    ''')

    # Create Events table (university happenings)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_name TEXT NOT NULL,
            event_type TEXT NOT NULL,
            event_date DATE NOT NULL,
            location TEXT,
            description TEXT,
            organizer TEXT
        )
    ''')
    
    # Create Faculty table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS faculty (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            faculty_id TEXT UNIQUE NOT NULL,
            department TEXT NOT NULL,
            designation TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    # Create Announcements table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS announcements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    
    # Insert sample data
    insert_sample_data(conn)
    
    conn.close()
    print("Database initialized successfully!")

def insert_sample_data(conn):
    """Insert sample data for testing"""
    cursor = conn.cursor()
    
    # Check if data already exists
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] > 0:
        return  # Data already exists
    
    # Insert sample users (students, faculty, admin)
    cursor.execute("""
        INSERT INTO users (username, password, user_type, full_name, email)
        VALUES 
        ('12309622', 'arpita2005', 'student', 'Arpita', 'arpita@university.edu'),
        ('2024001', 'ananjay2005', 'student', 'Alex Johnson', 'alex.j@university.edu'),
        ('2024002', 'pass123', 'student', 'Sarah Williams', 'sarah.w@university.edu'),
        ('faculty1', 'pass123', 'faculty', 'Dr. Robert Smith', 'robert.s@university.edu'),
        ('admin', 'admin123', 'admin', 'System Administrator', 'admin@university.edu')
    """)
    
    # Insert student details
    cursor.execute("""
        INSERT INTO students (user_id, student_id, program, semester, cgpa)
        VALUES 
        (1, '2024001', 'Computer Science', 6, 8.7),
        (2, '2024002', 'Information Technology', 6, 8.3)
    """)

    # Insert subjects
    cursor.execute("""
        INSERT INTO subjects (subject_code, subject_name, credits)
        VALUES 
        ('CS301', 'Data Structures', 4),
        ('CS302', 'Database Management Systems', 4),
        ('CS303', 'Operating Systems', 4),
        ('CS304', 'Computer Networks', 3),
        ('CS305', 'Software Engineering', 3)
    """)
    
    # Insert attendance for student 1
    cursor.execute("""
        INSERT INTO attendance (student_id, subject_id, total_classes, attended_classes)
        VALUES 
        (1, 1, 45, 41),
        (1, 2, 40, 35),
        (1, 3, 38, 32),
        (1, 4, 42, 33),
        (1, 5, 40, 38)
    """)
    
    # Insert assignments
    today = datetime.now()
    cursor.execute("""
        INSERT INTO assignments (subject_id, title, description, due_date, status)
        VALUES 
        (2, 'Database Project', 'Design and implement a library management system', ?, 'pending'),
        (3, 'OS Case Study', 'Analyze process scheduling algorithms', ?, 'pending'),
        (4, 'Network Design', 'Design a campus network topology', ?, 'upcoming')
    """, (
        (today + timedelta(days=9)).strftime('%Y-%m-%d'),
        (today + timedelta(days=12)).strftime('%Y-%m-%d'),
        (today + timedelta(days=17)).strftime('%Y-%m-%d')
    ))
    
    # Insert companies visited
    cursor.execute("""
        INSERT INTO companies (company_name, visit_date, position, package, description)
        VALUES 
        ('TechCorp', '2026-02-10', 'Software Engineer', '$95,000', 'Leading technology company'),
        ('DataSystems Inc', '2026-02-12', 'Data Analyst', '$80,000', 'Data analytics firm'),
        ('CloudNine', '2026-02-14', 'Cloud Engineer', '$105,000', 'Cloud computing solutions'),
        ('AI Solutions', '2026-02-15', 'ML Engineer', '$110,000', 'Artificial Intelligence startup')
    """)
    
    # Insert placement drives
    cursor.execute("""
        INSERT INTO placement_drives (company_name, position, eligibility_criteria, drive_date, status, min_cgpa, description)
        VALUES 
        ('MegaTech', 'Full Stack Developer', 'CGPA > 7.5, No backlogs', '2026-02-20', 'Open', 7.5, 'We are looking for a skilled Full Stack Developer to join our dynamic team. You will prompt be working on cutting-edge technologies and building scalable web applications.'),
        ('FinanceHub', 'Software Developer', 'CGPA > 8.0, Strong coding skills', '2026-02-22', 'Open', 8.0, 'Join our fintech revolution! We need software developers with strong algorithmic skills to build high-performance financial systems.'),
        ('StartupX', 'Backend Engineer', 'CGPA > 7.0, Python/Java', '2026-02-25', 'Open', 7.0, 'Fast-paced startup environment. Looking for backend engineers proficient in Python or Java to build robust APIs.'),
        ('GlobalTech', 'DevOps Engineer', 'CGPA > 7.8, Cloud experience', '2026-03-01', 'Upcoming', 7.8, 'Seeking a DevOps Engineer to manage our cloud infrastructure and CI/CD pipelines. Experience with AWS/Azure is a plus.')
    """)
    
    # Insert events
    cursor.execute("""
        INSERT INTO events (event_name, event_type, event_date, location, description, organizer)
        VALUES 
        ('Tech Fest 2026', 'Technical', '2026-03-15', 'Main Auditorium', 'Annual technical festival', 'CSE Department'),
        ('Career Fair', 'Placement', '2026-02-28', 'Sports Complex', 'Meet recruiters from top companies', 'Placement Cell'),
        ('Hackathon', 'Competition', '2026-03-05', 'Computer Lab', '24-hour coding competition', 'Tech Club'),
        ('Cultural Night', 'Cultural', '2026-03-20', 'Open Theater', 'Music, dance, and drama performances', 'Cultural Committee'),
        ('Workshop: Machine Learning', 'Workshop', '2026-02-25', 'Seminar Hall', 'Hands-on ML workshop', 'AI Club'),
        ('Sports Day', 'Sports', '2026-03-10', 'Sports Ground', 'Inter-department sports competition', 'Sports Committee')
    """)
    
    # Insert faculty
    cursor.execute("""
        INSERT INTO faculty (user_id, faculty_id, department, designation)
        VALUES 
        (3, 'FAC2024001', 'Computer Science', 'Professor')
    """)
    
    conn.commit()

# ==================== AUTHENTICATION DECORATOR ====================

def login_required(f):
    """Decorator to require login for protected routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def student_required(f):
    """Decorator to require student login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_type' not in session or session['user_type'] != 'student':
            flash('This page is only accessible to students.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to require admin login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_type' not in session or session['user_type'] != 'admin':
            flash('This page is only accessible to admins.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== ROUTES ====================

@app.route('/')
def index():
    """Home page - redirect to login if not logged in"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page for both students and faculty"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Query database for user
        conn = get_db_connection()
        user = conn.execute(
            'SELECT * FROM users WHERE username = ? AND password = ?',
            (username, password)
        ).fetchone()
        conn.close()
        
        if user:
            # Set session variables
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['user_type'] = user['user_type']
            session['full_name'] = user['full_name']
            
            flash(f'Welcome back, {user["full_name"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout user and clear session"""
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile page"""
    conn = get_db_connection()
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'update_details':
            email = request.form.get('email')
            conn.execute('UPDATE users SET email = ? WHERE id = ?', (email, session['user_id']))
            conn.commit()
            flash('Profile details updated successfully!', 'success')
            
        elif action == 'change_password':
            current_password = request.form.get('current_password')
            new_password = request.form.get('new_password')
            confirm_password = request.form.get('confirm_password')
            
            # Verify current password
            user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
            if user['password'] != current_password:
                flash('Incorrect current password.', 'danger')
            elif new_password != confirm_password:
                flash('New passwords do not match.', 'danger')
            else:
                conn.execute('UPDATE users SET password = ? WHERE id = ?', (new_password, session['user_id']))
                conn.commit()
                flash('Password changed successfully!', 'success')
        
        conn.close()
        return redirect(url_for('profile'))
    
    # GET request
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    conn.close()
    
    return render_template('profile.html', user=user)

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard with 3 tiles"""
    conn = get_db_connection()
    
    # Get student/faculty specific data
    if session['user_type'] == 'student':
        student = conn.execute('''
            SELECT s.* FROM students s
            WHERE s.user_id = ?
        ''', (session['user_id'],)).fetchone()
        
        # Get attendance summary
        attendance_summary = conn.execute('''
            SELECT 
                COUNT(*) as total_subjects,
                AVG(CAST(attended_classes AS FLOAT) / total_classes * 100) as avg_attendance
            FROM attendance
            WHERE student_id = ?
        ''', (student['id'],)).fetchone()
        
        # Get pending assignments count
        pending_assignments = conn.execute('''
            SELECT COUNT(*) as count FROM assignments
            WHERE status = 'pending' AND due_date >= date('now')
        ''').fetchone()
        
        # Get upcoming placement drives count
        eligible_drives = conn.execute('''
            SELECT COUNT(*) as count FROM placement_drives
            WHERE status = 'Open' AND min_cgpa <= ?
        ''', (student['cgpa'],)).fetchone()
        
        # Get upcoming events count
        upcoming_events = conn.execute('''
            SELECT COUNT(*) as count FROM events
            WHERE event_date >= date('now')
        ''').fetchone()
        
        # Get recent announcements
        announcements = conn.execute('''
            SELECT * FROM announcements 
            ORDER BY created_at DESC 
            LIMIT 5
        ''').fetchall()
        
        # Get fellow students (Peers) in the same program
        classmates = conn.execute('''
            SELECT u.full_name, u.email, s.program
            FROM students s
            JOIN users u ON s.user_id = u.id
            WHERE s.program = ? AND s.user_id != ?
            LIMIT 6
        ''', (student['program'], session['user_id'])).fetchall()
        
        conn.close()
        
        dashboard_data = {
            'student': student,
            'attendance_summary': attendance_summary,
            'pending_assignments': pending_assignments['count'],
            'eligible_drives': eligible_drives['count'],
            'upcoming_events': upcoming_events['count'],
            'announcements': announcements,
            'classmates': classmates
        }
        
        return render_template('dashboard.html', data=dashboard_data)
    
    else:  # Faculty
        faculty = conn.execute('''
            SELECT f.* FROM faculty f
            WHERE f.user_id = ?
        ''', (session['user_id'],)).fetchone()
        
        # Get recent announcements
        announcements = conn.execute('''
            SELECT * FROM announcements 
            ORDER BY created_at DESC 
            LIMIT 5
        ''').fetchall()
        
        conn.close()
        
        dashboard_data = {
            'faculty': faculty,
            'announcements': announcements
        }
        
        return render_template('dashboard_faculty.html', data=dashboard_data)

@app.route('/academics')
@login_required
@student_required
def academics():
    """Academics page - detailed view"""
    conn = get_db_connection()
    
    # Get student info
    student = conn.execute('''
        SELECT s.* FROM students s
        WHERE s.user_id = ?
    ''', (session['user_id'],)).fetchone()
    
    # Get detailed attendance with subject info
    attendance_data = conn.execute('''
        SELECT 
            s.subject_name,
            s.subject_code,
            a.total_classes,
            a.attended_classes,
            CAST(a.attended_classes AS FLOAT) / a.total_classes * 100 as percentage
        FROM attendance a
        JOIN subjects s ON a.subject_id = s.id
        WHERE a.student_id = ?
        ORDER BY percentage DESC
    ''', (student['id'],)).fetchall()
    
    # Get all assignments
    assignments = conn.execute('''
        SELECT 
            a.id,
            a.title,
            a.description,
            a.due_date,
            a.status,
            s.subject_name
        FROM assignments a
        JOIN subjects s ON a.subject_id = s.id
        WHERE a.due_date >= date('now')
        ORDER BY a.due_date ASC
    ''').fetchall()
    
    conn.close()
    
    return render_template('academics.html', 
                         student=student, 
                         attendance=attendance_data, 
                         assignments=assignments)

@app.route('/placements')
@login_required
@student_required
def placements():
    """Placement portal page"""
    conn = get_db_connection()
    
    # Get student info for eligibility check
    student = conn.execute('''
        SELECT s.* FROM students s
        WHERE s.user_id = ?
    ''', (session['user_id'],)).fetchone()
    
    # Get companies visited
    companies = conn.execute('''
        SELECT * FROM companies
        ORDER BY visit_date DESC
        LIMIT 10
    ''').fetchall()
    
    # Get registered drives
    registered_drives = conn.execute('''
        SELECT pd.*, dr.registration_date, dr.status as reg_status
        FROM placement_drives pd
        JOIN drive_registrations dr ON pd.id = dr.drive_id
        WHERE dr.student_id = ?
        ORDER BY pd.drive_date ASC
    ''', (student['id'],)).fetchall()
    
    # Get eligible placement drives (excluding registered ones)
    eligible_drives = conn.execute('''
        SELECT * FROM placement_drives
        WHERE min_cgpa <= ? 
        AND status = 'Open'
        AND id NOT IN (SELECT drive_id FROM drive_registrations WHERE student_id = ?)
        ORDER BY drive_date ASC
    ''', (student['cgpa'], student['id'])).fetchall()
    
    # Get all upcoming drives
    all_drives = conn.execute('''
        SELECT * FROM placement_drives
        WHERE status IN ('Open', 'Upcoming')
        ORDER BY drive_date ASC
    ''').fetchall()
    
    conn.close()
    
    return render_template('placements.html', 
                         student=student,
                         companies=companies, 
                         eligible_drives=eligible_drives,
                         registered_drives=registered_drives,
                         all_drives=all_drives)

@app.route('/apply-drive', methods=['POST'])
@login_required
@student_required
def apply_drive():
    """Register for a placement drive"""
    drive_id = request.form.get('drive_id')
    
    conn = get_db_connection()
    
    try:
        # Get student info
        student = conn.execute('SELECT id FROM students WHERE user_id = ?', (session['user_id'],)).fetchone()
        
        # Check if already registered
        existing = conn.execute('''
            SELECT * FROM drive_registrations 
            WHERE student_id = ? AND drive_id = ?
        ''', (student['id'], drive_id)).fetchone()
        
        if existing:
            flash('You have already registered for this drive.', 'warning')
        else:
            conn.execute('''
                INSERT INTO drive_registrations (student_id, drive_id)
                VALUES (?, ?)
            ''', (student['id'], drive_id))
            conn.commit()
            flash('Successfully registered for the placement drive!', 'success')
            
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'danger')
        
    finally:
        conn.close()
        
    return redirect(url_for('placements'))

@app.route('/events')
@login_required
def events():
    """University events and happenings page"""
    conn = get_db_connection()
    
    # Get upcoming events
    upcoming = conn.execute('''
        SELECT * FROM events
        WHERE event_date >= date('now')
        ORDER BY event_date ASC
    ''').fetchall()
    
    # Get past events
    past = conn.execute('''
        SELECT * FROM events
        WHERE event_date < date('now')
        ORDER BY event_date DESC
        LIMIT 5
    ''').fetchall()
    
    # Get registered events for current user
    registered_events = conn.execute('''
        SELECT e.*, er.registration_date
        FROM events e
        JOIN event_registrations er ON e.id = er.event_id
        WHERE er.user_id = ?
        ORDER BY er.registration_date DESC
    ''', (session['user_id'],)).fetchall()
    
    # Get recent announcements
    announcements = conn.execute('''
        SELECT * FROM announcements 
        ORDER BY created_at DESC 
        LIMIT 5
    ''').fetchall()
    
    conn.close()
    
    return render_template('events.html', 
                         upcoming_events=upcoming, 
                         past_events=past,
                         registered_events=registered_events,
                         announcements=announcements)

@app.route('/register-event/<int:event_id>', methods=['POST'])
@login_required
def register_event(event_id):
    """Register for an event"""
    conn = get_db_connection()
    
    try:
        # Check if already registered
        existing = conn.execute('''
            SELECT * FROM event_registrations 
            WHERE user_id = ? AND event_id = ?
        ''', (session['user_id'], event_id)).fetchone()
        
        if existing:
            flash('You are already registered for this event.', 'warning')
        else:
            conn.execute('''
                INSERT INTO event_registrations (user_id, event_id)
                VALUES (?, ?)
            ''', (session['user_id'], event_id))
            conn.commit()
            flash('Successfully registered for the event!', 'success')
            
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'danger')
        
    finally:
        conn.close()
        
    return redirect(url_for('events'))
# ==================== ADMIN ROUTES ====================

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get stats
    cursor.execute("SELECT COUNT(*) FROM students")
    student_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM faculty")
    faculty_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM placement_drives")
    drive_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM events")
    event_count = cursor.fetchone()[0]
    
    # Get recent announcements
    cursor.execute("SELECT * FROM announcements ORDER BY created_at DESC LIMIT 5")
    announcements = cursor.fetchall()
    
    conn.close()
    return render_template('admin_dashboard.html', 
                           student_count=student_count, 
                           faculty_count=faculty_count,
                           drive_count=drive_count,
                           event_count=event_count,
                           announcements=announcements)

@app.route('/admin/add_user', methods=['GET', 'POST'])
@admin_required
def admin_add_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['user_type']
        full_name = request.form['full_name']
        email = request.form['email']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("INSERT INTO users (username, password, user_type, full_name, email) VALUES (?, ?, ?, ?, ?)",
                           (username, password, user_type, full_name, email))
            user_id = cursor.lastrowid
            
            if user_type == 'student':
                student_id = request.form['student_id']
                program = request.form['program']
                semester = request.form['semester']
                cursor.execute("INSERT INTO students (user_id, student_id, program, semester) VALUES (?, ?, ?, ?)",
                               (user_id, student_id, program, semester))
            elif user_type == 'faculty':
                faculty_id = request.form['faculty_id']
                department = request.form['department']
                designation = request.form['designation']
                cursor.execute("INSERT INTO faculty (user_id, faculty_id, department, designation) VALUES (?, ?, ?, ?)",
                               (user_id, faculty_id, department, designation))
            
            conn.commit()
            flash(f'Successfully added {user_type}: {full_name}', 'success')
        except sqlite3.IntegrityError:
            flash('Username or ID already exists!', 'danger')
        finally:
            conn.close()
            
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin_add_user.html')

@app.route('/admin/students')
@admin_required
def admin_students():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.id, u.full_name, s.student_id, s.program, s.semester, s.cgpa 
        FROM students s 
        JOIN users u ON s.user_id = u.id
    """)
    students = cursor.fetchall()
    conn.close()
    return render_template('admin_students.html', students=students)

@app.route('/admin/student/<int:student_id>')
@admin_required
def admin_student_detail(student_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get student info
    cursor.execute("""
        SELECT s.*, u.full_name, u.email 
        FROM students s 
        JOIN users u ON s.user_id = u.id 
        WHERE s.id = ?
    """, (student_id,))
    student = cursor.fetchone()
    
    if not student:
        conn.close()
        flash('Student not found!', 'danger')
        return redirect(url_for('admin_students'))
    
    # Get attendance
    cursor.execute("""
        SELECT a.*, s.subject_name, s.subject_code 
        FROM attendance a 
        JOIN subjects s ON a.subject_id = s.id 
        WHERE a.student_id = ?
    """, (student_id,))
    attendance = cursor.fetchall()
    
    conn.close()
    return render_template('student_detail.html', student=student, attendance=attendance, admin_view=True)

@app.route('/admin/add_drive', methods=['POST'])
@admin_required
def admin_add_drive():
    company_name = request.form['company_name']
    position = request.form['position']
    eligibility = request.form['eligibility']
    drive_date = request.form['drive_date']
    min_cgpa = request.form['min_cgpa']
    description = request.form['description']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO placement_drives (company_name, position, eligibility_criteria, drive_date, min_cgpa, description)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (company_name, position, eligibility, drive_date, min_cgpa, description))
    conn.commit()
    conn.close()
    flash('Placement drive added successfully!', 'success')
    return redirect(url_for('placements'))

@app.route('/admin/delete_drive/<int:drive_id>')
@admin_required
def admin_delete_drive(drive_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM placement_drives WHERE id = ?", (drive_id,))
    cursor.execute("DELETE FROM drive_registrations WHERE drive_id = ?", (drive_id,))
    conn.commit()
    conn.close()
    flash('Placement drive removed!', 'info')
    return redirect(url_for('placements'))

@app.route('/admin/add_event', methods=['POST'])
@admin_required
def admin_add_event():
    event_name = request.form['event_name']
    event_type = request.form['event_type']
    event_date = request.form['event_date']
    location = request.form['location']
    description = request.form['description']
    organizer = request.form['organizer']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO events (event_name, event_type, event_date, location, description, organizer)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (event_name, event_type, event_date, location, description, organizer))
    conn.commit()
    conn.close()
    flash('Event added successfully!', 'success')
    return redirect(url_for('events'))

@app.route('/admin/delete_event/<int:event_id>')
@admin_required
def admin_delete_event(event_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))
    cursor.execute("DELETE FROM event_registrations WHERE event_id = ?", (event_id,))
    conn.commit()
    conn.close()
    flash('Event removed!', 'info')
    return redirect(url_for('events'))

@app.route('/admin/add_announcement', methods=['POST'])
@admin_required
def admin_add_announcement():
    title = request.form['title']
    content = request.form['content']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO announcements (title, content) VALUES (?, ?)", (title, content))
    conn.commit()
    conn.close()
    flash('Announcement posted!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete_announcement/<int:ann_id>')
@admin_required
def admin_delete_announcement(ann_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM announcements WHERE id = ?", (ann_id,))
    conn.commit()
    conn.close()
    flash('Announcement removed!', 'info')
    return redirect(url_for('admin_dashboard'))

# ==================== INITIALIZE DATABASE ON FIRST RUN ====================

if not os.path.exists('database'):
    os.makedirs('database')

if not os.path.exists(DATABASE):
    init_db()

# ==================== FACULTY ROUTES ====================

@app.route('/faculty/classes')
@login_required
def faculty_classes():
    """Get faculty classes for popup"""
    if session['user_type'] != 'faculty':
        return {'error': 'Unauthorized'}, 403
    
    conn = get_db_connection()
    
    # Get all subjects (in real app, filter by faculty)
    classes = conn.execute('''
        SELECT 
            s.id,
            s.subject_code,
            s.subject_name,
            s.credits,
            COUNT(DISTINCT st.id) as student_count
        FROM subjects s
        LEFT JOIN attendance a ON s.id = a.subject_id
        LEFT JOIN students st ON a.student_id = st.id
        GROUP BY s.id
    ''').fetchall()
    
    conn.close()
    
    return render_template('faculty_classes_popup.html', classes=classes)


@app.route('/faculty/mark-attendance/<int:subject_id>')
@login_required
def mark_attendance(subject_id):
    """Show attendance marking form"""
    if session['user_type'] != 'faculty':
        return {'error': 'Unauthorized'}, 403
    
    conn = get_db_connection()
    
    # Get subject details
    subject = conn.execute('SELECT * FROM subjects WHERE id = ?', (subject_id,)).fetchone()
    
    # Get all students with their attendance for this subject
    students = conn.execute('''
        SELECT 
            s.id,
            s.student_id,
            u.full_name,
            s.program,
            s.semester,
            COALESCE(a.total_classes, 0) as total_classes,
            COALESCE(a.attended_classes, 0) as attended_classes,
            a.id as attendance_id
        FROM students s
        JOIN users u ON s.user_id = u.id
        LEFT JOIN attendance a ON s.id = a.student_id AND a.subject_id = ?
        ORDER BY u.full_name
    ''', (subject_id,)).fetchall()
    
    conn.close()
    
    return render_template('mark_attendance_popup.html', subject=subject, students=students)


@app.route('/faculty/save-attendance', methods=['POST'])
@login_required
def save_attendance():
    """Save attendance marks"""
    if session['user_type'] != 'faculty':
        return {'error': 'Unauthorized'}, 403
    
    subject_id = request.form.get('subject_id')
    attended_students = request.form.getlist('attended[]')  # List of student IDs who attended
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get all students for this subject
    students = conn.execute('''
        SELECT s.id, a.id as attendance_id
        FROM students s
        LEFT JOIN attendance a ON s.id = a.student_id AND a.subject_id = ?
    ''', (subject_id,)).fetchall()
    
    for student in students:
        student_id = student['id']
        attendance_id = student['attendance_id']
        is_present = str(student_id) in attended_students
        
        if attendance_id:
            # Update existing record
            cursor.execute('''
                UPDATE attendance 
                SET total_classes = total_classes + 1,
                    attended_classes = attended_classes + ?
                WHERE id = ?
            ''', (1 if is_present else 0, attendance_id))
        else:
            # Create new record
            cursor.execute('''
                INSERT INTO attendance (student_id, subject_id, total_classes, attended_classes)
                VALUES (?, ?, 1, ?)
            ''', (student_id, subject_id, 1 if is_present else 0))
    
    conn.commit()
    conn.close()
    
    flash('Attendance marked successfully!', 'success')
    return redirect(url_for('dashboard'))


@app.route('/faculty/assignments')
@login_required
def faculty_assignments():
    """Get all assignments for faculty"""
    if session['user_type'] != 'faculty':
        return {'error': 'Unauthorized'}, 403
    
    conn = get_db_connection()
    
    assignments = conn.execute('''
        SELECT 
            a.id,
            a.title,
            a.description,
            a.due_date,
            a.status,
            s.subject_name,
            s.subject_code
        FROM assignments a
        JOIN subjects s ON a.subject_id = s.id
        ORDER BY a.due_date DESC
    ''').fetchall()
    
    # Get subjects for the add form
    subjects = conn.execute('SELECT id, subject_name, subject_code FROM subjects').fetchall()
    
    conn.close()
    
    return render_template('faculty_assignments_popup.html', assignments=assignments, subjects=subjects)


@app.route('/faculty/add-assignment', methods=['POST'])
@login_required
def add_assignment():
    """Add new assignment"""
    if session['user_type'] != 'faculty':
        return {'error': 'Unauthorized'}, 403
    
    subject_id = request.form.get('subject_id')
    title = request.form.get('title')
    description = request.form.get('description')
    due_date = request.form.get('due_date')
    
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO assignments (subject_id, title, description, due_date, status)
        VALUES (?, ?, ?, ?, 'pending')
    ''', (subject_id, title, description, due_date))
    conn.commit()
    conn.close()
    
    flash('Assignment added successfully!', 'success')
    return redirect(url_for('faculty_assignments'))


@app.route('/faculty/edit-assignment/<int:assignment_id>', methods=['POST'])
@login_required
def edit_assignment(assignment_id):
    """Edit existing assignment"""
    if session['user_type'] != 'faculty':
        return {'error': 'Unauthorized'}, 403
    
    title = request.form.get('title')
    description = request.form.get('description')
    due_date = request.form.get('due_date')
    status = request.form.get('status')
    
    conn = get_db_connection()
    conn.execute('''
        UPDATE assignments 
        SET title = ?, description = ?, due_date = ?, status = ?
        WHERE id = ?
    ''', (title, description, due_date, status, assignment_id))
    conn.commit()
    conn.close()
    
    flash('Assignment updated successfully!', 'success')
    return redirect(url_for('faculty_assignments'))


@app.route('/faculty/delete-assignment/<int:assignment_id>', methods=['POST'])
@login_required
def delete_assignment(assignment_id):
    """Delete assignment"""
    if session['user_type'] != 'faculty':
        return {'error': 'Unauthorized'}, 403
    
    conn = get_db_connection()
    conn.execute('DELETE FROM assignments WHERE id = ?', (assignment_id,))
    conn.commit()
    conn.close()
    
    flash('Assignment deleted successfully!', 'success')
    return redirect(url_for('faculty_assignments'))


@app.route('/faculty/reports')
@login_required
def faculty_reports():
    """View all students and their reports"""
    if session['user_type'] != 'faculty':
        return {'error': 'Unauthorized'}, 403
    
    conn = get_db_connection()
    
    # Get all students with basic info
    students = conn.execute('''
        SELECT 
            s.id,
            s.student_id,
            u.full_name,
            s.program,
            s.semester,
            s.cgpa,
            u.email
        FROM students s
        JOIN users u ON s.user_id = u.id
        ORDER BY u.full_name
    ''').fetchall()
    
    conn.close()
    
    return render_template('faculty_reports_popup.html', students=students)


@app.route('/faculty/student-detail/<int:student_id>')
@login_required
def student_detail(student_id):
    """Get detailed report for a specific student"""
    if session['user_type'] != 'faculty':
        return {'error': 'Unauthorized'}, 403
    
    conn = get_db_connection()
    
    # Get student info
    student = conn.execute('''
        SELECT 
            s.id,
            s.student_id,
            u.full_name,
            s.program,
            s.semester,
            s.cgpa,
            u.email
        FROM students s
        JOIN users u ON s.user_id = u.id
        WHERE s.id = ?
    ''', (student_id,)).fetchone()
    
    # Get attendance details
    attendance = conn.execute('''
        SELECT 
            s.subject_name,
            s.subject_code,
            a.total_classes,
            a.attended_classes,
            CAST(a.attended_classes AS FLOAT) / a.total_classes * 100 as percentage
        FROM attendance a
        JOIN subjects s ON a.subject_id = s.id
        WHERE a.student_id = ?
    ''', (student_id,)).fetchall()
    
    # Get assignments status
    assignments = conn.execute('''
        SELECT 
            a.title,
            s.subject_name,
            a.due_date,
            a.status
        FROM assignments a
        JOIN subjects s ON a.subject_id = s.id
        ORDER BY a.due_date DESC
    ''').fetchall()
    
    conn.close()
    
    return render_template('student_detail_popup.html', 
                         student=student, 
                         attendance=attendance,
                         assignments=assignments)

# ==================== RUN APPLICATION ====================

if __name__ == '__main__':
    app.run(debug=True, port=8000)
