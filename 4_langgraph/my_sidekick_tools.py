import os, requests
from dotenv import load_dotenv

from langchain.agents import Tool

from playwright.async_api import async_playwright
from langchain_community.agent_toolkits import FileManagementToolkit, PlayWrightBrowserToolkit
from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
from langchain_community.utilities import GoogleSerperAPIWrapper

from langchain_experimental.tools import PythonREPLTool

# Load environment variables

load_dotenv(override=True)
pushover_token = os.getenv("PUSHOVER_TOKEN")
pushover_user = os.getenv("PUSHOVER_USER")
pushover_url = "https://api.pushover.net/1/messages.json"
serper = GoogleSerperAPIWrapper()

# Tool Definitions

async def get_playwright_tools():
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False)
    toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=browser)
    return toolkit.get_tools(), playwright, browser #  playwright & browser are returned in order to clean resources

def get_file_tools():
    toolkit = FileManagementToolkit(root_dir='sandbox')
    return toolkit.get_tools()

def push(text: str):
    """Send a push notification to the user"""
    requests.post(pushover_url, data = {"token": pushover_token, "user": pushover_user, "message": text})
    return "success"

async def get_other_tools():
    
    file_tools = get_file_tools()
    push_tool = Tool(name='send_push_notification', func=push, description='Use this tool when you want to send a push notification')
    search_tool = Tool(name='search', func=serper.run, description='Use this tool when you want to get the results of an online web search')
    wiki_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
    python_repl = PythonREPLTool()
    # Can add more tools, from langchain ecosystem here (ask GPT or read documentation to get the tools and how to use them)

    other_tools = file_tools + [push_tool, search_tool, wiki_tool, python_repl]
    return other_tools