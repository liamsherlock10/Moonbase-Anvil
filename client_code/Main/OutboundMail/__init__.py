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
    '''
    [
        {"subject": "Welcome to AI Mail", "body": "Your first email!", "timestamp": "2025-03-25 09:00"},
        {"subject": "Your weekly update", "body": "Here are your stats...", "timestamp": "2025-03-26 10:30"},
        # ... add more emails as needed
    ]
    '''
    # Set the repeating panel's items to your email data list.
    self.EmailPanel.items = email_data
    self.outBound = State.sent_folder
    self.EmailPanel.visible = True
    #self.load()

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

  '''
  def load(self):
    email_data = anvil.server.call('get_sent_emails')
    self.EmailPanel.items = email_data
  '''


  '''
  Add this button feature after, easy enough and will make it more 
  professional and funcional. 

  def button_refresh_click(self, **event_args):
        """Refresh button to reload emails"""
        self.EmailPanel.load_emails()
  '''

