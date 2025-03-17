from ._anvil_designer import MonitorTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
from collections import defaultdict
from datetime import date


class Monitor(MonitorTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.cost, start_date = 253, date(2024, 8, 1)
    #try:
    self.docs = anvil.server.call("list_docs")
    self.lk_filedetail.text, fails, types = self.summarise_files(self.docs)
    self.dd_directory.items = types
    self.lk_filesuploaded.text = f"{len(self.docs) - fails} files uploaded to OpenAI"
    if fails: self.lk_filesuploaded.text += f". {fails} failed, under revision"
    self.lk_filesuploaded.text += ". Click for Detail"      
    chats = anvil.server.call("get_history_all")
    chats_user = [c for c in chats if c["user"] >= 0]
    chats_bot = [c for c in chats if c["user"] < 0]
    self.l_filelist.text = f"{len(chats)} interactions with Luna since its start. Average cost is {self.cost/len(chats):6.2f} €/interaction"
    current_date = date.today()
    month_difference = (current_date - start_date).days / 30
    self.rp_history_user.items = chats_user[-10:]
    self.rp_history_bot.items = chats_bot[-10:]
    self.l_filelist.text += f"\nEstimated run rate: {self.cost/month_difference:.2f} €/month"
    '''
    except Exception as e:
      print(f"{e}")
      alert("Lost connection to LUNA Server. Please try again and if it fails, contact diego.montoliu@delta-ai.com")
      anvil.server.reset_session()
    '''
    
  def fl_upload_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    num_files = anvil.server.call("upload_files", self.fl_upload.files)
    self.l_uploaded.text = f"{num_files} Uploaded"

  def summarise_files(self, docs, type=""):
    summary = defaultdict(list)
    typemap = {".txt": "Text File", "docx": "Word Document", ".pdf": "PDF Document", "json": "Text File", "pptx": "Powerpoint", "failed": "Not in Luna"}

    # Iterate through the list of strings
    self.l_filelist.text = ""
    for id, file in docs.items():
        if len(type) and typemap.get(file["type"], "") != type and file["type"] != type:
          continue
        doc, status, ftype = file["filename"], file["status"], file["type"]
        ftype = typemap.get(ftype, ftype)
        self.l_filelist.text += f"**{doc}** {file['about'][:45]}...\n"
        if status == "failed":
          summary["failed"].append(doc) 
        else:
          summary[ftype].append(doc)
            
    # Print the summary
    txt = "Correct:\n"
    for ftype, docs in summary.items():
      if ftype == "failed": continue  
      txt += f"{ftype}:\t{len(docs)}\t{('|').join(docs)}\n"
    if len(summary['failed']): txt += f"\nFAILS: {summary['failed']}"
    txt += "\nCLICK FOR FULL LIST"
    return txt, len(summary["failed"]), summary.keys()

  def lk_filesuploaded_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.lk_filedetail.visible = not(self.lk_filedetail.visible)
    self.l_filelist.visible = self.lk_filedetail.visible 

  def lk_filedetail_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.l_filelist.visible = not(self.l_filelist.visible)

  def dd_directory_change(self, **event_args):
    """This method is called when an item is selected"""
    if self.dd_directory.selected_value != "All":
      self.lk_filedetail.text, fails, types = self.summarise_files(self.docs, type=self.dd_directory.selected_value)
      self.l_filelist.visible = True
