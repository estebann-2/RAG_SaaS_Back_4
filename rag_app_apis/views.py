from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import APIDocument, APIConversation, APIMessage
from .serializers import DocumentSerializer, MessageSerializer, ConversationSerializer
from .utils import process_document, query_llm
from .retriever import retrieve_relevant_chunks
import logging


# Upload Document API
class UploadDocumentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if 'document' not in request.FILES:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        uploaded_file = request.FILES["document"]
        document_name = uploaded_file.name

        # Get user ID from the request body
        user_id = request.data.get("user")
        if not user_id:
            return Response({"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = get_object_or_404(User, id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Create conversation
        conversation = APIConversation.objects.create(user=user, title=document_name.split('.')[0])

        # Save document using the storage backend (GCS)
        document = APIDocument.objects.create(
            user=user,
            file=uploaded_file,  # This will use the configured storage backend
            title=document_name.split('.')[0],
            conversation=conversation
        )

        # Process document asynchronously
        process_document(document)

        # Save system message
        APIMessage.objects.create(
            conversation=conversation,
            sender=user,
            text=f"Documento '{document_name}' procesado y listo para consultas."
        )

        return Response({
            "success": True,
            "response": f"Documento '{document_name}' subido y procesado.",
            "conversation_id": conversation.id,
            "file_url": document.file.url  # Now returns the GCS URL
        }, status=status.HTTP_201_CREATED)


class ConversationHistoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Get user ID from the request query parameters
        user_id = request.query_params.get("user")

        if not user_id:
            return Response({"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = get_object_or_404(User, id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Retrieve conversations for the specified user
        conversations = APIConversation.objects.filter(user=user).order_by("-created_at")
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SendMessageView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):  # Eliminamos conversation_id de los parámetros
        user_id = request.data.get("user")
        conversation_id = request.data.get("conversation")  # Ahora lo extraemos del body

        if not user_id or not conversation_id:
            return Response({"error": "User ID and Conversation ID are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Validar usuario
        user = get_object_or_404(User, id=user_id)

        # Validar conversación
        conversation = get_object_or_404(APIConversation, id=conversation_id, user=user)

        user_message = request.data.get("message")
        if not user_message:
            return Response({"error": "Message cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)

        # Guardar mensaje del usuario
        message = APIMessage.objects.create(
            conversation=conversation,
            sender=user,
            role="user",
            text=user_message
        )

        # Recuperar chunks relevantes
        relevant_chunks = retrieve_relevant_chunks(user_message, conversation, top_k=3)

        # Formatear prompt
        context_text = "\n\n".join([
            f"Document: {c['document']}\nChunk {c['chunk_id']}:\n{c['content']}" 
            for c in relevant_chunks
        ]) if relevant_chunks else "No context available."

        prompt = f"Context:\n{context_text}\n\nUser Query: {user_message}"

        # Consultar al LLM
        llm_response = query_llm(prompt)

        # Guardar respuesta del asistente
        assistant_message = APIMessage.objects.create(
            conversation=conversation,
            sender=user,
            role="assistant",
            text=llm_response
        )

        return Response({
            "user_id": user.id,
            "conversation_id": conversation.id,
            "user_message": message.text,
            "assistant_response": assistant_message.text
        }, status=status.HTTP_200_OK)
