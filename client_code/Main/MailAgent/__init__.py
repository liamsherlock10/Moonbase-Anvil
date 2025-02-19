from ._anvil_designer import MailAgentTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import re

class Form1(): #Form1Template parameter for the class?
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
    
    def submit_button_click(self, **event_args):
        # Check which radio button is selected:
        if self.radio_4o.selected:
            chosen_model = "4o"
        elif self.radio_o1.selected:
            chosen_model = "o1"
        else:
            chosen_model = None
        
        # Do something with the chosen model, e.g. call a server function
        if chosen_model:
            anvil.server.call("use_model", chosen_model)
        else:
            alert("Please select a model first.")

    def radio_4o_change(self, **event_args):
      if self.radio_4o.selected:
          anvil.server.call("use_model", "4o")

    def radio_o1_change(self, **event_args):
      if self.radio_o1.selected:
          anvil.server.call("use_model", "o1")

  # Server Module code
    def use_model(self, model_name):
        # Pick which model to call, e.g. "4o" or "o1"
        if model_name == "4o":
            # code to use your "4o" model
            return do_something_with_4o()
        else:
            # code to use your "o1" model
            return do_something_with_o1()


