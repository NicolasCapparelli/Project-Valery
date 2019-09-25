import speech_recognition as sr
from valerymain import readyfunctions as rf
from valerymain.listeningdicators import indicators
import threading

# I.L.A: Intelligent Little Assistant

# Words that will cause Valery to start listening. 0-1 is the sensitivity of the wake word. 0 being least sensitive
FOCUS_WORDS = [("valery", 1), ("hey val", 1), ("v clear", 1), ("v lock", 1), ("ila", 1), ("hey ila", 1)]

# Words to identify intent
INTENT_WORDS_QUESTION = ["what", "how", "when", "who", "where"]
INTENT_WORDS_COMMUNICATION = ["message", "call", "email", "text", "send", "tell"]
INTENT_WORDS_SPECIAL = ["lock", "minimize"]
INTENT_WORDS_ACTION = ["find", "turn", "close", "copy", "look", "record", "display", "listen", "run"]
INTENT_WORDS_OPERATING_SYSTEM = ["open", "search"]

# These words are actually to be parsed with the background listening interpreter because they need to be executed
# quickly. The keyword val must be said directly beforehand as to not confuse the interpreter
INTENT_WORDS_READY_FUNCTIONS = ["v shutdown", "v lock", "v clear"]

SUB_INTENT_WORDS = ["then", "also"]

# platforms
PLATFORMS = ["discord", "text", "email"]


