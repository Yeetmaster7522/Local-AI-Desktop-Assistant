# Set ollama api key to access web search and fetch tools
import os

with open("private/apikey.txt", "r") as f:
    key = f.read()

os.environ["OLLAMA_API_KEY"] = key
print(os.getenv("OLLAMA_API_KEY"))


from chat import LM
from tts import TTS
from stt import STT
from threading import Thread
from queue import Queue
import tools


def worker() -> None:
    """
    A worker thread that manages requests
    """

    buffer = ""

    while True:
        chunk = sound_queue.get()
        buffer += chunk

        if buffer.endswith((".", "!", "?", "\n", "]", ",", ":", "。", "？", "～", "、")):
            tts.speak(buffer)
            buffer = ""
        sound_queue.task_done()

        # user_input = voice_queue.get().strip()
        # if user_input != "":
        #     lm.talk(user_input)
        
        # voice_queue.task_done()

def main() -> None:
    """
    Gets user input and passes it onto LM as well as flushing the voice queue.
    When user types /break it will stop the process.
    
    Args:
        sound_queue (Queue): Requests from the LM to say things
    """

    while True:
        # get message
        msg = input("\n\n-> ")
        if msg == "/break": break

        # flush voice queue
        while not sound_queue.empty():
            sound_queue.get_nowait()
            sound_queue.task_done()

        lm.talk(msg)
        
    # kill model
    lm.stop()

if __name__ == "__main__":
    # multithreading
    sound_queue = Queue()
    voice_queue = Queue()

    # setup language model and text-to-speech
    lm = LM(
        model="astra-q-uncensored", 
        tools={
            "web_search": tools.web_search, 
            "get_website_content": tools.get_website_content,
            "get_datetime": tools.get_datetime,
            "take_screenshot": tools.take_screenshot,
            "run_command": tools.run_command,
        },
        sound_queue=sound_queue
    )
    # set up TTS and STT
    tts = TTS(rate=200, voice_index=2)
    # stt = STT(voice_queue)

    t1 = Thread(target=main)
    t2 = Thread(target=worker, daemon=True)
    t1.start()
    t2.start()

    t1.join()