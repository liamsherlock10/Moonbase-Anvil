from ._anvil_designer import InvestorsTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
from collections import defaultdict
from datetime import date


class Investors(InvestorsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    try:
      lps = anvil.server.call("list_lps")
      self.lk_investors.text = f"{len(lps)} LP's"
      self.rp_lps.items = lps
    except Exception as e:
      print(f"{e}")
      alert(
        "Lost connection to LUNA Server. Please try again and if it fails, contact diego.montoliu@delta-ai.com"
      )
      anvil.server.reset_session()

  def bt_clear_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.rt_reply.content = ""

  def bt_go_async_click(self, **event_args):
    if self.rb_llm_openai4.selected:
      llm = "openai4"
    elif self.rb_o1.selected:
      llm = "openaio1"
      
    db = "openai"
    embed = "openai_small"
    #try:
    self.task = anvil.server.call("chat_async", self.dd_user.selected_value, self.ta_chat.text, llm, db, embed, 
                                                self.dd_length.selected_value, self.file_id)
    self.timer_1.enabled = True  # Enable the timer to start polling   

  def cb_suggest_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.ta_suggest.visible = self.cb_suggest.checked
