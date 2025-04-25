from typing import List,Optional,Literal
from pydantic import BaseModel, Field
from enum import Enum

    
class Task(BaseModel):
    task_id: str = Field(..., description="Hierarchical ID (e.g., 1.1.1) assigned to each task inside a user story.")
    task: str = Field(..., description="The name or title of the task.")
    description: str = Field(..., description="A detailed description of what the task entails.")
    priority: str = Field(..., description="The priority level of the task (e.g., High, Medium, Low).")
    labels: str = Field(..., description="Tags or labels associated with the task for categorization.")
    output: Optional[str] = Field(None, description="The expected or actual output/result of the task.")
    
class UserStory(BaseModel):
    userstory_id: str = Field(..., description="Hierarchical ID (e.g., 1.1) assigned to each user story inside an epic.")
    overview: str = Field(..., description="A high-level summary of the user story.")
    request: str = Field(..., description="The specific request or requirement from the user.")
    acceptance_criteria: str = Field(..., description="Conditions that must be met for the user story to be considered complete.")
    priority: str = Field(..., description="The priority level of the user story (e.g., High, Medium, Low).")
    labels: str = Field(..., description="Tags or labels associated with the user story for organization.")
    tasks: List[Task] = Field(default_factory=list, description="A list of tasks that need to be completed for this user story.")
    output: Optional[str] = Field(None, description="The expected or actual output/result of the user story.")
    
class Epic(BaseModel):
    epic_id: int = Field(..., description="Incremental unique ID assigned to each epic.")
    epic: str = Field(..., description="The name or title of the epic.")
    user_stories: List[UserStory] = Field(default_factory=list, description="A list of user stories that fall under this epic.")
    output: Optional[str] = Field(None, description="The expected or actual output/result of the epic.")
    
class Answer(BaseModel):
    epics: List[Epic] = Field(default_factory=list, description="A list of epics containing related user stories and tasks.")
    
# for structured response updation/ deletion 

class TaskToBeChanged(BaseModel):
    task_id: Optional[int] = Field(None, description="The ID of the task to be changed.")
    task_name: str = Field(..., description="The name of the task to be updated or deleted.")
    change_type: Literal['updation', 'deletion'] = Field(..., description="Whether it's an 'updation' or 'deletion'.")
    intention: str = Field(..., description="What should be changed in this task.")
    output: Optional[str] = Field(None, description="The expected result of the change.")


class UserStoryToBeChanged(BaseModel):
    userstory_id: Optional[int] = Field(None, description="The ID of the user story to be changed.")
    userstory_name: str = Field(..., description="The name of the user story to be updated or deleted.")
    change_type: Literal['updation', 'deletion'] = Field(..., description="Whether it's an 'updation' or 'deletion'.")
    intention: str = Field(..., description="What should be changed in this user story.")
    output: Optional[str] = Field(None, description="The expected result of the change.")
    tasks: Optional[List[TaskToBeChanged]] = Field(default_factory=list, description="Tasks under this user story that also need changes.")


class EpicToBeChanged(BaseModel):
    epic_id: Optional[int] = Field(None, description="The ID of the epic to be changed.")
    epic_name: str = Field(..., description="The name of the epic to be updated or deleted.")
    change_type: Literal['updation', 'deletion'] = Field(..., description="Whether it's an 'updation' or 'deletion'.")
    intention: str = Field(..., description="What should be changed in this epic.")
    output: Optional[str] = Field(None, description="The expected result of the change.")
    user_stories: Optional[List[UserStoryToBeChanged]] = Field(default_factory=list, description="User stories under this epic that also need changes.")


class EpicsToBeChanged(BaseModel):
    epics: List[EpicToBeChanged] = Field(
        default_factory=list,
        description="List of epics and their nested user stories and tasks to be changed."
    )


