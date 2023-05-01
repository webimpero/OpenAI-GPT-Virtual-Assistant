import openai
import os
import pyaudio
import speech_recognition as sr
from google.cloud import texttospeech
import pygame

# Set up OpenAI API credentials
openai.api_key = "PUT_YOUR_OPENAI_KEY_HERE" # Add OpenAI KEY to this line.

# Set up Google Cloud API credentials
credential_path = r"PUT_GOOGLE_JSON_FILE_HERE" # Add JSON file PATH to this line.
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

def text_to_speech(text):
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",   # Add country code to this line.
        name="en-US-Wavenet-A",  # Add voice name to this line.
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open("output.mp3", "wb") as out:
        out.write(response.audio_content)

def play_audio_file(filename):
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.quit()

def recognize_speech_from_mic():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say something!")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, timeout=20)

    try:
        text = r.recognize_google(audio, language="en-US")
        print("You said: " + text)
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition can't understand audio")
        return None
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return None

wake_word = "hello"
while True:
    speech_text = recognize_speech_from_mic()
    
    if speech_text is None:
        continue

    speech_text = speech_text.lower()

    if wake_word in speech_text:
        print("Wake word detected!")
        break

text_to_speech("Hi I'm your personal assistant, how can I help you?")
play_audio_file("output.mp3")

while True:
    print("Listening to your input...")
    speech_text = recognize_speech_from_mic()
    
    if speech_text is None:
        continue

    speech_text = speech_text.lower()

    if "close" in speech_text:
        break

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"'{speech_text}'",
        max_tokens=250,
        n=1,
        stop=None,
        temperature=0.7,
    )

    response_text = response.choices[0].text.strip()

    text_to_speech(response_text)
    play_audio_file("output.mp3")