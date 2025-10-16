# RAG Q&A Bot
An end-to-end Retrieval-Augmented Generation (RAG) app that answers course-related questions by retrieving relevant content from an Elasticsearch index and generating grounded responses using Google Gemini 2.5 Flash.

## Features

- **RAG-based Question Answering** – retrieves context from indexed FAQ documents.  
- **Gemini AI Integration** – uses Google’s latest Gemini 2.5 Flash model for accurate, grounded responses.  
- **Elasticsearch Backend** – stores and semantically searches contextual data.  
- **Streamlit Interface** – simple, user-friendly chat UI.  
- **Environment Management** – reproducible Pipenv + direnv setup for clean isolation.  
- **Extensible Design** – easily swap Gemini with OpenAI or Groq APIs.

## Tech Stack

| Layer | Technology | Description |
|-------|-------------|-------------|
| **Language** | Python 3.12 | Core language for RAG pipeline and UI |
| **LLM API** | Gemini 2.5 Flash | Used for natural language generation |
| **Database** | Elasticsearch 8.4 | For indexing and retrieving documents |
| **Frontend** | Streamlit | Web-based chat interface |
| **Env Management** | Pipenv + direnv | Manages dependencies and environment variables |
| **Containerization** | Docker | Runs Elasticsearch locally in isolation |

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/RAG.git
cd RAG
```
### 2. Install Dependencies
Install all required Python packages using Pipenv:
```bash
pipenv install
pipenv shell
```
### 3. Configure Environment Variables
Create a file named .envrc in your project root and add your Gemini API key:
```bash
export GEMINI_API_KEY="your_gemini_api_key_here"
```
Activate it using direnv:
```bash
direnv allow
```
Verify that your key is active:
```bash
echo $GEMINI_API_KEY
```
### 4. Run Elasticsearch (via Docker)
```bash
docker run -it --rm \
  --name elasticsearch \
  -m 2G \
  -p 9200:9200 \
  -p 9300:9300 \
  -e "discovery.type=single-node" \
  -e "xpack.security.enabled=false" \
  docker.elastic.co/elasticsearch/elasticsearch:8.4.3
```
Test that Elasticsearch is running:
```bash
curl http://localhost:9200
```
### 5. Run the App
launch the Streamlit interface
```bash
streamlit run app.py
```

### Project Structure
```graphql
RAG/
│
├── app.py              # Streamlit interface
├── qna_bot.py          # Core RAG pipeline (retrieval + generation)
├── documents.json      # Sample FAQ dataset
├── Pipfile             # Pipenv dependencies
├── Pipfile.lock
├── .gitignore
├── .envrc              # Holds your API key (ignored by Git)
└── README.md
```
### Architecture Overview
```text
┌────────────┐      ┌──────────────────┐      ┌────────────────┐      ┌────────────────────┐
│   User     │ ---> │   Streamlit UI   │ ---> │ Elasticsearch  │ ---> │   Gemini API (LLM) │
└────────────┘      └──────────────────┘      └────────────────┘      └────────────────────┘
        │                    │                          │                        │
        └────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                           Contextual Answer
```


