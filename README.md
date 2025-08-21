# Mini-RAG Learning Project

This repository documents my journey of learning how to build a deployment-level project from scratch. It's an educational endeavor to understand the components of a Retrieval-Augmented Generation (RAG) system while honing essential software development skills.

## My Learning Journey

This project is inspired by the incredible YouTube playlist by Abu Bark Soliman:

[**Build a RAG from Scratch**](https://www.youtube.com/playlist?list=PLvLvlVqNQGHCUR2p0b8a0QpVjDUg50wQj)

Following this playlist has been a fantastic learning experience, covering not just the technical implementation of RAG, but also crucial software engineering practices like:

- **Design Patterns**: MVC (Model-View-Controller), Factory Provider
- **Code Organization**: Structuring a project for scalability and maintainability
- **Clean Coding Practices**: Writing readable and efficient code

> **Disclaimer**: This project is unfinished and is intended for learning purposes only. It is not production-ready.

## Codebase Architecture

The project follows a modular architecture, separating concerns to make the codebase clean and scalable.

```
src/
├── main.py             # FastAPI application entry point
|
├── routes/             # API route definitions (the "View" in MVC)
│   ├── base.py
│   ├── data.py
│   └── nlp.py
|
├── controllers/        # Business logic and request handlers (the "Controller" in MVC)
│   ├── BaseController.py
│   ├── DataController.py
│   ├── NLPController.py
│   ├── ProcessController.py
│   └── ProjectController.py
|
├── models/             # Data models and database schemas (the "Model" in MVC)
│   ├── AssetModel.py
│   ├── ChunkModel.py
│   └── ProjectModel.py
|
├── stores/             # External service integrations (Factory Providers)
│   ├── llm/            # LLM provider implementations (OpenAI, Cohere)
│   └── vectordb/       # Vector database provider implementations (Qdrant)
|
└── helpers/            # Utility functions and configuration
    └── config.py
```

## Features

- Document upload and processing (text and PDF files)
- Text chunking with configurable size and overlap
- Integration with OpenAI and Cohere for embeddings using a factory provider pattern
- MongoDB for document and vector storage
- RESTful API built with FastAPI

## Prerequisites

- Python 3.8 or later
- Docker and Docker Compose
- API keys for OpenAI and/or Cohere

## Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/AbdoAlshoki2/mini-RAG-study.git
    cd mini-RAG-study
    ```

2.  **Set up a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: .\venv\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure environment variables**:

    Copy the example `.env` file:
    ```bash
    cp .env.example .env
    ```

    Then, edit the `.env` file with your API keys and settings.

## Running the Application

1.  **Start MongoDB with Docker**:
    ```bash
    cd docker
    docker-compose up -d
    ```

2.  **Run the FastAPI server**:
    ```bash
    cd src
    uvicorn main:app --reload --host 0.0.0.0 --port 5000
    ```

3.  **Access the API documentation**:
    -   **Swagger UI**: [http://localhost:5000/docs](http://localhost:5000/docs)
    -   **ReDoc**: [http://localhost:5000/redoc](http://localhost:5000/redoc)

## API Endpoints

### Base
- **GET** `/api/v1/`: Welcome endpoint that returns the application name and version

### Data Management

- **POST** `/api/v1/data/upload/{project_id}`
  - Upload a text or PDF document for processing
  - **Parameters**:
    - `project_id` (path): Project identifier
    - `file` (form-data): The file to upload
  - **Returns**: File ID for reference

- **POST** `/api/v1/data/process/{project_id}`
  - Process uploaded documents into chunks
  - **Parameters**:
    - `project_id` (path): Project identifier
    - `chunk_size` (query): Size of each text chunk (default: 100)
    - `overlap_size` (query): Overlap between chunks (default: 20)
    - `do_reset` (query): Whether to reset existing chunks (default: false)
    - `file_id` (query, optional): Specific file ID to process (processes all files if not provided)

### NLP Operations

- **POST** `/api/v1/nlp/index/push/{project_id}`
  - Index project documents into the vector database
  - **Parameters**:
    - `project_id` (path): Project identifier
    - `do_reset` (body): Whether to reset existing index (default: false)

- **GET** `/api/v1/nlp/index/info/{project_id}`
  - Get information about the project's vector index
  - **Parameters**:
    - `project_id` (path): Project identifier

- **POST** `/api/v1/nlp/search/{project_id}`
  - Search the vector database for relevant chunks
  - **Parameters**:
    - `project_id` (path): Project identifier
    - `query` (body): Search query
    - `top_k` (body, optional): Number of results to return (default: 5)

- **POST** `/api/v1/nlp/answer/{project_id}`
  - Get an answer from the RAG system
  - **Parameters**:
    - `project_id` (path): Project identifier
    - `query` (body): Question to answer
    - `top_k` (body, optional): Number of context chunks to use (default: 5)


