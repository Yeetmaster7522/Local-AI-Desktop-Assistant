"""
BRAINSTORM
- time management
    - planning schedules, deadlines, and meetings
- information management
    - organising files, managing contacts, and handling documents
- task coordination
    - scheduling tasks
    - following up on work
    - helping with assignments across different departments
- communication support
    - handling emails
    - scheduling calls
    - managing digital correspondence
- strategic planning
    - creating action plans and setting goals
- workflow automation
- play games
- look busy

NEED TO
- open programs
"""

# import os
import time
import subprocess
from pyautogui import screenshot
import tkinter as tk
from tkinter import messagebox
import json
# from playwright.sync_api import sync_playwright
# import html2text
from PIL import Image
from ddgs import DDGS

def get_datetime() -> str:
    """
    Returns local time as str
    """
    
    return time.strftime("%a %d %b %Y %H:%M:%S Local Time", time.localtime())

def take_screenshot() -> Image:
    """
    Takes a screenshot at screenshot.png
    """

    screenshot("screenshot.png")

def run_command(command: str) -> tuple[str, str] | None:
    """
    Executes a system command asynchronously after explicit user confirmation via a GUI dialog.

    Args:
        command (str): The system command

    Returns:
        tuple[str, str] | None: A tuple containing (stdout, stderr) as strings if the 
            user approves execution. Returns None if the user rejects the action or 
            closes the confirmation window.
    """
    output = None

    root = tk.Tk()
    root.withdraw()

    response = messagebox.askyesno(title="Confirmation", message="Do you want to proceed?", detail=command, icon="warning")

    if response:
        process = subprocess.Popen(
            command.split(" "),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
            )

        output = process.communicate()

    return output

def get_website_content(url: str) -> str:
    """
    Fetches the content of a webpage in the markdown format

    Args:
        url (str): The webpage url/address
    
    Returns:
        str: A str containing the content of the webpage in a markdown format
    """

    result = DDGS().extract(url, fmt="text_markdown")["content"]
    print("webpage content: " + result)
    return result

def web_search(query: str, max_results: int) -> list[str]:
    """
    Finds the top results of a web search including the title, href, and brief description.
    Use alongside get_website_content for more information.

    Args:
        query (str): the search terms and query
        max_results (int): the amount of results to pull

    Returns:
        str: A JSON-formatted string containing the title, href and body of the search results
    """
    result = json.dumps(DDGS().text(query, max_results=max_results, safesearch="moderate"))
    print("searches: " + result)
    return result

if __name__ == "__main__":
    # from ddgs import DDGS
    # print(DDGS().text("python programming", max_reslts=5, safesearch="off"))
    # print(DDGS().extract("https://ollama.com/", fmt="text_markdown")["content"])

    # print(get_website_content("https://www.mit.edu/"))
    pass