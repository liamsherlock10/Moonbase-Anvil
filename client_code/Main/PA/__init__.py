from ._anvil_designer import PATemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
from collections import defaultdict
from datetime import date


class PA(PATemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    try:
      pa_tasks = anvil.server.call("list_pa_tasks")
      self.lk_filesuploaded.text = f"{len(pa_tasks)} tasks in progress"
      chats = anvil.server.call("get_pa_all")
      self.rp_history.items = chats[-10:]
    except Exception as e:
      print(f"{e}")
      alert(
        "Lost connection to LUNA Server. Please try again and if it fails, contact diego.montoliu@delta-ai.com"
      )
      anvil.server.reset_session()

