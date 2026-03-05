import gradio as gr
from dotenv import load_dotenv

from rag_implementation.answer import answer_question
from knowledge_base.generate import create_knowledge_base_files
from evaluation.evaluator import main as evaluator

load_dotenv(override=True)

def format_context(context):
    result = "<h2 style='color: #ff7800;'>Relevant Context</h2>\n\n"
    for doc in context:
        result += f"<span style='color: #ff7800;'>Source: {doc.metadata['source']}</span>\n\n"
        result += doc.page_content + "\n\n"
    return result

def chat(history):
    last_message = history[-1]["content"]
    prior_history = history[:-1]
    answer, context = answer_question(last_message, prior_history)
    history.append({"role": "assistant", "content": answer})
    return history, format_context(context)

def main():
    def put_message_in_chatbot(message, history):
        return "", history + [{"role": "user", "content": message}]

    theme = gr.themes.Soft(font=["Inter", "system-ui", "sans-serif"])

    with gr.Blocks(title=" Expert Assistant", theme=theme) as ui:

        with gr.Row(): 
            with gr.Column():
                gr.Markdown("# Generate sample knowledge base for your company if one doesnt exists")
                company_description = gr.Textbox(
                    label = "Company description",
                    placeholder= "Your company description include mission, employee roles, products and culture"
                )
                generate_knowledgebase = gr.Button("Generate Knowledge Base")

            generate_knowledgebase.click(fn=create_knowledge_base_files, inputs=[company_description])

        gr.Markdown("# 🏢 Expert Assistant\nAsk me anything about your company!")

        with gr.Row():
            with gr.Column(scale=1):
                chatbot = gr.Chatbot(
                    label="💬 Conversation", height=600, type="messages", show_copy_button=True
                )
                message = gr.Textbox(
                    label="Your Question",
                    placeholder="Ask anything about your company...",
                    show_label=False,
                )

            with gr.Column(scale=1):
                context_markdown = gr.Markdown(
                    label="📚 Retrieved Context",
                    value="*Retrieved context will appear here*",
                    container=True,
                    height=600,
                )

        message.submit(
            put_message_in_chatbot, inputs=[message, chatbot], outputs=[message, chatbot]
        ).then(chat, inputs=chatbot, outputs=[chatbot, context_markdown])

        with gr.Row():
            rag_evaluation = gr.Button("Evaluate RAG Retrieval and Answers")
            rag_evaluation.click(fn=evaluator)
    ui.launch(inbrowser=True)


if __name__ == "__main__":
    main()