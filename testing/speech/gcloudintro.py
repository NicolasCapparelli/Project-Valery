from google.cloud import texttospeech
import pyaudio


p = pyaudio.PyAudio()
# G_cloud main class
client = texttospeech.TextToSpeechClient()


def synthesize_text(text):

    input_text = texttospeech.types.SynthesisInput(text=text)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-US', name="en-US-Wavenet-F",
        ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)

    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    response = client.synthesize_speech(input_text, voice, audio_config)

    # The response's audio_content is binary.
    with open('output.mp3', 'wb') as out:
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')

    import playsound
    playsound.playsound("output.mp3")


def list_voice_names():
    print(client.list_voices())


if __name__ == "__main__":
    # list_voice_names()
    synthesize_text("Sorry sir, I am unable to do that task at the moment.")
