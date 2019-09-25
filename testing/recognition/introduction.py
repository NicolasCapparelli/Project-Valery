# Guide I followed to make this introduction: https://realpython.com/python-speech-recognition/#working-with-microphones
import speech_recognition as sr

# The recognition library's main class
recog = sr.Recognizer()

# Prints the list of available microphones
# print(sr.Microphone.list_microphone_names())

# Using PyAudio to get our Microphone at index 1 of the microphone list
mic = sr.Microphone(device_index=1)

# Captures sound with the microphone above until silence is detected and places data in audio variable
with mic as source:
    # Adjusts for ambient noise. Default time for adjustment is 1 second.
    # recog.adjust_for_ambient_noise(source, duration=)

    audio = recog.listen(source)

# Using Google's speech recognition engine to parse the audio into text, if text is unrecognizable, catch the exception
try:
    speech_as_text = recog.recognize_google(audio)

except sr.UnknownValueError:
    speech_as_text = "Unrecognized Speech"

print(speech_as_text)

# NOTE: The google API only allows for 50 requests PER DAY. Change this to the CMU Sphinx Engine for production
