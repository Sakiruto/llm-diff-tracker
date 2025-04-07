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
from composio_openai import ComposioToolSet, App


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Task(BaseModel):
    task_id: int = Field(...,description="incremental unique id assigned to each task inside user story")
    task: str = Field(..., description="The name or title of the task.")
    description: str = Field(..., description="A detailed description of what the task entails.")
    priority: str = Field(..., description="The priority level of the task (e.g., High, Medium, Low).")
    labels: str = Field(..., description="Tags or labels associated with the task for categorization.")
    output: Optional[str] = Field(None, description="The expected or actual output/result of the task.")

class UserStory(BaseModel):
    userstory_id: int = Field(...,description="incremental unique id assigned to each user story inside epic")
    overview: str = Field(..., description="A high-level summary of the user story.")
    request: str = Field(..., description="The specific request or requirement from the user.")
    acceptance_criteria: str = Field(..., description="Conditions that must be met for the user story to be considered complete.")
    priority: str = Field(..., description="The priority level of the user story (e.g., High, Medium, Low).")
    labels: str = Field(..., description="Tags or labels associated with the user story for organization.")
    tasks: List[Task] = Field(default_factory=list, description="A list of tasks that need to be completed for this user story.")
    output: Optional[str] = Field(None, description="The expected or actual output/result of the user story.")

class Epic(BaseModel):
    epic_id: int = Field(...,description="incremental unique id assigned to each epic")
    epic: str = Field(..., description="The name or title of the epic.")
    user_stories: List[UserStory] = Field(default_factory=list, description="A list of user stories that fall under this epic.")
    output: Optional[str] = Field(None, description="The expected or actual output/result of the epic.")

class Answer(BaseModel):
    epics: List[Epic] = Field(default_factory=list, description="A list of epics containing related user stories and tasks.")
    json_answer: str = Field(..., description="A well-structured json response to the user query.")


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
            issues_response = json.loads(res.choices[0].message.content)
            print(json.dumps(issues_response, indent=2))
            md_content = "# Prd Issues Breakdown\n\n"

            for epic in issues_response.get("epics", []):
                md_content += f"## Epic: {epic['epic']}\n\n"

                for story in epic.get("user_stories", []):
                    md_content += f"### User Story: {story['overview']}\n"
                    md_content += f"**Request:** {story['request']}\n\n"
                    md_content += f"**Acceptance Criteria:** {story['acceptance_criteria']}\n\n"
                    md_content += f"**Priority:** {story['priority']}\n\n"
                    md_content += f"**Labels:** {story['labels']}\n\n"

                    md_content += "#### Tasks:\n"
                    for task in story.get("tasks", []):
                        md_content += f"- **Task:** {task['task']}\n"
                        md_content += f"  - **Description:** {task['description']}\n"
                        md_content += f"  - **Priority:** {task['priority']}\n"
                        md_content += f"  - **Labels:** {task['labels']}\n\n"

                md_content += "---\n\n"

            # Write the markdown content to a file
            with open(output_file, "w", encoding="utf-8") as md_file:
                md_file.write(md_content)

            logger.info(f"Response written to {output_file}")

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse OpenAI response: {e}")

