def calculate_ats_score(candidate_skills, required_skills):

    matched_skills = []

    for skill in required_skills:
        if skill.lower() in [s.lower() for s in candidate_skills]:
            matched_skills.append(skill)

    if not required_skills:
        score = 0
    else:
        score = (len(matched_skills) / len(required_skills)) * 100

    return {
        "score": round(score, 2),
        "matched_skills": matched_skills,
        "missing_skills": list(
            set(required_skills) - set(matched_skills)
        )
    }