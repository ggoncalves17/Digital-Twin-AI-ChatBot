def format_education(educations):
    if not educations:
        return "no listed educations"
    return "; ".join(
        f"{e.level} in {e.course} at {e.school} {e.date_started} - {e.date_finished} "
        f"(Graduated: {e.is_graduated} - Grade: {e.grade})"
        for e in educations
    )

def format_occupations(occupations):
    if not occupations:
        return "no listed occupations"
    return "; ".join(
        f"{e.position} at {e.workplace} {e.date_started} - {e.date_finished}"
        for e in occupations
    )

def format_hobbies(hobbies):
    if not hobbies:
        return "no listed hobbies"
    return "; ".join(f"{e.type} named {e.name} {e.freq}" for e in hobbies)
