from ._anvil_designer import OutboundMailTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
from ... import State

class OutboundMail(OutboundMailTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.EmailPanel.role = "title"
      # Example list of email data. Replace with your actual data.
    email_data = anvil.server.call('get_sent_emails')
    # Set the repeating panel's items to your email data list.
    self.EmailPanel.items = email_data
    self.outBound = State.sent_folder
    self.EmailPanel.visible = True