import gradio as gr
from groq import Groq
from dotenv import load_dotenv
import os

# ── LOAD ENV ─────────────────────────────
load_dotenv()

# ── GROQ CLIENT ───────────────────────────
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# ── SYSTEM PROMPTS ────────────────────────────────────
EMAIL_SYSTEM = """You are an expert email writer for busy professionals and small businesses.

When given an email and instructions, you write a clear, ready-to-send reply.

Rules:
- Never add placeholders like [Your Name]
- Match the tone requested exactly
- Keep replies concise unless told otherwise
- Always sound human, never robotic
- End with a clean sign-off
"""

SUMMARY_SYSTEM = """You are a professional document summarizer.

Extract the most important information clearly and concisely.

Rules:
- Use bullet points for key facts
- Keep summaries tight
- Preserve important names, numbers, and decisions
"""

# ── EMAIL FUNCTION ────────────────────────────────────
def generate_email_reply(email, instruction, tone, your_name):

    if not email.strip():
        return "⚠️ Please paste an email."

    if not instruction.strip():
        return "⚠️ Please enter instructions."

    prompt = f"""
Incoming email:
\"\"\"{email}\"\"\"

My instruction:
{instruction}

Tone:
{tone}

Sign off as:
{your_name if your_name.strip() else "Me"}

Write a reply I can send immediately.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": EMAIL_SYSTEM
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content

# ── TEXT CHUNKING ─────────────────────────────────────
def chunk_text(text, max_chars=3000):

    chunks = []

    while len(text) > max_chars:

        split_at = text.rfind(" ", 0, max_chars)

        if split_at == -1:
            split_at = max_chars

        chunks.append(text[:split_at])

        text = text[split_at:].strip()

    chunks.append(text)

    return chunks

# ── DOCUMENT SUMMARIZER ───────────────────────────────
def summarize_document(text):

    if not text.strip():
        return "⚠️ Please paste some text."

    chunks = chunk_text(text)

    summaries = []

    for chunk in chunks:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": SUMMARY_SYSTEM
                },
                {
                    "role": "user",
                    "content": f"Summarize this:\n\n{chunk}"
                }
            ]
        )

        summaries.append(
            response.choices[0].message.content
        )

    # Merge summaries if multiple chunks
    if len(summaries) > 1:

        merged_text = "\n\n".join(summaries)

        final_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": SUMMARY_SYSTEM
                },
                {
                    "role": "user",
                    "content": f"Merge these summaries into one clean final summary:\n\n{merged_text}"
                }
            ]
        )

        return final_response.choices[0].message.content

    return summaries[0]

# ── CUSTOM CSS ────────────────────────────────────────
custom_css = """
body {
    background: linear-gradient(135deg, #0f172a, #111827);
}

.gradio-container {
    max-width: 1450px !important;
    margin: auto;
    padding-top: 20px;
    font-family: 'Inter', sans-serif;
}

.main-title {
    text-align: center;
    margin-bottom: 25px;
    animation: fadeIn 1s ease;
}

.main-title h1 {
    font-size: 3.2rem;
    font-weight: 800;
    background: linear-gradient(to right, #60a5fa, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.main-title p {
    color: #cbd5e1;
    font-size: 1.1rem;
    margin-top: -8px;
}

.card {
    background: rgba(17, 24, 39, 0.78);
    backdrop-filter: blur(16px);
    border-radius: 26px;
    padding: 24px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 10px 40px rgba(0,0,0,0.28);
    transition: all 0.3s ease;
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 16px 45px rgba(0,0,0,0.4);
}

textarea,
input {
    border-radius: 16px !important;
}

button {
    border-radius: 16px !important;
    font-weight: 700 !important;
    transition: all 0.25s ease !important;
}

button:hover {
    transform: scale(1.02);
}

footer {
    visibility: hidden;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(12px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}
"""

# ── UI ────────────────────────────────────────────────
with gr.Blocks(
    title="AI Toolkit"
) as app:

    gr.HTML("""
    <div class="main-title">
        <h1>🤖 AI Toolkit</h1>
        <p>Professional AI utilities powered by Groq + LLaMA 3.3 70B</p>
    </div>
    """)

    with gr.Tabs():

        # ── EMAIL ASSISTANT TAB ────────────────────
        with gr.Tab("📧 Email Assistant"):

            with gr.Row():

                # LEFT PANEL
                with gr.Column(scale=1):

                    with gr.Group(elem_classes="card"):

                        gr.Markdown("## Generate Smart Email Replies")

                        email_input = gr.Textbox(
                            label="Incoming Email",
                            placeholder="Paste the email here...",
                            lines=10
                        )

                        instruction_input = gr.Textbox(
                            label="Instruction",
                            placeholder="e.g. decline politely, confirm meeting..."
                        )

                        tone_input = gr.Radio(
                            choices=[
                                "Professional & Formal",
                                "Friendly & Conversational",
                                "Assertive & Direct",
                                "Apologetic & Empathetic"
                            ],
                            label="Tone",
                            value="Professional & Formal"
                        )

                        name_input = gr.Textbox(
                            label="Your Name",
                            placeholder="Shahmeer"
                        )

                        email_btn = gr.Button(
                            "Generate Reply",
                            variant="primary"
                        )

                # RIGHT PANEL
                with gr.Column(scale=1):

                    with gr.Group(elem_classes="card"):

                        gr.Markdown("## Generated Reply")

                        email_output = gr.Textbox(
                            label="Ready-to-Send Email",
                            lines=18
                        )

        email_btn.click(
            fn=generate_email_reply,
            inputs=[
                email_input,
                instruction_input,
                tone_input,
                name_input
            ],
            outputs=email_output
        )

        # ── DOCUMENT SUMMARIZER TAB ────────────────
        with gr.Tab("📄 Document Summarizer"):

            with gr.Row():

                # LEFT PANEL
                with gr.Column(scale=1):

                    with gr.Group(elem_classes="card"):

                        gr.Markdown("## Smart Document Summarizer")

                        doc_input = gr.Textbox(
                            label="Paste Your Document",
                            placeholder="Paste articles, notes, reports, or long text here...",
                            lines=18
                        )

                        summary_btn = gr.Button(
                            "Summarize Document",
                            variant="primary"
                        )

                # RIGHT PANEL
                with gr.Column(scale=1):

                    with gr.Group(elem_classes="card"):

                        gr.Markdown("## AI Summary")

                        summary_output = gr.Textbox(
                            label="Summary Output",
                            lines=18
                        )

        summary_btn.click(
            fn=summarize_document,
            inputs=doc_input,
            outputs=summary_output
        )

# ── LAUNCH APP ───────────────────────────────────────
app.launch(
    css=custom_css,
    theme=gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="violet",
        neutral_hue="slate"
    )
)