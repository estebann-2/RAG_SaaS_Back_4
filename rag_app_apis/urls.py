from django.urls import path
from .views import UploadDocumentView, ConversationHistoryView, SendMessageView

urlpatterns = [
    path('api_upload/', UploadDocumentView.as_view(), name='api_upload_document'),
    path('api_conversation/history/', ConversationHistoryView.as_view(), name='api_conversation_history'),
    path('api_conversation/send/', SendMessageView.as_view(), name='api_send_message')
]
