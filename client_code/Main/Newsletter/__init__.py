from ._anvil_designer import NewsletterTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
from collections import defaultdict
from datetime import date


class Newsletter(NewsletterTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    themes = anvil.server.call("list_news_themes")
    self.lk_themes.text = f"{len(themes)} themes being developed."
    stories = anvil.server.call("get_news_stories")
    self.l_news_sections.text = f"{len(stories)} stories"
    self.rp_themes.items = themes[-10:]
    '''
    except Exception as e:
      print(f"{e}")
      alert(
        "Lost connection to LUNA Server. Please try again and if it fails, contact diego.montoliu@delta-ai.com"
      )
      anvil.server.reset_session()
    '''