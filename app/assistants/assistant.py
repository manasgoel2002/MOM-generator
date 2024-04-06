from dotenv import load_dotenv
import os
import marvin
from marvin.beta import Application
from marvin.beta.assistants import pprint_messages
from marvin.utilities.logging import get_logger, setup_logging
from typing import Optional
from pydantic import BaseModel, Field
from marvin.utilities.pydantic import parse_as
from app.models import search_request_model, prompt_model
from fastapi.encoders import jsonable_encoder



load_dotenv()

# Constants
MAX_TOKENS = 4000
TEMPERATURE = 0.0
OPENAI_TIMEOUT = 1200

# Marvin settings
marvin.settings.llm_temperature = 1
marvin.settings.llm_max_tokens = MAX_TOKENS
marvin.settings.llm_request_timeout_seconds = OPENAI_TIMEOUT
marvin.settings.log_level = "DEBUG"
marvin.settings.openai.api_key = os.getenv('OPENAI_API_KEY')
# marvin.settings.openai.organization = os.getenv('OPENAI_ORG_ID')

# Get root logger
logger = get_logger("marvin")

setup_logging(level="DEBUG")

# Define the FastAPI application
app = Application(
    # id="asst_OBD6QD0lkjx2Y2kgghgeEReC",
    name="Flight Search Assistant",
    instructions=""" 
Welcome to the Meeting Minutes Assistant! Your role is to efficiently generate meeting minutes from YouTube video transcripts. Follow the guidelines below:

1. Input Transcript Processing:
   - Accept YouTube video transcripts as input.
   - Use natural language processing techniques to extract relevant information from the transcript.

2. Classifying Meeting Elements:
   - Identify and classify the following meeting elements:
       - Members Presenting: Recognize speakers and identify their roles or affiliations within the organization.
       - Important Decisions: Highlight key decisions made during the meeting.
       - Tasks Assigned: Note tasks delegated during the meeting, including who is responsible and the specifics of the task.
       - Proposals Presented: Summarize proposals or ideas presented for consideration.
       - Issues and Challenges: Capture any challenges or issues discussed by departments or team members.
       - Other Points: Note any additional noteworthy information discussed during the meeting.

3. Formatting Meeting Minutes:
   - Organize the meeting minutes in a clear and structured format, including sections for each of the classified meeting elements.
   - Use bullet points or concise paragraphs to present information for easy readability.

4. Accuracy and Clarity:
   - Ensure accuracy in transcribing and summarizing the meeting content.
   - Maintain clarity in language and avoid ambiguity in conveying meeting details.

5. User Interaction:
   - Engage users in a conversational manner to clarify any ambiguous information or seek additional context if needed.
   - Provide opportunities for users to review and edit the generated meeting minutes for accuracy.

6. Guardrails:
   - Protect sensitive information discussed during the meeting by ensuring confidentiality and privacy.
   - Adhere to any organizational policies or guidelines regarding the handling of meeting minutes and confidential information.

Your mission is to facilitate the efficient creation of comprehensive meeting minutes, capturing the essence of discussions and decisions made during the meeting. Ensure the accuracy and clarity of the minutes to support effective communication and follow-up actions.
    """,
    state=search_request_model.MeetingMinutes(),
    model="gpt-3.5-turbo"
)


async def process_prompt(prompt: prompt_model.Prompt):
    try:
        # Get context using the assistant
        result =  app.say(prompt.message)
        response = {"state": jsonable_encoder(app.state.value), "result": result}
        print(response)
        # message_intention = response["state"]["messageIntention"]
        # # print(message_intention)
        # if message_intention == "search":
        #     # Validate and update the search state
        #     response["state"] = await search_validators.validate_search(response['state'])
        
        # if response["state"]["isComplete"] == True :
        #     response["state"]["nextStep"] = "flightSearch"

        # else:
        #     response["state"]["nextStep"] = "userFeedback"
        # # Return the result 
        return response
    
    except Exception as e:
        # Handle exceptions, log them, and return an error response
        logger.error(f"An error occurred: {str(e)}")
        return {"error": f"An error occurred: {str(e)}"}