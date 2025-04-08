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
    self.subject_label.text = self.item.get("subject", "No Subject")
    self.message_label.text = self.item.get("message", "No Message")