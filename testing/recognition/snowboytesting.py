import speech_recognition as sr


recog = sr.Recognizer()

mic = sr.Microphone(device_index=1)

with mic as source:
    recog.adjust_for_ambient_noise(source)

    audio = recog.listen(source)

# SCRAPPED BECAUSE SNOWBOY DOES NOT SUPPORT WINDOWS


