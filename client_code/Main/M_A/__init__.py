from ._anvil_designer import M_ATemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
from collections import defaultdict
from datetime import date


class M_A(M_ATemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.cost, start_date = 90, date(2024, 8, 1)
    try:
      docs = anvil.server.call("list_docs")
      targets = anvil.server.call("get_targets")
      self.l_targets.text = f"{len(targets)} targets"
      self.rp_targets.items = targets
    except Exception as e:
      print(f"{e}")
      alert(
        "Lost connection to LUNA Server. Please try again and if it fails, contact diego.montoliu@delta-ai.com"
      )
      anvil.server.reset_session()