prompt = """
Given the following Product Requirements Document (PRD), extract key features and convert them into structured Jira issues.

---

## **Guidelines:**

### **Identify Epics**
Group the requirements into high-level **Epics** based on functionality, such as:
- User Management & Authentication
- Core Platform Features
- Payment & Billing (if applicable)
- Security & Compliance
- Performance & Scalability
- Integrations & API Services
- Notifications & Alerts

---

## **Stories: User-Centric Stories**
Stories focus on delivering value to the end-user and describe a feature or functionality from the user's perspective.
Each user stories has 2 or mores Task  

### **When to use Stories:**
✅ To capture user requirements and functionality.  
✅ For tasks that deliver a specific piece of value to the user.  
✅ When breaking down an Epic into smaller, actionable items.  

### **How to use Stories effectively:**
- Write stories in a **"verb the noun"** format, forming imperative sentences like `"Create the event content type."`  
- Use **acceptance criteria** to define the conditions for completion.  
- Break down large stories into smaller tasks if they become too complex.  

---

### **Jira Issue Format:**
#### **User Story Format**
**Title:** A concise description of the feature/task  

**Description:**  
- **Overview:**: A high-level summary and the purpose of the ticket.  
- **Request:** A detailed description of the task.  
- **Acceptance Criteria:** Clearly defined conditions for successful completion.  
- **Resources:** (Optional) Links to related discussions or documents.  

**Priority:** High, Medium, or Low (based on business impact)  
**Assignee:** (Optional: Suggest a responsible team or leave unassigned)  
**Labels:** (e.g., frontend, backend, security, API, performance)  

---

## **Tasks: The Building Blocks**  
Tasks represent individual pieces of work that need to be completed, which may not necessarily deliver direct value to the user but are essential for the project's progress.

### **When to Use Tasks:**
✅ For technical work supporting a story.  
✅ For internal development or infrastructure work.  
✅ To track progress on backend, frontend, database, or API-related activities.  

#### **Task Format:**
**Task:** A concise description of the task  
**Description:** A clear and detailed explanation of the requirement  
**Priority:** High, Medium, or Low (based on business impact)  
**Assignee:** (Optional: Suggest a responsible team or leave unassigned)  
**Labels:** (e.g., frontend, backend, security, API, performance)  

---

# **Jira Issue Structure Example**  

## **Epic: User Management & Authentication**  

---

### **User Story 1: Enable users to sign up and log in securely using email and password**  

**Description:**  
- **Overview:** Implement a secure registration and login system to authenticate users using email or phone verification.  
- **Request:** Develop a user authentication system with secure registration, email/phone verification, and login. Ensure encryption and validation.  
- **Acceptance Criteria:**  
  - Users can register using an email or phone number and set a password.  
  - The system sends a verification email or SMS.  
  - Users can log in after successful verification.  
  - Passwords are stored securely using encryption.  
  - The system handles incorrect login attempts with error messages.  

**Priority:** High  
**Labels:** authentication, security, frontend, backend  

#### **Tasks:**  

1️⃣ **Implement user verification and account activation**  
   - **Description:** Develop mechanisms for verifying user accounts via email or SMS and activating the account upon verification.  
   - **Priority:** High  
   - **Labels:** backend, security  

2️⃣ **Develop login API and session management**  
   - **Description:** Build an API for handling user authentication, including login, session handling, and token expiration.  
   - **Priority:** High  
   - **Labels:** backend, API, authentication  

3️⃣ **Create UI for registration and login flow**  
   - **Description:** Design and develop the frontend UI for user registration, login, and error handling.  
   - **Priority:** High  
   - **Labels:** frontend, UI, authentication 
---

### **User Story 2: Enable two-factor authentication (2FA) for increased security**  

**Description:**  
- **Overview:** Users should be able to enable two-factor authentication (2FA) to enhance account security using OTP or authenticator apps.  
- **Request:** Develop a 2FA feature that allows users to enable and disable 2FA and manage recovery options.  
- **Acceptance Criteria:**  
  - Users can enable/disable 2FA from account settings.  
  - System supports authentication via OTP (SMS/email) or Authenticator apps.  
  - Recovery codes are provided when 2FA is enabled.  
  - Secure handling of authentication failures and user lockout scenarios.  

**Priority:** High  
**Labels:** security, authentication, backend  

#### **Tasks:**  

1️⃣ **Design UI for enabling/disabling 2FA**  
   - **Priority:** Medium  
   - **Labels:** frontend, UI, security  

2️⃣ **Implement backend API for 2FA activation**  
   - **Priority:** High  
   - **Labels:** backend, API, authentication  

3️⃣ **Generate and store recovery codes securely**  
   - **Priority:** High  
   - **Labels:** backend, security  

4️⃣ **Integrate OTP service for SMS/email authentication**  
   - **Priority:** High  
   - **Labels:** backend, security, API  
---

## **Epic: User Profile Management**  

---

### **User Story 1: Allow users to update their profile information**  

**Description:**  
- **Overview:** Users should be able to edit their personal details such as name, email, phone number, and profile picture.  
- **Request:** Provide a profile update page where users can modify their personal details securely. Ensure all changes are validated and stored correctly.  
- **Acceptance Criteria:**  
  - Users can update their name, email, and phone number.  
  - Users can upload or change their profile picture.  
  - System enforces validation for email format and phone number.  
  - Changes persist correctly in the database.  

**Priority:** Medium  
**Labels:** profile, frontend, backend  

#### **Tasks:**  

1️⃣ **Create frontend UI for profile editing**  
   - **Description:** Design and implement the frontend interface for users to update profile details.  
   - **Priority:** Medium  
   - **Labels:** frontend, UI, profile  

2️⃣ **Implement API for profile update requests**  
   - **Description:** Develop a secure API endpoint to handle profile update requests.  
   - **Priority:** High  
   - **Labels:** backend, API, security  

---

## **Epic: Dashboard & User Experience Improvements**  

---

### **User Story 1: Improve dashboard UI for better navigation**  

**Description:**  
- **Overview:** Enhance user experience by improving dashboard layout and design.  
- **Request:** Adjust spacing, add hover effects, and refine element alignments.  
- **Acceptance Criteria:**  
  - Buttons and elements are correctly aligned.  
  - Hover effects improve user interaction.  
  - Navigation is optimized for mobile devices.  

**Priority:** Low  
**Labels:** frontend, UI, design  

#### **Tasks:**  

1️⃣ **Fix padding and spacing inconsistencies**  
   - **Description:** Adjust UI elements for a cleaner look.  
   - **Priority:** Low  
   - **Labels:** frontend, UI  

2️⃣ **Add hover effects to buttons and links**  
   - **Description:** Improve interactivity with visual feedback.  
   - **Priority:** Low  
   - **Labels:** frontend, UX  

3️⃣ **Optimize dashboard layout for mobile screens**  
   - **Description:** Ensure proper rendering on small devices.  
   - **Priority:** Medium  
   - **Labels:** frontend, responsive design  

---

### **Additional Considerations:**
- The number of tasks **varies per story (between 1 and 8)**.  
- Stories follow **"verb the noun"** format.  
- Tasks ensure **frontend, backend, API, and security aspects** are addressed.  

""".strip()

