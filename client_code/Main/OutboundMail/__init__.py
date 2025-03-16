from ._anvil_designer import OutboundMailTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
from ... import State

class OutboundMail(OutboundMailTemplate):
  def __init__(self, **properties):
    self.outBound = State.sent_folder

  def Temp_func_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    print(self.outBound)
