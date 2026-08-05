# ----------------------------------------
# ATS Score Calculator
# ----------------------------------------

def calculate_ats(skills, resume_text):

    score = 0

    resume_text = resume_text.lower()

    # ====================================
    # 1. Technical Skills (40 Marks)
    # ====================================

    score += min(len(skills) * 5, 40)

    # ====================================
    # 2. Projects (15 Marks)
    # ====================================

    project_keywords = [
        "project",
        "projects",
        "developed",
        "built",
        "created",
        "implemented"
    ]

    if any(word in resume_text for word in project_keywords):
        score += 15

    # ====================================
    # 3. Education (10 Marks)
    # ====================================

    education_keywords = [
        "b.tech",
        "bachelor",
        "degree",
        "college",
        "university"
    ]

    if any(word in resume_text for word in education_keywords):
        score += 10

    # ====================================
    # 4. Certifications (10 Marks)
    # ====================================

    certification_keywords = [
        "certificate",
        "certification",
        "certified"
    ]

    if any(word in resume_text for word in certification_keywords):
        score += 10

    # ====================================
    # 5. GitHub (10 Marks)
    # ====================================

    if "github.com" in resume_text:
        score += 10

    # ====================================
    # 6. LinkedIn (10 Marks)
    # ====================================

    if "linkedin.com" in resume_text:
        score += 10

    # ====================================
    # 7. Email (3 Marks)
    # ====================================

    if "@" in resume_text:
        score += 3

    # ====================================
    # 8. Phone Number (2 Marks)
    # ====================================

    digits = "".join(ch for ch in resume_text if ch.isdigit())

    if len(digits) >= 10:
        score += 2

    # ====================================
    # Final Score
    # ====================================

    return min(score, 100)