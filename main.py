#!/usr/bin/env python
from widgets.loading_modal import LoadingModal
from widgets.confirmation_dialog import confirm_action
from create_prompt import create_prompt
from functools import partial
import os
import mistune
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk, filedialog
import customtkinter
from customtkinter import CTkLabel, CTkFrame, CTkButton, CTk, CTkRadioButton, CTkOptionMenu
import openai
import hashlib
import csv
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


# Set up the OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY', None)

if openai.api_key is None:
    print("Please set the OPENAI_API_KEY environment variable.")

USE_LISTBOX = True

cuomtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")


def generate_prompt(row):
    # title = row['title']
    return create_prompt(**row)


def markdown_to_html(content: str):
    # use mistune to parse markdown as html
    generated_html = mistune.markdown(content)

    # make BeautifulSoup
    soup = BeautifulSoup(generated_html, "html.parser")
    # prettify the html
    prettyHTML = soup.prettify()

    return prettyHTML


class Application(CTkFrame):
    sendFaq: tk.BooleanVar

    def __init__(self, master=None):
        super().__init__(master=master)
        # self.pack(pady=20, padx=20, fill="both", expand=True)

        self.grid(row=0, column=0, sticky=tk.NSEW, padx=20, pady=20)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        # self.rowconfigure(0, weight=0)
        # self.rowconfigure(2, weight=100)

        self.master = master
        self.sendFaq = tk.BooleanVar(master=None, value=True)

        # Set up a set to keep track of processed rows and prompts
        self.processed_rows = []

        # Load processed rows from file if it exists
        if os.path.isfile("processed_rows.txt"):
            with open("processed_rows.txt", "r") as f:
                self.processed_rows = f.read().splitlines()

        # Keep track of previous prompts to display in listbox
        self.processed_prompts = []

        self.current_prompt = ""

        # Create a variable to store the selected file path
        self.file_path = ""

        self.create_widgets()

    def create_widgets(self):
        # Create a label and button for selecting a CSV file
        self.file_label = CTkLabel(self, text="Select a CSV file:")
        self.file_label.grid(row=0, column=0, padx=5, pady=5)
        self.file_button = CTkButton(self,
                                     text="Browse",
                                     command=self.select_file)
        self.file_button.grid(row=0, column=1, padx=5, pady=5, sticky=tk.NW)

        # Create a label and text box for displaying the output
        self.output_label = CTkLabel(self, text="Output:")
        self.output_label.grid(row=1, column=0, padx=5, pady=5)
        self.output_text = tk.Text(self)
        self.output_text.grid(row=2, column=0, columnspan=2, padx=0, pady=0)

        # Create a label and listbox for displaying the current and processed prompts
        self.prompt_label = CTkLabel(self, text="Current prompt:")
        self.prompt_label.grid(row=4, column=0, padx=5, pady=5)
        if USE_LISTBOX is True:
            self.prompt_listbox = tk.Listbox(self, width=40, height=5)
            self.prompt_listbox.grid(row=2,
                                     column=3,
                                     columnspan=2,
                                     rowspan=2,
                                     padx=5,
                                     pady=5,
                                     sticky=tk.NW)
            self.prompt_listbox.insert(0, *self.processed_prompts)

        # Create a button for generating chat completion
        self.generate_button = CTkButton(self,
                                         text="Generate",
                                         command=self._create_chat_completion)
        self.generate_button.grid(row=3, column=1, padx=5, pady=5)

        # Create a button for processing the next row in the CSV file
        self.next_button = CTkButton(self,
                                     text="Next Prompt",
                                     command=self.process_next_row)
        self.next_button.grid(row=4, column=1, padx=5, pady=5)

        # Create a button for going to previous prompt
        # self.retry_button = CTkButton(self, text="Previous Prompt", command=lambda: self.previous_prompt)
        # self.retry_button.grid(row=5, column=1, padx=5, pady=5)

        # Create a dropdown for site url to upload to
        self.site_dropdown = CTkOptionMenu(
            self, values=['EFuel Nation', 'Gamerbulk'])
        self.site_dropdown.grid(row=4, column=2, padx=5, pady=5)

    def create_prompt_from_row(self, row):
        return row['title']

    def select_file(self):
        # Open a file dialog to select a CSV file
        self.file_path = filedialog.askopenfilename(filetypes=[("CSV Files",
                                                                "*.csv")])
        self.file_label.configure(text=f"Selected file: {self.file_path}")
        # TODO: Select closest value of self.site_dropdown by matching .values[] against
        # filename
        for site in self.site_dropdown._values:
            print(site)
        self.process_next_row()

    def previous_prompt(self):
        if len(self.processed_rows) == 0:
            return
        self.current_prompt = self.create_prompt_from_row(
            self.processed_rows.pop())
        self.prompt_label.configure(
            text=f"Current prompt: {self.current_prompt}")

    def _create_chat_completion(self, previous=False) -> None | str:
        if self.current_prompt is None or self.current_prompt == "":
            return

        if len(self.processed_prompts) > 0 and self.processed_prompts[
                len(self.processed_prompts) - 1] == self.current_prompt:
            if not confirm_action(
                    self.master, "Do you want to re-generate current prompt?"):
                return

        # Show the loading modal
        loading_modal = LoadingModal(self.master)

        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{
                    "role": "user",
                    "content": create_prompt(**self.current_row)
                    # self.current_row['title']
                }],
                max_tokens=3096,
            )
        except openai.InvalidRequestError as exc:
            raise exc
        except Exception as exc:
            raise Exception(
                f"Failed to create Completion - {str(exc)}") from exc
        finally:
            # Destroy the loading modal
            loading_modal.destroy()

        try:
            response = markdown_to_html(
                completion.choices[0].message.content.strip())
        except:
            response = completion.choices[0].message.content.strip()

        # Add the row to the processed rows list and save to file
        if self.current_row is not None:
            self.processed_rows.append(self.current_row)
            with open("processed_rows.txt", "a") as f:
                f.write(str(self.current_row) + "\n")

        # Display the output and add this row to the list of processed rows
        self.output_text.insert(
            tk.END, f"Prompt: {self.current_prompt}\nResponse: {response}\n\n")
        self.prompt_label.configure(
            text=f"Current prompt: {self.current_prompt}")
        self.processed_prompts.append(self.current_prompt)

        if USE_LISTBOX is True:
            self.prompt_listbox.delete(0, tk.END)
            self.prompt_listbox.insert(0, *self.processed_prompts)

        # self.current_prompt = None
        # self.current_row = None

    def process_next_row(self):
        # Check if a file has been selected
        if not self.file_path:
            self.output_text.insert(tk.END, "Please select a CSV file.\n")
            return

        # Open the CSV file and read the rows
        with open(self.file_path, "r", encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Generate a unique hash from the 'prompt' and 'site_url' columns
                # hash_value = hashlib.sha256(f"{row['title']}{row['site_url']}".encode()).hexdigest()

                # Check if this row has already been processed
                if row in self.processed_rows:
                    continue

                # Call the OpenAI API to generate a completion for this row
                # Note: you will need to customize this part based on your specific OpenAI API usage
                # prompt = f"{row['prompt']} {row['site_url']}"
                self.current_prompt = self.create_prompt_from_row(row)
                self.current_row = row

                self.prompt_label.configure(
                    text=f"Current prompt: {self.current_prompt}")
                self._create_chat_completion()

                return

        self.output_text.insert(
            tk.END, "Could not fin ad valid row to process.\n")

        # Run the Tkinter main loop
    def run(self):
        # Run the Tkinter main loop
        self.master.mainloop()


if __name__ == "__main__":
    # Create and run the application
    root = CTk()
    root.title("OpenAI CSV Processor")
    root.geometry('1024x860')
    root.resizable(False, False)

    main_frame = CTkFrame(master=root)
    main_frame.pack(fill=tk.BOTH, expand=1)
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_rowconfigure(0, weight=1)

    app = Application(master=main_frame)
    app.run()
