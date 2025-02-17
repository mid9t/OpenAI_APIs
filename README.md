# OpenAI API Practice Project

This project is a simple Flask-based web application designed to practice using the OpenAI API. It uses a local SQLite database to store keywords and associated business case data. The app demonstrates basic CRUD operations on the database as well as how to build prompts and call ChatGPT to generate consultant-level insights based on the stored data.

## Features

- **SQLite Database Storage:**  
  Stores records with the following fields:
  - **Keyword:** Unique identifier for the case.
  - **Business Problem:** Description of the business challenge.
  - **Industry:** (Optional) Industry context.
  - **Context:** (Optional) Additional details or background.
  - **Solution:** (Optional) A proposed solution.

- **Web Interface (Flask):**  
  Provides a simple UI to:
  - List all records.
  - Add new entries.
  - Edit existing entries.
  - Delete entries.

- **OpenAI ChatGPT Integration:**  
  For each stored record, the app builds a prompt using a predefined template and calls the ChatGPT API. The response is returned in bullet-point format with:
  - A summary of the main points.
  - Potential pitfalls.
  - Follow-up questions.
  - A combined case study.
  - A consultant-level solution.

- **JSON API Endpoint:**  
  The `/runChatGPTPipeline` route processes all records and returns the ChatGPT responses as a JSON array.

## Setup Instructions

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/XayHanmonty/NeuroParallel.ai.git
   cd NeuroParallel.ai

3. **Install Dependencies:
4. Set up a virtual environment and install the requirements:

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   pip install -r requirements.txt

3. **Configure Environment Variables:Create a .env file in the project root with at least the following keys (replace the example values with your own):

   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   OPENAI_MODEL=gpt-4-turbo-preview
   MONGODB_URL=mongodb://localhost:27017
   PERPLEXITY_API_KEY=your_perplexity_api_key_here
   CHROMA_API_KEY=your_chroma_api_key_here

4. **Run the Application:

   ```bush
   python app.py

6. **Access the App:
Open your browser and navigate to http://localhost:5000 to view the interface.
