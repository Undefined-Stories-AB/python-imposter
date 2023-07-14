import tkinter as tk
from customtkinter import CTkToplevel, CTkButton, CTkLabel


class ConfirmationDialog(CTkToplevel):
    result: bool | None
    def __init__(self, master, message):
        super().__init__(master)
        self.master = master
        self.transient(master)
        self.title("Confirmation")
        #self.geometry("+%d+%d" % #(master.winfo_rootx() + 50, master.winfo_rooty() + 50))

        self.result = None

        # Add a label to show the confirmation message
        self.message_label = CTkLabel(self, text=message)
        self.message_label.pack(side=tk.TOP, padx=20, pady=10)

        # Add a "Do it" button
        self.do_it_button = CTkButton(self, text="Do it", command=self.do_it)
        self.do_it_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # Add a "Cancel" button
        self.cancel_button = CTkButton(self,
                                       text="Cancel",
                                       command=self.cancel)
        self.cancel_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # Disable user input to the parent window
        master.grab_set()
        master.wait_visibility()
        #master.set_attributes(disabled=True)

    def do_it(self):
        # Enable user input to the parent window and destroy the dialog
        #self.master.wm_attributes(disabled=False)
        self.master.focus_set()
        self.result = True
        self.destroy()

    def cancel(self):
        # Enable user input to the parent window and destroy the dialog
        #self.master.set_attributes(disabled=False)
        self.master.focus_set()
        self.result = False
        self.destroy()


def confirm_action(parent, message):
    dialog = ConfirmationDialog(parent, message)
    parent.wait_window(dialog)
    return dialog.result