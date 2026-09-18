def normalize_skill(skill):
    return skill.strip().lower()

def calculate_technical_match(skills_required,matched_skills):
    if not skills_required:
        return 0
    
    required_skills = [
        normalize_skill(skill)
        for skill in skills_required.split(',')
        if skill.strip()
    ]
    matched = [
        normalize_skill(skill)
        for skill in matched_skills
    ]

    if not required_skills:
        return 0

    matched_count = sum(
        1 for skill in required_skills
        if skill in matched
    )

    score = (matched_count / len(required_skills)) * 100
    return round(score)

def calculate_experience_match(experience_evidence):
    if not experience_evidence:
        return 0

    evidence_count = len(experience_evidence)

    if evidence_count >= 4:
        return 100
    elif evidence_count ==3:
        return 80
    elif evidence_count ==2:
        return 60
    elif evidence_count ==1:
        return 30
    else:
        return 0

def calculate_overall_match(technical_match, experience_match):
    overall = (technical_match * 0.60 + experience_match * 0.40 )
    return round(overall)