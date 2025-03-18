from ._anvil_designer import EmailPanelTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files

from .email_row import EmailRow


class EmailPanel(EmailPanelTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    #email row has to be defined with other thing still
    self.EmailPanel.item_template = EmailRow

  def load(self):
    #getting rows from app table 
    rows = app_tables.sentemails.search()
    email_data = [{"recipient": row["recipient"], 
                   "subject": row["subject"], 
                   "message": row["message"]} 
                   for row in rows]
    #set items for the repeating panel, this component is the repeating panel
    #i don't understand if this component is actually supposed to be the repeating panel or not
    self.EmailPanel.items = email_data