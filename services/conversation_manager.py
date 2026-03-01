"""
Conversation Manager for handling interview flow
"""
from services.llm_service import LLMService
from services.data_handler import DataHandler
from prompts.system_prompt import SYSTEM_PROMPT, INTERVIEWER_PROMPT
from utils.validators import validate_input

class ConversationManager:
    """Manages the conversation flow during interviews"""
    
    def __init__(self):
        self.llm_service = LLMService()
        self.data_handler = DataHandler()
        self.conversation_history = []
        self.current_candidate = None
    
    def start_interview(self):
        """Start a new interview session"""
        print("\nStarting interview session...")
        print("Type 'exit' to end the interview\n")
        
        # Get candidate information
        candidate_name = input("Candidate Name: ").strip()
        position = input("Position Applied For: ").strip()
        
        if not validate_input(candidate_name) or not validate_input(position):
            print("Invalid input. Please try again.")
            return
        
        self.current_candidate = {
            "name": candidate_name,
            "position": position,
            "responses": []
        }
        
        # Initialize conversation
        system_message = SYSTEM_PROMPT
        position_prompt = INTERVIEWER_PROMPT.format(position=position)
        
        self.conversation_history = [
            {"role": "system", "content": system_message},
            {"role": "system", "content": position_prompt}
        ]
        
        # Start interview loop
        self.conduct_interview()
    
    def conduct_interview(self):
        """Conduct the interview conversation"""
        # Get initial greeting
        greeting = self.llm_service.generate_response(self.conversation_history)
        print(f"\nInterviewer: {greeting}\n")
        self.conversation_history.append({"role": "assistant", "content": greeting})
        
        while True:
            # Get candidate response
            user_input = input("Candidate: ").strip()
            
            if user_input.lower() == 'exit':
                self.end_interview()
                break
            
            if not validate_input(user_input):
                print("Please provide a valid response.\n")
                continue
            
            # Add to conversation history
            self.conversation_history.append({"role": "user", "content": user_input})
            self.current_candidate["responses"].append(user_input)
            
            # Get AI response
            ai_response = self.llm_service.generate_response(self.conversation_history)
            print(f"\nInterviewer: {ai_response}\n")
            self.conversation_history.append({"role": "assistant", "content": ai_response})
    
    def end_interview(self):
        """End the interview and save data"""
        print("\nEnding interview...")
        
        if self.current_candidate:
            # Save candidate data
            self.data_handler.save_candidate(self.current_candidate)
            print(f"Interview data saved for {self.current_candidate['name']}")
        
        print("Thank you for using TalentScout AI Hiring Assistant!\n")
    
    def get_conversation_summary(self) -> str:
        """Get a summary of the conversation"""
        return "\n".join([f"{msg['role']}: {msg['content']}" 
                         for msg in self.conversation_history])
