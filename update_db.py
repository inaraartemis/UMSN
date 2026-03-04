import sqlite3
import os

DATABASE = 'database/university.db'

def update_db():
    print(f"Connecting to {DATABASE}...")
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Create Drive Registrations table
    print("Creating drive_registrations table...")
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
    print("Creating event_registrations table...")
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
        # Create Announcements table
    print("Creating announcements table...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS announcements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Add admin user if not exists
    print("Checking for admin user...")
    cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
    if cursor.fetchone()[0] == 0:
        print("Adding admin user...")
        cursor.execute("""
            INSERT INTO users (username, password, user_type, full_name, email)
            VALUES ('admin', 'admin123', 'admin', 'System Administrator', 'admin@university.edu')
        """)

    # Update Placement Drives table schema if needed (adding description column if missing)
    # SQLite doesn't support IF NOT EXISTS for columns, so we check first
    print("Checking placement_drives schema...")
    cursor.execute("PRAGMA table_info(placement_drives)")
    columns = [info[1] for info in cursor.fetchall()]
    
    if 'description' not in columns:
        print("Adding description column to placement_drives...")
        cursor.execute("ALTER TABLE placement_drives ADD COLUMN description TEXT")
        
        # update description for existing records
        cursor.execute("UPDATE placement_drives SET description = 'No description available.' WHERE description IS NULL")
    
    # NEW MIGRATION: Add Arpita's credentials
    print("Adding/Updating credentials for Arpita (12309622)...")
    cursor.execute("SELECT id FROM users WHERE username = '12309622'")
    user = cursor.fetchone()
    if not user:
        cursor.execute("""
            INSERT INTO users (username, password, user_type, full_name, email)
            VALUES ('12309622', 'arpita2005', 'student', 'Arpita', 'arpita@university.edu')
        """)
        user_id = cursor.lastrowid
        cursor.execute("""
            INSERT INTO students (user_id, student_id, program, semester, cgpa)
            VALUES (?, '12309622', 'Computer Science', 6, 9.0)
        """, (user_id,))
    else:
        cursor.execute("UPDATE users SET password = 'arpita2005' WHERE username = '12309622'")

    # NEW MIGRATION: Fix password for user 2024001 (Ananjay)
    print("Fixing password for student 2024001...")
    cursor.execute("UPDATE users SET password = 'ananjay2005' WHERE username = '2024001'")
    
    conn.commit()
    conn.close()
    print("Database updated successfully!")

if __name__ == "__main__":
    if os.path.exists(DATABASE):
        update_db()
    else:
        print(f"Database file {DATABASE} not found!")
