from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import os

# File Validation
def validate_file_extension(value):
    """Allows only PDF, TXT, DOCX, and MD files"""
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.pdf', '.txt', '.docx', '.md']
    if ext not in valid_extensions:
        raise ValidationError(f"Invalid format. Allowed: {', '.join(valid_extensions)}")

def validate_file_size(value):
    """Restricts file size to 10MB"""
    limit = 10 * 1024 * 1024  # 10MB
    if value.size > limit:
        raise ValidationError("File too large. Maximum allowed size is 10MB.")

class APIDocument(models.Model):  # 👈 Cambié el nombre del modelo
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conversation = models.ForeignKey("APIConversation", on_delete=models.SET_NULL, null=True, blank=True)  # 👈 Cambié la referencia
    file = models.FileField(upload_to='documents/', validators=[validate_file_extension, validate_file_size])
    title = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    summary = models.TextField(blank=True, null=True)
    explanation = models.TextField(blank=True, null=True)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class APIConversation(models.Model):  # 👈 Cambié el nombre del modelo
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def save(self, *args, **kwargs):
        if not self.title:
            first_message = self.messages.first()
            if first_message:
                self.title = first_message.text[:30]
            else:
                self.title = "New Conversation"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
       
class APIMessage(models.Model):  # 👈 Cambié el nombre del modelo
    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
    ]

    conversation = models.ForeignKey(APIConversation, on_delete=models.CASCADE, related_name='messages_api')  # 👈 Cambié la referencia
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender.username} ({self.role}): {self.text[:30]}"
    
class APIChunk(models.Model):  # 👈 Cambié el nombre del modelo
    document = models.ForeignKey(APIDocument, on_delete=models.CASCADE, related_name="chunks_api")  # 👈 Cambié la referencia
    content = models.TextField()
    embedding = models.JSONField()

    def __str__(self):
        return f"Chunk from {self.document.title}" 
