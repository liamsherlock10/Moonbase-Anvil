from ._anvil_designer import EmailRowInTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Analysis


class EmailRowIn(EmailRowInTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    #Assuming self.item is a dictionary with keys "recipients", "subject", and "message"
    '''
    self.from_label.text = 
    self.subject_label.text = 
    self.message_label.text = 
    '''
    

  def Reply_click(self, **event_args):
    """This method is called when the button is clicked"""
    #switch page to MailAgent page with updated state being filled by the OpenAI reply
    pass
