from ollama import chat
from subprocess import run
from queue import Queue

class LM:
    """
    Utilises ollama to locally run a language model on your computer.

    Functions:
        talk: Sends a msg to the LM and the LM responds back with a print statement and voice
        stop: Stops the LM from running
    """
    
    def __init__(
            self, 
            model: str, 
            tools: dict, 
            sound_queue: Queue,
            think=False, 
            keep_alive="30m",
            ):
        """
        Args:
            model (str): Language model being used
            tools (dict): Dictionary defining external API calls supported by the model
            sound_queue (queue): the sound queue
            think (bool): Controls language model's internal reasoning before generating an input
            keep_alive (str): duration to ensure the model remains fully responsive for the defined period
        """
        
        self.__messages: list = []

        self.__model: str = model
        self.__tools: dict = tools
        self.__sq = sound_queue

        self.__think: bool | str = think
        self.__keep_alive: str = keep_alive

    def talk(self, msg: str, role="user") -> None:
        """
        sends message to LM and manages its outputs

        Args:
            msg: the msg being sent to the LM
            role: the role of the messenger
        """

        # if the msg is not empty it will append it to the chat history
        if msg != "": self.__messages.append({ "role": role, "content": msg })

        # gets output from LM
        content, tool_calls = self.__stream()

        # append accumulated fields to the messages for the next request
        if content or tool_calls:
            self.__messages.append({ "role": "assistant", "content": content, "tool_calls": tool_calls })

        # gets the information from the tool calls
        for call in tool_calls:
            try:
                fn = self.__tools[call.function.name]
                result = fn(**call.function.arguments)
                self.__messages.append({ "role": "tool", "tool_name": call.function.name, "content": str(result) })
            except Exception as e:
                print(e)

        # makes LM talk again to discuss results from tool calls
        if tool_calls: self.talk("")

    def __stream(self) -> tuple[str,list]:
        """
        Gets the output and tools from the LM.
        It will stream the content of the output in real time.

        Returns:
            content (str): The text output from the LM
            tool_calls (list): The tool calls from the LM
        """
        
        # get response from model
        stream = chat(
            model=self.__model,
            messages=self.__messages,
            stream=True,
            think=self.__think,
            tools=self.__tools.values(),
            keep_alive=self.__keep_alive,
        )

        # stream response
        content = ""
        tool_calls = []

        for chunk in stream:
            print(chunk.message.content, end="", flush=True)
            self.__sq.put(chunk.message.content)
            content += chunk.message.content

            if chunk.message.tool_calls:
                print(chunk.message.tool_calls)
                tool_calls.extend(chunk.message.tool_calls)

        return content, tool_calls

    def stop(self) -> None:
        """
        Kills the model by passing a command directly to the OS.
        """

        run(["ollama", "stop", self.__model])
        print("Model stopped succesfully")