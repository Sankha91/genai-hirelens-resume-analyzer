from langchain_google_genai import ChatGoogleGenerativeAI
from parsers.schema.skill_gap_analysis_schema import SkillGapAnalysisListSchema
from parsers.schema.resume_schema import ResumeSchema
from parsers.schema.job_description_schema import JDSchema 
from parsers.schema.result_schema import ResultListSchema
from parsers.schema.interview_questions_schema import InterviewQuestionListSchema, InterviewQuestionSchema
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from data.jd_data_model import JDDataModel

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite-preview", temperature=0.0)

resume_llm = llm.with_structured_output(ResumeSchema)
jd_llm = llm.with_structured_output(JDSchema)
result_llm = llm.with_structured_output(ResultListSchema)
interview_llm = llm.with_structured_output(InterviewQuestionListSchema)
skill_gap_llm = llm.with_structured_output(SkillGapAnalysisListSchema)

def summarize_jd_input(raw_text: str):
    prompt = PromptTemplate(template="""
    Summarize the following Job Description in not more than 10 concise lines.
    Requirements:
    Include all important information from the provided Job Description.
    Do not omit key details such as job title, experience, location, responsibilities, required skills, preferred skills, employment type, and education requirements if they are present.
    Use only information provided in the Job Description.
    Do not add, assume, or infer any information from outside the provided text.
    Do not repeat information unnecessarily.
    Keep the summary concise and factual.

    Job Description:
    {raw_text}
    """, input_variables=["raw_text"])
    chain = prompt | llm
    response = chain.invoke({"raw_text": raw_text})
    return response.content[0]["text"]

def parse_resume(resume_text):

    prompt = PromptTemplate(template=
    """
    Extract structured information
    from the following resume.

    Resume:
    {resume_text}
    """,
    input_variables=["resume_text"])

    chain = prompt | resume_llm
    response = chain.invoke({"resume_text": resume_text})

    return response

def parse_jd(jd_text):

    prompt = PromptTemplate(template=
    """
    Extract structured information
    from the following job description.

    Resume:
    {jd_text}
    """,
    input_variables=["jd_text"])

    chain = prompt | jd_llm
    response = chain.invoke({"jd_text": jd_text})

    return response

def parse_result(jd_text, all_resumes_text):
    prompt = PromptTemplate(template=
                            """
    You are an experienced technical recruiter.
    You will receive one JD and multiple resumes.
    Compare the following resumes against the job description.
    Evaluate EVERY resume independently.
    Do not skip any resume.

    ========================
    JOB DESCRIPTION
    ========================

    {jd_text}

    ========================
    CANDIDATE RESUMES
    ========================

    {all_resumes_text}
    
    """, input_variables=["jd_text", "all_resumes_text"])
    chain = prompt | result_llm
    result = chain.invoke({"jd_text": jd_text, "all_resumes_text": all_resumes_text})
    return result

def parse_interview_questions(skills: list[str], experience: int, summary: str) -> list[InterviewQuestionSchema]:
    prompt = PromptTemplate(
    template="""
    You are an expert technical recruiter and interviewer.

    Generate interview questions for the candidate based on their
    skills, professional experience and summary.

    Candidate Skills:
    {skills}

    Candidate Experience:
    {experience}

    Candidate Summary:
    {summary}

    Generate questions in exactly these 3 categories:

    1. Technical
    - Test knowledge of the candidate's technical skills.
    - Focus on concepts, implementation, architecture and problem solving.

    2. Experience
    - Ask questions based on the candidate's actual experience.
    - Focus on projects, responsibilities, challenges and decisions.

    3. Behavioral
    - Evaluate communication, ownership, leadership, collaboration
        and problem solving.

    Rules:
    - Generate 3 questions per category.
    - Total questions = 9.
    - Questions should be relevant to the candidate.
    - Difficulty should be Easy, Medium or Hard.
    - Do not invent technologies or experience not present in the input.
    - Answers should describe what a strong candidate answer should contain.
    - Return only the structured output.

    """, input_variables=["skills", "experience", "summary"]
    )
    chain = prompt | interview_llm
    result: InterviewQuestionListSchema = chain.invoke({"skills": skills, "experience": experience, "summary": summary})
    return result.qaList

