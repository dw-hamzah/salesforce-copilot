import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq 


# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def ask_product_info(question: str) -> str:
    # Load embeddings & vector store
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.load_local("rag/faiss_index", embeddings, allow_dangerous_deserialization=True)

    # Retrieve top 4 relevant chunks
    retriever = db.as_retriever(search_kwargs={"k": 4})
    docs = retriever.get_relevant_documents(question)

    # Combine text as context
    context = "\n".join(doc.page_content for doc in docs)

    # Initialize LLM
    llm = ChatGroq(api_key=GROQ_API_KEY, model_name="qwen/qwen3-32b")

    # Create prompt
    prompt = PromptTemplate.from_template(
        "You are a helpful AI assistant. Use the following product documents to answer the question.\n\n"
        "Context:\n{context}\n\n"
        "Question: {question}\n"
        "Answer:"
    )
    final_prompt = prompt.format(context=context, question=question)

    # Ask LLM
    answer = llm.invoke(final_prompt)

    return answer.content

if __name__ == "__main__":
    question = input("❓ Enter your question about product or safety info: ")
    answer = ask_product_info(question)
    print(f"\n✅ Answer: {answer}")