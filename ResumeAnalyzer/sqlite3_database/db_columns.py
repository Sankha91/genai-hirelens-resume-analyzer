class DBColumns:
    # Resume main table columns
    ID = "id"
    NAME = "name"
    EMAIL = "email"
    PHONE = "phone"
    SUMMARY = "summary"
    CURRENT_ROLE = "current_role"
    DOMAIN_EXPERTISE = "domain_expertise"
    TOTAL_EXPERIENCE = "total_experience_years"
    LOCATION = "location"

    # Skills
    SKILL = "skill"

    # Companies worked
    COMPANY_NAME = "company_name"

    # Certification
    CERTIFICATION_NAME = "certification_name"

    # Education
    QUALIFICATION = "qualification"

    # Projects
    PROJECT_NAME = "project_name"

    # Common FK
    RESUME_ID = "resume_id"

    CREATED_AT = "created_at"

    # JD main table
    JD_ID = "jd_id"
    JD_EXPERIENCE = "min_experience"
    JD_TITLE = "title"
    JD_RAW_TEXT = "raw_text"
    JD_RESPONSIBILITY = "responsibility"
    JD_JOB_TYPE = "job_type"

    # Analysis Result table
    SKILLS_MATCH = "skills_match"
    MISSING_SKILLS = "missing_skills"
    MATCH_PERCENT = "match_percent"
    RECOMMENDATION = "recommendation"
    STRENGTHS = "strengths"
    WEAKNESS = "weakness"

    