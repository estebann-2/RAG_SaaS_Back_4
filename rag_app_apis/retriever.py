from langchain.vectorstores import Chroma
from .models import APIChunk, APIDocument
import numpy as np
from .utils import embedding_model
import logging

def retrieve_relevant_chunks(query, conversation,top_k=3):
    """Retrieves the most relevant document chunks using embeddings."""

    # Obtener el documento asociado a la conversación
    document = APIDocument.objects.filter(conversation=conversation).first()
    
    if not document:
        logging.warning(f"⚠️ No se encontró un documento asociado a la conversación {conversation.id}.")
        return []
    
    logging.info(f"Recuperando chunks de: {document.title}")

    print(f"Recuperando chunks de: {document.title}")

    # Obtener solo los chunks del documento correcto
    document_chunks = APIChunk.objects.filter(document=document)

    print(document_chunks)

    # Si no hay chunks en la base de datos para este documento
    if not document_chunks.exists():
        logging.warning(f"No se encontraron chunks para el documento {document.title}.")
        return []

    # Generar embedding de la consulta
    query_embedding = embedding_model.embed_documents([query])[0]

    # Compute similarity scores
    def cosine_similarity(a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    scored_chunks = [
        (chunk, cosine_similarity(query_embedding, chunk.embedding))
        for chunk in document_chunks
    ]


    # Sort by similarity and return top_k chunks
    scored_chunks.sort(key=lambda x: x[1], reverse=True)
    top_chunks = scored_chunks[:top_k]

    # Log and return the selected chunks with metadata
    for chunk, score in top_chunks:
        logging.info(f"Selected Chunk ID: {chunk.id} from Document: {chunk.document.title} (Score: {score:.4f})")
        print(f"Selected Chunk ID: {chunk.id} from Document: {chunk.document.title} (Score: {score:.4f})")

    return [
        {"content": chunk.content, "document": chunk.document.title, "chunk_id": chunk.id, "score": score}
        for chunk, score in top_chunks
    ]
