# AI Interview

An AI-powered technical interview system that conducts automated interviews using Large Language Models.

## Features

### Core Features

#### Multi-language Support
- Supports both English and Chinese interviews
- Automatic language detection and response
- Consistent evaluation across languages

#### Dynamic Interview Process
- Customizable job roles and requirements
- Knowledge point-based question generation
- Adaptive difficulty based on candidate responses
- Real-time interview progress tracking

#### Answer Analysis
- Real-time response evaluation
- Structured feedback generation
- Technical accuracy assessment
- Code review and analysis
- Answer completeness checking

#### Interview Control
- Time tracking and management
- Interview pause/resume capability
- Manual interview termination ("End Interview" command)
- "Give up" option for difficult questions

#### Result Generation
- Comprehensive interview summary
- Technical skill assessment
- Knowledge coverage report
- Score breakdown by topic
- Improvement suggestions

### Technical Features

#### State Management
- Persistent interview state
- Recoverable interview sessions
- Question-answer history tracking
- Interview checkpoint system

#### Logging System
- Detailed interview logs
- Debug information for development
- Performance metrics tracking
- Error handling and reporting

#### Configuration
- Customizable model selection
- Adjustable interview parameters
- Environment-based settings
- Prompt template management

## Installation

### Install from PyPI
```bash
pip install ai-interview
```

### Install from source
```bash
git clone https://github.com/gckjdev/ai-interview.git
cd ai-interview
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
from agent.workflow import build_graph
from datetime import datetime

# Initialize interview
graph = build_graph()

# Configure interview parameters
inputs = {
    "job_title": "Python Developer",
    "knowledge_points": [
        "Python",
        "Data Structures",
        "Algorithms",
        "System Design"
    ],
    "interview_time": 30,  # minutes
    "language": "English",  # or "Chinese"
    "start_time": datetime.now(),
    "qa_history": []
}

# Run interview
for output in graph.stream(inputs):
    if "user_answer" in output:
        # Get user's answer when prompted
        answer = input("Your answer: ")
        # Use "End Interview" to terminate the interview
        output["user_answer"] = answer
```

### Interview Commands
- `End Interview` - Terminate the interview
- `Give up` - Skip current question
- `Ctrl+C` - Emergency stop

## Configuration

### Environment Variables
Create a `.env` file in your project root:

```bash
# Required: OpenAI API configuration
OPENAI_API_KEY=your-api-key
OPENAI_BASE_URL=your-base-url
```

### Model Configuration
The system uses GPT-4 by default. You can configure different models:
```python
config = {"configurable": {"model_name": "gpt-4"}}
graph.stream(inputs, config=config)
```

## Requirements

- Python >= 3.10
- Dependencies:
  - langchain >= 0.3.12
  - langchain-openai >= 0.2.12
  - langgraph >= 0.2.59
  - pydantic >= 2.10.3
  - python-dotenv >= 1.0.1
  - loguru >= 0.7.3

## Project Structure

```
ai-interview/
├── agent/
│   ├── prompts/          # Interview prompt templates
│   │   ├── kickoff_interview.txt
│   │   ├── analyze_answer.txt
│   │   └── summarize_interview.txt
│   ├── workflow.py       # Main interview workflow
│   ├── qa_analyzer.py    # Answer analysis
│   └── agent_state.py    # State management
└── utils/
    ├── llm.py           # LLM configuration
    ├── log_utils.py     # Logging utilities
    └── prompt_utils.py  # Prompt handling
```

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details. 