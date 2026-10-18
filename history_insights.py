def build_history_progress(resumes):

    enriched_resumes = []

    for index, resume in enumerate(resumes):

        enriched_resume = dict(resume)
        current_score = enriched_resume.get("ats_score")
        previous_resume = resumes[index + 1] if index + 1 < len(resumes) else None
        previous_score = previous_resume.get("ats_score") if previous_resume else None

        score_change = None
        progress_label = "First upload"
        progress_status = "neutral"

        if current_score is not None and previous_score is not None:

            score_change = current_score - previous_score

            if score_change > 0:

                progress_label = "Improved"
                progress_status = "positive"

            elif score_change < 0:

                progress_label = "Dropped"
                progress_status = "negative"

            else:

                progress_label = "No change"

        enriched_resume["score_change"] = score_change
        enriched_resume["progress_label"] = progress_label
        enriched_resume["progress_status"] = progress_status

        enriched_resumes.append(enriched_resume)

    return enriched_resumes
