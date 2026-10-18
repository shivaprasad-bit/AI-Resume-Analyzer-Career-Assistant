/* =========================================================
   CAREERAI GUIDE
   ========================================================= */

(function () {

    const guide = document.querySelector("[data-ai-guide]");

    if (!guide) {
        return;
    }

    const toggle = guide.querySelector("[data-ai-guide-toggle]");
    const panel = guide.querySelector("[data-ai-guide-panel]");
    const close = guide.querySelector("[data-ai-guide-close]");
    const form = guide.querySelector("[data-ai-guide-form]");
    const input = guide.querySelector("[data-ai-guide-input]");
    const messages = guide.querySelector("[data-ai-guide-messages]");
    const prompts = guide.querySelectorAll("[data-ai-guide-prompt]");

    function openGuide() {
        panel.hidden = false;
        toggle.setAttribute("aria-expanded", "true");
        guide.classList.add("is-open");
        input.focus();
    }

    function closeGuide() {
        panel.hidden = true;
        toggle.setAttribute("aria-expanded", "false");
        guide.classList.remove("is-open");
    }

    function addMessage(text, type) {
        const message = document.createElement("article");
        message.className = "ai-guide-message ai-guide-message-" + type;
        message.textContent = text;
        messages.appendChild(message);
        messages.scrollTop = messages.scrollHeight;
    }

    function getReply(question) {
        const text = question.toLowerCase();

        if (text.includes("ats") || text.includes("score")) {
            return "To improve ATS score, add clear technical skills, projects, certifications, GitHub/LinkedIn links, education, and measurable achievements. Upload an updated PDF and compare the score in History.";
        }

        if (text.includes("skill") || text.includes("missing")) {
            return "Open the result page and check Skills to strengthen. Start with high-value skills for your target role, then add one project that proves each skill.";
        }

        if (text.includes("career") || text.includes("role") || text.includes("path")) {
            return "CareerAI recommends the role with the strongest match to your detected skills. If the recommendation feels off, add more role-specific skills and projects to your resume.";
        }

        if (text.includes("history") || text.includes("progress")) {
            return "Use Resume History to compare uploads. The Change column shows whether your latest ATS score improved, dropped, or stayed the same.";
        }

        if (text.includes("upload") || text.includes("pdf")) {
            return "Upload a text-based PDF resume. Scanned image PDFs may not work well because the analyzer needs readable text.";
        }

        if (text.includes("project") || text.includes("github")) {
            return "Add 2-3 strong projects with tech stack, your role, features built, measurable result, and GitHub links. Projects help both ATS and career matching.";
        }

        if (text.includes("certificate") || text.includes("certification")) {
            return "Add relevant certifications with issuer and date. Certifications are most useful when paired with projects that prove the same skill.";
        }

        return "Good next step: upload your resume, review detected skills, check missing skills, then improve one section at a time. Ask me about ATS, skills, career, projects, history, or uploads.";
    }

    function askGuide(question) {
        const cleanQuestion = question.trim();

        if (!cleanQuestion) {
            return;
        }

        addMessage(cleanQuestion, "user");
        addMessage(getReply(cleanQuestion), "agent");
    }

    toggle.addEventListener("click", function () {
        if (panel.hidden) {
            openGuide();
        } else {
            closeGuide();
        }
    });

    close.addEventListener("click", closeGuide);

    form.addEventListener("submit", function (event) {
        event.preventDefault();
        askGuide(input.value);
        input.value = "";
    });

    prompts.forEach(function (prompt) {
        prompt.addEventListener("click", function () {
            askGuide(prompt.dataset.aiGuidePrompt);
        });
    });

    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") {
            closeGuide();
        }
    });

})();
