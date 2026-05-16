# AI Toolkit

A lightweight AI-powered toolkit with two practical tools, a Document Summarizer and an Email AI Assistant, wrapped in a clean browser interface built with Gradio.

---

## Tools

### Document Summarizer
Upload any text document and get a clean, structured summary. Handles long documents through chunking so nothing gets cut off.

### Email AI Assistant
Write professional emails with AI. Choose your tone, regenerate as many times as you want, tweak the output, and add your sign-off name before sending.

---

## Tech Stack

| Layer | Tool |
|---|---|
| Language | Python 3.13 |
| LLM API | [Groq](https://console.groq.com) (free tier) |
| Model | `llama-3.3-70b-versatile` |
| UI | Gradio |

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/bytesentinal/AI-Toolkit-Saas-Product.git
cd ai-toolkit
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set your Groq API key

Get a free key at [console.groq.com](https://console.groq.com), then create a `.env` file in the root of the project:

```
GROQ_API_KEY=your_key_here
```

> `.env` is listed in `.gitignore`so your key will never be pushed to GitHub.

### 4. Run the app

```bash
python app.py
```

Open your browser at `http://localhost:7860` and you're good to go.

---

## Project Structure

```
ai-toolkit/
├── app.py               # Main app — Document Summarizer + Email Assistant (Gradio UI)
├── requirements.txt     # Python dependencies
├── .env                 # Your API key (never commit this)
├── LICENSE
└── .gitignore
```

---

## Use Cases

- Summarize long contracts, reports, or research papers in seconds
- Draft client emails, follow-ups, or cold outreach with the right tone
- Automate repetitive writing tasks for your business or freelance work

---

## License

MIT: free to use, modify, and build on.
