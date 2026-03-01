"""
Technical questions prompts for different roles
"""


def build_technical_questions_prompt(tech_stack: str) -> str:
    """
    Builds structured prompt for generating technical questions
    based on candidate's tech stack.
    """

    return f"""
You are a senior technical interviewer.

Candidate Tech Stack:
{tech_stack}

Generate 3-5 technical questions per technology.

Rules:
- Include conceptual questions.
- Include at least one scenario-based question.
- Difficulty level: Moderate to Advanced.
- Keep questions concise.
- Avoid generic beginner questions.
"""
