# How to Run the Streamlit App

## Installation Steps

1. **Activate Virtual Environment:**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install Streamlit specifically:
   ```bash
   pip install streamlit
   ```

3. **Verify OpenAI API Key:**
   - Open `.env` file
   - Ensure `OPENAI_API_KEY=your_key_here` is set

## Running the Application

```bash
streamlit run app.py
```

Or:

```bash
python -m streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

## Features

- **Interactive Chat Interface**: Clean, professional UI for candidate screening
- **Structured Workflow**: Collect name, email, phone, experience, position, location, tech stack
- **Phone Validation**: Default +91 (India), supports country code change
- **Tech Question Generation**: AI generates 3-5 tailored questions based on tech stack
- **Data Persistence**: Saves candidate data to `data/candidates.json`
- **Exit Keywords**: Type "exit", "quit", or "bye" to end conversation
- **Clear Chat**: Sidebar button to reset conversation

## Troubleshooting

**Streamlit not found:**
```bash
pip install streamlit
```

**OpenAI API errors:**
- Check your API key in `.env`
- Verify you have credits/quota on OpenAI account

**Rate limit errors:**
- Your API key has rate limits
- Wait a moment and try again
