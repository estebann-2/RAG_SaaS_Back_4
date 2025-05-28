from django import forms
from .models import Document, Message
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import os

# Document Upload Form with Better Validation
class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['file', 'title']

    def clean_file(self):
        file = self.cleaned_data.get('file', False)

        if not file:
            raise ValidationError("Debes subir un archivo.")

        # Use model's validation function
        from .models import validate_file_extension
        validate_file_extension(file)

        # Validate file size (10MB limit)
        max_size = 10 * 1024 * 1024  # 10MB
        if file.size > max_size:
            raise ValidationError("El archivo es demasiado grande. Máximo 10MB.")

        return file

# Message Form with Trimmed Text
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["text"]
        widgets = {
            "text": forms.TextInput(attrs={
                "placeholder": "Escribe un mensaje...",
                "maxlength": "500",  # Prevent excessively long messages
                "autocomplete": "off",
            }),
        }

    def clean_text(self):
        text = self.cleaned_data.get("text", "").strip()
        if not text:
            raise ValidationError("El mensaje no puede estar vacío.")
        return text
