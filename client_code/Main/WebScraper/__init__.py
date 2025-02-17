from ._anvil_designer import WebScraperTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
from collections import defaultdict
from datetime import date


class WebScraper(WebScraperTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.cost, start_date = 90, date(2024, 8, 1)
    try:
      docs = anvil.server.call("list_docs")
      self.lk_filedetail.text, fails = self.summarise_files(docs)
      self.lk_filesuploaded.text = f"{len(docs) - fails} files uploaded to OpenAI"
      if fails:
        self.lk_filesuploaded.text += f". {fails} failed, under revision"
      self.lk_filesuploaded.text += ". Click for Detail"
      chats = anvil.server.call("get_history_all")
      self.l_filelist.text = f"{len(chats)} interactions with Luna since its start. Average cost is {self.cost/len(chats):6.2f} €/interaction"
      current_date = date.today()
      month_difference = (current_date - start_date).days / 30
      self.rp_history.items = chats[-10:]
      self.l_filelist.text += (
        f"\nEstimated run rate: {self.cost/month_difference:.2f} €/month"
      )
    except Exception as e:
      print(f"{e}")
      alert(
        "Lost connection to LUNA Server. Please try again and if it fails, contact diego.montoliu@delta-ai.com"
      )
      anvil.server.reset_session()

  def fl_upload_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    num_files = anvil.server.call("upload_files", self.fl_upload.files)
    self.l_uploaded.text = f"{num_files} Uploaded"

  def summarise_files(self, docs):
    summary = defaultdict(list)

    # Iterate through the list of strings
    self.l_filelist.text = ""
    for id, file in docs.items():
      doc, status, ftype = file["filename"], file["status"], file["type"]
      self.l_filelist.text += f"\n{doc}|{ftype}|{file['about'][:40]}"
      if status == "failed":
        summary["failed"].append(doc)
      else:
        summary[ftype].append(doc)

    # Print the summary
    txt = "Correct:\n"
    for ftype, docs in summary.items():
      if ftype == "failed":
        continue
      txt += f"{ftype}:\t{len(docs)}\n"
    if len(summary["failed"]):
      txt += f"\nFAILS: {summary['failed']}"
    txt += "\nCLICK FOR FULL LIST"
    return txt, len(summary["failed"])

  def lk_themes_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.lk_filedetail.visible = not (self.lk_filedetail.visible)
    self.l_filelist.visible = self.lk_filedetail.visible and self.l_filelist.visible

  def lk_filedetail_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.l_filelist.visible = not (self.l_filelist.visible)
