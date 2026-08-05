# ----------------------------------------
# AI Recommendation Engine
# ----------------------------------------

def generate_recommendations(score, missing_skills):

    recommendations = []

    # ====================================
    # ATS Score Recommendations
    # ====================================

    if score < 40:

        recommendations.append(
            "Your ATS score is very low. Improve your resume by adding technical skills, projects, certifications, and achievements."
        )

    elif score < 60:

        recommendations.append(
            "Your ATS score is below average. Add more technical skills and practical projects."
        )

    elif score < 80:

        recommendations.append(
            "Good resume. Improve it by adding certifications, internships, and GitHub projects."
        )

    elif score < 90:

        recommendations.append(
            "Very good resume. Add advanced skills and measurable achievements to stand out."
        )

    else:

        recommendations.append(
            "Excellent resume! Keep your profile updated with new projects and certifications."
        )

    # ====================================
    # Skill Learning Suggestions
    # ====================================

    skill_tips = {

        "python": "Practice Python daily and solve coding problems.",

        "java": "Learn Core Java and Object-Oriented Programming concepts.",

        "sql": "Practice SQL queries and database normalization.",

        "mysql": "Learn MySQL database design and optimization.",

        "machine learning": "Build Machine Learning projects using Scikit-learn.",

        "deep learning": "Study Neural Networks and Deep Learning concepts.",

        "tensorflow": "Build Deep Learning applications using TensorFlow.",

        "keras": "Learn Keras for building Deep Learning models.",

        "flask": "Develop Flask web applications and REST APIs.",

        "django": "Learn Django to build scalable web applications.",

        "html": "Improve HTML structure and semantic elements.",

        "css": "Practice responsive web design using CSS.",

        "javascript": "Build interactive web applications with JavaScript.",

        "react": "Learn React to develop modern frontend applications.",

        "node.js": "Learn backend development using Node.js.",

        "power bi": "Create dashboards using Power BI.",

        "tableau": "Learn Tableau for business intelligence.",

        "statistics": "Study Statistics for Data Science and Analytics.",

        "excel": "Master Excel formulas, PivotTables, and charts.",

        "pandas": "Practice data manipulation using Pandas.",

        "numpy": "Learn numerical computing using NumPy.",

        "git": "Learn Git version control and GitHub workflow.",

        "github": "Upload your projects to GitHub regularly.",

        "aws": "Learn AWS Cloud fundamentals.",

        "azure": "Learn Microsoft Azure fundamentals."

    }

    # ====================================
    # Skill-Based Recommendations
    # ====================================

    for skill in missing_skills:

        tip = skill_tips.get(skill.lower())

        if tip:

            recommendations.append(tip)

    # ====================================
    # Remove Duplicates
    # ====================================

    recommendations = list(dict.fromkeys(recommendations))

    # ====================================
    # Sort Recommendations
    # ====================================

    recommendations.sort()

    return recommendations