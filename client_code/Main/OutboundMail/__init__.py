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
    self.emailPanel.visible = True

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
    rows = app_tables.sentemails.search()
    email_data = [{"recipient": row["recipient"],
                   "subject": row['subject'], "message": 
                   row["message"]} 
                  for row in rows]
    self.emailPanel.items = email_data
    

  '''
  Add this button feature after, easy enough and will make it more 
  professional and funcional. 

  def button_refresh_click(self, **event_args):
        """Refresh button to reload emails"""
        self.emailPanel.load_emails()
  '''

  
