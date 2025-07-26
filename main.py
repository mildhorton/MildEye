from fasthtml.common import *
from crewai import Crew, Task, Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from tools import CsvSearchTool, search_tool # Import both tools
import os
from dotenv import load_dotenv

load_dotenv()

# --- Agent Definitions ---
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=os.environ.get("GOOGLE_API_KEY"))

# Define our first specialized "Executive" agent
sec_filings_agent = Agent(
    role="SEC Filings Analyst",
    goal="Analyze SEC 10-K and 10-Q filings to summarize risk and debt for a given company.",
    backstory="You are an expert financial analyst specializing in extracting key information from public company filings.",
    llm=llm,
    tools=[search_tool], # Give the agent the web search tool
    verbose=True
)

# --- fasthtml Application Setup ---
app, rt = fast_app()

def page_layout(main_content):
    # This layout function is the same as before
    return Html(Head(Title('MildEye - Executive Agent'), Script(src="https://unpkg.com/htmx.org@1.9.12"), Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css")),Body(Header(H1('Ask the SEC Filings Agent')), Main(main_content, cls='container'), Footer(P('© 2025 - MildEye Inc.'))))

@rt('/')
def get():
    input_form = Form(Input(id='user_text', name='user_text', placeholder='Enter a company name...'), Button('Submit'), hx_post='/submit', hx_target='#response-div', hx_indicator='#spinner')
    spinner = Div(id='spinner', cls='htmx-indicator', inner='Loading...')
    response_div = Div(id='response-div')
    return page_layout(Group(input_form, spinner, response_div))

@rt('/submit')
def post(user_text: str):
    # Create a task for our new agent
    task = Task(
        description=f"Find the latest SEC 10-K filing for {user_text} and summarize its key risk factors.",
        expected_output="A concise summary of the most important risk factors mentioned in the filing.",
        agent=sec_filings_agent
    )
    crew = Crew(agents=[sec_filings_agent], tasks=[task], verbose=2)
    result = crew.kickoff()
    return P(result)

# Run the app
serve()