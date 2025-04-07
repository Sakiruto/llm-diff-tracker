from dotenv import load_dotenv
from openai import OpenAI
from composio_openai import ComposioToolSet, App, Action
import os
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
toolset = ComposioToolSet(api_key=os.getenv("PRS_COMPOSIO_API_KEY"))

connection = toolset.get_connected_account("9cfad38a-eac3-4d65-bc67-c226ab91fcf7")


def gmail_preprocessor(inputs: dict) -> dict:
    inputs["recipient_email"] = "sama@composio.dev"  # Change to an email you can access to test!
    return inputs


def gmail_schema_processor(schema: dict) -> dict:
    del schema["recipient_email"]
    return schema


processed_send_email_tool = toolset.get_tools(
    actions=[Action.GMAIL_SEND_EMAIL],
    processors={
        "schema": {Action.GMAIL_SEND_EMAIL: gmail_schema_processor},
        "pre": {Action.GMAIL_SEND_EMAIL: gmail_preprocessor},
    },
    check_connected_accounts=False,
)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are head of AGI at OpenAI."},
        {
            "role": "user",
            "content": "Send an email to Sam Altman in one sentence that AGI is coming 5 years earlier.",
        },
    ],
    tools=processed_send_email_tool,
)

exec_response = toolset.handle_tool_calls(response)

print(exec_response)