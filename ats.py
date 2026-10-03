# ----------------------------------------
# ATS Score Calculator
# ----------------------------------------


def get_ats_breakdown(skills, resume_text):
    """Return the existing ATS criteria as display-ready score categories."""

    resume_text = resume_text.lower()

    project_keywords = [
        "project",
        "projects",
        "developed",
        "built",
        "created",
        "implemented"
    ]
    education_keywords = [
        "b.tech",
        "bachelor",
        "degree",
        "college",
        "university"
    ]
    certification_keywords = [
        "certificate",
        "certification",
        "certified"
    ]
    digits = "".join(ch for ch in resume_text if ch.isdigit())

    breakdown = [
        {
            "label": "Technical skills",
            "score": min(len(skills) * 5, 40),
            "maximum": 40
        },
        {
            "label": "Projects",
            "score": 15 if any(word in resume_text for word in project_keywords) else 0,
            "maximum": 15
        },
        {
            "label": "Education",
            "score": 10 if any(word in resume_text for word in education_keywords) else 0,
            "maximum": 10
        },
        {
            "label": "Certifications",
            "score": 10 if any(word in resume_text for word in certification_keywords) else 0,
            "maximum": 10
        },
        {
            "label": "GitHub profile",
            "score": 10 if "github.com" in resume_text else 0,
            "maximum": 10
        },
        {
            "label": "LinkedIn profile",
            "score": 10 if "linkedin.com" in resume_text else 0,
            "maximum": 10
        },
        {
            "label": "Email address",
            "score": 3 if "@" in resume_text else 0,
            "maximum": 3
        },
        {
            "label": "Phone number",
            "score": 2 if len(digits) >= 10 else 0,
            "maximum": 2
        }
    ]

    for category in breakdown:
        category["percentage"] = int(
            (category["score"] / category["maximum"]) * 100
        )

    return breakdown


def calculate_ats(skills, resume_text):
    breakdown = get_ats_breakdown(skills, resume_text)
    score = sum(category["score"] for category in breakdown)

    return min(score, 100)
