# CareerAI — AI Resume Analyzer & Career Assistant

CareerAI is a Flask-based web application that analyzes PDF resumes, calculates an ATS-style score, detects technical skills, recommends career paths, identifies skill gaps, and tracks resume improvement over time.

## Features

- **Resume Analysis:** Upload a text-based PDF resume and extract readable text.
- **ATS-Style Scoring:** Evaluate technical skills, projects, education, certifications, professional links, and contact details.
- **Skill Detection:** Identify technical skills from resume content.
- **Career Recommendations:** Match detected skills against predefined career requirements.
- **Skill-Gap Analysis:** Identify missing skills and improvement priorities for a recommended career path.
- **Resume Recommendations:** Generate rule-based suggestions using the ATS score and skill gaps.
- **User Authentication:** Register, log in, and log out with password hashing.
- **Resume History:** Review previous analyses, ATS scores, and career recommendations.
- **Progress Tracking:** Compare recent scores and view score changes over time.
- **Resume Management:** View and delete saved resume records.
- **CareerAI Guide:** Use a built-in, rule-based guidance widget for common resume and career questions.
- **Theme Options:** Switch between available visual themes.
- **Responsive Interface:** Navigate the application through its dashboard and responsive layouts.
- **SQLite Storage:** Store user accounts and resume analysis history locally.

## How It Works

1. Register an account and sign in.
2. Upload a text-based PDF resume.
3. CareerAI extracts the resume text.
4. The analyzer detects skills and the ATS module calculates a score.
5. The career module recommends a suitable career direction.
6. The skill-gap module identifies missing skills.
7. The recommendation module generates improvement suggestions.
8. The analysis is saved so you can review progress through Resume History.

## ATS-Style Scoring

The current scoring model allocates up to 100 points:

| Category | Maximum points |
|---|---:|
| Technical skills | 40 |
| Projects | 15 |
| Education | 10 |
| Certifications | 10 |
| GitHub | 10 |
| LinkedIn | 10 |
| Email | 3 |
| Phone number | 2 |
| **Total** | **100** |

The scoring implementation is maintained in `ats.py`.

**Important:** This is a project-specific ATS-style score. It is not an official score from, or an exact reproduction of, a proprietary recruitment system. Results depend on the text that can be extracted from the uploaded resume and the rules implemented in the application.

## Technology Stack

- **Backend:** Python, Flask
- **PDF Processing:** PyPDF2
- **Frontend:** HTML, CSS, JavaScript, Jinja2 templates
- **Database:** SQLite
- **Authentication:** Werkzeug password hashing
- **Development:** Git, GitHub, Python virtual environment

## Project Structure

```text
AI-Resume-Analyzer-Career-Assistant/
├── app.py
├── analyzer.py
├── ats.py
├── career.py
├── database.py
├── history_insights.py
├── recommendations.py
├── skill_gap.py
├── upload_validation.py
├── requirements.txt
├── .gitignore
├── README.md
├── static/
│   ├── style.css
│   ├── theme.js
│   └── guide.js
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── result.html
│   ├── history.html
│   ├── 404.html
│   └── 500.html
└── uploads/
```

The `uploads/` directory and local database are runtime data, not source files to publish. The exact files in your local project may differ slightly as the application evolves.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/shivaprasad-bit/AI-Resume-Analyzer-Career-Assistant.git
cd AI-Resume-Analyzer-Career-Assistant
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the application locally

```bash
python app.py
```

Open the local address shown in the terminal, normally:

```text
http://127.0.0.1:5000
```

## Data and Privacy

CareerAI stores user accounts and resume analysis records in a local SQLite database named `users.db`. Uploaded PDF files are stored under the configured upload directory.

The repository should not contain real user resumes, database files, credentials, environment files, or virtual environments. Keep personal resume data private and use sample data when demonstrating the project.

Before deploying the application publicly, configure a strong secret key through an environment variable, disable Flask debug mode, and configure persistent storage for both the database and uploaded files.


## Running Tests

Activate your Python virtual environment and run:

python -m pytest -q -p no:cacheprovider

The test suite covers skill detection, career recommendations, database history, history insights, recommendations, and upload validation.

## Limitations

- The application currently supports PDF resumes rather than every document format.
- Scanned PDFs without readable text may not be analyzed correctly.
- Career recommendations use predefined skill mappings.
- The built-in CareerAI Guide uses predefined rules and responses; it is not a live generative AI chatbot.
- The ATS-style score is an estimate based on this project's scoring rules, not a guarantee of recruitment success.

## Future Improvements

Potential enhancements include job-description matching, keyword comparison, additional career paths, downloadable analysis reports, and integration with an external AI service.

## Author

**Shivaprasad Marapally**

GitHub: https://github.com/shivaprasad-bit

---

*Built with Python and Flask to help users understand and improve their resumes.*
