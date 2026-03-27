from pydantic import BaseModel, Field
from agents import Agent


INSTRUCTIONS = (
    "You are a research assistant helping to clarify a user's research query. "
    "Given a query, generate exactly 3 concise clarifying questions that will help "
    "focus and improve the research. Questions should address scope, depth, audience, "
    "or specific angles the user might care about. Keep each question short and direct."
)


class ClarifyingQuestions(BaseModel):
    questions: list[str] = Field(
        description="Exactly 3 clarifying questions to better understand the research needs.",
        min_length=3,
        max_length=3,
    )


clarifying_agent = Agent(
    name="ClarifyingAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=ClarifyingQuestions,
)
