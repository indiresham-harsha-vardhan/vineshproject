import os

from openai import OpenAI


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_ai_response(user_message):

    response = client.responses.create(
        model="gpt-5.6-luna",

        instructions="""
        You are the AI assistant for Prime Estates,
        a real-estate company.

        Be friendly, professional and helpful.

        Do not invent company-specific information.
        If you don't know something, say that you
        don't have that information.
        """,

        input=user_message
    )

    return response.output_text