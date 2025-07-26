import os
from dotenv import load_dotenv
from fasthtml.common import *
from smolagents import ToolCallingAgent, ToolCollection
from mcp import StdioServerParameters
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# --- Model and Tool Server Setup ---
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=os.environ.get("GOOGLE_API_KEY"))

tool_server_params = StdioServerParameters(
    command="python",
    args=["tool_server.py"],
)

# --- fasthtml Application Setup ---
app, rt = fast_app()

def page_layout(main_content):
    return Html(Head(Title('MildEye - Tool User'), Script(src="https://unpkg.com/htmx.org@1.9.12"), Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css")),Body(Header(H1('Ask the Tool-Using Agent')), Main(main_content, cls='container'), Footer(P('© 2025 - MildEye Inc.'))))

@rt('/')
def get():
    input_form = Form(Input(id='user_text', name='user_text', placeholder='Ask a question...'), Button('Submit'), hx_post='/submit', hx_target='#response-div', hx_indicator='#spinner')
    spinner = Div(id='spinner', cls='htmx-indicator', inner='Loading...')
    response_div = Div(id='response-div')
    return page_layout(Group(input_form, spinner, response_div))

# The post function now handles the agent and tool creation
@rt('/submit')
async def post(user_text: str):
    # Use the 'with' statement to correctly acquire the tools
    with ToolCollection.from_mcp(tool_server_params, trust_remote_code=True) as tool_collection:
        # Create the agent inside the 'with' block, using the acquired tools
        research_agent = ToolCallingAgent(
            tools=[*tool_collection.tools],
            model=llm
        )
        
        # Run the agent with the user's input
        result = await research_agent.arun(user_text)
    
    return P(result)

serve()