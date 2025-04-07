import uuid
import os
import json
from loguru import logger
from openai import OpenAI
from tqdm import tqdm
from time import time
from typing import List,Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_community.document_loaders import Docx2txtLoader
from composio_openai import ComposioToolSet, App

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Task(BaseModel):
    task: str
    description: str
    priority: str
    labels: str
    output: Optional[str] = None

class UserStory(BaseModel):
    overview: str
    request: str
    acceptance_criteria: str
    priority: str
    labels: str
    tasks: List[Task]
    output: Optional[str] = None

class Epic(BaseModel):
    epic: str
    user_stories: List[UserStory]
    output: Optional[str] = None

class Answer(BaseModel):
    epics: List[Epic]
    markdown_answer: str = Field(
        description="A well-structured markdown response to the user query."
    )

## this prompt has tokens of 2,167
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

## **Stories: User-Centric Narratives**
Stories focus on delivering value to the end-user and describe a feature or functionality from the user's perspective.

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

### **How to Use Tasks Effectively:**
- Clearly define the scope and requirements for each task.  
- Use **subtasks** to break down complex tasks into smaller, manageable pieces.  
- Assign tasks to team members with the appropriate skills and expertise.  

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

4️⃣ **Implement password reset and recovery**  
   - **Description:** Develop the mechanism for users to reset passwords using email or SMS-based verification.  
   - **Priority:** Medium  
   - **Labels:** backend, security, authentication  

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

5️⃣ **Implement authentication via authenticator apps**  
   - **Priority:** High  
   - **Labels:** backend, security, API  

6️⃣ **Handle lockout scenarios and recovery flow**  
   - **Priority:** High  
   - **Labels:** backend, security  

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

4️⃣ **Update icons for better accessibility**  
   - **Description:** Use clear, high-contrast icons for better visibility.  
   - **Priority:** Low  
   - **Labels:** frontend, accessibility  

---

## **Epic: Security & Access Control**  

---

### **User Story 1: Implement role-based access control (RBAC)**  

**Description:**  
- **Overview:** Develop a role-based access system to control permissions.  
- **Request:** Implement an RBAC system with different permission levels.  
- **Acceptance Criteria:**  
  - Admins can assign roles to users.  
  - Access is restricted based on user roles.  
  - Unauthorized users cannot perform restricted actions.  

**Priority:** High  
**Labels:** security, backend  

#### **Tasks:**  

1️⃣ **Design role hierarchy in database schema**  
   - **Description:** Create database models to store role-based permissions.  
   - **Priority:** High  
   - **Labels:** backend, security  

2️⃣ **Implement role-based authorization in API**  
   - **Description:** Restrict API endpoints based on user roles.  
   - **Priority:** High  
   - **Labels:** backend, API  

3️⃣ **Develop admin panel for role management**  
   - **Description:** Provide UI for assigning and modifying user roles.  
   - **Priority:** Medium  
   - **Labels:** frontend, admin-panel

---

### **Additional Considerations:**
- The number of tasks **varies per story (between 1 and 8)**.  
- Stories follow **"verb the noun"** format.  
- Tasks ensure **frontend, backend, API, and security aspects** are addressed.  

"""

loader = Docx2txtLoader("files/rideshare_platform_plan.docx")
data = loader.load()

prd_text = f"Product Requirements Document : <prd>{data[0].page_content}</prd>"

def get_open_ai_response(prd: str, prompt: str):
    return client.beta.chat.completions.parse(
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


final_res = get_open_ai_response(prd_text,prompt)
issues_response = final_res.choices[0].message.parsed.markdown_answer

logger.info("OpenAI Response: \n{}".format(issues_response))
task = f"Create issues from these issues data : {issues_response}"
