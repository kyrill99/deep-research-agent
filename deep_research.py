import gradio as gr
from dotenv import load_dotenv
from research_manager import ResearchManager

load_dotenv(override=True)

# State shape: {"stage": "clarifying" | "researching", "query": str}
INITIAL_STATE = {"stage": "clarifying", "query": ""}


async def handle(message: str, history: list, state: dict):
    history = history + [{"role": "user", "content": message}]
    yield "", history, state

    if state["stage"] == "clarifying":
        questions = await ResearchManager().clarify(message)
        numbered = "\n".join(f"{i+1}. {q}" for i, q in enumerate(questions))
        response = (
            "Before I start researching, I have a few clarifying questions:\n\n"
            + numbered
            + "\n\nPlease answer them so I can tailor the research."
        )
        history = history + [{"role": "assistant", "content": response}]
        new_state = {"stage": "researching", "query": message}
        yield "", history, new_state

    else:
        query = state["query"]
        new_state = {"stage": "clarifying", "query": ""}
        accumulated = ""
        history = history + [{"role": "assistant", "content": ""}]
        async for chunk in ResearchManager().run(query, message):
            accumulated += chunk
            history[-1]["content"] = accumulated
            yield "", history, new_state


with gr.Blocks() as ui:
    gr.Markdown("# Deep Research")

    state = gr.State(INITIAL_STATE)
    chatbot = gr.Chatbot(label="Research Assistant", height=600)
    msg_input = gr.Textbox(
        label="Your message",
        placeholder="Enter a research topic to get started...",
        lines=2,
    )
    send_button = gr.Button("Send", variant="primary")

    send_button.click(
        fn=handle,
        inputs=[msg_input, chatbot, state],
        outputs=[msg_input, chatbot, state],
    )
    msg_input.submit(
        fn=handle,
        inputs=[msg_input, chatbot, state],
        outputs=[msg_input, chatbot, state],
    )

ui.launch(inbrowser=True, theme=gr.themes.Default(primary_hue="sky"))
