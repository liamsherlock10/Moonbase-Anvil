from ._anvil_designer import EmailRowTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class EmailRow(EmailRowTemplate):
  def __init__(self, **properties):
    # Set up the form components
    self.init_components(**properties)
    
    # Assuming self.item is a dictionary with keys "recipients", "subject", and "message"
    self.recipients_label.text = self.item.get("recipients", "No Recipients")
    #gets rid of the double brackets because I use a 2D list to process
    n = len(self.recipients_label.text[0])
    self.recipients_label.text = self.recipients_label.text[0][0:n]
    self.subject_label.text = self.item.get("subject", "No Subject")
    self.message_label.text = self.item.get("message", "No Message")
    self.message_container.visible = False

  def show_message_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.message_container.visible = not self.message_container.visible
