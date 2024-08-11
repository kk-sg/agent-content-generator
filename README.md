# AI Content Generator

## Overview

This project is an AI-powered content generation tool that creates blog posts on any given topic. It utilizes OpenAI's language models and the CrewAI framework to plan, write, and edit articles automatically.

## Features

- Automated content planning, writing, and editing
- Web interface using Streamlit
- Command-line interface for basic operations
- Modular design with reusable components
- OpenAI API integration for advanced language processing

## Project Structure

```
ai-content-generator/
│
├── utils/
│   ├── common_utils.py
│   └── ai_models.py
│
├── research_write_article_streamlit.py
├── research_write_article_basic.py
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ai-content-generator.git
   cd ai-content-generator
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key (you'll be prompted to enter this when running the application).

## Usage

### Local Web Interface

To run the Streamlit local web application:

```
streamlit run research_write_article_streamlit.py
```

Access the web interface at `http://localhost:8501`.

### Command-Line Interface

To run the basic version in the terminal:

```
python research_write_article_basic.py
```

Follow the prompts to enter your OpenAI API key and the topic for the article.

## Modules

### utils/common_utils.py

Contains reusable utility functions for:
- Managing API keys
- Handling user input
- Displaying content and messages
- Creating download buttons

### utils/ai_models.py

Defines custom AI model classes, including:
- `OpenAILanguageModel`: A wrapper for OpenAI's language models

## Dependencies

Main dependencies include:
- crewai
- openai
- streamlit
- langchain

For a full list of dependencies, see `requirements.txt`.

## Live Demo

Access the live Streamlit web application at [https://basic-conversation-chatbot.streamlit.app/](https://agent-content-generator.streamlit.app/)

## Contributing

Contributions to this project are welcome. Please fork the repository and submit a pull request with your changes.

## Acknowledgments

- OpenAI for providing the language model API
- CrewAI for the AI agent framework
- Streamlit for the web application framework
