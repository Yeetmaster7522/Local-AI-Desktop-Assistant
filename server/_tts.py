import pyttsx3
from scipy.io import wavfile
import numpy as np

class TTS:
    """
    Turns txt into speech

    Functions:
        worker: Runs in a loop. Checks sound queue for sound requests and fulfills them.
    """
    
    def __init__(self, rate=150, volume=1.0, voice_index=0, server_queue=None):
        """
        Args
            rate: rate of speech / how fast it talks
            volume: from 0 to 1. Controls volume of speech
            voice_index: allows for selection of voice from engine.getProperty("voices")
        """
        
        self.__rate = rate
        self.__volume = volume
        self.__server_queue = server_queue
        self.voice_index = voice_index

    def speak(self, txt: str) -> None:
        """
        Converts txt into speech.
        Because of some technical issues regarding multiprocessing and pyttsx3,
        this method is currently the best way to do it.

        Args:
            txt: the txt that will be turned into speech
        """

        # sets property of voice engine
        self.__engine = pyttsx3.init()
        self.__engine.setProperty("rate", self.__rate)
        self.__engine.setProperty("volume", self.__volume)

        voices = self.__engine.getProperty("voices")
        self.__engine.setProperty("voice", voices[self.voice_index].id)

        # says txt aloud and allows it to finish
        self.__engine.save_to_file(txt, "speech.wav")
        self.__engine.runAndWait()
        self.__engine.say(txt)
        if self.__server_queue:
            try:
                self.__server_queue.put_nowait(self.get_normalized_amplitude())
            except ValueError:
                pass

        self.__engine.runAndWait()
        self.__engine.stop()

    def get_normalized_amplitude(self):
        epsilon = 1e-10
        rate, data = wavfile.read("speech.wav")
        dbs = 20 * np.log10(np.abs(data) + epsilon)
        
        return rate, (dbs - dbs.min()) / (dbs.max() - dbs.min())