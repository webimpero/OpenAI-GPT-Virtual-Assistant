# GPT-Voice-Assistant
This is a Python voice assistant that requires a wake word to request the OpenAI GPT API. And a close word to close the program.
For transcribing this program implements Speech Recognition. Text-to-speech is done with Google API.

# Installation
1. Clone the repository and navigate to the project directory.
2. Install the requirements. Use `pip install -r requirements.txt` to install all the required libraries
3. Sign up for an account at https://beta.openai.com/signup/, then find your API key.
4. Create a Google Cloud account and set up a project at https://cloud.google.com/. 
    - Enable the Text-to-Speech API for your project and create a JSON key for your service account. 
    - Download the JSON key file and provide its path in the code.
5. Make sure your microphone is properly connected and working.
After meeting these requirements, you should be able to run the code successfully.