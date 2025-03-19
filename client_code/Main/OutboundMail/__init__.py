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
    self.outBound = State.sent_folder
    self.EmailPanel.visible = True

    self.load()

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    current_sent = anvil.server.call('get_emails')
    print(current_sent)
    recipients_list = [row["recipients"] for row in current_sent]
    subjects_list = [row["subject"] for row in current_sent]
    messages_list = [row["message"] for row in current_sent]

    print("Recipients:", recipients_list)
    print("Subjects:", subjects_list)
    print("Messages:", messages_list)

  
  def load(self):
    email_data = anvil.server.call('get_sent_emails')
    self.EmailPanel.items = email_data
    

  '''
  Add this button feature after, easy enough and will make it more 
  professional and funcional. 

  def button_refresh_click(self, **event_args):
        """Refresh button to reload emails"""
        self.EmailPanel.load_emails()
  '''

  
