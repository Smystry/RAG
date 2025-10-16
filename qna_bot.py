"""
qna_bot.py
------------------------------------
Retrieval-Augmented Q&A bot using:
- Elasticsearch for context retrieval
- Gemini (Google Generative AI) for response generation
"""

from elasticsearch import Elasticsearch
import google.generativeai as genai
import os

# Configure Gemini API key (ensure GEMINI_API_KEY is set in your environment or .envrc)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize Elasticsearch
es = Elasticsearch("http://localhost:9200")


# ---------------------------
# Retrieve relevant FAQ documents
# ---------------------------
def retrieve_documents(query, index_name="course-questions", max_results=5):
    """Search the Elasticsearch index for relevant context documents."""
    search_query = {
        "size": max_results,
        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": query,
                        "fields": ["question^3", "text", "section"],
                        "type": "best_fields"
                    }
                },
                "filter": {
                    "term": {"course": "data-engineering-zoomcamp"}
                }
            }
        }
    }

    response = es.search(index=index_name, body=search_query)
    documents = [hit["_source"] for hit in response["hits"]["hits"]]
    return documents


# ---------------------------
# Templates
# ---------------------------
context_template = """
Section: {section}
Question: {question}
Answer: {text}
""".strip()

prompt_template = """
You're a course teaching assistant.
Answer the user QUESTION based on CONTEXT — the documents retrieved from our FAQ database.
Don't use any external knowledge. If the CONTEXT doesn't contain the answer, return "NONE".

QUESTION:
{user_question}

CONTEXT:
{context}
""".strip()


# ---------------------------
# Build context and prompt
# ---------------------------
def build_context(documents):
    """Concatenate retrieved documents into a readable context string."""
    context_result = ""
    for doc in documents:
        doc_str = context_template.format(**doc)
        context_result += "\n\n" + doc_str
    return context_result.strip()


def build_prompt(user_question, documents):
    """Inject context and question into the main RAG prompt."""
    context = build_context(documents)
    prompt = prompt_template.format(
        user_question=user_question,
        context=context
    )
    return prompt


# ---------------------------
# Generate answer from Gemini
# ---------------------------
def ask_gemini(prompt, model="gemini-2.5-flash"):
    """Call Gemini model to generate content."""
    model = genai.GenerativeModel(f"models/{model}")
    response = model.generate_content(prompt)
    return response.text


# ---------------------------
# Main QA bot function
# ---------------------------
def qa_bot(user_question):
    """
    Main entry point for Q&A.
    1. Retrieve documents from Elasticsearch.
    2. Build prompt with retrieved context.
    3. Query Gemini for the answer.
    """
    try:
        context_docs = retrieve_documents(user_question)
        prompt = build_prompt(user_question, context_docs)
        answer = ask_gemini(prompt)
        return answer
    except Exception as e:
        return f"Error in qa_bot: {e}"
