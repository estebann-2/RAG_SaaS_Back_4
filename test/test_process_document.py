import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RAG_SaaS.settings")
django.setup()

from rag_app.models import Document
from rag_app.utils import process_document

if __name__ == "__main__":
    # Fetch the latest document
    doc = Document.objects.last()
    
    if doc:
        print(f"Testing document processing: {doc.title}")
        process_document(doc)
        print("✅ Document processed successfully!")
    else:
        print("❌ No document found in the database.")
