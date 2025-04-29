from ._anvil_designer import EmailRowInTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Analysis
from ... import State


class EmailRowIn(EmailRowInTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Access the email information from the first element of the 2D list
    email = self.item[0]
    self.from_label.text = email.get("from", "Unknown")
    self.subject_label.text = email.get("subject", "No Subject")
    self.message_label.text = email.get("text", "")

    self.column_panel_1.role = "email-row"
    self.message_container.visible = False

    # Optionally, you could display analysis information too:
    #self.analysis_label.text = str(self.item[1])


  def Reply_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    # Retrieve the email details from the first element of the list
    response = self.item[1]
    print(response)
    State.mail_to = self.item[0].get("from")
    State.mail_subject = self.item[0].get("subject")
    State.mail_text = response[2:]
    # Switch to a reply form, passing the email data if needed
    open_form("Main.MailAgent")

  def forward_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    State.mail_to = ""
    State.mail_subject = "Forward, " + self.item[0].get("subject")
    State.mail_text = self.item[0].get("text", "")

    open_form("Main.MailAgent")

  def show_message_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.message_container.visible = not self.message_container.visible
    
    
