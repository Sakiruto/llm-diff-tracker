import uuid
import os
import json
from loguru import logger
from openai import OpenAI
from tqdm import tqdm
import time
from typing import List,Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_community.document_loaders import Docx2txtLoader
from prompts.prompt import prompt_intention,prd_to_iisues
from prd_to_issues.user_intention import UserIntentionJson
from prd_to_issues.base import EpicsToBeChanged,Epic,Answer

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Chatbot():
    def __init__(self,prompt:str,model="gpt-4o"):
        self.model = model
        self.history = []
        self.prompt = prompt
        self.add_message("system",prompt)

    def add_message(self,role: str,user_input: str):
        self.history += [
            {
                "role": role,
                "content":[
                    {
                    "type": "text",
                    "text": user_input
                    }
                ]
            }
        ]

    def get_openai_response(self,user_input:str):
        if user_input is not None and user_input != "":
            self.add_message("user",user_input)
        
        structured_response = client.beta.chat.completions.parse(
            model=self.model,
            messages = self.history,
            response_format = Answer
        )
        return structured_response
        
    def show_response(self, res, output_file="openai_response.md"):
        # Writes the OpenAI response to a structured Markdown file.
        try:
            epics = res.choices[0].message.parsed.epics
            md_content = "# Prd Issues Breakdown\n\n"

            for epic in epics:
                epic_title = getattr(epic, "epic", "Untitled Epic")
                md_content += f"## Epic: {epic_title}\n\n"

                user_stories = getattr(epic, "user_stories", [])
                for story in user_stories:
                    story_overview = getattr(story, "overview", "No overview provided")
                    story_request = getattr(story, "request", "No request provided")
                    story_criteria = getattr(story, "acceptance_criteria", "Not specified")
                    story_priority = getattr(story, "priority", "Normal")
                    story_labels = getattr(story, "labels", "None")
                    
                    md_content += f"### User Story: {story_overview}\n"
                    md_content += f"**Request:** {story_request}\n\n"
                    md_content += f"**Acceptance Criteria:** {story_criteria}\n\n"
                    md_content += f"**Priority:** {story_priority}\n\n"
                    md_content += f"**Labels:** {story_labels}\n\n"

                    md_content += "#### Tasks:\n"
                    tasks = getattr(story, "tasks", [])
                    for task in tasks:
                        task_title = getattr(task, "task", "No title")
                        task_description = getattr(task, "description", "No description")
                        task_priority = getattr(task, "priority", "Normal")
                        task_labels = getattr(task, "labels", "None")
                        md_content += f"- **Task:** {task_title}\n"
                        md_content += f"  - **Description:** {task_description}\n"
                        md_content += f"  - **Priority:** {task_priority}\n"
                        md_content += f"  - **Labels:** {task_labels}\n"
                md_content += "---\n\n"

            # Write the markdown content to a file
            with open(output_file, "w", encoding="utf-8") as md_file:
                md_file.write(md_content)

            logger.info(f"Response written to {output_file}")

        except AttributeError as e:
            logger.error(f"Unexpected structure in OpenAI response: {e}")
        except Exception as e:
            logger.error(f"An error occurred while processing the response: {e}")


loader = Docx2txtLoader("data/rideshare_platform_plan.docx")
data = loader.load()
prd_text = f"""
## Product Requirements Document
```PRD
{data[0].page_content}
"""
# Initial
bot = Chatbot(prd_to_iisues,"gpt-4o")
res = bot.get_openai_response(prd_text)

bot.show_response(res, "responses/openai_response_1.md")




# giving a gap between ouputs 
time.sleep(5)
print("""

      

      
# This is the output after feedback 
      

      
# """)
# giving feedback and generating output 


epics_dict = [epic.model_dump() for epic in res.choices[0].message.parsed.epics]
epics_json_str = json.dumps(epics_dict, indent=2)

bot.add_message("system", epics_json_str)

consistency = """
Ensure strict adherence to the original Jira issue structure:
- **User Stories must retain clear structure** (Title, Description, Request, Acceptance Criteria, Priority, Labels).
- **All Tasks within a User Story must align in description, priority, and labels.**
- **Do not alter the priority or labels unless user feedback explicitly requests it.**
- **Expand epics where necessary but avoid unnecessary modifications.**
- **Preserve consistent wording, formatting, and structure across all elements.**
- **Ensure no missing sections or formatting discrepancies.**
"""
# Userfeed back input 

parser = UserIntentionJson()

user_feedback :str =  input("Enter the feedback")

user_feedback_json = parser.get_structured_intention_response(prompt_intention, user_feedback, EpicsToBeChanged)

final_feedback = f"""
{consistency}

{user_feedback_json}
"""


res1 = bot.get_openai_response(final_feedback)
bot.show_response(res1, "responses/openai_response_2.md")

