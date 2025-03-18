from ._anvil_designer import EmailPanelTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files


class EmailPanel(EmailPanelTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    
    # Any code you write here will run before the form opens.
