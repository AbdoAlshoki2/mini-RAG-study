# Mini-RAG Study

An educational project implementing a basic RAG (Retrieval-Augmented Generation) system using FastAPI, MongoDB, and LLM providers.

## Features

- Document upload and processing (text and PDF files)
- Text chunking with configurable size and overlap
- Integration with OpenAI and Cohere for embeddings
- MongoDB for document and vector storage
- RESTful API for document management

## Prerequisites

- Python 3.8 or later
- Docker and Docker Compose
- MongoDB (can be run via Docker)
- API keys for OpenAI and/or Cohere

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/mini-rag.git
   cd mini-rag
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```
   
   Or using conda:
   ```bash
   conda create -n rag python=3.8
   conda activate rag
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   ```bash
   cp .env.example .env
   ```
   
   Edit the `.env` file with your API keys and settings:
   ```
   # Required API keys
   OPENAI_API_KEY=your_openai_api_key
   COHERE_API_KEY=your_cohere_api_key
   
   # MongoDB configuration
   MONGODB_URL=mongodb://localhost:27017
   MONGODB_DATABASE=mini-rag
   
   # File handling
   FILE_ALLOWED_TYPES=["text/plain","application/pdf"]
   FILE_MAX_SIZE=10  # MB
   ```

## Running the Application

1. Start MongoDB using Docker:
   ```bash
   cd docker
   docker compose up -d
   ```

2. Run the FastAPI server:
   ```bash
   cd src
   uvicorn main:app --reload --host 0.0.0.0 --port 5000
   ```

3. Access the API documentation:
   - Swagger UI: http://localhost:5000/docs
   - ReDoc: http://localhost:5000/redoc

## API Endpoints

### 1. Upload Document
- **POST** `/api/v1/data/upload/{project_id}`
  - Upload a text or PDF document for processing
  - Required: `file` (form-data)
  - Returns: File ID for reference

### 2. Process Document
- **POST** `/api/v1/data/process/{project_id}`
  - Process uploaded document into chunks
  - Parameters:
    - `file_id`: ID of the uploaded file
    - `chunk_size`: Size of each text chunk (default: 100)
    - `overlap_size`: Overlap between chunks (default: 20)
    - `do_reset`: Whether to reset existing chunks (default: 0)

## Project Structure

```
src/
├── controllers/        # Business logic and request handlers
│   ├── BaseController.py
│   ├── DataController.py
│   ├── ProcessController.py
│   └── ProjectController.py
├── models/            # Data models and database schemas
├── routes/            # API route definitions
│   ├── base.py
│   └── data.py
├── stores/            # External service integrations
│   └── llm/           # LLM provider implementations
│   └── vectordb/      # Vector database provider implementations
└── helpers/           # Utility functions
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MONGODB_URL` | MongoDB connection URL | `mongodb://localhost:27017` |
| `MONGODB_DATABASE` | Database name | `mini-rag` |
| `FILE_ALLOWED_TYPES` | Allowed file types | `["text/plain","application/pdf"]` |
| `FILE_MAX_SIZE` | Maximum file size in MB | `10` |
| `OPENAI_API_KEY` | OpenAI API key | - |
| `COHERE_API_KEY` | Cohere API key | - |
| `VECTOR_DB_PATH` | Vector database path | `vector_db` |
| `VECTOR_DB_DISTANCE_METHOD` | Vector database distance method | `cosine` |
| `VECTOR_DB_PROVIDER` | Vector database provider | `qdrant` |


