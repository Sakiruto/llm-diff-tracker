import uuid
import os
import json
from loguru import logger
from openai import OpenAI
from typing import Type
from tqdm import tqdm
import time
from typing import List,Optional,Literal
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_community.document_loaders import Docx2txtLoader

from prompts.prompt import chatbot_prompt , ipl_feedback_1,ipl_feedback_2

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class IntentSchema(BaseModel):
    live_commentary: Literal["yes", "no"]
    message: str

class UserIntentionJson():
    def __init__(self,model:str = "gpt-4o"):
        self.model = model
        
    def get_structured_intention_response(
        self, 
        system_prompt: str, 
        user_input: str, 
        schema: Type[BaseModel]
    ) -> dict:
        try:
            response = client.beta.chat.completions.parse(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": [{"type": "text", "text": system_prompt}]
                    },
                    {
                        "role": "user",
                        "content": [{"type": "text", "text": user_input}]
                    }
                ],
                response_format=schema
            )
            structured_output = response.choices[0].message.parsed
            return structured_output.model_dump()


        except Exception as e:
            logger.error(f"Failed to get structured response: {e}")
            return {}

if __name__ == "__main__":
    user_intention = UserIntentionJson()

    response_data = user_intention.get_structured_intention_response(chatbot_prompt,ipl_feedback_1,IntentSchema) 
    print(json.dumps(response_data,indent=4))