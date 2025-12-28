# Imports
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader
import json
import os
import requests
import gradio as gr

# The usual start
load_dotenv(override=True)

# Function to send a push notification
def send_push_notification(message):
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER"),
            "message": message
        }
    )


# Function to record details of user that is interested in being in touch
def record_user_details(email, name="not provided", notes="not provided"):
    """Records details of a user who is interested in being in touch."""
    if not email:
        return "Error: Email is required to record user details."

    send_push_notification(f"Recording interest from {name} with email {email} and notes {notes}")

    # Return a simple string to confirm success
    return f"Successfully logged details for {name} ({email})."    

# Function to record unanswered questions
def record_unanswered_question(question):
    """Records a user's question that the model could not answer."""

    if not question:
        return "Error: No question was provided to record."

    send_push_notification(f"Recording this question that I couldn't answer: {question}")

    # Return a simple string to confirm success
    return f"Successfully logged question: {question}"

# Tool Definitions in JSON format. The suffix "_TOOL" clearly states their purpose.
# Using UPPER_SNAKE_CASE, as these are module-level constants.
# These tools are used to record user details and unanswered questions.

RECORD_USER_DETAILS_TOOL = {
    "name": "record_user_details",
    "description": "Records details of a user who is interested in being in touch.",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The user's email address.",
            },
            "name": {
                "type": "string",
                "description": "The user's name.",
            },
            "notes": {
                "type": "string",
                "description": "Any additional notes the user provided.",
            },
        },
        "required": ["email"],
        "additionalProperties": False 
    }
}

RECORD_UNANSWERED_QUESTION_TOOL = {
    "name": "record_unanswered_question",
    "description": "Always use this tool to record any question that the user asked but couldn't be answered.",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question that couldn't be answered"
            }
        },
        "required": ["question"],
        "additionalProperties": False 
    }
}

# Assemble the Final Tools List
tools = [
    {"type": "function", "function": RECORD_USER_DETAILS_TOOL},
    {"type": "function", "function": RECORD_UNANSWERED_QUESTION_TOOL}
]

# The Me class is the main class for the chatbot.
# It is used to represent the person the chatbot is representing.
# It is also used to handle the tool calls and the system prompt.

class Me:
    def __init__(self):
        self.openai = OpenAI()
        # Define the name of the person the chatbot is representing
        # This is used to personalize the chatbot's responses
        self.name = "Ed Donner"
        # Read the LinkedIn PDF file using the pypdf library
        self.linkedin_text = ""
        reader = PdfReader("me/linkedin.pdf")
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.linkedin_text += text
        # Read the summary of the person the chatbot is representing
        # This is used to provide context to the chatbot's responses
        with open("me/summary.txt", "r", encoding="utf-8") as f:
            self.summary = f.read()


    # This is a more elegant way that avoids the IF statement/function.
    def handle_tool_calls(self, tool_calls):
        """
        Takes a list of tool_calls from an OpenAI response, executes them,
        and returns a list of "tool" messages.
        """
        tool_output = []

        for tool_call in tool_calls:
            # Get the function name and the function to call
            function_name = tool_call.function.name
            function_to_call = globals().get(function_name)

            if not function_to_call:
                # Handle cases where the model tries to call a function that doesn't exist
                function_response = f"Error: Function '{function_name}' not found."
            else:
                try:
                    # 1. Parse the JSON string of arguments
                    function_args = json.loads(tool_call.function.arguments)
                    # 2. Call the function using ** to unpack the dictionary as arguments
                    print(f"Tool called: {function_name}", flush=True)
                    function_response = function_to_call(**function_args)
                except Exception as e:
                    # Handle any errors during function execution
                    function_response = f"Error executing {function_name}: {str(e)}"

            tool_output.append({"role": "tool", "tool_call_id": tool_call.id, "content": json.dumps(function_response)})

        return tool_output     


    def system_prompt(self):
        """
        Defines the system prompt for the chatbot which uses GPT-4o-mini model
        """
        system_prompt = f"You are acting as {self.name}. You are answering questions on {self.name}'s website, \
        particularly questions related to {self.name}'s career, background, skills and experience. \
        Your responsibility is to represent {self.name} for interactions on the website as faithfully as possible. \
        You are given a summary of {self.name}'s background and LinkedIn profile which you can use to answer questions. \
        Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
        If you don't know the answer to any question, use your record_unanswered_question tool to record the question that you couldn't answer, even if it's about something trivial or unrelated to career. \
        If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and record it using your record_user_details tool. "

        system_prompt += f"\n\n## Summary:\n{self.summary}\n\n## LinkedIn Profile:\n{self.linkedin_text}\n\n"
        system_prompt += f"With this context, please chat with the user, always staying in character as {self.name}."
        return system_prompt
    

    def chat(self, message, history):
        messages = [{"role": "system", "content": self.system_prompt()}] + history + [{"role": "user", "content": message}]
        
        done = False
        while not done:

            # This is the call to the LLM - see that we pass in the tools json
            response = self.openai.chat.completions.create(model="gpt-4o-mini", messages=messages, tools=tools)

            finish_reason = response.choices[0].finish_reason
            
            # If the LLM wants to call a tool, we do that!
            if finish_reason == "tool_calls":
                response_message = response.choices[0].message
                tool_calls = response_message.tool_calls
                tool_outputs = self.handle_tool_calls(tool_calls)
                messages.append(response_message)
                messages.extend(tool_outputs)
            else:
                response_message = response.choices[0].message
                done = True
        return response_message.content

# The main function is the entry point for the chatbot.
# It creates an instance of the Me class and launches the chat interface.
if __name__ == "__main__":
    me = Me()
    gr.ChatInterface(me.chat, type="messages").launch()

