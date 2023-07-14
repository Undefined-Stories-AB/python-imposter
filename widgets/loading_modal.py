import tkinter as tk
from customtkinter import CTkToplevel, CTkFrame, CTkLabel

class LoadingModal(CTkToplevel):
    master: CTkFrame
    def __init__(self, master: CTkFrame):
        super().__init__()
        self.transient(master)
        self.title("Loading...")
        # Hide the root window drag bar and close button
        #self.overrideredirect(True)
        # Make the root window always on top
        #master.wm_attributes("-topmost", True)
        #self.geometry("+%d+%d" % (master.winfo_rootx()+50, master.winfo_rooty()+50))

        # Add a label to show a message
        self.message_label = CTkLabel(self, text="Please wait...")
        self.message_label.pack(padx=20, pady=10)

        # Disable user input to the parent window
        #.grab_set()
        #master.wait_visibility()
        #master.wm_attributes("-disabled", True)

    def destroy(self):
        # Re-enable user input to the parent window
        #self.master.wm_attributes("-disabled", False)
        self.master.focus_set()
        super().destroy()
