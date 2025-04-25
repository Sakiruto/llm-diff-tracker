from dotenv import load_dotenv
from tqdm import tqdm
from time import time
from pydantic import BaseModel, Field
import uuid
from loguru import logger
from openai import OpenAI
import json
from composio_openai import ComposioToolSet, action
from typing import Annotated
from openai import OpenAI
import math
import os
from jira import JIRA
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
toolset = ComposioToolSet(api_key=os.getenv("PRS_COMPOSIO_API_KEY"))
print(toolset)
completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[{
        "role": "user",
        "content": "Write a one-sentence bedtime story about a unicorn."
    }]
)

# toolset.create_integration(
#     app=App.J,
#     auth_mode="OAUTH2",
#     force_new_integration=True,
#     use_composio_oauth_app=False,
#     auth_config={
#         "client_id": "1234567890",
#         "client_secret": "1234567890",
#         "redirect_uri": "https://backend.yourapp.com/handle-redirect-uri/",
#         "scopes": ["repo", "user"],
#     },
# )

## code for creating a user for my jira integration 

from composio import ComposioToolSet, App
toolset = ComposioToolSet(api_key="getzq3sc7nampw1qet3z9k")

integration = toolset.get_integration(id="99235517-f141-4e80-870a-6142cdee4b2f")
# Collect auth params from your users
print(integration.expectedInputFields)

connection_request = toolset.initiate_connection(
    integration_id=integration.id,
    entity_id="default",
)

# Redirect step require for OAuth Flow
print(connection_request.redirectUrl)
print(connection_request.connectedAccountId)
