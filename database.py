
import json
import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = os.path.abspath(
    os.environ.get("CAREERAI_DATABASE_PATH", "users.db")
)

RESUME_ANALYSIS_COLUMNS = {
    "skills": "TEXT",
    "missing_skills": "TEXT",
    "recommendations": "TEXT",
}


# ----------------------------------------
# Database Connection
# ----------------------------------------

def get_connection():

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    return conn


def serialize_list(items):

    return json.dumps(items or [])


def decode_resume_row(row):

    if row is None:

        return None

    resume = dict(row)

    for field in RESUME_ANALYSIS_COLUMNS:

        try:

            resume[field] = json.loads(resume.get(field) or "[]")

        except json.JSONDecodeError:

            resume[field] = []

    return resume


def migrate_resume_history(cursor):

    cursor.execute("PRAGMA table_info(resume_history)")

    existing_columns = {
        column["name"]
        for column in cursor.fetchall()
    }

    for column, column_type in RESUME_ANALYSIS_COLUMNS.items():

        if column not in existing_columns:

            cursor.execute(
                f"ALTER TABLE resume_history ADD COLUMN {column} {column_type}"
            )


# ----------------------------------------
# Create Database
# ----------------------------------------

def create_database():

    conn = get_connection()
    cursor = conn.cursor()

    # Users Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            fullname TEXT NOT NULL,

            email TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL

        )
    """)

    # Resume History Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resume_history(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            resume_name TEXT NOT NULL,

            resume_path TEXT NOT NULL,

            ats_score INTEGER,

            career TEXT,

            skills TEXT,

            missing_skills TEXT,

            recommendations TEXT,

            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)
            REFERENCES users(id)

        )
    """)

    migrate_resume_history(cursor)

    conn.commit()
    conn.close()
# ----------------------------------------
# Register User
# ----------------------------------------

def register_user(fullname, email, password):

    conn = get_connection()
    cursor = conn.cursor()

    hashed_password = generate_password_hash(password)

    try:

        cursor.execute("""

            INSERT INTO users(

                fullname,
                email,
                password

            )

            VALUES(?,?,?)

        """, (

            fullname,
            email,
            hashed_password

        ))

        conn.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        conn.close()


# ----------------------------------------
# Login User
# ----------------------------------------

def login_user(email, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(

        "SELECT * FROM users WHERE email=?",

        (email,)

    )

    user = cursor.fetchone()

    conn.close()

    if user and check_password_hash(
        user["password"],
        password
    ):

        return user

    return None
# ----------------------------------------
# Save Resume
# ----------------------------------------

def save_resume(

    user_id,
    resume_name,
    resume_path,
    ats_score,
    career,
    skills=None,
    missing_skills=None,
    recommendations=None

):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO resume_history(

            user_id,
            resume_name,
            resume_path,
            ats_score,
            career,
            skills,
            missing_skills,
            recommendations

        )

        VALUES(?,?,?,?,?,?,?,?)

    """, (

        user_id,
        resume_name,
        resume_path,
        ats_score,
        career,
        serialize_list(skills),
        serialize_list(missing_skills),
        serialize_list(recommendations)

    ))

    conn.commit()
    conn.close()


# ----------------------------------------
# Latest Resume
# ----------------------------------------

def get_latest_resume(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT *

        FROM resume_history

        WHERE user_id=?

        ORDER BY upload_date DESC

        LIMIT 1

    """, (user_id,))

    resume = cursor.fetchone()

    conn.close()

    return decode_resume_row(resume)


# ----------------------------------------
# Resume History
# ----------------------------------------

def get_resume_history(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT *

        FROM resume_history

        WHERE user_id=?

        ORDER BY upload_date DESC

    """, (user_id,))

    history = [
        decode_resume_row(resume)
        for resume in cursor.fetchall()
    ]

    conn.close()

    return history
# ----------------------------------------
# Get User By ID
# ----------------------------------------

def get_user_by_id(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(

        "SELECT * FROM users WHERE id=?",

        (user_id,)

    )

    user = cursor.fetchone()

    conn.close()

    return user


# ----------------------------------------
# Get Resume By ID
# ----------------------------------------

def get_resume_by_id(resume_id, user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM resume_history
        WHERE id=? AND user_id=?
        """,
        (resume_id, user_id)
    )

    resume = cursor.fetchone()

    conn.close()

    return decode_resume_row(resume)


# ----------------------------------------
# Delete Resume
# ----------------------------------------

def delete_resume(resume_id, user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM resume_history
        WHERE id=? AND user_id=?
        """,
        (resume_id, user_id)
    )

    deleted = cursor.rowcount > 0

    conn.commit()
    conn.close()

    return deleted
