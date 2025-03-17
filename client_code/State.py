import anvil.server
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
# This is a module.
# You can define variables and functions here, and use them from any form. For example, in a top-level form:
#
#    from ..Main import Module1
#
#    Module1.say_hello()
#
mail_to = "liamsherlock55@gmail.com" #"liamsherlock.tester@gmail.com"
mail_subject = "Meeting time"
mail_text = "Hello"

sent_folder = {}
