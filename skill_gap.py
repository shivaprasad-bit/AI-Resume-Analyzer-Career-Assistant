# ----------------------------------------
# Required Skills for Each Career
# ----------------------------------------

REQUIRED_SKILLS = {

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
# Find Missing Skills
# ----------------------------------------

def find_missing_skills(career, user_skills):

    user_skills = [skill.lower() for skill in user_skills]

    required_skills = REQUIRED_SKILLS.get(career, [])

    missing = sorted(
        list(
            set(required_skills) - set(user_skills)
        )
    )

    return missing


# ----------------------------------------
# Total Missing Skills
# ----------------------------------------

def total_missing_skills(career, user_skills):

    return len(
        find_missing_skills(
            career,
            user_skills
        )
    )


# ----------------------------------------
# Skill Match Percentage
# ----------------------------------------

def skill_match_percentage(career, user_skills):

    user_skills = [skill.lower() for skill in user_skills]

    required_skills = REQUIRED_SKILLS.get(career, [])

    if not required_skills:
        return 0

    matched = len(
        set(user_skills) &
        set(required_skills)
    )

    percentage = int(
        (matched / len(required_skills)) * 100
    )

    return percentage


# ----------------------------------------
# Learning Priority
# ----------------------------------------

def learning_priority(missing_skills):

    high_priority = {

        "python",
        "java",
        "sql",
        "machine learning",
        "deep learning",
        "tensorflow",
        "flask",
        "django",
        "react",
        "javascript"

    }

    priority = {}

    for skill in missing_skills:

        if skill.lower() in high_priority:

            priority[skill] = "High"

        else:

            priority[skill] = "Medium"

    return priority


# ----------------------------------------
# Learning Roadmap
# ----------------------------------------

def learning_roadmap(missing_skills):

    roadmap = []

    priorities = learning_priority(missing_skills)

    for skill in missing_skills:

        roadmap.append({

            "skill": skill,

            "priority": priorities[skill]

        })

    roadmap.sort(

        key=lambda x:

        x["priority"]

    )

    return roadmap