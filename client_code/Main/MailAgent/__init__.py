from ._anvil_designer import MailAgentTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import re

class MailAgent(MailAgentTemplate):
    def __init__(self, **properties):
      # Set Form properties and Data Bindings.
      self.init_components(**properties)
      self.dd_length.items = [
        ("1", 1),
        ("2", 2),
        ("5", 5),
        ("10", 10),
        ("30", 30),
        ("50", 50),
      ]
      self.dd_length.selected_value = 30
      self.dd_user.items = [
        ("Anonymous", 0),
        ("Ibrahim", 1),
        ("Nejma", 2),
        ("Aly", 3),
        ("Luca", 4),
        ("Diego", 5),
      ]
      self.cp_settings.visible = False
      self.link_1.icon = "fa:angle-down"
      self.file_id = ""
      self.docs = anvil.server.call("list_docs")
      try:
        cur_user = anvil.server.call("alive")
        self.dd_user.selected_value = cur_user
        self.dd_user_change()
      except Exception as e:
        print(f"{e}")
        alert(
          "Lost connection to LUNA Server. Please try again and if it fails, contact diego.montoliu@delta-ai.com"
        )
        anvil.server.reset_session()
    
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
            #anvil.server.call("use_model", chosen_model)
            print("use model" + chosen_model)
        else:
            alert("Please select a model first.")




  #Radio button for using 4o
    def radio_4o_change(self, **event_args):
      if self.radio_4o.selected:
          #anvil.server.call("use_model", "4o")
          print("use model 4o")

  #radio button for using o1
    def radio_o1_change(self, **event_args):
      if self.radio_o1.selected:
          print("use model o1")
          #anvil.server.call("use_model", "o1")

    def generate_button_click(self, **event_args):
      """
      Called when the "Generate" button is clicked.
      This might call a server function to generate an email draft
      based on the selected model and user-entered data.
      """
      # Figure out which model is selected
      if self.radio_gpt_4o.selected:
          model_choice = "GPT_4o"
      elif self.radio_gpt_o1.selected:
          model_choice = "GPT_o1"
      else:
          model_choice = None
      
      # Grab the user's subject and message from the text boxes
      recipient = self.recipient_textbox.text or ""
      subject = self.subject_textbox.text or ""
      body = self.message_textbox.text or ""
      
      # For now, let's just demonstrate the placeholders
      if model_choice is None:
          anvil.alert("Please select a model first.")
          return
      
      if not subject and not body:
          anvil.alert("Provide at least a subject or body to help generate content!")
          return

      # --- Placeholder for your real server function ---
      # Suppose you have a server function called 'generate_email_draft'
      # In the future, you'd do:  draft = anvil.server.call("generate_email_draft", model_choice, subject, body)
      # For now, we'll do a placeholder:
      draft = self._placeholder_generate_email(model_choice, subject, body)
      
      # Optionally, populate the text_box_1 with the generated draft
      self.text_box_1.text = draft


