# LLM Projects Portfolio

A collection of **production-style applications** that demonstrate end-to-end use of Large Language Models (LLMs), from web scraping and multi-model orchestration to agentic tools, speech processing, and synthetic data generation. Built with Python, Jupyter, and both frontier APIs (OpenAI, Anthropic, Google) and open-source models (Hugging Face, Ollama).

---

## Overview

This repository showcases practical LLM engineering: building real workflows that combine **APIs, databases, web automation, and multimodal outputs** (text, image, audio). Projects range from local/Ollama-based scrapers to cloud-ready notebooks using Gradio UIs, SQLite, and streaming responses—suitable for demos, learning, or extending into production pipelines.

---

## Tech Stack

| Category           | Technologies                                                        |
| ------------------ | ------------------------------------------------------------------- |
| **LLM APIs**       | OpenAI, Anthropic (Claude), Google (Gemini), Ollama (local)         |
| **Open-source ML** | Hugging Face (Transformers, pipelines), BitsAndBytes (quantization) |
| **Web & Data**     | Selenium, BeautifulSoup, SQLite, Pandas, JSON/JSONL                 |
| **UI & Demo**      | Gradio (chat, audio, image, file upload)                            |
| **Environment**    | Python, Jupyter, `python-dotenv`, Google Colab–compatible notebooks |

---

## Projects

### 1. Sports Website Scraper Aggregator

**`1 - WebScraper/`**

Scrapes sports websites (including JavaScript-rendered content) and uses an **Ollama-based LLM** to aggregate and summarize the content into a single, readable view.

- **Highlights:** Headless Chrome (Selenium), BeautifulSoup, local LLM via Ollama, no API key required for core flow.
- **Use case:** Automated sports news aggregation and summarization.

---

### 2. Brochure Builder

**`2 - BrochureBuilder/`**

Takes a **company website URL** and produces a concise, professional summary suitable for clients, investors, or recruits. Uses multiple LLM steps: link relevance filtering (one-shot prompting), content extraction, and streaming brochure generation.

- **Highlights:** Selenium scraper (with shared `scraper.py`), multi-call LLM pipeline, JSON-structured outputs, streaming responses, optional Gradio UI.
- **Use case:** Quick company overviews from any URL.

---

### 3. Multi-Model Chat: Group Vacation Planner

**`3 - ChatBotConversation/`**

A **three-way conversation** between different frontier models (e.g., OpenAI, Anthropic, Gemini) simulating friends planning a group vacation. Illustrates conversation history as a single sequence of API calls and compares model “personalities” and behavior.

- **Highlights:** Multi-provider clients, shared conversation state, long-context message history.
- **Use case:** Multi-agent dialogue patterns and model comparison.

---

### 4. Event Booking Agent

**`4 - EventBookingAgent/`**

An **agentic chatbot** that helps users find and book events. It uses **tool calling** (e.g., query price, date, city, capacity, book event) against a **SQLite** backend, handles **nested tool calls**, and after a booking generates a **custom image** (OpenAI Image API) and **audio** (OpenAI TTS) as a thank-you.

- **Highlights:** Function/tool definitions, SQLite for events, nested tool-call handling, image + audio generation, Gradio chat + image + audio UI.
- **Use case:** Agent design, RAG-free tool use, and multimodal rewards.

---

### 5. Speech-to-Text Summarization

**`5 - SpeechToText/`**

**Speech → text** (OpenAI Whisper-style API) then **summarization** with a Hugging Face open-source model. Includes tokenization, quantization for lower GPU memory, and a Gradio interface with file upload.

- **Highlights:** OpenAI speech-to-text, Hugging Face pipelines, quantization, Gradio audio upload.
- **Use case:** Voice memos or meeting notes → transcript + summary (runnable on Colab with GPU).

---

### 6. Synthetic Data Generator

**`6 - SyntheticDataGenerator/`**

Generates **business-style datasets** using a mix of Hugging Face open-source models and optional frontier models. Users can supply a sample schema; the app produces structured data (e.g., JSONL), with Pandas for preview and analysis, and supports multiple output formats.

- **Highlights:** Quantization, tokenizer + model parsing for assistant-only output, JSONL, Pandas, error handling, Gradio blocks with multiple inputs/outputs.
- **Use case:** Synthetic training data, demos, or schema-driven data generation (Colab-friendly).

---

### 7. Code Translator

**`6 - CodeTranslator/`**

Generates **optimized code** in a different language using frontier and open source models. So users can compare speeds and select the most efficient and cost effective model for their needs. Reads the users system spec and provides the compile
and run command specialized for their machine.

- **Highlights:** System spec reading, code generation, model comparison.
- **Use case:** Code optimization, interpreted language to compiled language, in app code execution.

---

## Repository Structure

```
LLM-Projects/
├── 1 - WebScraper/          # Sports scraper + Ollama summarization
├── 2 - BrochureBuilder/     # URL → company brochure (scraper + multi-LLM)
├── 3 - ChatBotConversation/ # Multi-model vacation planning chat
├── 4 - EventBookingAgent/   # Tool-using agent + SQLite + image/audio
├── 5 - SpeechToText/        # Transcribe + summarize with HF + OpenAI
├── 6 - SyntheticDataGenerator/ # Schema-aware synthetic data + Gradio
├── 7 - CodeTranslator/ # System spec reader + code optimization + Gradio
└── README.md
```

Each project is self-contained in its folder, typically with a Jupyter notebook (`.ipynb`) and, where needed, a `.env.example` or `.env` for API keys (OpenAI, Anthropic, Google, Hugging Face as required).

---

## Getting Started

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/LLM-Projects.git
   cd LLM-Projects
   ```

2. **Per-project setup**
   - Open the notebook for the project you want to run (e.g., `4 - EventBookingAgent/eventBookingAgent.ipynb`).
   - Install dependencies used in the notebook (e.g., `openai`, `gradio`, `selenium`, `transformers`, etc.). Some notebooks include `!pip install` cells for Colab.
   - For API-based projects, add a `.env` in that project folder with the needed keys (e.g. `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, `HF_TOKEN`). Do not commit `.env` files.

3. **Run**
   - Execute the notebook cells in order. Several projects expose a Gradio UI at the end; the notebook will print the local or public URL.

**Note:** Projects 1 and 2 can use **Ollama** locally with no API key. Others typically require at least an OpenAI key; Speech-to-Text and Synthetic Data Generator are designed to run on **Google Colab** with GPU for heavier models.

---

## Skills Demonstrated

- **LLM integration:** Chat completions, tool/function calling, streaming, multi-model orchestration.
- **Agent design:** Tool definitions, nested tool handling, stateful conversation with tools and databases.
- **Multimodal outputs:** Text, image generation, text-to-speech, and UIs that display them.
- **Data and infra:** SQLite, Pandas, JSON/JSONL, structured prompts (e.g., JSON output).
- **Web automation:** Selenium, BeautifulSoup, headless Chrome for JS-heavy sites.
- **Efficiency:** Quantization (e.g., 4-bit) for running open-source models on limited hardware.
- **UX:** Gradio interfaces for chat, audio, image, and file uploads.

---

## License

This repository is for portfolio and educational use. Respect each provider’s API terms (OpenAI, Anthropic, Google, Hugging Face) and do not commit API keys or secrets.
