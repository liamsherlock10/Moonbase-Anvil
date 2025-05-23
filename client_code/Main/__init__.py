from ._anvil_designer import MainTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
from .Monitor import Monitor
from .Chatbot import Chatbot
from .Newsletter import Newsletter
from .Investors import Investors
from .PA import PA
from .M_A import M_A
from .WebScraper import WebScraper
from .Searchers import Searchers
from .Hubspot import Hubspot
from .MailAgent import MailAgent
from .OutboundMail import OutboundMail
from .Analysis import Analysis
from .. import State

class Main(MainTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    pant = properties.get("subform", "chatbot")
    if pant == "chatbot":
      self.b_chatbot_click()
    else:
      self.b_monitor_click()
    # Any code you write here will run before the form opens.

  def b_monitor_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.column_panel_2.clear()
    self.column_panel_2.add_component(Monitor(), full_width_row=True)
    self.b_monitor.enabled = False
    self.b_chatbot.enabled = True
    self.b_newsletter.enabled = True
    self.b_investors.enabled = True
    self.b_pa.enabled = True
    self.b_ma.enabled = True
    self.b_scraper.enabled = True
    self.b_searchers.enabled = True
    self.b_hubspot.enabled = True

  def b_chatbot_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.column_panel_2.clear()
    self.column_panel_2.add_component(Chatbot(), full_width_row=True)
    self.b_monitor.enabled = True
    self.b_chatbot.enabled = False
    self.b_newsletter.enabled = True
    self.b_investors.enabled = True
    self.b_pa.enabled = True
    self.b_ma.enabled = True
    self.b_scraper.enabled = True
    self.b_searchers.enabled = True
    self.b_hubspot.enabled = True

  def b_newsletter_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.column_panel_2.clear()
    self.column_panel_2.add_component(Newsletter(), full_width_row=True)
    self.b_monitor.enabled = True
    self.b_chatbot.enabled = True
    self.b_newsletter.enabled = False
    self.b_investors.enabled = True
    self.b_pa.enabled = True
    self.b_ma.enabled = True
    self.b_scraper.enabled = True
    self.b_searchers.enabled = True

  def b_investors_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.column_panel_2.clear()
    self.column_panel_2.add_component(Investors(), full_width_row=True)
    self.b_monitor.enabled = True
    self.b_chatbot.enabled = True
    self.b_newsletter.enabled = True
    self.b_investors.enabled = False
    self.b_pa.enabled = True
    self.b_ma.enabled = True
    self.b_scraper.enabled = True
    self.b_searchers.enabled = True
    self.b_hubspot.enabled = True
    
  def b_pa_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.column_panel_2.clear()
    self.column_panel_2.add_component(PA(), full_width_row=True)
    self.b_monitor.enabled = True
    self.b_chatbot.enabled = True
    self.b_newsletter.enabled = True
    self.b_investors.enabled = True
    self.b_pa.enabled = False
    self.b_ma.enabled = True
    self.b_scraper.enabled = True
    self.b_searchers.enabled = True

  def b_ma_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.column_panel_2.clear()
    self.column_panel_2.add_component(M_A(), full_width_row=True)
    self.b_monitor.enabled = True
    self.b_chatbot.enabled = True
    self.b_newsletter.enabled = True
    self.b_investors.enabled = True
    self.b_pa.enabled = True
    self.b_ma.enabled = False
    self.b_scraper.enabled = True
    self.b_searchers.enabled = True
    self.b_hubspot.enabled = True

  def b_scraper_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.column_panel_2.clear()
    self.column_panel_2.add_component(WebScraper()(), full_width_row=True)
    self.b_monitor.enabled = True
    self.b_chatbot.enabled = True
    self.b_newsletter.enabled = True
    self.b_investors.enabled = True
    self.b_pa.enabled = True
    self.b_ma.enabled = False
    self.b_scraper.enabled = True
    self.b_searchers.enabled = True
    self.b_hubspot.enabled = True

  def b_searchers_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.column_panel_2.clear()
    self.column_panel_2.add_component(Searchers(), full_width_row=True)
    self.b_monitor.enabled = True
    self.b_chatbot.enabled = True
    self.b_newsletter.enabled = True
    self.b_investors.enabled = True
    self.b_pa.enabled = True
    self.b_ma.enabled = True
    self.b_scraper.enabled = True
    self.b_searchers.enabled = False
    self.b_hubspot.enabled = True

  def b_hubspot_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.column_panel_2.clear()
    self.column_panel_2.add_component(Hubspot(), full_width_row=True)
    self.b_monitor.enabled = True
    self.b_chatbot.enabled = True
    self.b_newsletter.enabled = True
    self.b_investors.enabled = True
    self.b_pa.enabled = True
    self.b_ma.enabled = True
    self.b_scraper.enabled = True
    self.b_searchers.enabled = True
    self.b_hubspot.enabled = False

  def OutboundMail_click(self, **event_args):
    """This method is called when the button is clicked"""
    '''
    I need to add the self.b_outboundmail component and do the same thing for 
    mail agent in order to allow for them to be added. 
    
    Note: not rly sure where this part happened. 
    '''
    self.column_panel_2.clear()
    self.column_panel_2.add_component(OutboundMail(), full_width_row=True)
    self.b_monitor.enabled = True
    self.b_chatbot.enabled = True
    self.b_newsletter.enabled = True
    self.b_investors.enabled = True
    self.b_pa.enabled = True
    self.b_ma.enabled = True
    self.b_scraper.enabled = True
    self.b_searchers.enabled = False
    self.b_hubspot.enabled = True

  def MailAgentButton_click(self, **event_args):
    """This method is called when the button is clicked"""

    '''
    Same issue as the Outbound button. need to figure out where the other
    component names came from and how to encorporate them into here
    and add this component as part of the other buttons functions. 
    ''' 
    self.column_panel_2.clear()
    self.column_panel_2.add_component(MailAgent(), full_width_row=True)
    self.b_monitor.enabled = True
    self.b_chatbot.enabled = True
    self.b_newsletter.enabled = True
    self.b_investors.enabled = True
    self.b_pa.enabled = True
    self.b_ma.enabled = True
    self.b_scraper.enabled = True
    self.b_searchers.enabled = True
    self.b_hubspot.enabled = False


  def Analysis_click(self, **event_args):
    """This method is called when the button is clicked"""
    
    #note: should still probably figure out what to do about the stuff at the bottom,
    #adding true/false and actually enabling the new components we have created. 
    
    self.column_panel_2.clear()
    self.column_panel_2.add_component(Analysis(), full_width_row=True)
    self.b_monitor.enabled = True
    self.b_chatbot.enabled = True
    self.b_newsletter.enabled = True
    self.b_investors.enabled = True
    self.b_pa.enabled = True
    self.b_ma.enabled = True
    self.b_scraper.enabled = True
    self.b_searchers.enabled = False
    self.b_hubspot.enabled = True