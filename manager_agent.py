from agents import Agent
from planner_agent import planner_agent
from search_agent import search_agent
from writer_agent import writer_agent
from email_agent import email_agent

INSTRUCTIONS = """You are a research manager coordinating a deep research pipeline.
Given a research query and optional clarifications from the user, you must:

1. Call `plan_searches` with the query and clarifications to get a set of targeted search queries.
2. Call `web_search` for EACH of the search queries returned by the planner (usually 5 searches).
3. Call `write_report` with the original query and ALL the search summaries combined.
4. Call `send_email` with the final markdown report.
5. Return the final markdown report as your response.

Important: perform all searches before writing the report. Collect every search result first."""

manager_agent = Agent(
    name="ResearchManager",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    tools=[
        planner_agent.as_tool(
            tool_name="plan_searches",
            tool_description=(
                "Plan a set of web search queries for a research topic. "
                "Input should include the query and any user clarifications."
            ),
        ),
        search_agent.as_tool(
            tool_name="web_search",
            tool_description=(
                "Search the web for a specific term and return a concise summary. "
                "Input format: 'Search term: <term>\\nReason for searching: <reason>'"
            ),
        ),
        writer_agent.as_tool(
            tool_name="write_report",
            tool_description=(
                "Write a comprehensive markdown research report from search results. "
                "Input format: 'Original query: <query>\\nSummarized search results: <results>'"
            ),
        ),
        email_agent.as_tool(
            tool_name="send_email",
            tool_description="Convert a markdown report to HTML and send it via email.",
        ),
    ],
)
