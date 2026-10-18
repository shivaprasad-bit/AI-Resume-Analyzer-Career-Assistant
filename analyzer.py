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
    "azure",
    "mongodb",
    "express.js",
    "tailwind css",
    "rest api",
    "nlp",
    "scikit-learn",
    "spring boot",
    "postgresql",
    "docker",
    "kubernetes"
]

SKILL_ALIASES = {
    "javascript": ["js"],
    "node.js": ["nodejs", "node js"],
    "artificial intelligence": ["ai"],
    "machine learning": ["ml"],
    "power bi": ["powerbi"],
    "opencv": ["open cv"],
    "mongodb": ["mongo db"],
    "express.js": ["express", "expressjs", "express js"],
    "rest api": ["rest apis", "restful api", "restful apis"],
    "nlp": ["natural language processing"],
    "scikit-learn": ["sklearn", "scikit learn"],
    "postgresql": ["postgres"],
}
# ----------------------------------------
# Extract Resume Text
# ----------------------------------------

def normalize_resume_text(text):

    if not text:

        return ""

    text = text.replace("\u00a0", " ")

    text = re.sub(r"[\u2010-\u2015]", "-", text)

    text = re.sub(r"([a-zA-Z])-\s*\n\s*([a-zA-Z])", r"\1\2", text)

    text = re.sub(r"\s+", " ", text)

    text = re.sub(r"(?<![a-z0-9])c\s*\+\s*\+(?![a-z0-9])", "c++", text, flags=re.IGNORECASE)

    text = re.sub(r"\b(node|express)\s*\.\s*js\b", r"\1.js", text, flags=re.IGNORECASE)

    text = re.sub(r"\b(scikit)\s*-\s*(learn)\b", r"\1-\2", text, flags=re.IGNORECASE)

    text = re.sub(r"\b(github|linkedin)\s*\.\s*com\b", r"\1.com", text, flags=re.IGNORECASE)

    return text.strip().lower()


def extract_text(pdf_path):

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:

            text += page_text + "\n"

    return normalize_resume_text(text)


# ----------------------------------------
# Detect Skills
# ----------------------------------------

def detect_skills(text):

    text = text.lower()

    found_skills = []

    for skill in SKILLS:

        skill_terms = [skill] + SKILL_ALIASES.get(skill, [])

        for term in skill_terms:

            pattern = r"(?<![a-z0-9+#.])" + re.escape(term.lower()) + r"(?![a-z0-9+#])"

            if re.search(pattern, text):

                found_skills.append(skill)

                break

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
