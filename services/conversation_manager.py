"""
Create a conversation manager class for TalentScout Hiring Assistant.

Requirements:
- Implement state machine for structured hiring workflow.
- Manage stages:
    greeting
    collect_name
    collect_email
    collect_phone
    collect_experience
    collect_position
    collect_location
    collect_tech_stack
    generate_questions
    end
- Store candidate data in dictionary.
- Maintain conversation history list for LLM context.
- Detect exit keywords: exit, quit, bye.
- Provide methods:
    get_current_prompt()
    update_state(user_input)
    is_conversation_over()
- Follow clean architecture principles.
"""
import re

class ConversationManager:
    """
    Handles conversation flow and state transitions
    for the TalentScout Hiring Assistant.
    """

    EXIT_KEYWORDS = ["exit", "quit", "bye"]

    def __init__(self):
        self.stage = "greeting"
        self.candidate_data = {}
        self.conversation_history = []
        self.pending_country_code = "+91"  # Default India country code
        self.validation_error = ""  # Store validation error messages
        
        # Question tracking for staged question generation
        self.questions_list = []  # Store all generated questions
        self.current_question_index = -1  # Track which question we're on
        self.answers = []  # Store answers to questions

    def is_exit(self, user_input: str) -> bool:
        return user_input.lower().strip() in self.EXIT_KEYWORDS
    
    def validate_email(self, email: str) -> tuple:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, email):
            return True, ""
        return False, "❌ Invalid email format. Please use format: name@example.com"
    
    def validate_experience(self, experience: str) -> tuple:
        """Validate years of experience (numbers only)"""
        experience = experience.strip()
        try:
            years = float(experience)
            if 0 <= years <= 70:
                return True, ""
            return False, "❌ Experience must be between 0 and 70 years"
        except ValueError:
            return False, "❌ Please enter only numbers for experience (e.g., 5 or 5.5)"
    
    def validate_phone_number(self, phone: str) -> bool:
        """Validate that phone number contains exactly 10 digits"""
        # Remove spaces and common separators
        cleaned = phone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        # Check if it's exactly 10 digits
        return cleaned.isdigit() and len(cleaned) == 10

    def set_questions(self, questions_list: list):
        """Set the list of generated questions"""
        self.questions_list = questions_list
        self.current_question_index = 0  # Start at first question

    def get_next_question(self) -> str:
        """Get the current question to ask"""
        if self.current_question_index < len(self.questions_list):
            return self.questions_list[self.current_question_index]
        return ""

    def has_more_questions(self) -> bool:
        """Check if there are more questions to ask"""
        return self.current_question_index < len(self.questions_list)

    def record_answer(self, answer: str):
        """Record the answer to current question"""
        self.answers.append(answer)
        self.current_question_index += 1

    def get_all_answers(self) -> str:
        """Get formatted summary of all answers"""
        result = "Interview Summary:\n\n"
        for i, (question, answer) in enumerate(zip(self.questions_list, self.answers)):
            result += f"Q{i+1}: {question}\nA: {answer}\n\n"
        return result

    def get_current_prompt(self) -> str:
        prompts = {
            "greeting": "Hello! Welcome to TalentScout Hiring Assistant. Let's begin your screening process.\nWhat is your full name?",
            "collect_email": "Please provide your email address (e.g., name@example.com).",
            "collect_phone": f"Please provide your 10-digit phone number (Country code: {self.pending_country_code})\nTo change country code, type it first (e.g., +1, +44, +91):",
            "collect_experience": "How many years of professional experience do you have? (Enter numbers only, e.g., 5)",
            "collect_position": "What position(s) are you applying for?",
            "collect_location": "What is your current location?",
            "collect_tech_stack": "Please list your tech stack (languages, frameworks, databases, tools).",
            "end": "Thank you for your time. Our recruitment team will contact you soon."
        }

        return prompts.get(self.stage, "")

    def update_state(self, user_input: str) -> tuple:
        """
        Update state based on user input.
        Returns: (success: bool, error_message: str)
        """
        if self.is_exit(user_input):
            self.stage = "end"
            return True, ""

        if self.stage == "greeting":
            self.candidate_data["full_name"] = user_input
            self.stage = "collect_email"
            return True, ""

        elif self.stage == "collect_email":
            # Validate email format
            is_valid, error_msg = self.validate_email(user_input)
            if is_valid:
                self.candidate_data["email"] = user_input
                self.stage = "collect_phone"
                return True, ""
            else:
                return False, error_msg

        elif self.stage == "collect_phone":
            # Check if user is changing country code
            if user_input.startswith("+") and len(user_input) <= 4:
                self.pending_country_code = user_input
                # Stay in collect_phone stage to get the actual number
                return True, f"✓ Country code changed to {self.pending_country_code}. Now please enter your 10-digit phone number."
            
            # Validate phone number (must be 10 digits)
            if self.validate_phone_number(user_input):
                cleaned_phone = user_input.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
                self.candidate_data["phone"] = f"{self.pending_country_code} {cleaned_phone}"
                self.candidate_data["country_code"] = self.pending_country_code
                self.stage = "collect_experience"
                return True, ""
            else:
                # Invalid phone - stay in same stage
                return False, "❌ Please enter exactly 10 digits for phone number (without country code)"

        elif self.stage == "collect_experience":
            # Validate experience (numbers only)
            is_valid, error_msg = self.validate_experience(user_input)
            if is_valid:
                self.candidate_data["experience"] = user_input
                self.stage = "collect_position"
                return True, ""
            else:
                return False, error_msg

        elif self.stage == "collect_position":
            self.candidate_data["desired_position"] = user_input
            self.stage = "collect_location"
            return True, ""

        elif self.stage == "collect_location":
            self.candidate_data["location"] = user_input
            self.stage = "collect_tech_stack"
            return True, ""

        elif self.stage == "collect_tech_stack":
            self.candidate_data["tech_stack"] = user_input
            self.stage = "generate_questions"
            return True, ""

        elif self.stage == "generate_questions":
            # In this stage, we handle questions one by one in app.py
            # Just record the answer here
            self.record_answer(user_input)

            return True, ""
        
        return True, ""

    def is_conversation_over(self) -> bool:
        return self.stage == "end"
