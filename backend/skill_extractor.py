import re
from backend.skills import SKILLS

def extract_skills(text):
    found_skills = []

    text = text.lower()

    for skill in SKILLS:
        pattern = r'(?<![a-z0-9])' + re.escape(skill.lower()) + r'(?![a-z0-9])'
        if re.search(pattern, text):
            found_skills.append(skill)

    return list(set(found_skills))
