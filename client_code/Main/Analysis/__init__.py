from ._anvil_designer import AnalysisTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


'''
To do this week (today is april 3):
 -make everything more astetically pleasing, esspecially the repeating panel
 -create a summary, figure out system for that, for recieving emails
'''
class Analysis(AnalysisTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Define the prompt you want to ask


    '''ASK ABOUT DURING MEETING!!!'''
    #temporary test variable with email/temp_email situation
    #Let's figure out the most efficient way to break up API calls so that 
    # we don't have to do this, or figure out if there should be a maximum that we summarize. 
    test = False
    '''
    Develop a method for OpenAI to digest this in Chunks, get small one line 
    summaries and write a paragraph summarizing all recieved emails. 

    To start: go from 5 to 20 messages, write a summary of top 3 most important 
    emails, then paragraph summarizing the rest. 
    '''
    emails = anvil.server.call('check_email', platest=test, pmailbox=False, phubspot=True)
    if not test:
      temp_emails = []
      for j in range(5):
        temp_emails.append(emails[j])
    else:
      temp_emails = emails
    '''
    try making a list of summaries and creating a new server call for digesting that list
    '''
    self.Summary_textbox.text = ""
    self.Summary_textbox.text += anvil.server.call("mail_summary", temp_emails)
    response_required = []
    no_response = []
    for i in range(len(temp_emails)):
      analysis = anvil.server.call('mail_ingestion', temp_emails[i].get("text"))
      if analysis[0] == "1":
        response_required.append([temp_emails[i], analysis])
      else:
        print("this didn't need a response, " + str(i))
        no_response.append([temp_emails[i], "no response required"])

    new_emails = response_required + no_response

    self.AnalysisPanel.items = new_emails

    
    '''
    # Make the API call to the ChatCompletion endpoint
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[{"role": "user", "content": user_prompt}]
    )
    
    # Extract and print the response
    answer = response.choices[0].message['content']
    print("ChatGPT says:", answer)
    '''
    # Any code you write here will run before the form opens.

    '''
    What to impliment: 

    -We want a list of emails that should be responded to in the same repeating panel
    format as the outBound mail. We then want a button that switches to the mailAgent page
    when it is clicked and inputs the suggested response.

    Below, it will also have the important emails that dont need to be responded to, 
    and the non important emails, maybe suggested responses for these too. (eventually,
    this is not the priority)

    Challenges: 
    -We have to try to keep server functions in Anvil as lean as possible, so we will
    try to transfer some over to Jupyter labs and use data from there as opposed to 
    the SentEmails server code that we have in Anvil currently.
    -We also need to use the GetEmails (or something like that) function from Jupyter
    Labs to load all of the recieved emails.
    -We also need to impliment a functional openAI import in either Anvil or Jupyter labs
    that can be used to gather suggested responses and summaries for emails. Before that,
    We will also need to use these imports to classify these emails, and categorize them in
    server data so that we can display them in different places in the repeating panel. 
    -Note: There could be issues with running directly on Server.ipynb instead of 
    ServerLiam.ipynb, in which case we will have to run it on ServerLiam still and 
    delegate server functions to the Server file, which I am not exactly sure how to do. 

    Plan: 
    -First: Figure out how to use the GetEmail function (in Server.ipynb) in order to
    actually retrieve emails that are sent. 
      issues: 
        -not sure what the associated email address is or if that will be important
          -(might just be the luna one and hardcoded in the server function)
        -More Important: Not sure how we're going to access and use data in a valuable
        way. 
    -Second: Once we have the data, we will throw it in an openAI script that categorizes
    each email by: important- respond, important- dont respond, nonimportant
    -Third: We create a repeating panel that starts with important-respond and suggested
    responses, then follows with the rest. 
    -Fourth: We create a reply button that moves from the email to the MailAgent with the
    suggested response already loaded into it, so that the user can look at it, choose 
    to edit it, and then send a message. 
    '''

  def Cancel_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("Main")

  def Analyse_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

    

    