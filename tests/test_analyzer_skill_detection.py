import unittest
from unittest.mock import MagicMock, patch

with patch.dict("sys.modules", {"PyPDF2": MagicMock()}):
    import analyzer
    from analyzer import detect_skills, extract_text, normalize_resume_text


class SkillDetectionTests(unittest.TestCase):
    def test_c_is_not_detected_inside_regular_words(self):
        text = "Career college certificate work includes communication and coaching."

        self.assertNotIn("c", detect_skills(text))

    def test_c_and_cpp_are_distinguished(self):
        self.assertEqual(detect_skills("Built systems with C++ and Python."), ["c++", "python"])
        self.assertEqual(detect_skills("Built systems with C and Python."), ["c", "python"])
        self.assertEqual(detect_skills("Built systems with C, C++, and Python."), ["c", "c++", "python"])

    def test_java_does_not_match_inside_javascript(self):
        self.assertEqual(detect_skills("Frontend work with JavaScript and React."), ["javascript", "react"])
        self.assertEqual(detect_skills("Backend work with Java and SQL."), ["java", "sql"])

    def test_sql_and_mysql_are_distinguished(self):
        self.assertEqual(detect_skills("Database experience with MySQL."), ["mysql"])
        self.assertEqual(detect_skills("Database experience with SQL."), ["sql"])
        self.assertEqual(detect_skills("Database experience with SQL and MySQL."), ["mysql", "sql"])

    def test_punctuation_based_skills_are_detected(self):
        self.assertEqual(
            detect_skills("Built APIs using Node.js, Flask, and Git."),
            ["flask", "git", "node.js"],
        )

    def test_phase_5b_common_stack_skills_are_detected(self):
        text = "Built MERN apps with MongoDB, Express.js, React, Node.js, Tailwind CSS, and Docker."

        self.assertEqual(
            detect_skills(text),
            ["css", "docker", "express.js", "mongodb", "node.js", "react", "tailwind css"],
        )

    def test_phase_5b_aliases_return_canonical_skill_names(self):
        text = "Used JS, nodejs, PowerBI, Open CV, sklearn, Postgres, and RESTful APIs."

        self.assertEqual(
            detect_skills(text),
            ["javascript", "node.js", "opencv", "postgresql", "power bi", "rest api", "scikit-learn"],
        )

    def test_phase_5b_ai_aliases_are_detected(self):
        text = "Projects include AI, ML, NLP, and natural language processing."

        self.assertEqual(
            detect_skills(text),
            ["artificial intelligence", "machine learning", "nlp"],
        )

    def test_phase_5b_avoids_alias_substring_false_positives(self):
        text = "This reactive design uses expressway maps, docks, and javascripted notes."

        self.assertEqual(detect_skills(text), [])

    def test_phase_5c_normalizes_pdf_spacing_artifacts(self):
        text = "Worked with Pyt-\n hon, C ++, Node . js, Express . js, and Scikit - Learn."

        self.assertEqual(
            normalize_resume_text(text),
            "worked with python, c++, node.js, express.js, and scikit-learn.",
        )

    def test_phase_5c_normalizes_profile_links(self):
        text = "GitHub . com/shiva\nLinkedIn . com/in/shiva"

        self.assertEqual(
            normalize_resume_text(text),
            "github.com/shiva linkedin.com/in/shiva",
        )

    def test_phase_5c_extract_text_skips_empty_pages_and_normalizes_output(self):
        page_with_text = MagicMock()
        page_with_text.extract_text.return_value = "Node . js and C ++"
        empty_page = MagicMock()
        empty_page.extract_text.return_value = None

        with patch.object(analyzer, "PdfReader", return_value=MagicMock(pages=[page_with_text, empty_page])):
            self.assertEqual(extract_text("resume.pdf"), "node.js and c++")

    def test_phase_5c_normalized_text_improves_skill_detection(self):
        text = normalize_resume_text("Built APIs with Node . js, Express . js, and Scikit - Learn.")

        self.assertEqual(
            detect_skills(text),
            ["express.js", "node.js", "scikit-learn"],
        )


if __name__ == "__main__":
    unittest.main()
