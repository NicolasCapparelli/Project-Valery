import speech_recognition as sr
import time

# Recognizer Class
recog = sr.Recognizer()


def main():

    # The source from which the sound is coming from (Microphone)
    mic = sr.Microphone(device_index=1)

    # Attempt to use capture device as microphone
    try:

        # Calibrating the mic for ambient noise
        with mic as source:
            recog.adjust_for_ambient_noise(source)

    # OSError is raised the capture device at the given index does not exist
    except OSError:
        print("No microphones detected")

    # Runs a new thread for the speech library to start listening in the background, takes an argument of the
    # recognizer class and a function that takes two parameters, a source and a callback, which will be called once
    # the background listener has picked up a phrase
    background_listener = recog.listen_in_background(source=mic, callback=callback)

    # Since the background thread will not stop the stop the program from ending, we have the main thread sleep for 20
    # seconds while we test the background listener
    time.sleep(60)

    # Changing the variable in the function background_listener to False, which will stop the background listener
    background_listener(wait_for_stop=False)

    print("Finished!")


# The function that will be called once the background listener picks up a phrase
def callback(recog_instance, audio_data):

    # Using PocketSphinx to parse the audio data to text
    try:

        speech_as_text = recog.recognize_sphinx(audio_data,
                                                keyword_entries=[("ila", 1), ("hey ila", 1)])  # ila ela

        # speech_as_text = recog.recognize_sphinx(audio_data,
        #                                       grammar="hello.jsgf")

    except sr.UnknownValueError:
        speech_as_text = "Unrecognized Speech"

    print(speech_as_text)


if __name__ == "__main__":
    main()


