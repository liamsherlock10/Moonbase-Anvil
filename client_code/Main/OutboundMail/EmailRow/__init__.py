from ._anvil_designer import EmailRowTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class EmailRow(EmailRowTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)

        # Set the labels based on passed properties
        self.label_recipient.text = properties.get("recipient", "Unknown")
        self.label_subject.text = properties.get("subject", "No Subject")
        self.label_message.text = properties.get("message", "No Message")
