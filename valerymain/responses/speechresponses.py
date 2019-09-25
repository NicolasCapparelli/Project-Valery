import playsound
from valerymain.responses.types import postaction
from valerymain.responses.types import greetings
from valerymain.responses.types import windows
from valerymain.responses.types import subintent


class SpeechResponse:
    def __init__(self, response_text, response_file):
        self.text = response_text
        self.audio_file_path = response_file

    def play_audio(self):
        playsound.playsound(self.audio_file_path)


# Chooses a random response from the given response type.
# Takes in one of the dictionaries above (speech_responses.COMPLETE_ACTION, etc...) | Returns SpeechResponse
def choose_random_response(response_type=postaction.COMPLETE_ACTION):
    import random

    selection = random.choice(list(response_type.keys()))

    return SpeechResponse(selection, response_type[selection])


