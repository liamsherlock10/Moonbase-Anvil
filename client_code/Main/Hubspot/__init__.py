from ._anvil_designer import HubspotTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
from collections import defaultdict
from datetime import date


class Hubspot(HubspotTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.dd_sources.items = [("HubSpot - Companies", 0), ("HubSpot - Files", 1), ("HubSpot - Contacts", 2),
                            ("HubSpot - Calendars", 3), ("HubSpot - Pipeline Stages", 4), ("HubSpot - Deals", 5),
                            ("DecileHub - People", 6), ("DecileHub - Companies", 7)]
    self.dd_sources.selected_value = 0
    self.dd_sources_change()
    '''
    except Exception as e:
      print(f"{e}")
      alert(
        "Lost connection to LUNA Server. Please try again and if it fails, contact diego.montoliu@delta-ai.com"
      )
      anvil.server.reset_session()
    '''

  def dd_sources_change(self, **event_args):
    """This method is called when an item is selected"""
    if self.dd_sources.selected_value == 0:
      things = anvil.server.call("get_hs_companies")
      self.lk_hubspot.text = f"{len(things)} Companies in Hubspot"
      self.rp_hs_items.items = things
    elif self.dd_sources.selected_value == 1:
      things = anvil.server.call("get_hs_files")
      self.lk_hubspot.text = f"{len(things)} Files in Hubspot"
      self.rp_hs_items.items = things
    elif self.dd_sources.selected_value == 2:
      things = anvil.server.call("get_hs_contacts")
      self.lk_hubspot.text = f"{len(things)} Contacts in Hubspot"
      self.rp_hs_items.items = things
    elif self.dd_sources.selected_value == 3:
      things = anvil.server.call("get_hs_meeting_links")
      self.lk_hubspot.text = f"{len(things)} Calendars in Hubspot"
      self.rp_hs_items.items = things
    elif self.dd_sources.selected_value == 4:
      things = anvil.server.call("get_hs_pipeline_stages")
      self.lk_hubspot.text = f"{len(things)} Pipeline Stages in Hubspot"
      self.rp_hs_items.items = things
    elif self.dd_sources.selected_value == 5:
      things = anvil.server.call("get_hs_companies")
      self.lk_hubspot.text = f"{len(things)} Deals in Hubspot"
      self.rp_hs_items.items = things
    elif self.dd_sources.selected_value == 6:
      things = anvil.server.call("get_dh_people")
      self.lk_hubspot.text = f"{len(things)} People in DecileHub"
      self.rp_hs_items.items = things
    elif self.dd_sources.selected_value == 7:
      things = anvil.server.call("get_dh_orgs")
      self.lk_hubspot.text = f"{len(things)} Companies in DecileHub"
      self.rp_hs_items.items = things
