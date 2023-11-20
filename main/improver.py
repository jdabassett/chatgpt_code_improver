import os
from openai import OpenAI, APIError
import pyperclip
import logging
import tkinter
from dotenv import load_dotenv
from rich.console import Console
from rich.theme import Theme


# load global variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# setup openAI with api key
client = OpenAI(api_key=api_key)

# set theme for printing to console.
improve_code_theme = Theme({
    "good": "bold green",
    "bad": "bold red",
    "neutral": "green",
})
console = Console(theme=improve_code_theme)

# setup logging to track errors
logging.basicConfig(
    filename='error_log.txt',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def display_results(response,timeout=120000):
    try:
        root = tkinter.Tk()
        root.geometry("400x700+200+200")
        T = tkinter.Text(root, height=50, width=80)
        l = tkinter.Label(root, text="ChatGPT Response:\nResponse copied to clipboard.\nWindow will disappear in 2 minutes.")
        l.config(font=("Courier", 14))
        l.pack()
        T.pack()
        T.insert(tkinter.END, response)
        root.after(timeout, lambda: root.destroy())
        tkinter.mainloop()
    except Exception as err:
        console.print(f"GUI is not functioning: {err}", style="bad")
        raise Exception


def improve_code(prompt: str, model="gpt-3.5-turbo") -> str:
    messages = [{
        "role": "system",
        "content": "You are a helpful assistant."
        }, {
        "role": "user",
        "content":
        f"""Can you return an improved version of this code? Return only code, no commentary or explanations.
        ```
        {prompt}
        ```
        """
    }]
    try:
        console.print("""Request made to ChatGPT to improve code.\nIf a response is not returned in 60seconds the script will terminate.""", style="neutral", sep="\n")
        # make request
        response = client.chat.completions.create(model=model, messages=messages, timeout=60)
        # if successful, print and return
        console.print("Response received!", style="neutral", sep="\n")
        console.print(f"""{response.choices[0].message.content}""", style="good", sep="\n")
        return response.choices[0].message.content
    except APIError as err:
        # print error, log error, and return empty string
        console.print(f"Error making request: {err}", style="bad")
        logging.error(f"An error occurred: {str(err)}", exc_info=True)
        return ""


if __name__ == "__main__":
    new_prompt = pyperclip.paste()
    output_code = improve_code(new_prompt)
    if output_code:
        pyperclip.copy(output_code)
        display_results(output_code)
    else:
        pyperclip.copy("Code not working check the error logs.")
