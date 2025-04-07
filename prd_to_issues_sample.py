import uuid
from loguru import logger
from openai import OpenAI
import json
from tqdm import tqdm
from time import time
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_community.document_loaders import Docx2txtLoader
from composio_openai import ComposioToolSet, App

load_dotenv()
openai_client = OpenAI()
token = ""
with open("jira_access_token.txt", "r") as f:
    token = f.read().strip()
logger.debug(f"Token: {token}")
toolset = ComposioToolSet()
toolset.add_auth(
    app=App.JIRA,
    parameters=[
        dict(
            name="Authorization",
            in_="header",
            value=f"Bearer {token}",
        )
    ],
)
tools = toolset.get_tools(actions=['JIRA_CREATE_ISSUE'])
print(tools)

prompt = """
"Given the following Product Requirements Document (PRD), extract key features and convert them into structured Jira issues. 

Follow these guidelines:

Identify Epics:

Group the requirements into high-level Epics based on functionality, such as:
User Management & Authentication
Core Platform Features
Payment & Billing (if applicable)
Security & Compliance
Performance & Scalability
Integrations & API Services
Notifications & Alerts
Break down Epics into User Stories & Tasks

Format each issue as follows:
Title: A concise description of the feature/task
Description: A clear and detailed explanation of the requirement
Acceptance Criteria: Define testable conditions for successful completion
Priority: High, Medium, or Low (based on business impact)
Assignee: (Optional: Suggest a responsible team or leave unassigned)
Labels: (e.g., frontend, backend, security, API, performance)

Example Jira Issue Structure:
    Epic: User Management & Authentication
    User Story: "As a user, I want to sign up and log in securely using email and password."
    Description: Implement user registration and authentication, including email verification and password encryption.
    Acceptance Criteria:
    User can create an account with an email and password.
    System validates credentials securely.
    Passwords are stored in an encrypted format.
    Priority: High
    Labels: authentication, security, frontend, backend
    Tasks & Subtasks:

Break complex user stories into technical tasks (e.g., API development, UI implementation, database schema updates).
Bug Tracking & Edge Cases:


Identify potential risks or failure points and create corresponding bug-tracking tasks if needed.
Convert the PRD into this structured Jira issue format, ensuring all functional and non-functional requirements are covered for efficient tracking and development."
"""

intial_tool_call_prompt = """You are a helpful assistant.\
Only complete required arguments and if you have no details of a certain argument, leave it empty.\
Write jql query if needed to get the required data. \
Important Note:
- Only complete required arguments; leave optional ones empty if no details available
- Include relevant queries (SQL/JQL) if data retrieval is needed
- Focus on extracting only these fields : ['description','summary','status','priority','assignee','duedate'] in the response

Examples of jql query formation from user query:
Provide a list of all issues reported by me or assigned to me. : reporter = currentUser() OR assignee = currentUser()
Select all open tasks in project XYZ : project = XYZ AND issuetype = task AND status != Closed
Show me all critical bugs in project ABC. : project = ABC AND issuetype = bug AND priority = Critical
Display all issues with the "urgent" label : labels = "urgent"
Select all unresolved issues reported this week. : created >= startOfWeek() AND status != Resolved
Show me all issues related to the "customer" module. : module = "customer"
Provide a list of all issues with attachments. : attachments is not empty
Display all issues with comments from the past 24 hours. : commentDate >= -24h
List all open bugs in project ABC : project = ABC AND issuetype = bug AND status != Closed
Display all high-priority issues assigned to me : priority = High AND assignee = currentUser()
Only select my bugs in XYZ project for a bug fix team : project = XYZ AND team = bugfix AND issuetype = bug AND (fixVersion in unreleasedVersions() or fixVersion is empty)
Select all issues assigned to team XYZ in the current sprint : team = XYZ AND sprint = currentSprint()
Select all issues reported by user "john.doe" in the last 7 days : reporter = "john.doe" AND created >= -7d
Show all issues with the label "urgent" or "critical" : labels in ("urgent", "critical")
Select all issues that have been modified in the past 24 hours : updated >= -24h
List all issues assigned to a user with the username "jane.smith : assignee = "jane.smith"
Select all issues that have been flagged as "blocked" : flagged = Blocked
Show all issues with a due date within the next 3 days : due <= endOfDay("+3d")
Show all issues that are currently being worked on : status = "In Progress"
Select all issues that have a "2023-06-30" due date : due = "2023-06-30"
Select all issues that have a "TASK-123" parent issue : parent = "TASK-123"
"""


loader = Docx2txtLoader("prd/rideshare_platform_plan.docx")
data = loader.load()

prd_text = f"Product Requirements Document : <prd>{data[0].page_content}</prd>"
logger.debug(prd_text)
class Answer(BaseModel):
    answer: str = Field(
        description="The answer to the user query in well-structured markdown format."
    )
def get_open_ai_response(prd,prompt):
    return openai_client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prd
                    }
                ]
            }
        ],
        response_format=Answer
    )
def open_ai_tool_call(task,full_prompt,tools):
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        tools=tools,
        messages=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": full_prompt
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": task
                    }
                ]
            }
        ],
        temperature=0,
        max_tokens=1024,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response

final_res = get_open_ai_response(prd_text,prompt)
issues_response = final_res.choices[0].message.parsed.answer

logger.info("OpenAI Response: \n{}".format(issues_response))
task = f"Create issues from these issues data : {issues_response}"
response = open_ai_tool_call(task, intial_tool_call_prompt, tools)
tool_calls = response.choices[0].message.tool_calls
for tool_call in tool_calls:
    formatted_json = json.dumps(json.loads(tool_call.function.arguments), indent=4)
    logger.debug(formatted_json)
result = toolset.handle_tool_calls(response)