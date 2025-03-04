from ._anvil_designer import MailAgentTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import re
from .. import State 

'''
This code has a lot of AI generated comments, I have been working on it using
AI and haven't decided to rewrite comments yet, so for the purpose of acccurate
documentation, I have decided to maintain the AI generated stuff. 

Note: we are using liam.ipynb for server functions, 
at least that is what was being used in the last test
'''
class MailAgent(MailAgentTemplate):
    def __init__(self, **properties):
      # Set Form properties and Data Bindings.
      self.init_components(**properties)
      # On form load, populate the fields from State
      # (Adjust for how you store multiple recipients in State.mail_to)
      
      # If the State has recipients as a list, this is supposed to handle it
      '''
      I have concerns about this because I don't know if the user is going to
      split up contacts with commas, spaces or anything else. Right now I am 
      instructing the user to split up entries with semicolons, and then changing 
      any list that is coming from state to the same format
      '''
      
      #enabling the recipient and subject textboxes
      self.recipient_textbox.enabled = True
      self.subject_textbox.enabled = True

      
      self.text_area_tester.enabled = True
      self.text_area_tester.text = State.mail_text or ""


      #setting up the Richtext box
      self.message_rich_text.enable_editor = True
      self.message_rich_text.enabled = True
      self.message_rich_text.read_only = False
  
      '''
      if isinstance(State.mail_to, list):
        self.recipient_textbox.text = ";".join(State.mail_to)
      else:
        self.recipient_textbox.text = State.mail_to or "" # In case it's just a string or None
      '''
      self.recipient_textbox.text = State.mail_to or ""
      
      self.subject_textbox.text = State.mail_subject or ""
      
      self.message_rich_text.content = State.mail_text or ""

      




    def send_button_click(self, **event_args):
      """Called when the user clicks the 'Send' button"""

      '''
      This line below is designed to allow for a user to separate recipients
      with commas as well to be more user friendly. commented out for now, but 
      could be a good idea in the future because email adresses don't have comamas. 
      '''
      #recipients_str = self.recipient_textbox.text.replace(",", ";")
      '''
      This is the code for creating a list of recipients, right now we suspect
      that the send_email function is only working with strings so we are waiting to
      impliment this part
      recipients = [
        r.strip() for r in self.recipient_textbox.text.split(";") if r.strip()
      ]
      '''
      recipients = self.recipient_textbox.text
      #recipients = self.reci
      #checking to make sure that recipients box is filled with at least one person
      if not recipients:
        alert("Please enter at least one recipient.")
        return
      
      subject = self.subject_textbox.text
      '''This is what is supposed to be used in the end, using another component
      in order to test out if the email formatting gets fixed by this change'''
      #body = self.message_rich_text.content  # content returns the rich text's HTML/text
      body = self.text_area_tester.text

      print("recipients: " + recipients + "type: " + str(type(recipients)))
      # Call the server function (already defined in your Server Module)
      anvil.server.call('send_email', recipients, subject, body)
      
      # Update State variables
      State.mail_to = recipients
      State.mail_subject = subject
      State.mail_text = body
      
      # Show the Main form (assuming you have a form named "Main" in your app)
      open_form("Main")

    def cancel_button_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form("Main") #Should this go to a different page instead?
    




'''
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
      body = self.message_rich_text.content or ""
      
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
'''

