import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = "users.db"


# ----------------------------------------
# Database Connection
# ----------------------------------------

def get_connection():

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    return conn


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

            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)
            REFERENCES users(id)

        )
    """)

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
    career

):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO resume_history(

            user_id,
            resume_name,
            resume_path,
            ats_score,
            career

        )

        VALUES(?,?,?,?,?)

    """, (

        user_id,
        resume_name,
        resume_path,
        ats_score,
        career

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

    return resume


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

    history = cursor.fetchall()

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
# Delete Resume
# ----------------------------------------

def delete_resume(resume_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(

        "DELETE FROM resume_history WHERE id=?",

        (resume_id,)

    )

    conn.commit()
    conn.close()


# ----------------------------------------
# Delete User
# ----------------------------------------

def delete_user(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(

        "DELETE FROM users WHERE id=?",

        (user_id,)

    )

    conn.commit()
    conn.close()


# ----------------------------------------
# Initialize Database
# ----------------------------------------

create_database()