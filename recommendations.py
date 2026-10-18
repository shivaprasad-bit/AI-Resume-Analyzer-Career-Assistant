# ----------------------------------------
# AI Recommendation Engine
# ----------------------------------------

def generate_recommendations(score, missing_skills):

    recommendations = []
    score = score or 0

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

        "azure": "Learn Microsoft Azure fundamentals.",

        "artificial intelligence": "Build AI projects that show clear problem-solving and measurable outcomes.",

        "data analysis": "Add data analysis projects with clear insights, charts, and business impact.",

        "data science": "Build data science projects covering cleaning, modeling, evaluation, and storytelling.",

        "opencv": "Create computer vision projects using OpenCV and document the results.",

        "mongodb": "Practice MongoDB schema design, queries, indexes, and CRUD operations.",

        "express.js": "Build Express.js APIs with routing, validation, authentication, and error handling.",

        "tailwind css": "Practice building responsive interfaces with Tailwind CSS utility classes.",

        "rest api": "Build REST APIs with clean endpoints, validation, status codes, and documentation.",

        "nlp": "Build NLP projects such as text classification, summarization, or resume parsing.",

        "scikit-learn": "Practice Scikit-learn workflows for preprocessing, training, evaluation, and tuning.",

        "spring boot": "Build Spring Boot REST APIs with database integration and layered architecture.",

        "postgresql": "Practice PostgreSQL schema design, joins, indexing, and query optimization.",

        "docker": "Containerize your projects with Docker and include setup instructions.",

        "kubernetes": "Learn Kubernetes basics such as pods, deployments, services, and scaling."

    }
    generic_skill_tip = "Add practical proof for {skill}, such as a project, certification, or measurable resume bullet."

    # ====================================
    # Skill-Based Recommendations
    # ====================================

    for skill in missing_skills:

        skill_name = skill.lower()
        tip = skill_tips.get(skill_name)

        if not tip:

            tip = generic_skill_tip.format(skill=skill)

        recommendations.append(tip)

    # ====================================
    # Remove Duplicates
    # ====================================

    recommendations = list(dict.fromkeys(recommendations))

    return recommendations
