import unittest

from history_insights import build_history_progress


class HistoryInsightTests(unittest.TestCase):
    def test_build_history_progress_compares_each_resume_to_previous_upload(self):
        resumes = [
            {"resume_name": "latest.pdf", "ats_score": 82},
            {"resume_name": "middle.pdf", "ats_score": 70},
            {"resume_name": "oldest.pdf", "ats_score": 74},
        ]

        progress = build_history_progress(resumes)

        self.assertEqual(progress[0]["score_change"], 12)
        self.assertEqual(progress[0]["progress_label"], "Improved")
        self.assertEqual(progress[0]["progress_status"], "positive")
        self.assertEqual(progress[1]["score_change"], -4)
        self.assertEqual(progress[1]["progress_label"], "Dropped")
        self.assertEqual(progress[1]["progress_status"], "negative")
        self.assertIsNone(progress[2]["score_change"])
        self.assertEqual(progress[2]["progress_label"], "First upload")

    def test_build_history_progress_handles_same_score(self):
        resumes = [
            {"resume_name": "latest.pdf", "ats_score": 80},
            {"resume_name": "older.pdf", "ats_score": 80},
        ]

        progress = build_history_progress(resumes)

        self.assertEqual(progress[0]["score_change"], 0)
        self.assertEqual(progress[0]["progress_label"], "No change")
        self.assertEqual(progress[0]["progress_status"], "neutral")

    def test_build_history_progress_handles_missing_scores(self):
        resumes = [
            {"resume_name": "latest.pdf", "ats_score": None},
            {"resume_name": "older.pdf", "ats_score": 80},
        ]

        progress = build_history_progress(resumes)

        self.assertIsNone(progress[0]["score_change"])
        self.assertEqual(progress[0]["progress_label"], "First upload")
        self.assertEqual(progress[0]["progress_status"], "neutral")

    def test_build_history_progress_does_not_mutate_original_rows(self):
        resumes = [{"resume_name": "latest.pdf", "ats_score": 90}]

        progress = build_history_progress(resumes)

        self.assertNotIn("score_change", resumes[0])
        self.assertIn("score_change", progress[0])


if __name__ == "__main__":
    unittest.main()
