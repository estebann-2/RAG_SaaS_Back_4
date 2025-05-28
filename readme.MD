# RAG_SaaS: A Django-based Retrieval-Augmented Generation (RAG) System

## Introduction
**RAG_SaaS** is a **Django-based Retrieval-Augmented Generation (RAG) system** that allows users to **upload documents and query them** using an **LLM-powered AI assistant**. The system extracts, processes, and stores text from uploaded files, enabling **intelligent document-based queries**.

---

### Instructions to run on your own device:

Reach this URL: http://23.22.249.53:8000/

-Use the following credentials:

-User: ubuntu

-Password: ubuntu

Thank you very much!

---

## Tech Stack

- **Backend**: Django 4.2.10
- **Database**: MySQL
- **Task Queue**: Celery with Redis broker
- **AI/ML**: 
  - OpenAI Embeddings (text-embedding-3-small)
  - GPT-4 for text generation
- **File Processing**: 
  - PyMuPDF for PDF processing
  - python-docx for Word documents
  - Custom text processing utilities

---

## Prerequisites

- Python 3.11+
- MySQL 8.0+
- Redis Server
- OpenAI API key


---

## 🛠️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/estebann-2/RAG_SaaS.git
cd RAG_SaaS
```

### 2️⃣ Create a Virtual Environment & Install Dependencies

```bash
conda create -n rag_saas python=3.12.7
conda activate rag_saas
pip install -r requirements.txt
```

### 3️⃣ Apply Migrations & Create Superuser

```python
python manage.py migrate
python manage.py createsuperuser  # Follow the prompt to set up an admin user
```

### 4️⃣ Run the Development Server
```python
python manage.py runserver
```

Now, open your browser and go to:
http://127.0.0.1:8000/

---

## 🚀 Running with Docker
To deploy the app using Docker, run:

```bash
docker-compose up --build
````

```
RAG_SaaS
├─ .DS_Store
├─ Dockerfile
├─ Documentacion
│  ├─ E1-Plan de análisis de capacidad.pdf
│  ├─ Entrega 1 - G9 - Arquitectura, conclusiones y consideraciones.pdf
│  ├─ Entrega 1 - G9 - Diagrama despliegue.pdf
│  ├─ Entrega 1 - G9 - Documentación endpoints.json
│  ├─ Entrega 1 - G9 - Historias de Usuario.pdf
│  └─ Entrega 1 - G9 - Video Sustentacion.mp4
├─ RAG_SaaS
│  ├─ __init__.py
│  ├─ asgi.py
│  ├─ settings.py
│  ├─ urls.py
│  └─ wsgi.py
├─ RAG_SaaS endpoints.postman_collection.json
├─ db.sqlite3
├─ docker-compose.yaml
├─ document_processing.log
├─ dump.rdb
├─ entrega-1-DSC
├─ manage.py
├─ media
│  └─ documents
├─ rag_app
│  ├─ .DS_Store
│  ├─ __init__.py
│  ├─ admin.py
│  ├─ apps.py
│  ├─ context_processors.py
│  ├─ forms.py
│  ├─ migrations
│  │  ├─ 0001_initial.py
│  │  ├─ 0002_document_processed.py
│  │  ├─ 0003_alter_document_file.py
│  │  ├─ 0004_conversation_message_alter_document_file_and_more.py
│  │  ├─ 0005_chunk.py
│  │  └─ __init__.py
│  ├─ models.py
│  ├─ retriever.py
│  ├─ services
│  │  ├─ llm_processor.py
│  │  └─ text_summarizer.py
│  ├─ static
│  │  ├─ .DS_Store
│  │  └─ rag_app
│  │     ├─ css
│  │     │  └─ styles_v1.css
│  │     ├─ images
│  │     │  └─ uniandes.png
│  │     └─ js
│  ├─ tasks.py
│  ├─ templates
│  │  ├─ .DS_Store
│  │  └─ rag_app
│  │     ├─ .DS_Store
│  │     ├─ base.html
│  │     ├─ conversation_detail.html
│  │     ├─ conversation_history.html
│  │     ├─ login.html
│  │     ├─ query.html
│  │     ├─ start_conversation.html
│  │     └─ upload.html
│  ├─ tests.py
│  ├─ urls.py
│  ├─ utils.py
│  └─ views.py
├─ rag_app_apis
│  ├─ __init__.py
│  ├─ admin.py
│  ├─ apps.py
│  ├─ forms.py
│  ├─ migrations
│  │  ├─ 0001_initial.py
│  │  └─ __init__.py
│  ├─ models.py
│  ├─ retriever.py
│  ├─ serializers.py
│  ├─ tests.py
│  ├─ urls.py
│  ├─ utils.py
│  └─ views.py
├─ readme.MD
├─ requirements.txt
└─ test
   └─ test_process_document.py

```