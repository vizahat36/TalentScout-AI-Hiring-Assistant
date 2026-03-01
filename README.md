# TalentScout AI Hiring Assistant

An AI-powered hiring assistant that conducts intelligent interviews and evaluates candidates.

## Features

- Automated candidate interviews
- Technical question generation
- Intelligent conversation management
- Candidate data storage and evaluation

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure your `.env` file with necessary API keys
5. Run the application:
   ```bash
   python app.py
   ```

## Project Structure

```
TalentScout-AI-Hiring-Assistant/
├── app.py                      # Main application entry point
├── config/                     # Configuration files
├── prompts/                    # AI prompt templates
├── services/                   # Core business logic
├── utils/                      # Utility functions
└── data/                       # Data storage
```

## Configuration

Edit `.env` file to add your API keys and configuration:
- `OPENAI_API_KEY`: Your OpenAI API key
- Other configuration as needed

## Usage

Run the main application:
```bash
python app.py
```

## License

MIT License
