import unittest

from career import career_match_percentage, get_career_details, recommend_career
from skill_gap import find_missing_skills, skill_match_percentage


class CareerRecommendationTests(unittest.TestCase):
    def test_full_stack_recommendation_uses_phase_5b_skills(self):
        skills = [
            "javascript",
            "react",
            "node.js",
            "express.js",
            "mongodb",
            "tailwind css",
            "rest api",
            "docker",
        ]

        self.assertEqual(recommend_career(skills), "Full Stack Developer")

    def test_ai_recommendation_uses_modern_ml_skills(self):
        skills = [
            "python",
            "artificial intelligence",
            "machine learning",
            "scikit-learn",
            "nlp",
            "numpy",
            "pandas",
        ]

        self.assertEqual(recommend_career(skills), "AI / Machine Learning Engineer")

    def test_data_analyst_recommendation_prefers_analytics_stack(self):
        skills = ["sql", "excel", "power bi", "tableau", "data analysis", "pandas"]

        self.assertEqual(recommend_career(skills), "Data Analyst")

    def test_no_matching_skills_returns_general_software_engineer(self):
        self.assertEqual(recommend_career(["communication", "leadership"]), "General Software Engineer")

    def test_match_percentages_use_same_career_requirements(self):
        skills = ["java", "spring boot", "sql", "rest api"]

        self.assertEqual(
            career_match_percentage("Java Developer", skills),
            skill_match_percentage("Java Developer", skills),
        )

    def test_missing_skills_follow_recommended_career_map(self):
        skills = ["javascript", "react", "node.js", "express.js", "mongodb", "rest api"]
        career = recommend_career(skills)

        self.assertEqual(career, "Full Stack Developer")
        self.assertIn("docker", find_missing_skills(career, skills))
        self.assertIn("docker", get_career_details(career)["required_skills"])


if __name__ == "__main__":
    unittest.main()
