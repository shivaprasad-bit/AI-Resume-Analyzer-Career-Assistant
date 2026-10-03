from flask import Flask, flash, render_template, request, redirect, session, url_for
from datetime import datetime
import os

from analyzer import extract_text, detect_skills
from ats import calculate_ats, get_ats_breakdown
from career import recommend_career
from skill_gap import find_missing_skills
from recommendations import generate_recommendations

from database import (
    register_user,
    login_user,
    save_resume,
    get_latest_resume,
    get_resume_history
)

# ----------------------------------------
# Flask App Configuration
# ----------------------------------------

app = Flask(__name__)

app.secret_key = "AI_Career_Assistant_2026"

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# ----------------------------------------
# Home Page
# ----------------------------------------

@app.route("/")
def home():

    if "user" not in session:
        return redirect("/login")

    latest_resume = get_latest_resume(session["user_id"])
    resume_history = get_resume_history(session["user_id"])

    latest_score = None
    best_ats_score = None
    score_change = None
    recommended_next_steps = []

    if latest_resume:
        latest_score = latest_resume["ats_score"]
        best_ats_score = max(
            resume["ats_score"]
            for resume in resume_history
            if resume["ats_score"] is not None
        )

        if len(resume_history) > 1:
            previous_score = resume_history[1]["ats_score"]
            if previous_score is not None:
                score_change = latest_score - previous_score

        # History stores scores, not skill gaps, so only use score-based advice here.
        recommended_next_steps = generate_recommendations(latest_score, [])

    return render_template(
        "index.html",
        username=session["user"],
        latest_resume=latest_resume,
        resume_count=len(resume_history),
        recent_resumes=resume_history[:5],
        progress_resumes=list(reversed(resume_history[:6])),
        latest_score=latest_score,
        best_ats_score=best_ats_score,
        score_change=score_change,
        recommended_next_steps=recommended_next_steps
    )


# ----------------------------------------
# Register
# ----------------------------------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form["fullname"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        success = register_user(
            fullname,
            email,
            password
        )

        if success:
            flash("Your CareerAI account is ready. Please sign in.", "success")
            return redirect(url_for("login"))

        flash("An account with that email already exists.", "error")
        return redirect(url_for("register"))

    return render_template("register.html")


# ----------------------------------------
# Login
# ----------------------------------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"].strip().lower()
        password = request.form["password"]

        user = login_user(email, password)

        if user:

            session["user"] = user["fullname"]
            session["email"] = user["email"]
            session["user_id"] = user["id"]

            flash("Welcome back, " + user["fullname"] + ".", "success")
            return redirect(url_for("home"))

        flash("Invalid email or password.", "error")
        return redirect(url_for("login"))

    return render_template("login.html")


# ----------------------------------------
# Logout
# ----------------------------------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")
# ----------------------------------------
# Upload Resume
# ----------------------------------------

@app.route("/upload", methods=["POST"])
def upload_resume():

    if "user" not in session:
        return redirect("/login")

    if "resume" not in request.files:
        flash("Choose a resume before starting the analysis.", "error")
        return redirect(url_for("home") + "#analyze-resume")

    file = request.files["resume"]

    if file.filename == "":
        flash("Choose a PDF resume before starting the analysis.", "error")
        return redirect(url_for("home") + "#analyze-resume")

    # ----------------------------------------
    # Create User Folder
    # ----------------------------------------

    user_folder = os.path.join(
        app.config["UPLOAD_FOLDER"],
        session["email"]
    )

    os.makedirs(user_folder, exist_ok=True)

    # ----------------------------------------
    # Unique File Name
    # ----------------------------------------

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"{timestamp}_{file.filename}"

    file_path = os.path.join(
        user_folder,
        filename
    )

    file.save(file_path)

    # ----------------------------------------
    # Resume Analysis
    # ----------------------------------------

    resume_text = extract_text(file_path)

    skills = detect_skills(resume_text)

    ats_score = calculate_ats(
        skills,
        resume_text
    )
    ats_breakdown = get_ats_breakdown(
        skills,
        resume_text
    )

    career = recommend_career(skills)

    missing_skills = find_missing_skills(
        career,
        skills
    )

    recommendations = generate_recommendations(
        ats_score,
        missing_skills
    )

    # ----------------------------------------
    # Save Resume
    # ----------------------------------------

    save_resume(
        session["user_id"],
        filename,
        file_path,
        ats_score,
        career
    )

    # ----------------------------------------
    # Result Page
    # ----------------------------------------

    return render_template(
        "result.html",
        filename=filename,
        score=ats_score,
        ats_breakdown=ats_breakdown,
        skills=skills,
        career=career,
        missing_skills=missing_skills,
        recommendations=recommendations,
        analyzed_at=datetime.now()
    )


# ----------------------------------------
# Resume History
# ----------------------------------------

@app.route("/history")
def history():

    if "user" not in session:
        return redirect("/login")

    resumes = get_resume_history(
        session["user_id"]
    )

    latest_score = resumes[0]["ats_score"] if resumes else None
    best_ats_score = max(
        (resume["ats_score"] for resume in resumes if resume["ats_score"] is not None),
        default=None
    )

    return render_template(
        "history.html",
        resumes=resumes,
        resume_count=len(resumes),
        latest_score=latest_score,
        best_ats_score=best_ats_score
    )


# ----------------------------------------
# Error Pages
# ----------------------------------------

@app.errorhandler(404)
def page_not_found(error):

    return render_template(
        "404.html"
    ), 404


@app.errorhandler(500)
def internal_server_error(error):

    return render_template(
        "500.html"
    ), 500


# ----------------------------------------
# Run Application
# ----------------------------------------

if __name__ == "__main__":

    app.run(
        debug=True
    )
