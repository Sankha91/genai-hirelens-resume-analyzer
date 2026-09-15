# genai-hirelens-resume-analyzer

🚀 **Built a GenAI-powered Resume Analyzer — HireLens**

As part of my ongoing **GenAI learning journey**, I’ve been building a project to understand how LLMs, RAG, vector databases, prompt engineering, and traditional databases can work together to solve a practical problem.

### 💡 The idea

HR can upload multiple **resumes** along with their respective **Job Descriptions (JDs)**.

HireLens then analyzes each resume against the selected JD and provides insights that can help HR during the initial screening process.

### 🔍 What does it provide?

For each resume, the system generates:

✅ Resume–JD matching score
✅ Matched skills
✅ Missing skills
✅ Strengths
✅ Weaknesses
✅ Recommendations
✅ Skill gap analysis
✅ Randomized interview questions

This gives recruiters more context to decide which candidates should move forward to the interview stage.

### 🔄 Re-analyze feature

One interesting feature I implemented is **Re-analyze Resume**.

The same resume can be analyzed again against a different JD, allowing the system to evaluate the candidate from a completely different job perspective.

### 🛠️ Tech Stack

* 🐍 **Python**
* 🎨 **Streamlit** — UI
* 🤖 **Google Gemini** — LLM
* 🧠 **ChromaDB** — Vector database / semantic search
* 🗄️ **SQLite** — Structured data storage

### ⚙️ Some interesting implementation decisions

While building the project, I experimented with several techniques beyond simply calling an LLM API.

🔹 **Prompt optimization**
Several internal prompt optimization techniques are being used to reduce unnecessary token consumption while maintaining useful outputs.

🔹 **Hybrid database architecture**
SQLite is used for structured filtering and initial candidate selection before querying the vector database for semantic matching.

This helps avoid blindly sending every resume into the vector search pipeline.

🔹 **RAG-based matching**
ChromaDB is used to support semantic similarity and retrieve relevant resume information during the matching process.

### 🚧 What's next?

The next major addition I'm exploring is an **AI Agent** that can interact with recruiters through chat.

Instead of navigating through multiple screens, HR could ask questions such as:

> "Show me the top candidates for this JD."

> "Which candidates are missing Kotlin and Jetpack Compose?"

> "Why did this candidate receive a 78% match?"

> "Generate interview questions for this candidate."

The goal is to make the system more **agentic and conversational**.

This project has been a great hands-on way for me to explore **GenAI, RAG, vector databases, prompt engineering, LLM applications, and AI agents** by building something practical rather than learning the concepts in isolation.

I'm still exploring and learning. **Any suggestions, feedback, or ideas that could improve the project or my GenAI learning path would be highly appreciated.** 🙌

