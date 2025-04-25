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


prompt_intention = """
You are a helpful assistant that extracts structured information from user feedback related to Epics, User Stories, and Tasks in a project management system.

Your primary task is to identify which Epics, User Stories, and Tasks are being referred to in the feedback, and whether they need to be **updated** or **deleted**.

For each level (Epic, User Story, Task), do the following:
- Determine the **name** (and optionally **ID**) the user is referring to.
- Identify the **change_type**: either 'updation' or 'deletion'.
- Capture the **intention**: what the user wants to change or remove.
- Optionally include the **expected output**: what change or outcome the user anticipates or desires.

The relationships are as follows:
- Each Epic can contain multiple User Stories.
- Each User Story can contain multiple Tasks.

Return your answer in the following JSON format:

{
  "epics": [
    {
      "epic_id": 1,
      "epic_name": "Epic A",
      "change_type": "updation",
      "intention": "Update the epic description for clarity.",
      "output": "A simplified epic summary.",
      "user_stories": [
        {
          "userstory_id": null,
          "userstory_name": "Login Functionality",
          "change_type": "updation",
          "intention": "Clarify the requirements for social login.",
          "output": "Include Google and Facebook login.",
          "tasks": [
            {
              "task_id": 101,
              "task_name": "Design login screen",
              "change_type": "updation",
              "intention": "Make the UI more intuitive.",
              "output": "Redesigned login UI mockups."
            },
            {
              "task_id": null,
              "task_name": "Remove deprecated login API",
              "change_type": "deletion",
              "intention": "This task is outdated and no longer needed.",
              "output": "Remove the task from backlog."
            }
          ]
        }
      ]
    }
  ],
  "json_answer": "<The above structure stringified into a JSON string>"
}
"""
chatbot_prompt = """
You are an assistant whose only task is to detect whether the user is asking for live IPL commentary for the following match:

Match Details:
{
"live_commentary": "yes",
"message": "The IPL clash between Royal Challengers Bengaluru and Punjab Kings kicks off today at 7:30 PM IST at the iconic M.Chinnaswamy Stadium in Bengaluru. Stay tuned for ball-by-ball commentary once the match begins—you can follow live updates at the provided link."
}

If the user’s input is related to IPL but outside live commentary windows (e.g. asking for past scores or schedules), respond with exactly:

{
"live_commentary": "no",
"message": "The IPL match is scheduled at 7:30 PM today at Bengaluru, M.Chinnaswamy Stadium. Live commentary will be available only during match hours."
}

If the user’s input is completely unrelated to IPL live commentary, respond with exactly:

{
"live_commentary": "no",
"message": "Only live commentary of IPL is provided."
}

"""

ipl_feedback_1 = """
hey I want live commentary of f1 game 
"""
ipl_feedback_2 = """
hey I want live commentary of todays IPL game , current_datetime: 8:48 april 18th
match score data  [
    {
        "title": "Royal Challengers Bengaluru vs Punjab Kings",
        "link": "https://www.cricbuzz.com/live-cricket-scores/115174/rcb-vs-pbks-34th-match-indian-premier-league-2025",
        "today": "Today",
        "time": "7:30 PM",
        "stadium": "Bengaluru, M.Chinnaswamy Stadium"
    }
]
"""
# future_addition to make 
future_prompt_addition = """
User stories inside the Epics(if user provides userstory_id and epic name or epic_id it is a bonus) ,
Tasks inside the User Stories(if user provides task_id && user story name or userstory_id && epic_id is a bonus) that need to be Updated or deleted 

"""

# a structured userfeed back for checking the user intention 