def parse_skill_gap_analysis(jd_mandatory_skills, jd_preferred_skills, 
                             candidate_skills, projects, certifications, candidate_summary, domain_expertise) -> SkillGapAnalysisListSchema:

    skill_gap_prompt = PromptTemplate(
        template="""
        You are an expert technical recruiter and interviewer.

        Analyze the skill gaps between the job requirements and the candidate's qualifications.

        Job Required Skills:
        {jd_mandatory_skills}

        Job Preferred Skills:
        {jd_preferred_skills}

        Candidate Skills:
        {candidate_skills}

        Candidate Projects:
        {projects}

        Candidate Certifications:
        {certifications}

        Candidate Summary:
        {candidate_summary}

        Candidate Domain Expertise:
        {domain_expertise}

        Generate a detailed skill gap analysis for each required skill, including the candidate's proficiency level, the gap score, and recommendations to bridge the gap.

        Return only the structured output.
        """,
        input_variables=["jd_mandatory_skills", "jd_preferred_skills", "candidate_skills", "projects", "certifications", "candidate_summary", "domain_expertise"]
    )
    chain = skill_gap_prompt | skill_gap_llm
    result: SkillGapAnalysisListSchema = chain.invoke({
        "jd_mandatory_skills": jd_mandatory_skills,
        "jd_preferred_skills": jd_preferred_skills,
        "candidate_skills": candidate_skills,
        "projects": projects,
        "certifications": certifications,
        "candidate_summary": candidate_summary,
        "domain_expertise": domain_expertise
    })
    return result

def resume_embedding_format(resume: ResumeSchema):
    embedding_text = f"""
        Skills: {', '.join(resume.skills)} 
        Projects: {', '.join(resume.projects) if resume.projects else "Not mentioned"} 
        Education: {', '.join(resume.education) if resume.education else "Not mentioned"}
        Certification: {', '.join(resume.certifications) if resume.certifications else "Not mentioned"}
        Domains: {', '.join(resume.domain_expertise) if resume.domain_expertise else "Not mentioned"} 
        Summary: {resume.summary}
        """
    return embedding_text

def jd_evaluation_format(jd: JDSchema = None, jd_model: JDDataModel = None):
    if jd_model:
        jd_text = f"""
        Role: {jd_model.title} 
        Job type: {jd_model.jobType}
        Location: {', '.join(jd_model.location) if jd_model.location else "Not mentioned"}
        Required Skills: {', '.join(jd_model.mandatorySkills) if jd_model.mandatorySkills else "Not mentioned"} 
        Preferred Skills: {', '.join(jd_model.preferredSkills) if jd_model.preferredSkills else "Not mentioned"} 
        Responsibilities: {', '.join(jd_model.responsibility) if jd_model.responsibility else "Not mentioned"}
        """
    else:
        jd_text = f"""
        Role: {jd.role} 
        Job type: {jd.job_type}
        Location: {', '.join(jd.location) if jd.location else "Not mentioned"}
        Required Skills: {', '.join(jd.required_skills) if jd.required_skills else "Not mentioned"} 
        Preferred Skills: {', '.join(jd.preferred_skills) if jd.preferred_skills else "Not mentioned"} 
        Responsibilities: {', '.join(jd.responsibilities) if jd.responsibilities else "Not mentioned"}
        """
    return jd_text

def jd_raw_text(jd: JDSchema = None, jd_model: JDDataModel = None):
    if jd_model:
        jd_text = f"""
        Role: {jd_model.title}
        Location: {jd_model.location}
        Minimum experience years: {jd_model.minExperience}
        Job type: {jd_model.jobType}
        Required Skills: {', '.join(jd_model.mandatorySkills) if jd_model.mandatorySkills else "Not mentioned"}
        Preferred Skills: {', '.join(jd_model.preferredSkills) if jd_model.preferredSkills else "Not mentioned"} 
        Responsibilities: {', '.join(jd_model.responsibility) if jd_model.responsibility else "Not mentioned"}
        """
    else:   
        jd_text = f"""
        Role: {jd.role}
        Location: {jd.location}
        Minimum experience years: {jd.minimum_experience_years}
        Job type: {jd.job_type}
        Required Skills: {', '.join(jd.required_skills) if jd.required_skills else "Not mentioned"}
        Preferred Skills: {', '.join(jd.preferred_skills) if jd.preferred_skills else "Not mentioned"} 
        Responsibilities: {', '.join(jd.responsibilities) if jd.responsibilities else "Not mentioned"}
        """
    return jd_text