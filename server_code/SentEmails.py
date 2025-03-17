import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.server
import anvil.tables as tables
from anvil.tables import app_tables

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#

outbound_emails = {}

@anvil.server.callable
def add_email(recipients, subject, message):
    """Insert a new email into the Emails Data Table."""
    app_tables.sentemails.add_row(
        recipients=recipients,
        subject=subject,
        message=message
    )
    return "Email added."

@anvil.server.callable
def get_emails():
    """Retrieve all emails from the Emails Data Table."""
    # This returns an iterable of rows, which can be converted into dictionaries in the client if needed.
    return app_tables.sentemails.search()
