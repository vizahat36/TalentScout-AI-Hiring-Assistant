"""
Create a Streamlit chat interface for TalentScout Hiring Assistant.

Requirements:
- Use st.session_state to persist conversation.
- Initialize ConversationManager once.
- Display chat messages in clean format.
- Handle user input and state transitions.
- When stage == generate_questions:
    - Call LLM to generate technical questions.
    - Display them.
    - Move to end stage.
- Handle exit keywords.
- Add sidebar with project description.
- Add Clear Chat button.
- Keep UI professional.
"""
import re
import streamlit as st
from services.conversation_manager import ConversationManager
from services.gemini_service import GeminiService
from prompts.system_prompt import SYSTEM_PROMPT
from prompts.tech_questions_prompt import build_technical_questions_prompt
from services.data_handler import save_candidate_data


def parse_technical_questions(raw_text: str) -> list:
    """Extract 3-5 clean technical questions from LLM output."""
    if not raw_text:
        return []

    questions = []

    for line in raw_text.splitlines():
        cleaned = line.strip()
        if not cleaned:
            continue

        cleaned = re.sub(r"^(\d+[\).:-]?\s*|[-*]\s+|Q\d+[\).:-]?\s*)", "", cleaned)

        if cleaned.endswith("?") and len(cleaned) > 15:
            questions.append(cleaned)

    if len(questions) < 3:
        sentence_candidates = re.findall(r"[^\n\r\?]{10,}\?", raw_text)
        for sentence in sentence_candidates:
            cleaned = sentence.strip()
            cleaned = re.sub(r"^(\d+[\).:-]?\s*|[-*]\s+|Q\d+[\).:-]?\s*)", "", cleaned)
            if cleaned not in questions and len(cleaned) > 15:
                questions.append(cleaned)

    deduped = []
    for question in questions:
        if question not in deduped:
            deduped.append(question)

    return deduped[:5]


st.set_page_config(page_title="TalentScout Hiring Assistant", layout="centered")

st.title("🤖 TalentScout AI Hiring Assistant")

# Sidebar
st.sidebar.title("About")
st.sidebar.info(
    "This AI-powered Hiring Assistant collects candidate information "
    "and generates tailored technical interview questions based on tech stack."
)

# Initialize session state
if "manager" not in st.session_state:
    st.session_state.manager = ConversationManager()

if "llm" not in st.session_state:
    st.session_state.llm = GeminiService()

if "messages" not in st.session_state:
    st.session_state.messages = []

manager = st.session_state.manager
llm = st.session_state.llm


# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# Initial greeting
if manager.stage == "greeting" and len(st.session_state.messages) == 0:
    greeting = manager.get_current_prompt()
    st.session_state.messages.append({"role": "assistant", "content": greeting})
    st.rerun()


# Chat input
user_input = st.chat_input("Type your response here...", disabled=manager.stage == "end")

if user_input:

    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    if manager.is_exit(user_input):
        manager.stage = "end"

    else:
        # Update state and get validation result
        success, error_msg = manager.update_state(user_input)
        
        if not success:
            # Show validation error message
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
            st.rerun()
            st.stop()

        # Special handling for question generation stage
        if manager.stage == "generate_questions" and len(manager.questions_list) == 0:
            # Just entered question generation stage - generate questions
            tech_stack = manager.candidate_data.get("tech_stack", "")
            desired_role = manager.candidate_data.get("desired_position", "")
            prompt = (
                build_technical_questions_prompt(tech_stack)
                + f"\n\nCandidate target role: {desired_role}\n"
                + "Ask exactly 3 to 5 interview questions total, tailored to both role and tech stack."
            )

            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ]

            try:
                response = llm.generate_response(messages)
                questions = parse_technical_questions(response)

                if len(questions) < 3:
                    fallback_questions = [
                        f"Can you explain your hands-on experience with {tech_stack}?",
                        f"What is a challenging problem you solved using {tech_stack}?",
                        f"How do you optimize performance and reliability when working with {tech_stack}?"
                    ]
                    questions = fallback_questions
                
                # Set questions in manager
                manager.set_questions(questions)
                
                # Show first question
                if manager.has_more_questions():
                    first_question = manager.get_next_question()
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": f"📝 Question 1 of {len(manager.questions_list)}:\n\n{first_question}"
                    })
            
            except Exception as e:
                error_response = f"❌ Technical Question Error: {str(e)}\n\nPlease note: Due to API limits, we couldn't generate custom questions.\nYour information has been saved for our team to review."
                st.session_state.messages.append({"role": "assistant", "content": error_response})
                save_candidate_data(manager.candidate_data)
                manager.stage = "end"

        elif manager.stage == "generate_questions" and len(manager.questions_list) > 0:
            # Already in question generation - user just answered a question
            # Update state already recorded the answer
            # Now ask the next question or end
            
            if manager.has_more_questions():
                next_question = manager.get_next_question()
                question_num = manager.current_question_index + 1
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"📝 Question {question_num} of {len(manager.questions_list)}:\n\n{next_question}"
                })
            else:
                # All questions answered - save and end
                summary = manager.get_all_answers()
                manager.candidate_data["technical_questions"] = manager.questions_list
                manager.candidate_data["technical_answers"] = manager.answers
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"✅ {summary}\n\nThank you for answering all the questions! Our recruitment team will contact you soon."
                })
                save_candidate_data(manager.candidate_data)
                manager.stage = "end"

        else:
            # Standard flow - not in question generation
            # Get the next prompt for the new stage
            next_prompt = manager.get_current_prompt()
            st.session_state.messages.append({"role": "assistant", "content": next_prompt})

    st.rerun()


# Clear chat button
if st.sidebar.button("Clear Conversation"):
    st.session_state.clear()
    st.rerun()
