from ._anvil_designer import SearchersTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
from collections import defaultdict
from datetime import date


class Searchers(SearchersTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    try:
      searchers, searchers_sc = anvil.server.call("get_searchers")
      self.lk_searchers.text = f"{len(searchers)} Searchers"
      self.rp_searchers.items = anvil.server.call("get_searcher_details")
    except Exception as e:
      print(f"{e}")
      alert(
        "Lost connection to LUNA Server. Please try again and if it fails, contact diego.montoliu@delta-ai.com"
      )
      anvil.server.reset_session()

