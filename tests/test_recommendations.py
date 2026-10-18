import unittest

from recommendations import generate_recommendations


class RecommendationEngineTests(unittest.TestCase):
    def test_score_recommendation_stays_first(self):
        recommendations = generate_recommendations(55, ["python", "docker"])

        self.assertEqual(
            recommendations[0],
            "Your ATS score is below average. Add more technical skills and practical projects.",
        )
        self.assertIn("Practice Python daily and solve coding problems.", recommendations)
        self.assertIn("Containerize your projects with Docker and include setup instructions.", recommendations)

    def test_phase_5b_skills_have_specific_learning_tips(self):
        recommendations = generate_recommendations(
            82,
            ["mongodb", "express.js", "rest api", "scikit-learn", "spring boot", "postgresql"],
        )

        self.assertIn("Practice MongoDB schema design, queries, indexes, and CRUD operations.", recommendations)
        self.assertIn("Build Express.js APIs with routing, validation, authentication, and error handling.", recommendations)
        self.assertIn("Build REST APIs with clean endpoints, validation, status codes, and documentation.", recommendations)
        self.assertIn(
            "Practice Scikit-learn workflows for preprocessing, training, evaluation, and tuning.",
            recommendations,
        )
        self.assertIn(
            "Build Spring Boot REST APIs with database integration and layered architecture.",
            recommendations,
        )
        self.assertIn("Practice PostgreSQL schema design, joins, indexing, and query optimization.", recommendations)

    def test_unknown_missing_skill_gets_actionable_generic_tip(self):
        recommendations = generate_recommendations(90, ["system design"])

        self.assertIn(
            "Add practical proof for system design, such as a project, certification, or measurable resume bullet.",
            recommendations,
        )

    def test_duplicate_recommendations_are_removed_without_sorting(self):
        recommendations = generate_recommendations(75, ["python", "python"])

        self.assertEqual(recommendations.count("Practice Python daily and solve coding problems."), 1)
        self.assertEqual(
            recommendations[0],
            "Good resume. Improve it by adding certifications, internships, and GitHub projects.",
        )

    def test_none_score_uses_low_score_guidance(self):
        recommendations = generate_recommendations(None, [])

        self.assertEqual(
            recommendations,
            [
                "Your ATS score is very low. Improve your resume by adding technical skills, projects, certifications, and achievements."
            ],
        )


if __name__ == "__main__":
    unittest.main()
