from PyPDF2 import PdfReader
import re

# ----------------------------------------
# Skills Database
# ----------------------------------------

SKILLS = [
    "python",
    "java",
    "c",
    "c++",
    "sql",
    "mysql",
    "html",
    "css",
    "javascript",
    "bootstrap",
    "flask",
    "django",
    "react",
    "node.js",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data science",
    "data analysis",
    "power bi",
    "tableau",
    "excel",
    "pandas",
    "numpy",
    "tensorflow",
    "keras",
    "opencv",
    "git",
    "github",
    "linux",
    "aws",
    "azure"
]
# ----------------------------------------
# Extract Resume Text
# ----------------------------------------

def extract_text(pdf_path):

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:

            text += page_text + "\n"

    return text.lower()


# ----------------------------------------
# Detect Skills
# ----------------------------------------

def detect_skills(text):

    text = text.lower()

    found_skills = []

    for skill in SKILLS:

        if skill.lower() in text:

            found_skills.append(skill)

    return sorted(set(found_skills))


# ----------------------------------------
# Total Skills
# ----------------------------------------

def total_skills(skills):

    return len(skills)
# ----------------------------------------
# GitHub
# ----------------------------------------

def has_github(text):

    return "github.com" in text.lower()


# ----------------------------------------
# LinkedIn
# ----------------------------------------

def has_linkedin(text):

    return "linkedin.com" in text.lower()


# ----------------------------------------
# Projects
# ----------------------------------------

def has_projects(text):

    keywords = [

        "project",

        "projects",

        "developed",

        "built",

        "created",

        "implemented"

    ]

    return any(word in text.lower() for word in keywords)


# ----------------------------------------
# Certifications
# ----------------------------------------

def has_certification(text):

    keywords = [

        "certificate",

        "certification",

        "certified"

    ]

    return any(word in text.lower() for word in keywords)


# ----------------------------------------
# Education
# ----------------------------------------

def has_education(text):

    keywords = [

        "b.tech",

        "bachelor",

        "degree",

        "college",

        "university"

    ]

    return any(word in text.lower() for word in keywords)