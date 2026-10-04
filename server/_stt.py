import speech_recognition as sr
from queue import Queue

class STT:
    """
    Utilises faster whisper to listen to speech in the background.

    Functions:
        stop: stops the STT from running
    """
    def __init__(self, voice_queue: Queue, device_index=None):
        """
        Args:
            voice_queue (Queue): the queue for where the voices will be sent
            device_index (str | None): which device it will take input from
        """
        self.__r = sr.Recognizer()
        self.__r.pause_threshold = 1.5
        self.__r.dynamic_energy_threshold = False
        self.__m = sr.Microphone(device_index=device_index, sample_rate=16000)

        self.voice_queue = voice_queue
        
        print("calibrating")
        with self.__m as source:
            self.__r.adjust_for_ambient_noise(source)
        print("finished calibrating, starting recording")

        self.__stop_listening = self.__r.listen_in_background(self.__m, self.__callback)

    def __callback(self, recognizer, audio) -> None:
        """
        Tries to understand what was spoken and put it into the voice queue
        """    
        
        try:
            recording = recognizer.recognize_faster_whisper(audio, init_options={"compute_type": "float32"})
            print(recording)
            self.voice_queue.put(recording)
        except sr.UnknownValueError:
            print("Whisper could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Whisper; {e}")

    def stop(self) -> None:
        """
        stops listening
        """
        
        self.__stop_listening(wait_for_stop=False)

if __name__ == "__main__":
    import time

    stt = STT()
    while True: time.sleep(0.1)