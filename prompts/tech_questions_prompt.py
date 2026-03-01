"""
Technical questions prompts for different roles
"""

TECH_QUESTIONS = {
    "software_engineer": """
    Generate technical questions for a Software Engineer position focusing on:
    - Data structures and algorithms
    - System design principles
    - Coding best practices
    - Software development lifecycle
    - Version control and collaboration
    """,
    
    "data_scientist": """
    Generate technical questions for a Data Scientist position focusing on:
    - Machine learning algorithms
    - Statistical analysis
    - Data preprocessing and cleaning
    - Model evaluation and optimization
    - Programming skills (Python, R, SQL)
    """,
    
    "frontend_developer": """
    Generate technical questions for a Frontend Developer position focusing on:
    - HTML, CSS, JavaScript fundamentals
    - Modern frameworks (React, Vue, Angular)
    - Responsive design and accessibility
    - Performance optimization
    - Browser compatibility
    """,
    
    "backend_developer": """
    Generate technical questions for a Backend Developer position focusing on:
    - API design and development
    - Database design and optimization
    - Server-side programming
    - Security best practices
    - Scalability and performance
    """,
    
    "devops_engineer": """
    Generate technical questions for a DevOps Engineer position focusing on:
    - CI/CD pipelines
    - Infrastructure as Code
    - Containerization and orchestration
    - Cloud platforms (AWS, Azure, GCP)
    - Monitoring and logging
    """
}

def get_tech_questions_prompt(role: str) -> str:
    """Get technical questions prompt for a specific role"""
    return TECH_QUESTIONS.get(role.lower().replace(" ", "_"), 
                              "Generate relevant technical questions for this role.")
