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

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    current_sent = anvil.server.call('get_emails')
    print(current_sent)

  