# SRL = Speech Recognition Library
class Valery:
    def __init__(self):

    # Settings
        # The recognition engine used to parse speech to text
        self.recog_engine = "b_speech"

        # The amount of time the background listener listens for a phrase in seconds
        self.background_interval = .7  # 1.3

        # The threshold for the microphone to pickup noise
        self.threshold = 500

        self.ambient_noise_real_noise_ratio = 2.0  # Default 1.5

        #  The minimum length of silence (in seconds) that will register as the end of a phrase.
        self.pause_length = .5  # Default 0.8

        # The preferred microphone
        self.preferred_source = "Microphone (Blue Snowball )"

        # Which interpreters Valery will use
        self.interpreters = None

        # The type of response valery will give be it speech, text, or both.
        self.response_type = 2

        self.listening_indicator = "lt_flash_key"  # "lt_flash_keyboard"

    # Speech Library Requirements
        self.recognizer = sr.Recognizer()
        self.source = ""
        self.configure_source()

        self.background_listener = ""

    # Cleans a command before passing it to the interpreters
    # Removes intent word and  punctuation, turns all chars to lowercase and removes any trailing or leading whitespace
    def _clean_command(self, command, intent_word):

        clean_command = command.replace(intent_word, "")
        clean_command = clean_command.translate(str.maketrans('', '', """!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""))
        clean_command = clean_command.lower()
        clean_command = clean_command.strip()

        return clean_command

    def quick_start(self):

        print("Loading interpreters...")
        self.load_interpreters()

        print("waking p1")
        self.wake()

    def load_interpreters(self, all_interpreters=True):

        # Import all interpreters
        if all_interpreters:
            import valerymain.interpreters as all_interpreters
            self.interpreters = all_interpreters
            print(self.interpreters.interpreter_windows.INTENT_WORD_DICT.keys())

        else:
            print("Only importing some interpreters")

        # TODO: Make a way to import only some interpreters

    # Configures the mic to be used for input
    def configure_source(self):

        # Prints the list of available microphones
        mic_list = sr.Microphone.list_microphone_names()

        # If the preferred microphone is in the list, set it as the source
        if self.preferred_source in mic_list:
            self.source = sr.Microphone(device_index=mic_list.index(self.preferred_source))

        # Else use the default mic as source
        else:
            self.source = sr.Microphone()

        # Recognizer settings
        self.recognizer.dynamic_energy_ratio = self.ambient_noise_real_noise_ratio
        self.recognizer.energy_threshold = self.threshold
        self.recognizer.dynamic_energy_threshold = True

    # Tells Valery to start listening in the background
    def wake(self):

        print("Waking up...")

        # Listen to phrases in the background with 1 second intervals after
        self.background_listener = self.recognizer.listen_in_background(source=self.source,
                                                                        callback=self.background_interpreter,
                                                                        phrase_time_limit=self.background_interval)

    # Interprets phrases picked up Valery's background listening
    def background_interpreter(self, recognizer, audio_data):

        # Using PocketSphinx to parse the audio data to text, looking specifically for keywords (focus words)
        try:
            speech_as_text = self.recognizer.recognize_sphinx(audio_data, keyword_entries=FOCUS_WORDS)
            speech_as_text = speech_as_text.strip()

            # print("!!!!! " + speech_as_text)

        except sr.UnknownValueError:
            speech_as_text = "Unrecognized Speech"

        # If the wake words are recognized, start listening with the main interpreter
        if "valery" in speech_as_text or "hey val" in speech_as_text or "ila" in speech_as_text:
            self.focus()

        # If speech as text is any of the words in INTENT_WORDS_READY_FUNCTIONS
        elif speech_as_text in INTENT_WORDS_READY_FUNCTIONS:

            print("RF")

            # Call the function stored in the function dictionary with the key being the word that was said
            rf.function_dict[speech_as_text]()

        # If no wake words are found
        else:
            print("NON: ", speech_as_text)
            pass

    # Tells valery to start listening for a command
    def focus(self):

        indicators.start()

        # Calls the listening indicator function # TODO: Check for leftover threads?
        s = threading.Thread(target=indicators.INDICATORS[self.listening_indicator])
        s.start()

        # Start listening and store the audio in this variable
        audio_data = self.recognizer.listen(self.source)

        indicators.stop()

        # Pass the data to the main interpreter
        self.main_interpreter(audio_data)

    # Handles the interpretation of commands | Takes an AudioData object as its only parameter
    def main_interpreter(self, audio_data=None, passed_command=None):

        sub_intent = False
        second_command = None

        # If there is audio data to be parsed
        if audio_data is not None:
            # Parse the audio data, turning it into a string, then turn all characters in the string to lowercase
            command = self.parse_with_select_engine(audio_data)

        # If there is a command that was passed
        elif passed_command is not None:
            command = passed_command.strip()

        else:
            print("No data was passed to interpret")
            return

        # Make all of the words in the command lowercase
        command = command.lower()

        # If any of the words in the SUB_INTENT_WORDS list are in the command, set the sub-intent flag to true
        if any(word in command for word in SUB_INTENT_WORDS):

            # TODO: Check for sub intent AFTER the and. so if any(word in command.split(" ")[index of and] in SUB_INTENT_WORDS)
            sub_intent = True

        # If the word "and" is in the command, but there are no sub intent words, treat everything after "and" a separate command
        elif "and" in command:
            second_command = command.split("and")[1]

        # The first word in the command, used to identify the intent of the command
        intent_word = command.split(" ", 1)[0]

        print("interpreting")

        # Logic to figure out intent of command
        if intent_word in INTENT_WORDS_QUESTION:
            # Send to question interpreter
            s = 11

        elif intent_word in INTENT_WORDS_COMMUNICATION:
            # Send to communication interpreter
            s = 11

        elif intent_word in INTENT_WORDS_OPERATING_SYSTEM:

            try:
                clean_command = self._clean_command(command, intent_word)
                response = self.interpreters.interpreter_windows.main_windows_interpreter(intent_word, clean_command, sub_intent)
                self.talk(response)

            except ImportError:
                print("This module does not exist or is not currently loaded")
                print(">: ", command)

            except AttributeError:
                print("This module does not exist or is not currently loaded")
                print(">>: ", command)

        else:
            print("No intent found")
            print(">>>: ", command)

        # If there is a second command, run this method again with that command
        if second_command is not None:

            print("SECOND TIME THROUGH MAIN INTERPRETER")
            self.main_interpreter(None, second_command)


        return

    # This method will attempt to parse the data with the preferred recognition engine, but if it's unable to it will
    # attempt to use all of the other ones.
    # Takes an AudioData object as its only parameter | Returns a string containing the parsed text
    def parse_with_select_engine(self, audio_data):

        # Choosing which engine to use
        if self.recog_engine == "b_speech":

            try:
                # Using bing_speech to parse the audio data to text
                speech_as_text = self.recognizer.recognize_bing(audio_data, key="bb344e9e8de04d8983e9d07c83512d35")

            # If the audio cannot be parsed
            except sr.UnknownValueError:
                speech_as_text = "unrecognized"

            # If there is a problem with the bing_speech library (API limit reach or no internet)
            except sr.RequestError:

                # Change the desired recognition engine to google_cloud
                self.recog_engine = "g_cloud"

                # Re-run this method (because it will use the sphinx interpreter)
                self.parse_with_select_engine(audio_data)

                return

        # If it should recognize with google_cloud
        elif self.recog_engine == "g_cloud":

            # Using PocketSphinx to parse the audio data to text
            try:
                speech_as_text = self.recognizer.recognize_sphinx(audio_data)

            except sr.UnknownValueError:
                speech_as_text = "unrecognized"

            # If there is a problem with the google_cloud library (API limit reach or no internet)
            except sr.RequestError:

                # Change the desired recognition engine to sphinx
                self.recog_engine = "p_sphinx"

                # Re-run this method (because it will use the sphinx interpreter)
                self.parse_with_select_engine(audio_data)

                return

        # If it should recognize with pocketsphinx
        elif self.recog_engine == "p_sphinx":

            # Using PocketSphinx to parse the audio data to text
            try:
                speech_as_text = self.recognizer.recognize_sphinx(audio_data)

            # If the audio cannot be parsed
            except sr.UnknownValueError:
                speech_as_text = "unrecognized"

        else:
            return

        return speech_as_text

    # speech_response: speechresponses.SpeechResponse Object
    # response_type: 0 == text and speech | 1 == speech only | 2 == text only
    def talk(self, speech_response, response_type=None):

        # If no response type is passed, use the one configured in the settings
        if response_type is None:
            response_type = self.response_type

        if response_type == 0:

            print(speech_response.text)

            # Attempt to play sound. If there is an issue switch response_type to text only
            try:
                speech_response.play_audio()

            except Exception:

                # TODO: Figure out the correct exception to catch here
                self.talk(speech_response, 2)

        elif response_type == 1:
            speech_response.play_audio()

        elif response_type == 2:
            print(speech_response.text)

    def output(self, output):
        print(output)

    # TODO: Create Auto Ambient Adjust Algorithm
    def auto_ambient_adjust(self):

        # This method will use the background listening thread and average the loudness in decibels.
        # If decibel average changes, time to re-adjust the ambient noise
        return 11