loader = Docx2txtLoader("files/rideshare_platform_plan.docx")
data = loader.load()
prd_text = f"""
## Product Requirements Document
```PRD
{data[0].page_content}
"""
# Initial
bot = Chatbot(prompt,"gpt-4o")
res = bot.get_openai_response(prd_text)

bot.show_response(res, "openai_response_1.md")



# # giving a gap between ouputs 
# time.sleep(5)
# print("""

      
# This is the output after feedback 

      
# """)
# # giving feedback and generating output 


# bot.add_message("system",res.choices[0].message.parsed.json_answer)

# consistency = """
# Ensure strict adherence to the original Jira issue structure:
# - **User Stories must retain clear structure** (Title, Description, Request, Acceptance Criteria, Priority, Labels).
# - **All Tasks within a User Story must align in description, priority, and labels.**
# - **Do not alter the priority or labels unless user feedback explicitly requests it.**
# - **Expand epics where necessary but avoid unnecessary modifications.**
# - **Preserve consistent wording, formatting, and structure across all elements.**
# - **Ensure no missing sections or formatting discrepancies.**
# """


# user_feedback :str =  input("Enter the feedback")

# final_feedback = f"""
# {consistency}

# {user_feedback}
# """


# res1 = bot.get_openai_response(final_feedback)
# bot.show_response(res1, "openai_response_3.md")

