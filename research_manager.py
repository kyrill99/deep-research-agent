from agents import Runner, trace, gen_trace_id
from clarifying_agent import clarifying_agent, ClarifyingQuestions
from manager_agent import manager_agent


class ResearchManager:

    async def clarify(self, query: str) -> list[str]:
        """Generate 3 clarifying questions for the given query."""
        result = await Runner.run(clarifying_agent, f"Query: {query}")
        return result.final_output_as(ClarifyingQuestions).questions

    async def run(self, query: str, clarifications: str = ""):
        """Run the deep research process via the manager agent, yielding status updates."""
        trace_id = gen_trace_id()
        with trace("Research trace", trace_id=trace_id):
            print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}")
            yield f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}\n\n"

            input_text = f"Query: {query}"
            if clarifications:
                input_text += f"\nClarifications: {clarifications}"

            result = Runner.run_streamed(manager_agent, input_text)
            async for event in result.stream_events():
                if event.type == "run_item_stream_event":
                    item = event.item
                    if item.type == "tool_call_item":
                        tool_name = getattr(item.raw_item, "name", "tool")
                        yield f"**Agent calling:** `{tool_name}`...\n\n"

            yield result.final_output
