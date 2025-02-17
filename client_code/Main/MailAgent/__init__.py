from ._anvil_designer import MailAgentTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import re


class MailAgent(MailAgentTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.dd_length.items = [
      ("1", 1),
      ("2", 2),
      ("5", 5),
      ("10", 10),
      ("30", 30),
      ("50", 50),
    ]
    self.dd_length.selected_value = 30
    self.dd_user.items = [
      ("Anonymous", 0),
      ("Ibrahim", 1),
      ("Nejma", 2),
      ("Aly", 3),
      ("Luca", 4),
      ("Diego", 5),
    ]
    self.cp_settings.visible = False
    self.link_1.icon = "fa:angle-down"
    self.file_id = ""
    self.docs = anvil.server.call("list_docs")
    try:
      cur_user = anvil.server.call("alive")
      self.dd_user.selected_value = cur_user
      self.dd_user_change()
    except Exception as e:
      print(f"{e}")
      alert(
        "Lost connection to LUNA Server. Please try again and if it fails, contact diego.montoliu@delta-ai.com"
      )
      anvil.server.reset_session()

    # Any code you write here will run before the form opens.

  def cb_suggest_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.ta_suggest.visible = self.cb_suggest.checked

  def ob_feedback_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.server.call("feedback", self.id, self.ta_feedback.text)
    self.ta_feedback.visible = False
    self.ob_feedback.visible = False
    self.ta_feedback.text = ""

  def bt_clear_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.rt_reply.content = ""

  def identify_matching_lines(self, text):
    # Regex to match the format #t1#t2#t3#t4
    pattern = re.compile(r"#[^#]+#[^#]+#[^#]+#[^#]+")
    matching_lines = []
    lines = text.split("\n")
    for line in lines:
      if pattern.search(line):
        matching_lines.append(line)
    return matching_lines

  def replace_lines_with_t4(self, text, matching_lines):
    # Splitting the text into lines
    lines = text.split("\n")
    replaced_lines = []
    for line in lines:
      if line in matching_lines:
        # Extract t4 from the matched line
        t4 = line.split("#")[-1]  # Last token
        replaced_lines.append(t4)
      else:
        replaced_lines.append(line)
    return "\n".join(replaced_lines)

  def tail_hist(self, text):
    # Get the last 2000 characters
    last_2000 = text[-2000:]

    matching_lines = self.identify_matching_lines(last_2000)
    last_2000 = self.replace_lines_with_t4(last_2000, matching_lines)

    # Find the first newline character
    newline_index = last_2000.find("\n")

    # If newline is found, slice the string from that point
    if newline_index != -1:
      return last_2000[newline_index + 1 :]
    else:
      return last_2000

  def dd_user_change(self, **event_args):
    """This method is called when an item is selected"""
    hist = anvil.server.call("get_history_user", self.dd_user.selected_value)
    tailh = self.tail_hist(hist).replace("()", "")
    print(tailh)
    th = self.extract_and_remove(tailh)
    self.rt_reply.content = self.remove_markdown(th[1]) + "\n"
    for fl in th[0]:
      self.draw_filelink_name(fl, self.rt_reply, fl)

  def link_1_click(self, **event_args):
    if self.cp_settings.visible:
      self.cp_settings.visible = False
      self.link_1.icon = "fa:angle-down"
    else:
      self.cp_settings.visible = True
      self.link_1.icon = "fa:angle-up"

  def lk_promo_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("Main", subform="monitor")

  def dict_list_to_markdown_table(self, dict_list):
    if not dict_list or len(dict_list) == 0:
      return "Empty list"

    try:
      dict_list = eval(dict_list)
    except:
      return dict_list

    # Get the headers from the keys of the first dictionary
    headers = list(dict_list[0].keys())

    # Create the header row
    markdown = "| " + " | ".join(headers) + " |\n"
    markdown += "| " + " | ".join(["---" for _ in headers]) + " |\n"

    # Add each row
    for item in dict_list:
      row = "| " + " | ".join(str(item.get(header, "")) for header in headers) + " |"
      markdown += row + "\n"

    return markdown

  def draw_filelink_id(self, pid):
    if len(pid):
      down_url = (
        f"https://deep-chief-reality.anvil.app/_/api/download_id/{pid}".replace(
          "_", "\_"
        ).replace(" ", "%20")
      )
      file = self.docs.get(pid, {"filename": "Related File"})
      mu_link = f'\n[{file["filename"]}]({down_url})'
      self.rt_files.content += mu_link

  def draw_filelink_name(self, pfile, prt, pname):
    if len(pname) and "source" not in pfile:
      pfile = re.sub(r"【.+†", "", pfile).replace("】", "")
      pname = re.sub(r"【.+†", "", pname).replace("】", "")
      down_url = (
        f"https://deep-chief-reality.anvil.app/_/api/download_name/{pfile}".replace(
          "_", "\_"
        ).replace(" ", "%20")
      )
      if "." in pname:
        pname = pfile
      mu_link = f'\n[{pname.replace("%20", " ")}]({down_url})'
      prt.content += mu_link

  def fl_chat_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    self.file_id = anvil.server.call("upload_file_ass", self.fl_chat.files)
    self.rt_reply.content += f"\nFile {self.fl_chat.files[0].name} Uploaded\n"

  def extract_and_remove(self, text):
    pattern = r"\[[^\]]+\]\(sandbox:(.+/[^)]+)\)"
    file_names = []

    # Use re.finditer to find all matches in the text
    matches = re.finditer(pattern, text)

    for match in matches:
      f_name = match.group(1)
      if "/" in f_name:
        f_name = f_name.split("/")[-1]
      print("Found sandbox", f_name)
      file_names.append(f_name)

    # Replace all matches with "(see below)"
    text = re.sub(pattern, "(see below)", text).strip()

    pattern = r"【([^】]+)】"
    match = re.search(pattern, text)

    if match:
      file_names.append(match.group(1))
      text = re.sub(pattern, "", text).strip()

    pattern = r'"([^"]+\.[a-zA-Z]{3,4})"'

    # Use re.finditer to find all matches in the text
    matches = re.finditer(pattern, text)

    for match in matches:
      f_name = match.group(1)
      if "/" in f_name:
        f_name = f_name.split("/")[-1]
      file_names.append(f_name)

    print(file_names)
    return file_names, text

  def remove_markdown(self, text):
    # Replace headers (e.g., # Header) with just the header text
    text = re.sub(r"(?<!\\)#{1,6}\s*(.*)", r"\1", text)

    # Replace bold and italic (e.g., **bold**, *italic*) with plain text
    text = re.sub(r"(?<!\\)[*_]{1,3}(.+?)[*_]{1,3}", r"\1", text)

    # Replace inline code (e.g., `code`) with just the code
    text = re.sub(r"(?<!\\)`(.+?)`", r"\1", text)

    # Replace strikethrough (e.g., ~~text~~) with plain text
    text = re.sub(r"(?<!\\)~{2}(.+?)~{2}", r"\1", text)

    # Replace unordered list markers (-, +, *) with a dash and space
    text = re.sub(r"(?:^|\n)[-+*]\s+", r"- ", text)

    # Replace ordered list markers (e.g., 1. item) with just the item
    text = re.sub(r"(?:^|\n)\d+\.\s+", "", text)

    # Replace blockquotes (e.g., > quote) with just the quoted text
    text = re.sub(r"(?:^|\n)>+\s+", "", text)

    # Remove escape characters for Markdown symbols (e.g., \*)
    text = re.sub(r"\\([*_~`>])", r"\1", text)

    return text

  def bt_go_async_click(self, **event_args):
    if self.rb_llm_openai4.selected:
      llm = "openai4"
    elif self.rb_o1.selected:
      llm = "openaio1"

    db = "openai"
    embed = "openai_small"
    # try:
    self.task = anvil.server.call(
      "chat_async",
      self.dd_user.selected_value,
      self.ta_chat.text,
      llm,
      db,
      embed,
      self.dd_length.selected_value,
      self.file_id,
    )
    self.timer_1.enabled = True  # Enable the timer to start polling

  def timer_1_tick(self, **event_args):
    """Poll the server for task progress."""
    if hasattr(self, "task") and self.task:
      self.l_status.visible = True
      progress = self.task.get_state("progress")  # Get progress updates
      if progress:
        self.l_status.text = progress.get(
          "progress", "Waiting..."
        )  # Update UI with progress
      else:
        self.l_status.text = "Waiting for updates..."

      if self.task.is_completed():  # Stop polling when done
        self.timer_1.enabled = False

        # Get final result of the task
        self.l_status.visible = False
        retval = self.task.get_return_value()
        self.l_status.text = retval
        reply, _, self.id = retval
        print("reply", reply)

        history = (
          f"\n=======================\n\t{self.ta_chat.text}\n=======================\n"
        )

        if "```json" in reply:
          jsplit = reply.split("```")
          reply = jsplit[0]
          print(jsplit[1].replace("json", ""))

          try:
            xtra = eval(jsplit[1].replace("json", ""))
          except Exception as e:
            xtra = {"confidence": "high"}
            print("Wrong JSON")

          if isinstance(xtra, dict) and (
            "file_ids" in xtra.keys() or "file_id" in xtra.keys()
          ):
            self.rt_files.content = "**RELATED FILES**\n"
            for f in xtra.get("file_ids", []) + [xtra.get("file_id", "")]:
              self.draw_filelink_id(f)

          if str(xtra.get("confidence", "")).upper() in ["HIGH", "EASY", "1"]:
            self.l_confidence.text = "CONFIDENT"
            self.l_confidence.background = "green"
          elif (
            str(xtra.get("confidence", "")).upper() == "MEDIUM"
            or str(xtra.get("confidence", "_"))[0].isdigit()
          ):
            self.l_confidence.text = "DOUBTS"
            self.l_confidence.background = "amber"
          elif xtra.get("confidence"):
            self.rt_reply.content += self.remove_markdown(
              history
              + "SPECULATIVE ANSWER. TRY INCREASING CONTEXT LENGTH OR PROVIDING MORE BACKGROUND\n"
            )
            self.l_confidence.text = "CLUELESS"
            self.l_confidence.background = "red"
            return
        """
              except Exception as e:
                alert(f"Please try again or reload: {e}")
                anvil.server.reset_session()
                print(f"{e}")
                return
              """

        if "#Special#" in reply:
          print("REPLY:====\n", reply, "\n====REPLY")
          rep_parts = reply.split("#")
          f_names, rep_text = "", ""
          if "#Scorefile#" in reply:
            self.rt_reply.content += self.remove_markdown(
              history + rep_parts[4] + "\nScorecard ready for downloading \n"
            )
            self.draw_filelink_name(rep_parts[3], self.rt_reply, "Scorecard")
          elif "#AddAdvisor#" in reply:
            self.rt_reply.content += self.remove_markdown(
              history + rep_parts[4] + "\nYou can download the new version."
            )
            anvil.server.call("refresh_advisors")
            self.draw_filelink_name("Advisors.xlsx", self.rt_reply, "Advisors")
          elif "#Advisorfile#" in reply:
            adv_table = self.dict_list_to_markdown_table(rep_parts[4])
            self.rt_reply.content += self.remove_markdown(history + "\n" + adv_table)
            anvil.server.call("refresh_advisors")
            self.draw_filelink_name("Advisors.xlsx", self.rt_reply, "Advisors")
          elif "#Mitigants#" in reply:
            mit_table = self.dict_list_to_markdown_table(rep_parts[4])
            self.rt_reply.content += self.remove_markdown(
              f"{history}\nMissing Mitigants: \n{mit_table}\nPlease provide mitigants on the related files, if available, and upload again"
            )
          elif "#Graph#" in reply:
            self.rt_reply.content += self.remove_markdown(
              history + "\nGraph ready for downloading \n"
            )
            self.draw_filelink_name(rep_parts[3], self.rt_reply, "Graph")
          elif "#IM#" in reply:
            self.rt_reply.content += self.remove_markdown(
              history + "\nMoonbase IM ready for downloading \n"
            )
            self.draw_filelink_name(rep_parts[3], self.rt_reply, "Moonbase IM")
          elif "#Searchers#" in reply:
            mit_table = rep_parts[4]
            self.rt_reply.content += self.remove_markdown(
              f"{history}\nSearchers without scorecard: \n{mit_table}\nPlease indicate which scorecard you want to generate"
            )
          elif "#Projects#" in reply:
            mit_table = rep_parts[4]
            self.rt_reply.content += self.remove_markdown(
              f"{history}\nProjects without DD scorecard: \n{mit_table}\nPlease indicate which scorecard you want to generate"
            )
          elif "#Updated#" in reply:
            f_names, rep_text = self.extract_and_remove(
              re.sub(r"\[([^\]]+)\]\([^\)]+\)", "", rep_parts[4])
            )
            self.draw_filelink_name(rep_parts[3], self.rt_reply, "Updated File")
          elif "#Mail#" in reply:
            self.rt_reply.content += self.remove_markdown(history + f"\n{rep_parts[4]}")
          else:
            self.rt_reply.content += self.remove_markdown(
              history + f"\nSpecial task being generated ({reply})"
            )
        else:
          f_names, rep_text = self.extract_and_remove("\n" + reply)

        self.rt_reply.content += self.remove_markdown(history + "\n" + rep_text + "\n")
        print("rep_text", rep_text)

        pattern = r'"([^"]+\.[a-zA-Z]{3,4})"'
        file_names = []

        # Use re.finditer to find all matches in the text
        matches = re.finditer(pattern, rep_text)

        for match in matches:
          f_name = match.group(1)
          if "/" in f_name:
            f_name = f_name.split("/")[-1]
          print("Found File", f_name)
          file_names.append(f_name)

        # Replace all matches with "(see below)"
        rep_text = re.sub(pattern, "(see below)", rep_text).strip()

        if f_names and len(f_names):
          for f_name in f_names:
            self.draw_filelink_name(f_name, self.rt_files, f_name)

        self.ta_feedback.visible = True
        self.ob_feedback.visible = True
        self.task = None
        self.timer_1.enabled = False
        print("===FINAL REPLY===\n", self.rt_reply.content, "\n======")
