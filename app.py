from flask import Flask, flash, render_template, request, redirect, session, url_for, send_file
from datetime import datetime
import os

from analyzer import extract_text, detect_skills
from ats import calculate_ats, get_ats_breakdown
from career import recommend_career
from skill_gap import find_missing_skills
from recommendations import generate_recommendations
from history_insights import build_history_progress
from upload_validation import is_allowed_resume_file

from database import (
    create_database,
    register_user,
    login_user,
    save_resume,
    get_latest_resume,
    get_resume_history,
    get_resume_by_id,
    delete_resume
)

# ----------------------------------------
# Flask App Configuration
# ----------------------------------------


app = Flask(__name__)

# Security configuration
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

if not app.config["SECRET_KEY"]:
    if os.environ.get("APP_ENV", "development").lower() == "production":
        raise RuntimeError("SECRET_KEY must be configured in production.")

    # Local development only
    app.config["SECRET_KEY"] = "dev-only-change-me"

# Upload configuration
UPLOAD_FOLDER = os.path.abspath(
    os.environ.get("UPLOAD_FOLDER", "uploads")
)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


create_database()


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

    if not is_allowed_resume_file(file.filename):
        flash("Only PDF resumes are supported. Please upload a .pdf file.", "error")
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

    try:

        resume_text = extract_text(file_path)

    except Exception:

        if os.path.exists(file_path):

            os.remove(file_path)

        flash("CareerAI could not read that PDF. Please upload a text-based resume PDF.", "error")
        return redirect(url_for("home") + "#analyze-resume")

    if not resume_text:

        if os.path.exists(file_path):

            os.remove(file_path)

        flash("No readable text was found in that PDF. Please upload a text-based resume PDF.", "error")
        return redirect(url_for("home") + "#analyze-resume")

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
        career,
        skills,
        missing_skills,
        recommendations
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
    resumes = build_history_progress(resumes)

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
# View Resume
# ----------------------------------------

@app.route("/resume/<int:resume_id>")
def view_resume(resume_id):

    if "user" not in session:
        return redirect(url_for("login"))

    resume = get_resume_by_id(
        resume_id,
        session["user_id"]
    )

    if resume is None:
        return "Resume not found.", 404

    if not os.path.exists(resume["resume_path"]):
        return "Resume file not found.", 404

    return send_file(
        resume["resume_path"],
        mimetype="application/pdf",
        as_attachment=False
    )
# ----------------------------------------
# Delete Resume
# ----------------------------------------

@app.route("/resume/<int:resume_id>/delete", methods=["POST"])
def remove_resume(resume_id):

    if "user" not in session:
        return redirect(url_for("login"))

    resume = get_resume_by_id(
        resume_id,
        session["user_id"]
    )

    if resume is None:
        flash("Resume not found.", "error")
        return redirect(url_for("history"))

    resume_path = resume["resume_path"]

    deleted = delete_resume(
        resume_id,
        session["user_id"]
    )

    if deleted:
        if os.path.exists(resume_path):
            os.remove(resume_path)

        flash(
            f'"{resume["resume_name"]}" was deleted successfully.',
            "success"
        )
    else:
        flash("Unable to delete the resume.", "error")

    return redirect(url_for("history"))


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
        debug=os.environ.get("FLASK_DEBUG", "0") == "1"
    )