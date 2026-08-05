# ----------------------------------------
# Career Skill Database
# ----------------------------------------

CAREER_PATHS = {

    "AI / Machine Learning Engineer": [
        "python",
        "machine learning",
        "deep learning",
        "tensorflow",
        "keras",
        "numpy",
        "pandas",
        "sql"
    ],

    "Data Analyst": [
        "python",
        "sql",
        "excel",
        "power bi",
        "tableau",
        "statistics",
        "pandas"
    ],

    "Python Developer": [
        "python",
        "flask",
        "django",
        "html",
        "css",
        "javascript",
        "mysql"
    ],

    "Java Developer": [
        "java",
        "spring",
        "mysql",
        "sql",
        "html",
        "css"
    ],

    "Full Stack Developer": [
        "html",
        "css",
        "javascript",
        "react",
        "node.js",
        "python",
        "flask",
        "mysql"
    ]

}


# ----------------------------------------
# Recommend Career
# ----------------------------------------

def recommend_career(user_skills):

    user_skills = [skill.lower() for skill in user_skills]

    best_career = "General Software Engineer"
    highest_score = 0

    for career, required_skills in CAREER_PATHS.items():

        matched = len(set(user_skills) & set(required_skills))

        if matched > highest_score:

            highest_score = matched
            best_career = career

    return best_career


# ----------------------------------------
# Career Match Percentage
# ----------------------------------------

def career_match_percentage(career, user_skills):

    user_skills = [skill.lower() for skill in user_skills]

    required_skills = CAREER_PATHS.get(career, [])

    if not required_skills:
        return 0

    matched = len(set(user_skills) & set(required_skills))

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