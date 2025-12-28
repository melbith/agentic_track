import os, sendgrid
from agents import Agent, function_tool
from sendgrid.helpers.mail import Email, Mail, Content, To
from typing import Dict

# Setup the Function Tool to send HTML email

@function_tool
def send_email(subject: str, html_body: str) -> Dict[str, str]:
    """ Send out an email with the given subject and HTML body """

    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get("SENDGRID_API_KEY"))

    from_email = Email("skillshift.ai@gmail.com") # SendGrid verified sender
    to_email = To("melbith@gmail.com")
    content = Content("text/html", html_body)

    mail = Mail(from_email, to_email, subject, content)

    try:
        sg.client.mail.send.post(request_body=mail.get())
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

EA_INSTRUCTIONS = """
You are able to send a nicely formatted HTML email based on a detailed report.
You will be provided with a detailed report. You should use your tool to send one email, providing the 
report converted into clean, well presented HTML with an appropriate subject line.
"""

email_agent = Agent(
    name="Email Agent",
    instructions=EA_INSTRUCTIONS,
    model="gpt-4o-mini",
    tools=[send_email]
)