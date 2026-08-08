# 🤖 AI Resume Analyzer & Career Assistant

An intelligent Flask-based web application that analyzes resumes, calculates an ATS-style score, detects technical skills, recommends suitable career paths, identifies missing skills, and provides personalized improvement suggestions.

## 🚀 Features

* 📄 **Resume PDF Upload**
* 🔍 **Resume Text Extraction**
* 🧠 **Technical Skill Detection**
* 📊 **ATS Score Calculation**
* 💼 **Career Path Recommendation**
* 🎯 **Missing Skill Detection**
* 💡 **Resume Improvement Recommendations**
* 👤 **User Registration & Login**
* 🔐 **Password Hashing**
* 🗂️ **Resume History**
* 📈 **Latest Resume Tracking**
* 🖥️ **Flask Web Interface**
* 🗄️ **SQLite Database**

## 🧠 How It Works

```text
                 ┌─────────────────┐
                 │   User Login    │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ Upload Resume   │
                 │      PDF        │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ Extract Resume  │
                 │      Text       │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ Detect Skills   │
                 └────────┬────────┘
                          │
              ┌───────────┼───────────┐
              ▼           ▼           ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │ ATS Score│ │ Career   │ │ Skill Gap│
        │ Analysis │ │ Matching │ │ Analysis │
        └────┬─────┘ └────┬─────┘ └────┬─────┘
             │            │            │
             └────────────┼────────────┘
                          ▼
                 ┌─────────────────┐
                 │ Recommendations │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ Analysis Result │
                 └─────────────────┘
```

## 📊 ATS Analysis

The current ATS scoring system evaluates several resume elements:

| Category         | Maximum Score |
| ---------------- | ------------: |
| Technical Skills |            40 |
| Projects         |            15 |
| Education        |            10 |
| Certifications   |            10 |
| GitHub           |            10 |
| LinkedIn         |            10 |
| Email            |             3 |
| Phone Number     |             2 |
| **Total**        |       **100** |

The scoring implementation is contained in `ats.py`.

> **Note:** This is an ATS-style scoring system developed for this project and should not be considered an exact replica of proprietary recruitment ATS systems.

## 💼 Career Recommendation

The application currently compares detected resume skills against predefined career skill requirements.

Current career paths include:

* AI / Machine Learning Engineer
* Data Analyst
* Python Developer
* Java Developer
* Full Stack Developer

The recommendation engine selects the career path with the highest number of matching skills.

## 🎯 Skill Gap Analysis

After identifying a recommended career, the application compares the user's detected skills with the skills required for that career.

It identifies:

* ✅ Existing skills
* ❌ Missing skills
* 🔥 High-priority skills
* 📚 Learning roadmap

The project also contains skill-match and learning-priority functionality.

## 💡 Recommendations

The recommendation engine provides suggestions based on the ATS score and missing skills.

Examples include recommendations for improving technical skills, projects, certifications, GitHub presence, and learning specific technologies.

## 🔐 Authentication & Database

The application includes:

* User registration
* Secure password hashing
* Login authentication
* Logout
* User-specific resume history
* Latest resume tracking

Passwords are stored using Werkzeug password hashing rather than plain text.

SQLite is used to store user accounts and resume analysis history.

## 🛠️ Technologies Used

### Backend

* Python
* Flask
* PyPDF2

### Frontend

* HTML
* CSS
* Jinja2 Templates

### Database

* SQLite

### Development Tools

* Git
* GitHub
* Python Virtual Environment

## 📂 Project Structure

```text
AI-Resume-Analyzer-Career-Assistant/
│
├── app.py
├── analyzer.py
├── ats.py
├── career.py
├── database.py
├── recommendations.py
├── skill_gap.py
│
├── static/
│   ├── images/
│   └── style.css
│
├── templates/
│   ├── dashboard.html
│   ├── history.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   └── result.html
│
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/shivaprasad-bit/AI-Resume-Analyzer-Career-Assistant.git
```

### 2. Navigate to the project

```bash
cd AI-Resume-Analyzer-Career-Assistant
```

### 3. Create a virtual environment

Windows:

```powershell
python -m venv .venv
```

### 4. Activate the virtual environment

PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```powershell
pip install -r requirements.txt
```

### 6. Run the application

```powershell
python app.py
```

### 7. Open the application

Visit:

```text
http://127.0.0.1:5000
```

## 🔒 Important

User-uploaded resumes, the local SQLite database, virtual environments, and temporary Python files are excluded from the GitHub repository using `.gitignore`.

This helps prevent personal resume files and local database information from being accidentally committed.

## 🔮 Future Enhancements

The current version provides the core resume-analysis functionality. Planned improvements include:

* 🎯 Job Description Matching
* 🔑 Job-specific Keyword Analysis
* 🤖 AI-powered Resume Suggestions
* 📊 Advanced ATS Analysis
* 📈 ATS Score Progress Dashboard
* 💼 More Career Paths
* 📚 Personalized Learning Roadmap
* 📄 Downloadable Resume Analysis Report
* 📊 Resume Analytics
* 🌐 Production Deployment
* 🎨 Improved Responsive UI
* 🌙 Dark Mode

## 📌 Project Status

**Current Version: v1.1**

The project currently includes the core Flask resume-analysis system and project dependency configuration.

Future versions will progressively introduce advanced ATS analysis, job-description matching, AI-powered recommendations, analytics, and deployment improvements.

## 👨‍💻 Author

**Shivaprasad Marapally**

GitHub:
https://github.com/shivaprasad-bit

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

---

### 🚀 Built with Python, Flask & a goal to make resume analysis smarter.
