import os
import sqlite3
import sys
import tempfile
import types
import unittest

security_module = types.ModuleType("werkzeug.security")
security_module.generate_password_hash = lambda password: "hashed-" + password
security_module.check_password_hash = lambda hashed, password: hashed == "hashed-" + password
werkzeug_module = types.ModuleType("werkzeug")
werkzeug_module.security = security_module
sys.modules.setdefault("werkzeug", werkzeug_module)
sys.modules.setdefault("werkzeug.security", security_module)

import database


class ResumeHistoryDatabaseTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_database = database.DATABASE
        database.DATABASE = os.path.join(self.temp_dir.name, "test_users.db")

    def tearDown(self):
        database.DATABASE = self.original_database
        self.temp_dir.cleanup()

    def test_create_database_adds_analysis_columns(self):
        database.create_database()

        conn = sqlite3.connect(database.DATABASE)
        columns = {
            column[1]
            for column in conn.execute("PRAGMA table_info(resume_history)").fetchall()
        }
        conn.close()

        self.assertIn("skills", columns)
        self.assertIn("missing_skills", columns)
        self.assertIn("recommendations", columns)

    def test_save_resume_stores_analysis_details(self):
        database.create_database()

        database.save_resume(
            1,
            "resume.pdf",
            "uploads/resume.pdf",
            86,
            "Full Stack Developer",
            ["react", "node.js"],
            ["docker"],
            ["Containerize your projects with Docker and include setup instructions."],
        )

        latest = database.get_latest_resume(1)

        self.assertEqual(latest["skills"], ["react", "node.js"])
        self.assertEqual(latest["missing_skills"], ["docker"])
        self.assertEqual(
            latest["recommendations"],
            ["Containerize your projects with Docker and include setup instructions."],
        )

    def test_migration_preserves_older_resume_rows(self):
        conn = sqlite3.connect(database.DATABASE)
        conn.execute(
            """
            CREATE TABLE resume_history(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                resume_name TEXT NOT NULL,
                resume_path TEXT NOT NULL,
                ats_score INTEGER,
                career TEXT,
                upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            """
            INSERT INTO resume_history(user_id, resume_name, resume_path, ats_score, career)
            VALUES(?,?,?,?,?)
            """,
            (1, "old_resume.pdf", "uploads/old_resume.pdf", 70, "Python Developer"),
        )
        conn.commit()
        conn.close()

        database.create_database()
        latest = database.get_latest_resume(1)

        self.assertEqual(latest["resume_name"], "old_resume.pdf")
        self.assertEqual(latest["skills"], [])
        self.assertEqual(latest["missing_skills"], [])
        self.assertEqual(latest["recommendations"], [])


if __name__ == "__main__":
    unittest.main()
