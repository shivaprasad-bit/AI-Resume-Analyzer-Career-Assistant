# ----------------------------------------
# Career Skill Database
# ----------------------------------------

CAREER_PATHS = {

    "AI / Machine Learning Engineer": [
        "python",
        "artificial intelligence",
        "machine learning",
        "deep learning",
        "scikit-learn",
        "tensorflow",
        "keras",
        "numpy",
        "pandas",
        "nlp",
        "opencv",
        "sql"
    ],

    "Data Analyst": [
        "python",
        "sql",
        "excel",
        "power bi",
        "tableau",
        "data analysis",
        "data science",
        "statistics",
        "numpy",
        "pandas"
    ],

    "Python Developer": [
        "python",
        "flask",
        "django",
        "html",
        "css",
        "javascript",
        "mysql",
        "postgresql",
        "rest api",
        "git",
        "docker"
    ],

    "Java Developer": [
        "java",
        "spring boot",
        "mysql",
        "postgresql",
        "sql",
        "html",
        "css",
        "rest api",
        "git"
    ],

    "Full Stack Developer": [
        "html",
        "css",
        "javascript",
        "tailwind css",
        "react",
        "node.js",
        "express.js",
        "python",
        "flask",
        "mysql",
        "mongodb",
        "rest api",
        "git",
        "docker"
    ]

}


# ----------------------------------------
# Recommend Career
# ----------------------------------------

def recommend_career(user_skills):

    user_skills = set(skill.lower() for skill in user_skills)

    best_career = "General Software Engineer"
    best_score = (0, 0, 0)

    for career, required_skills in CAREER_PATHS.items():

        required_skill_set = set(required_skills)
        matched_skills = user_skills & required_skill_set
        matched = len(matched_skills)

        if matched == 0:

            continue

        percentage = matched / len(required_skill_set)
        coverage = matched / len(user_skills) if user_skills else 0
        score = (percentage, matched, coverage)

        if score > best_score:

            best_score = score
            best_career = career

    return best_career


# ----------------------------------------
# Career Match Percentage
# ----------------------------------------

def career_match_percentage(career, user_skills):

    user_skills = set(skill.lower() for skill in user_skills)

    required_skills = CAREER_PATHS.get(career, [])

    if not required_skills:
        return 0

    matched = len(user_skills & set(required_skills))

    percentage = int((matched / len(required_skills)) * 100)

    return percentage


# ----------------------------------------
# Career Details
# ----------------------------------------

def get_career_details(career):

    return {

        "career": career,

        "required_skills": CAREER_PATHS.get(career, [])

    }


# ----------------------------------------
# All Careers
# ----------------------------------------

def get_all_careers():

    return sorted(CAREER_PATHS.keys())
