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

---

## 🚀 Getting Started

### 1️⃣ Clone the repository
```bash
git clone https://github.com/yourusername/salesforce-copilot.git
cd salesforce-copilot
```

### 2️⃣ Create and activate virtual environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Linux / macOS
source venv/bin/activate
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

## 🛠️ Environment Setup
### 4️⃣ Setup environment variables
```bash
GROQ_API_KEY=your_groq_api_key_here
DATABASE_URL=postgresql://username:password@localhost:5432/salesforce_copilot
```

## 🏗️ Database Setup
### 5️⃣ Create the database
Create your DB with postgres or mysql with name: salesforce_copilot
```bash
python scripts/init_db.py
```

## ▶️ Running the Project
```bash
python app/app.py
```