user_feedback = """
Epic: User Management needs updation — its description should be clearer and more user-focused.

Under User Management:
- User Story: Login Experience should be updated to include support for biometric login. The output should be a user-friendly login process using fingerprint or face recognition.
  - Task: "Implement social login" should be updated to include Twitter in addition to Google and Facebook.
  - Task: "Legacy login UI support" should be deleted as it is no longer required.

- User Story: Password Reset should be deleted completely as it's handled externally now.

Epic: Security and Compliance needs to be broken down into more granular user stories to better manage the scope.

Under Security and Compliance:
- Add a new user story: "Data Encryption at Rest" — ensure all stored data is encrypted using AES-256.
- Add a new user story: "Two-Factor Authentication" — require OTP via email or SMS during login.

Epic with epic_id 6 needs to be deleted entirely as it is out of scope.

"""
prd_to_iisues = """
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



user_feedback_2 = """
Epic: User Management & Authentication needs refinement — its epic description should emphasize secure onboarding and access.

Under User Management & Authentication:
- User Story: Authentication should support biometric login. Update the acceptance criteria to include fingerprint and face recognition options. The output should describe a seamless and secure biometric login flow.
  - Task: "Implement password management system" should be updated to support passwordless login options such as OTP or biometric fallback.
  - Task: Add a new task: "Integrate biometric authentication module" — this should cover iOS and Android support for Face ID and fingerprint login.

- User Story: Profile creation should be updated to include KYC verification using government-issued ID.

Epic: Core Platform Features needs to be more modular.

Under Core Platform Features:
- User Story: Ride-sharing should also support recurring rides for daily commuters. Update the overview and acceptance criteria accordingly.
  - Task: Add a new task: "Implement recurring ride booking UI" — allow users to schedule rides for an entire week in advance.
  - Task: "Develop ride-sharing coordination interface" should also handle multiple match suggestions.

Epic: Payment & Billing should be split into two user stories — one for **Payment Integration** and one for **User Wallet** features.

Under Payment & Billing:
- User Story: Payment method management should include support for UPI and international cards.
  - Task: Add a new task: "Add UPI integration for Indian users."

Epic: User Experience & Interface Improvements:
- User Story: Improve layout should focus on accessibility standards (WCAG compliance). Update the acceptance criteria to mention keyboard navigation and screen reader support.
  - Task: "Enhance navigational elements" should include better tab-indexing and ARIA tags.

Epic with epic_id 5 should be deleted — it was for internal testing only and is out of scope.
"""

user_feedback_3 = """
Epic: User Management & Authentication needs refinement — its epic description should emphasize secure onboarding and access.

Under User Management & Authentication:
- User Story: Authentication should also support biometric login along with phone verification. Update the acceptance criteria to include fingerprint and face recognition options. The output should describe a seamless and secure biometric login flow.
              change priority to medium 
  - Task: "Implement password management system" should be updated to support passwordless login options such as OTP or biometric fallback.
  - Task: Add a new task: "Integrate biometric authentication module" — this should cover iOS and Android support for Face ID and fingerprint login.

Completely delete the Epic : performance and scability 
"""


user_feedback_4 = """
Under Epic User Management & Authentication  
- User Story: Facilitate user registration with secure authentication.
Authentication should also support biometric login along with phone verification. Update the acceptance criteria to include fingerprint and face recognition options. The output should describe a seamless and secure biometric login flow.
change user story priority to medium 

  - Task: Add a new task: "Implement password management system" should  support passwordless login options such as OTP or biometric fallback.
  - Task: Add a new task: "Integrate biometric authentication module" — this should cover iOS and Android support for Face ID and fingerprint login.

"""

user_feedback_5 = """
Under Payment and Billing Management
- add User Story: Payment method management should include support for UPI and international cards.
and keep priority high for this user story 
  - Task: Add a new task: "Add UPI integration for Indian users.
  you can add more task along with above task based on requirement 
"""

user_feedback_6 = """
Completely remove the Epic Safety & Compliance
"""

user_feedback_7 = """
Inside the epic Core PLatform Features remove the User Story: Integrate in-ride experiences and GPS tracking.
make the priority of user story in this epic medium  
"""

user_feedback_8 = """
remove the third task from the
User Story: Implement a secure registration and login system for users and drivers 
inside Epic: User Management & Authentication.
"""