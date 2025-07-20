# 🧠 Salesforce Copilot

**Salesforce Copilot** is an AI agent assistant designed to empower sales field teams to:
- ✅ Check stock availability
- 🛒 Take and process orders
- 📇 Retrieve customer detail information
- 📦 Get product information on demand

Built as an **AI-first backend service**, it helps sales teams access business-critical data easily using natural language.

---

## ⚙️ Technical Overview

Current tech stack:
- **Python**: main programming language
- **LangChain**: framework to orchestrate LLM calls and agent logic
- **Groq**: LLM provider, currently using the model `qwen/qwen3-32b`  
- **PostgreSQL**: stores transactional data (e.g., stock, orders, customer profiles)

**Planned / in progress:**
- Vector store (e.g., FAISS / Chroma) to store embeddings for faster semantic retrieval
- REST API built with FastAPI to expose endpoints for integration with frontend or mobile app

---

## 🚀 Getting Started

### 1️⃣ Clone the repository
```bash
git clone https://github.com/yourusername/salesforce-copilot.git
cd salesforce-copilot
