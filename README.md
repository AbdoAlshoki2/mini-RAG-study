# mini-RAG-study

This is an educational project to study the RAG (Retrieval Augmented Generation) 

## Requirements

- Python 3.8 or later

### Installation
1) download and install miniconda from [here](https://www.anaconda.com/docs/getting-started/miniconda/install)
2) create a conda environment with python 3.8 using this command:
```bash
conda create -n rag python=3.8
```
3) activate the environment:
```bash
conda activate rag
```
### (Optional) Setup you command line interface for better readability

```bash
export PS1="\[\033[01;32m\]\u@\h:\w\n\[\033[00m\]\$ "
```

## Installation

### Install the required packages

```bash
$ pip install -r requirements.txt
```

### Setup the environment variables

```bash
$ cp .env .env.example
```

This project uses a `.env` file to store the environment variables. You can copy the `.env.example` file to `.env` and set your environment variables.

## Run the FastAPI server

```bash
$ uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

## POSTMAN Collection

Download the POSTMAN collection from [/assets/mini-rag.postman_collection.json](/assets/mini-rag.postman_collection.json)