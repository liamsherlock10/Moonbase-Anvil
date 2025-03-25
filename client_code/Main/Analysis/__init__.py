from ._anvil_designer import AnalysisTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import openai




class Analysis(AnalysisTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Define the prompt you want to ask
    user_prompt = "What is the capital of France?"

    # Make the API call to the ChatCompletion endpoint
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[{"role": "user", "content": user_prompt}]
    )

    # Extract and print the response
    answer = response.choices[0].message['content']
    print("ChatGPT says:", answer)

    # Any code you write here will run before the form opens.
  
  
