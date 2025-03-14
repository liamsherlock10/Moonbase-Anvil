from ._anvil_designer import MailAgentTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import re
from ..State import State

class MailAgent(MailAgentTemplate):
    def __init__(self, **properties):
      # Set Form properties and Data Bindings.
      self.init_components(**properties)
      # On form load, populate the fields from State
      # (Adjust for how you store multiple recipients in State.mail_to)
      
      # If the State has recipients as a list, this is supposed to handle it
      
      #enabling the recipient and subject textboxes
      self.recipient_textbox.enabled = True
      self.subject_textbox.enabled = True

      self.message_textbox.enabled = True
      self.message_textbox.text = State.mail_text or ""
      
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
      self.message_textbox.text = State.mail_text or ""

      
    def send_button_click(self, **event_args):
      """Called when the user clicks the 'Send' button"""

      '''
      This line below is designed to allow for a user to separate recipients
      with commas as well to be more user friendly. commented out for now, but 
      could be a good idea in the future because email adresses don't have comamas. 
      '''
      #recipients_str = self.recipient_textbox.text.replace(",", ";")

      #Creating a list for recipients to put into server function. 
      recipients = [
        r.strip() for r in self.recipient_textbox.text.split(";") if r.strip()
      ]
      print(recipients)
      
      if not recipients:
        alert("Please enter at least one recipient.")
        return
      
      subject = self.subject_textbox.text

      '''
      Converting textbox into an invisible richtextbox for safe html content that
      will not be altered. '''
      self.message_rich_text.content = self.message_textbox.text
      body = self.message_rich_text.content

      # Call the server function (already defined in your Server Module)
      #for i in range(len(recipients)):
        #anvil.server.call('send_email', recipients[i], subject, body)

      #anvil.server.call('send_email', recipients, subject, body)
      
      # Update State variables
      State.mail_to = recipients
      State.mail_subject = subject
      State.mail_text = body
      
      # Show the Main form (assuming you have a form named "Main" in your app)
      open_form("Main")

    def cancel_button_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form("Main") #Should this go to a different page instead?
    
